import numpy as np

from . import Config
from .utils import chosen_estimator
from pyroll.core import SymmetricRollPass, Hook

SymmetricRollPass.Roll.relative_neutral_angle = Hook[float]()
"""Relative Neutral angle defined by Lippmann and Mahrenholz for the roll pass."""

@SymmetricRollPass.Roll.relative_neutral_angle
def relative_neutral_angle(self: SymmetricRollPass.Roll):
    rp = self.roll_pass
    mean_flow_stress = (rp.in_profile.flow_stress + 2 * rp.out_profile.flow_stress) / 3
    abs_rel_draught  = abs(rp.rel_draught)
    back_tension_model_definition = -rp.back_tension
    front_tension_model_definition = -rp.front_tension
    relative_tension = (back_tension_model_definition - front_tension_model_definition) / mean_flow_stress

    p1 = np.sqrt((1 - abs_rel_draught) / abs_rel_draught)
    p2 = 1 / 2 * np.sqrt(rp.out_profile.equivalent_height / self.working_radius) * (relative_tension + np.log(1 - abs_rel_draught))
    p3 = 1 / 2 * np.arctan(np.sqrt(abs_rel_draught / (1 - abs_rel_draught)))

    return p1 * np.tan(p2 + p3)


@SymmetricRollPass.Roll.neutral_angle
def neutral_angle(self: SymmetricRollPass.Roll):
    if chosen_estimator(Config.ESTIMATOR, "lippmann-mahrenholz"):
        return self.entry_angle * self.relative_neutral_angle
