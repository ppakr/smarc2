# TODO: thrust allocation for sam control
import numpy as np

class ThrustAlloc:
    def __init__(self, thruster_arm, force_data, rpm_data, rpm_signs, nozzle_signs, vbs_neutral, lcg_neutral, rpm_min, angle_max, angle_sum_max):
        """
        force_data:
        rpm_data:
        rpm_signs:
        nozzle_signs:
        vbs_neutral:
        lcg_neutral:
        rpm_min:
        angle_max:
        angle_sum_max:
        """
        # initialize class variables
        self.force_data = np.array(force_data, dtype=float, copy=True)
        self.rpm_data = np.array(rpm_data, dtype=float, copy=True)
        self.rpm_signs = np.array(rpm_signs, dtype=int)
        self.nozzle_signs = np.array(nozzle_signs, dtype=int)
        self.vbs_neutral = vbs_neutral
        self.lcg_neutral = lcg_neutral
        self.rpm_min = rpm_min
        self.angle_max = angle_max
        self.angle_sum_max = angle_sum_max
        # construct matrix B
        # From Fossen, T. I. (2021), pg. 316, eq. 11.1
        # Matrix B is the input matrix that maps the thruster forces to forces in 6 DoF
        # NED (North, East, Down) frame used.
        self.B = np.array([
            [1, 0, 0],
            [0, 1, 0],
            [0, 0, 1],
            [0, 0, 0],
            [0, 0, thruster_arm],
            [0, -thruster_arm, 0],
        ], dtype=float)
        # calculate pinv of B
        self.B_pinv = np.linalg.pinv(self.B)

    def allocate(self, tau):
        """Convert [X,Y,Z,K,M,N] forces and moments (N/Nm) to thruster commands."""
        # TODO: initialize tau
        tau = np.array(tau, dtype=float)
        # TODO: calculate force: F = B_pinv * tau
        F = self.B_pinv @ tau
        return F

    def thrust_force_to_rpm(self):
        """Convert per motor forward force (N) to RPM"""
        # TODO: no look up table, so use linear model i guess
        pass
