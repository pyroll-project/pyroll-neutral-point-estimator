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


@RollPass.Roll.neutral_angle
def neutral_angle(self: RollPass.Roll):
    if chosen_estimator(Config.ESTIMATOR, "ford-ellis-bland"):
        import pyroll.interface_friction
        rp = self.roll_pass

        entry_point_height = 2 * np.sqrt(rp.roll.working_radius / rp.out_profile.equivalent_height) * np.arctan(
            np.sqrt(rp.roll.working_radius / rp.out_profile.equivalent_height) * rp.entry_angle)

        approximate_neutral_plane_height = entry_point_height / 2 - 1 / (2 * rp.coulomb_friction_coefficient) * np.log(
            rp.in_profile.equivalent_height / rp.out_profile.equivalent_height * (
                    (1 - rp.front_tension / rp.out_profile.flow_stress) / (
                    1 - rp.back_tension / rp.in_profile.flow_stress)))

        return np.sqrt(rp.out_profile.equivalent_height / self.working_radius) * np.tan(
            np.sqrt(rp.out_profile.equivalent_height / self.working_radius) * approximate_neutral_plane_height / 2)
