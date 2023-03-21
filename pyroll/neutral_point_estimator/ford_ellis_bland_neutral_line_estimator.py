import numpy as np

from . import Config
from .utils import chosen_estimator
from pyroll.core import RollPass, Hook
import pyroll.interface_friction

RollPass.Roll.ford_ellis_bland_neutral_point_estimator = Hook[float]()
"""Neutral line estimator setting the neutral point according to the Ford-Ellis-Bland solution."""


@RollPass.front_tension
def front_tension(self: RollPass):
    raise ValueError(
        "Please provide a front tension to use the Ford-Ellis-Bland estimator of the pyroll-neutral-line-estimator plugin.")


@RollPass.back_tension
def back_tension(self: RollPass):
    raise ValueError(
        "Please provide a back tension to use the Ford-Ellis-Bland estimator of the pyroll-neutral-line-estimator plugin.")


@RollPass.Roll.ford_ellis_bland_neutral_point_estimator
def ford_ellis_bland_neutral_point_estimator(self: RollPass.Roll):
    if chosen_estimator(Config.ESTIMATOR, "ford-ellis-bland"):
        rp = self.roll_pass

        return -self.working_radius * np.sin(rp.gap / self.working_radius * np.tan(0.25 * np.sqrt(
            rp.gap / self.working_radius) * rp.in_profile.equivalent_height - 1 / rp.coulomb_friction_coefficient * np.log(
            rp.in_profile.equivalent_height / rp.gap) * ((1 - rp.front_tension / rp.out_profile.flow_stress) / (
                1 - rp.back_tension / rp.out_profile.flow_stress))))


def neutral_point(self: RollPass.Roll):
    return self.ford_ellis_bland_neutral_point_estimator
