from pyroll.core import config as _config
from . import utils

VERSION = "2.0"


@_config("PYROLL_NEUTRAL_POINT_ESTIMATOR")
class Config:
    ESTIMATOR = ""


from . import osborn_neutral_point_estimator
from . import ford_ellis_bland_neutral_line_estimator
from . import siebel_neutral_point_estimator
from . import sims_neutral_point_estimator
from . import equal_neutral_line_estimator
