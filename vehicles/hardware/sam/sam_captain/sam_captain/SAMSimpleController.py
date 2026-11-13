# TODO: simple SAM controller
# pitch-depth control
# velocity control
from sam_diving_controller.controllers.PIDControl import PIDControl
from sam_captain.control_type import ControlState, ActuatorCmd

class SAMSimpleController:
    """A simple controller for the SAM vehicle"""

    def __init__(self, cap) -> None:
        self.cap = cap
        # TODO: independent PID instances
        # TODO: surge pid
        self.surge_pid = PIDControl(Kp=1.0, Ki=0.1, Kd=2.0, Kaw=0.0, u_neutral = 0.0, u_min = -1.0, u_max = 1.0)
        # TODO: depth pid
        self.depth_pid = PIDControl(Kp=1.0, Ki=0.1, Kd=2.0, Kaw=0.0, u_neutral = 0.0, u_min = -1.0, u_max = 1.0)
        # TODO: pitch pid
        self.pitch_pid = PIDControl(Kp=1.0, Ki=0.1, Kd=2.0, Kaw=0.0, u_neutral = 0.0, u_min = -1.0, u_max = 1.0)
        pass

    def update(self):
        """Takes state, desired state, and dt to compute control. Returns actuators controls"""
        # TODO: get current state
        # TODO: get desired state
        # TODO: compute control
        # TODO: allocate control
        pass

    def reset(self):
        """Resets PID"""
        self.surge_pid.reset()
        self.depth_pid.reset()
        self.pitch_pid.reset()

