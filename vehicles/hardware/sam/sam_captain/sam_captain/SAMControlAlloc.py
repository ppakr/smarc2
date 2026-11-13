"""Map the effort requested by SAMSimpleController to actuator commands."""

from .control_type import ActuatorCmd, RequestedEffort


class SAMControlAlloc:
    def __init__(self, cap) -> None:
        # TODO: SAMSimpleController creates this once with SAMControlAlloc(cap).
        # TODO: Read allocation coefficients, trims and actuator bounds from cap's
        # parameters here
        # TODO: Confirm signed Unity gains/trim and reject invalid coefficients/bounds
        pass

    def allocate(self, requested: RequestedEffort) -> ActuatorCmd:
        # TODO: Called by SAMSimpleController.update() after its three PIDs.
        # requested contains surge/heave forces [N] and pitch moment [N m],
        # not velocity/depth/pitch errors. Agree on signs at that boundary.
        # This method only converts those efforts into actuator commands:
        #
        # rpm = X / ((K_front + K_back) * reverse_factor)
        # vbs = vbs_trim + (Z - Z0) / k_vbs
        # lcg = lcg_trim + (M - M0) / k_lcg

        pass
