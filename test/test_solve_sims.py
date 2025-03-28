import logging
import webbrowser
from pathlib import Path

from pyroll.core import Profile, PassSequence, RollPass, Roll, CircularOvalGroove, Transport, RoundGroove, root_hooks


def test_solve(tmp_path: Path, caplog, monkeypatch):
    caplog.set_level(logging.INFO, logger="pyroll")

    import pyroll.neutral_point_estimator
    monkeypatch.setenv("PYROLL_NEUTRAL_POINT_ESTIMATOR_ESTIMATOR", "SIMS")

    root_hooks.add(Roll.neutral_point)
    try:
        in_profile = Profile.round(
            diameter=30e-3,
            temperature=1200 + 273.15,
            strain=0,
            material=["C45", "steel"],
            flow_stress=100e6,
            density=7.5e3,
            thermal_capacity=690,
        )

        sequence = PassSequence([
            RollPass(
                label="Oval I",
                roll=Roll(
                    groove=CircularOvalGroove(
                        depth=8e-3,
                        r1=6e-3,
                        r2=40e-3
                    ),
                    nominal_radius=160e-3,
                    rotational_frequency=1
                ),
                gap=2e-3,
                coulomb_friction_coefficient=0.4,
                back_tension=0,
                front_tension=5e6
            ),
            Transport(
                label="I => II",
                duration=1
            ),
            RollPass(
                label="Round II",
                roll=Roll(
                    groove=RoundGroove(
                        r1=1e-3,
                        r2=12.5e-3,
                        depth=11.5e-3
                    ),
                    nominal_radius=160e-3,
                    rotational_frequency=1
                ),
                gap=2e-3,
                coulomb_friction_coefficient=0.4,
                back_tension=5e6,
                front_tension=0
            ),
        ])

        try:
            sequence.solve(in_profile)

            assert sequence[0].roll.neutral_point < 0
            assert sequence[2].roll.neutral_point < 0
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
