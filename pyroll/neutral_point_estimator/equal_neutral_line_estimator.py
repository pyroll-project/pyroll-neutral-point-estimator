from . import Config
from .utils import chosen_estimator
from pyroll.core import RollPass


@RollPass.Roll.neutral_point
def neutral_point(self: RollPass.Roll):
    if chosen_estimator(Config.ESTIMATOR, "equal"):
        return self.contact_length / 2
