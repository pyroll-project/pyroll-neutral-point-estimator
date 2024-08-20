import logging
import webbrowser
from pathlib import Path

from pyroll.core import Profile, PassSequence, RollPass, Roll, CircularOvalGroove, Transport, RoundGroove, root_hooks, EquivalentRibbedGroove


def test_solve(tmp_path: Path, caplog, monkeypatch):
    caplog.set_level(logging.INFO, logger="pyroll")

    import pyroll.neutral_point_estimator
    monkeypatch.setenv("PYROLL_NEUTRAL_POINT_ESTIMATOR_ESTIMATOR", "NAPATOV-RIBBED-PROFILE")

    root_hooks.add(Roll.neutral_point)

    try:
        in_profile = Profile.from_groove(
            groove=CircularOvalGroove(
                depth=5e-3,
                r1=0.2e-3,
                r2=16e-3,
            ),
            filling=1,
            gap=2e-3,
            depth=5e-3,
            r1=0.2e-3,
            r2=16e-3,
            temperature=1200 + 273.15,
            strain=0,
            material=["C45", "steel"],
            flow_stress=100e6,
            density=7.5e3,
            thermal_capacity=690,
        )

        sequence = PassSequence([
            RollPass(
                label="ribbed_equivalent",
                roll=Roll(
                    groove=EquivalentRibbedGroove(
                        r1=0.2e-3,
                        r3=3.45e-3,
                        rib_distance=8.4e-3,
                        rib_width=1.4e-3,
                        rib_angle=45,
                        base_body_height=11.78e-3,
                        nominal_outer_diameter=14e-3,
                        usable_width=13.7e-3,
                        depth=5.5e-3,
                        rib_flank_angle=35,
                    ),
                    nominal_radius=160e-3 / 2,
                    rotational_frequency=1,
                ),
                gap=2.2e-3,
                coulomb_friction_coefficient=0.4,
                back_tension=5e6,
                front_tension=0
            ),
        ])

        try:
            sequence.solve(in_profile)

            assert sequence[0].roll.neutral_point < 0

        finally:
            print("\nLog:")
            print(caplog.text)
    finally:
        root_hooks.remove(Roll.neutral_point)

    try:
        import pyroll.report

        report = pyroll.report.report(sequence)

        report_file = tmp_path / "report.html"
        report_file.write_text(report, encoding="utf-8")
        print(report_file)
        webbrowser.open(report_file.as_uri())

    except ImportError:
        pass
