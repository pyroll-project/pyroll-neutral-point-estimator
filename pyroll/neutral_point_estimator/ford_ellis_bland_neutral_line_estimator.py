import numpy as np

from . import Config
from .utils import chosen_estimator
from pyroll.core import RollPass


@RollPass.front_tension
def front_tension(self: RollPass):
    raise ValueError(
        "Please provide a front tension to use the Ford-Ellis-Bland estimator of the pyroll-neutral-line-estimator plugin.")


@RollPass.back_tension
def back_tension(self: RollPass):
    raise ValueError(
        "Please provide a back tension to use the Ford-Ellis-Bland estimator of the pyroll-neutral-line-estimator plugin.")


@RollPass.Roll.neutral_point
def neutral_point(self: RollPass.Roll):
    return self.ford_ellis_bland_neutral_point_estimator
