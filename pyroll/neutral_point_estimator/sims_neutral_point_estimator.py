import numpy as np

from . import Config
from .utils import chosen_estimator
from pyroll.core import RollPass, Hook

RollPass.Roll.sims_neutral_point_estimator = Hook[float]()
"""Neutral line estimator setting the neutral point according to the Sims solution."""


@RollPass.front_tension
def front_tension(self: RollPass):
    raise ValueError(
        "Please provide a front tension to use the Sims estimator of the pyroll-neutral-line-estimator plugin.")


@RollPass.back_tension
def back_tension(self: RollPass):
    raise ValueError(
        "Please provide a back tension to use the Sims estimator of the pyroll-neutral-line-estimator plugin.")


@RollPass.Roll.sims_neutral_point_estimator
def sims_neutral_point_estimator(self: RollPass.Roll):
    if chosen_estimator(Config.ESTIMATOR, "sims"):
        rp = self.roll_pass
        mean_flow_stress = (rp.in_profile.flow_stress + 2 * rp.out_profile.flow_stress) / 3

        return -self.working_radius * np.sin(np.sqrt(rp.gap / self.working_radius) * np.tan(
            0.5 * (np.arctan(np.sqrt(rp.in_profile.equivalent_height / rp.gap - 1))
                   + np.sqrt(rp.gap / self.working_radius) * (
                           0.25 * np.pi * np.log(rp.in_profile.equivalent_height / rp.gap) + (
                           rp.front_tension - rp.back_tension) / mean_flow_stress)
                   )))


@RollPass.Roll.neutral_point
def neutral_point(self: RollPass.Roll):
    return self.sims_neutral_point_estimator
