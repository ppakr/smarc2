# TODO: simple SAM controller
# pitch-depth control
# velocity control
from dataclasses import dataclass
from sam_diving_controller.controllers.PIDControl import PIDControl

@dataclass
class ControlState:
    surge_m_s: float
    depth_m: float
    pitch_deg: float

@dataclass
class ActuatorCmd:
    rpm: float
    thrust_vect: float
    vbs: float
    lcg: float

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
        pass

    def reset(self):
        """Resets PID"""
        self.surge_pid.reset()
        self.depth_pid.reset()
        self.pitch_pid.reset()

