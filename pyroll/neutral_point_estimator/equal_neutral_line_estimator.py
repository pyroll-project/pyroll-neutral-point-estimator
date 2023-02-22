from . import ESTIMATOR
from .utils import chosen_estimator
from pyroll.core import RollPass, Hook

equal_neutral_point_estimator = Hook[float]()
"""Neutral line estimator setting the neutral point to half of the contact length."""


@RollPass.Roll.equal_neutral_point_estimator
def equal_neutral_point_estimator(self: RollPass.Roll):
    if chosen_estimator(ESTIMATOR, "equal"):
        return self.contact_length / 2


@RollPass.Roll.neutral_point
def neutral_point(self: RollPass.Roll):
    return self.equal_neutral_point_estimator
