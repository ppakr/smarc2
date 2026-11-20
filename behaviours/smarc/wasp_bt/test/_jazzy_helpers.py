"""Scripted action server and bounded waits for live WASP tests."""

import time

from smarc_action_base.gentler_action_server import GentlerActionServer


ACTION = 'wait'


class ScriptedServer:
    """A GentlerActionServer whose loop_inner follows a script.

    ``ticks_to_finish`` loop calls return None, then ``outcome`` is returned
    (True = succeed, False = fail, None = run until cancelled).
    ``accept_delay_s`` holds the goal response, so a test can act while the
    client is still SENT.
    """

    def __init__(self, node, ticks_to_finish=3, outcome=True, accept_goals=True,
                 accept_cancels=True, accept_delay_s=0.0):
        self.ticks_to_finish = ticks_to_finish
        self.outcome = outcome
        self.accept_goals = accept_goals
        self.accept_cancels = accept_cancels
        self.accept_delay_s = accept_delay_s
        self.goals = []
        self.cancels = 0
        self.ticks = 0
        self.server = GentlerActionServer(
            node, ACTION, self.on_goal, self.on_cancel, self.prepare, self.loop,
            self.feedback, loop_frequency=20.0)

    def on_goal(self, goal):
        time.sleep(self.accept_delay_s)
        self.goals.append(goal)
        return self.accept_goals

    def on_cancel(self):
        self.cancels += 1
        return self.accept_cancels

    def prepare(self):
        self.ticks = 0

    def loop(self):
        self.ticks += 1
        if self.ticks < self.ticks_to_finish:
            return None
        return self.outcome

    def feedback(self):
        return f'tick {self.ticks}'


def wait_for(predicate, timeout_s=5.0, period_s=0.02):
    deadline = time.monotonic() + timeout_s
    while time.monotonic() < deadline:
        result = predicate()
        if result:
            return result
        time.sleep(period_s)
    return predicate()
