from dataclasses import dataclass

@dataclass
class ControlState:
    surge_m_s: float
    depth_m: float
    pitch_rad: float

@dataclass
class ActuatorCmd:
    rpm_front: float
    rpm_back: float
    thrust_vect: float
    vbs: float
    lcg: float
    