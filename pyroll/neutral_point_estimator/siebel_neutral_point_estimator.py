import numpy as np

from . import Config
from .utils import chosen_estimator
from pyroll.core import RollPass, Hook
import pyroll.interface_friction

RollPass.Roll.siebel_neutral_point_estimator = Hook[float]()
"""Neutral line estimator setting the neutral point according to the Siebel solution."""


@RollPass.front_tension
def front_tension(self: RollPass):
    raise ValueError(
        "Please provide a front tension to use the Siebel estimator of the pyroll-neutral-line-estimator plugin.")


@RollPass.back_tension
def back_tension(self: RollPass):
    raise ValueError(
        "Please provide a back tension to use the Siebel estimator of the pyroll-neutral-line-estimator plugin.")


@RollPass.Roll.siebel_neutral_point_estimator
def siebel_neutral_point_estimator(self: RollPass.Roll):
    if chosen_estimator(Config.ESTIMATOR, "siebel"):
        rp = self.roll_pass
        mean_flow_stress = (rp.in_profile.flow_stress + 2 * rp.out_profile.flow_stress) / 3
        entry_angle = np.arcsin(self.contact_length / self.working_radius)

        return -self.working_radius * np.sin(
            1 / (4 * self.working_radius * mean_flow_stress * rp.coulomb_fricition_coefficient) * (
                    rp.front_tension * rp.in_profile.equivalent_height - rp.back_tension * rp.gap + 2 * self.working_radius * mean_flow_stress * (
                    entry_angle ** 2 / 2 + rp.coulomb_fricition_coefficient * entry_angle)))


@RollPass.Roll.neutral_point
def neutral_point(self: RollPass.Roll):
    return self.siebel_neutral_point_estimator
