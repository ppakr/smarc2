from types import SimpleNamespace
from unittest.mock import Mock

import pytest

from sam_captain.control_type import ActuatorCmd, RequestedEffort
from sam_captain.SAMControlAlloc import SAMControlAlloc


def make_allocator(**overrides):
    values = {f'allocation_{key}': value for key, value in overrides.items()}
    cap = Mock()
    cap.has_parameter.side_effect = lambda name: name in values
    cap.declare_parameter.side_effect = lambda name, value: values.setdefault(name, value)
    cap.get_parameter.side_effect = lambda name: SimpleNamespace(value=values[name])
    return SAMControlAlloc(cap), cap


def test_zero_effort_returns_trim():
    allocator, _ = make_allocator()
    assert allocator.allocate(RequestedEffort(0, 0, 0)) == ActuatorCmd(0, 0, 0, 50, 50)


@pytest.mark.parametrize('surge, rpm', [(1.0, 100), (-0.6, -100)])
def test_forward_and_reverse_equal_rpm(surge, rpm):
    allocator, _ = make_allocator()
    command = allocator.allocate(RequestedEffort(surge, 0, 0))
    assert command.rpm_front == command.rpm_back == rpm
    assert command.thrust_vect == 0


def test_signed_gains_offsets_and_non_midpoint_trims():
    allocator, cap = make_allocator(vbs_gain=0.025, lcg_gain=-0.015,
                                    vbs_trim=35.0, lcg_trim=60.0,
                                    heave_offset=0.3, pitch_offset=-0.2)
    command = allocator.allocate(RequestedEffort(0, 0.55, -0.05))
    assert command.vbs == pytest.approx(45)
    assert command.lcg == pytest.approx(50)
    # Existing captain parameters are read without being redeclared.
    assert 'allocation_vbs_gain' not in [c.args[0] for c in cap.declare_parameter.call_args_list]


@pytest.mark.parametrize('surge, heave, pitch, rpm, vbs, lcg', [
    (100, 100, 100, 800, 100, 0),
    (-100, -100, -100, -400, 0, 100),
])
def test_unreachable_requests_are_clipped(surge, heave, pitch, rpm, vbs, lcg):
    allocator, _ = make_allocator()
    assert allocator.allocate(RequestedEffort(surge, heave, pitch)) == ActuatorCmd(
        rpm, rpm, 0, vbs, lcg)


def test_integer_rpm_stays_inside_fractional_bounds():
    allocator, _ = make_allocator(rpm_min=-2.8, rpm_max=2.8)
    assert allocator.allocate(RequestedEffort(1, 0, 0)).rpm_front == 2
    assert allocator.allocate(RequestedEffort(-1, 0, 0)).rpm_front == -2


def test_default_parameters_are_declared_on_captain():
    allocator, cap = make_allocator()
    cap.declare_parameter.assert_any_call('allocation_front_gain', 0.005)
    cap.declare_parameter.assert_any_call('allocation_reverse_multiplier', 0.6)
    assert allocator.vbs_trim == allocator.lcg_trim == 50.0


@pytest.mark.parametrize('surge, expected_rpm', [(0.016, 2), (-0.0096, -2)])
def test_rpm_rounds_to_nearest_integer(surge, expected_rpm):
    allocator, _ = make_allocator()
    command = allocator.allocate(RequestedEffort(surge, 0, 0))
    assert command.rpm_front == command.rpm_back == expected_rpm
    assert isinstance(command.rpm_front, int)


@pytest.mark.parametrize('heave, pitch, expected_vbs, expected_lcg', [
    (0.24451425, 0.1509759, 60, 40),
    (-0.24451425, -0.1509759, 40, 60),
])
def test_default_heave_and_pitch_gain_signs(heave, pitch, expected_vbs, expected_lcg):
    allocator, _ = make_allocator()
    command = allocator.allocate(RequestedEffort(0, heave, pitch))
    assert command.vbs == pytest.approx(expected_vbs)
    assert command.lcg == pytest.approx(expected_lcg)
    assert command.rpm_front == command.rpm_back == 0


def test_custom_bounds_are_used():
    allocator, _ = make_allocator(rpm_min=-100, rpm_max=200,
                                  vbs_min=20.0, vbs_max=80.0,
                                  lcg_min=30.0, lcg_max=70.0)
    assert allocator.allocate(RequestedEffort(100, 100, 100)) == ActuatorCmd(
        200, 200, 0, 80, 30)
    assert allocator.allocate(RequestedEffort(-100, -100, -100)) == ActuatorCmd(
        -100, -100, 0, 20, 70)
