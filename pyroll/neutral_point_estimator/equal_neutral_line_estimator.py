from . import Config
from .utils import chosen_estimator
from pyroll.core import Roll


@Roll.neutral_point
def neutral_point(self: Roll):
    if chosen_estimator(Config.ESTIMATOR, "equal"):
        return self.contact_length / 2
