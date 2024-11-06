from . import Config
from .utils import chosen_estimator
from pyroll.core import BaseRollPass


@BaseRollPass.Roll.neutral_point
def neutral_point(self: BaseRollPass.Roll):
    if chosen_estimator(Config.ESTIMATOR, "equal"):
        return - self.contact_length / 2
