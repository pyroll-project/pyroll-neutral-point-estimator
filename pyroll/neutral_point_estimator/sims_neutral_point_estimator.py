import numpy as np

from . import Config
from .utils import chosen_estimator
from pyroll.core import RollPass


@RollPass.front_tension
def front_tension(self: RollPass):
    raise ValueError(
        "Please provide a front tension to use the Sims estimator of the pyroll-neutral-line-estimator plugin.")


@RollPass.back_tension
def back_tension(self: RollPass):
    raise ValueError(
        "Please provide a back tension to use the Sims estimator of the pyroll-neutral-line-estimator plugin.")


@RollPass.Roll.neutral_angle
def neutral_angle(self: RollPass.Roll):
    if chosen_estimator(Config.ESTIMATOR, "sims"):
        rp = self.roll_pass
        mean_flow_stress = (rp.in_profile.flow_stress + 2 * rp.out_profile.flow_stress) / 3

        return - np.sqrt(rp.gap / self.working_radius) * np.tan(
            0.5 * (np.arctan(np.sqrt(rp.in_profile.equivalent_height / rp.gap - 1))
                   + np.sqrt(rp.gap / self.working_radius) * (
                           0.25 * np.pi * np.log(rp.in_profile.equivalent_height / rp.gap) + (
                           rp.front_tension - rp.back_tension) / mean_flow_stress)
                   ))
