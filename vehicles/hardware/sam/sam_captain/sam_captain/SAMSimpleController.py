# TODO: simple SAM controller
# pitch-depth control
# velocity control
class SAMSimpleController:
    """A simple controller for the SAM vehicle"""

    def __init__(self, cap) -> None:
        # TODO: calls PID controller from sam_diving_controller

        # TODO: independent PID instances
        # TODO: surge pid
        # TODO: depth pid
        # TODO: pitch pid
        pass

    def update(self):
        """Takes state, desired state, and dt to compute control. Returns actuators controls"""
        pass

    def reset(self):
        """Resets PID"""
        pass
