import numpy as np

from . import ESTIMATOR
from .utils import chosen_estimator
from pyroll.core import RollPass, Hook

osborn_neutral_point_estimator = Hook[float]()
"""Neutral line estimator setting the neutral point according to the Osborn solution."""

coulomb_friction_coefficient = Hook[float]()
"""Friction coefficient of Coulomb's friction model."""


@RollPass.coulombs_fricition_coefficient
def coulomb_friction_coefficient(self: RollPass):
    raise ValueError(
        "You must provide Coulomb's friction coefficient to use the Ford-Ellis-Bland estimator of the pyroll-neutral-line-estimator plugin.")


@RollPass.front_tension
def front_tension(self: RollPass):
    raise ValueError(
        "You must provide a front tension to use the Ford-Ellis-Bland estimator of the pyroll-neutral-line-estimator plugin.")


@RollPass.back_tension
def back_tension(self: RollPass):
    raise ValueError(
        "You must provide a back tension to use the Ford-Ellis-Bland estimator of the pyroll-neutral-line-estimator plugin.")


@RollPass.Roll.osborn_neutral_point_estimator
def osborn_neutral_point_estimator(self: RollPass.Roll):
    if chosen_estimator(ESTIMATOR, "osborn"):
        rp = self.roll_pass

        return -self.working_radius * np.sin(
            0.5 * np.sqrt((rp.in_profile.equivalent_height - rp.gap) / self.working_radius) * (
                    3 * rp.gap / (rp.in_profile.equivalent_height + 2 * rp.gap))
            - 0.25 * (rp.gap * (rp.in_profile.equivalent_height - rp.gap) / self.working_radius * 1 / 3 * (
                    rp.in_profile.equivalent_height + 2 * rp.gap) + 0.275 * rp.gap / (
                              rp.coulomb_friction_coefficient * self.working_radius) * (
                              rp.front_tension / rp.out_profile.flow_stress - rp.back_tension / rp.in_profile.flow_stress)
                      ))


@RollPass.Roll.neutral_point
def neutral_point(self: RollPass.Roll):
    return self.osborn_neutral_point_estimator
