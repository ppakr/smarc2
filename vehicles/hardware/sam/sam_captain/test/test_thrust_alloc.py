"""Check the force vector returned by ThrustAlloc.allocate()."""

import numpy as np
import pytest

from sam_captain.ThrustAlloc import ThrustAlloc


@pytest.fixture(params=[0.5, 1.0, 2.0], ids=['short-arm', 'unit-arm', 'long-arm'])
def allocator(request):
    """Use synthetic calibration; only the arm affects force allocation."""
    arm = request.param
    alloc = ThrustAlloc(
        thruster_arm=arm,
        force_data=[0, 10],
        rpm_data=[0, 1000],
        rpm_signs=[1, 1],
        nozzle_signs=[1, 1],
        vbs_neutral=50,
        lcg_neutral=50,
        rpm_min=200,
        angle_max=0.122173,
        angle_sum_max=0.231,
    )
    return alloc, arm


def test_zero_wrench_returns_zero_force(allocator):
    alloc, _ = allocator

    force = alloc.allocate([0] * 6)

    assert force.shape == (3,)
    np.testing.assert_allclose(force, [0, 0, 0], atol=1e-12)


@pytest.mark.parametrize('axis', range(6), ids=[
    'surge', 'sway', 'heave', 'roll', 'pitch', 'yaw',
])
@pytest.mark.parametrize('direction', [-1, 1], ids=['negative', 'positive'])
def test_individual_wrench_axes(allocator, axis, direction):
    alloc, arm = allocator
    tau = np.zeros(6)
    tau[axis] = direction * 10
    denominator = 1 + arm ** 2
    expected = np.array([
        [10, 0, 0],
        [0, 10 / denominator, 0],
        [0, 0, 10 / denominator],
        [0, 0, 0],
        [0, 0, 10 * arm / denominator],
        [0, -10 * arm / denominator, 0],
    ])[axis] * direction

    np.testing.assert_allclose(alloc.allocate(tau), expected, atol=1e-12)


def test_mixed_wrench_matches_analytic_least_squares_solution(allocator):
    alloc, arm = allocator
    tau = [10, -4, 6, 7, -3, 5]
    x, y, z, _, pitch, yaw = tau
    # B maps F to [Fx, Fy, Fz, 0, arm*Fz, -arm*Fy].
    # Minimizing ||B F - tau|| squared gives these independent equations.
    expected = [
        x,
        (y - arm * yaw) / (1 + arm ** 2),
        (z + arm * pitch) / (1 + arm ** 2),
    ]

    np.testing.assert_allclose(alloc.allocate(tau), expected, atol=1e-12)


def test_achievable_wrench_recovers_original_force(allocator):
    alloc, arm = allocator
    expected = [2, -3, 5]
    # Construct the wrench independently of the allocator's B matrix.
    tau = [2, -3, 5, 0, 5 * arm, 3 * arm]

    np.testing.assert_allclose(alloc.allocate(tau), expected, atol=1e-12)
