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
    if chosen_estimator(Config.ESTIMATOR, "osborn"):
        import pyroll.interface_friction
        
        rp = self.roll_pass
        osborn_solution = 0.5 * np.sqrt((rp.in_profile.equivalent_height - rp.gap) / self.working_radius) * (
                3 * rp.gap / (rp.in_profile.equivalent_height + 2 * rp.gap))
        - 0.25 * (rp.gap * (rp.in_profile.equivalent_height - rp.gap) / self.working_radius * 1 / 3 * (
                rp.in_profile.equivalent_height + 2 * rp.gap) + 0.275 * rp.gap / (
                          rp.coulomb_friction_coefficient * self.working_radius) * (
                          rp.front_tension / rp.out_profile.flow_stress - rp.back_tension / rp.in_profile.flow_stress)
                  )
    return -self.working_radius * np.sin(osborn_solution)
