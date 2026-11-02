# TODO: thrust allocation for sam control
import numpy as np

class ThrustAlloc:
    def __init__(self):
        # TODO:initialize force, data, rpm_signs, nozzle_signs, vbs_neutral, lcg_neutral, rpm min-max, angle min-max
        # assign values to the variables
        # self.force = np array(force_data)
        # self.rpm_data = np array(rpm_data)
        
        # construct matrix B
        # calculate pinv of B
        pass

    def allocate(self, tau):
        """Convert [X,Y,Z,K,M,N] forces and moments (N/Nm) to thruster commands."""
        # TODO: initialize tau
        # TODO: calculate force: F = B_pinv * tau
        pass

    def thrust_force_to_rpm(self):
        """Convert per motor forward force (N) to RPM"""
        # TODO: no look up table, so use linear model i guess
        pass
