"""Exercise WASP's real client and full tree against a Jazzy action server."""
import json
from types import SimpleNamespace

from _jazzy_helpers import ScriptedServer, wait_for
import pytest
from smarc_msgs.msg import Topics
from std_msgs.msg import Int8, String
from wasp_bt.bt.ros_bt import BT
from wasp_bt.waraps.waraps_task_handler import WaraPSTaskHandler


def setup_tree(ros_graph, **server_options):
    server = ScriptedServer(ros_graph('server', namespace='/audit'), **server_options)
    node = ros_graph('wasp', namespace='/audit')
    handler = WaraPSTaskHandler(node, {
        'name': 'audit', 'agent-uuid': 'audit', 'pulse_rate': 1.0,
        'levels': ['direct_execution', 'tst_execution'],
    }, start_offset=0.0)
    vehicle = SimpleNamespace(heartbeat=lambda: True)

    def now():
        return node.get_clock().now().nanoseconds / 1e9

    tree = BT(vehicle, handler, now)
    tree.setup()
    assert wait_for(lambda: bool(handler.get_available_tasks()))
    # Health comes through the actual ROS subscription.
    health = node.create_publisher(Int8, Topics.VEHICLE_HEALTH_TOPIC, 10)

    def ready():
        health.publish(Int8(data=Topics.VEHICLE_HEALTH_READY))
        return handler.health_status == Topics.VEHICLE_HEALTH_READY

    assert wait_for(ready)
    tree.tick()  # Dynamic discovery builds the task subtree.
    command = node.create_publisher(String, Topics.WARA_PS_EXEC_COMMAND_TOPIC, 10)
    assert wait_for(lambda: command.get_subscription_count() > 0)
    command.publish(String(data=json.dumps({
        'command': 'start-task', 'com-uuid': 'audit', 'task-uuid': 'task1',
        'task': {'name': 'wait', 'params': {'n': 1}},
    })))
    assert wait_for(lambda: bool(handler.tasks_executing))
    return tree, handler, server, health


def tick_until(tree, predicate):
    def tick():
        tree.tick()
        return predicate()
    return wait_for(tick)


@pytest.mark.parametrize('outcome', [True, False])
def test_full_tree_discovers_executes_and_clears(ros_graph, outcome):
    tree, handler, server, health = setup_tree(ros_graph, outcome=outcome)
    assert tick_until(tree, lambda: bool(server.goals) and not handler.tasks_executing)
    assert server.goals == [{'n': 1}]


def test_health_preemption_cancels_running_goal(ros_graph):
    tree, handler, server, health = setup_tree(ros_graph, outcome=None)
    assert tick_until(tree, lambda: server.ticks > 2)
    health.publish(Int8(data=Topics.VEHICLE_HEALTH_ERROR))
    assert wait_for(lambda: handler.health_status == Topics.VEHICLE_HEALTH_ERROR)
    assert tick_until(tree, lambda: server.cancels > 0)


def test_discovery_rebuild_keeps_active_client(ros_graph):
    tree, handler, server, health = setup_tree(ros_graph, outcome=None)
    assert tick_until(tree, lambda: server.ticks > 2)
    client = tree._action_client_cache['/audit/wait']
    handler._action_hb_callback(String(data='/audit/unavailable'))
    tree.tick()
    assert tree._action_client_cache['/audit/wait'] is client
    health.publish(Int8(data=Topics.VEHICLE_HEALTH_ERROR))
    assert wait_for(lambda: handler.health_status == Topics.VEHICLE_HEALTH_ERROR)
    assert tick_until(tree, lambda: server.cancels > 0)
