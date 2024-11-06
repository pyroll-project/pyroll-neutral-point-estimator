import logging
import webbrowser
from pathlib import Path

from pyroll.core import Profile, Roll, ThreeRollPass, Transport, RoundGroove, CircularOvalGroove, PassSequence, root_hooks


def test_solve3(tmp_path: Path, caplog, monkeypatch):
    caplog.set_level(logging.DEBUG, logger="pyroll")

    import pyroll.neutral_point_estimator
    pyroll.neutral_point_estimator.Config.ESTIMATOR

    monkeypatch.setenv("PYROLL_NEUTRAL_POINT_ESTIMATOR_ESTIMATOR", "EQUAL")

    root_hooks.add(Roll.neutral_point)

    in_profile = Profile.round(
        diameter=55e-3,
        temperature=1200 + 273.15,
        strain=0,
        material=["C45", "steel"],
        flow_stress=100e6,
        density=7.5e3,
        thermal_capacity=690,
    )

    sequence = PassSequence([
        ThreeRollPass(
            label="Oval I",
            roll=Roll(
                groove=CircularOvalGroove(
                    depth=8e-3,
                    r1=6e-3,
                    r2=40e-3,
                    pad_angle=30
                ),
                nominal_radius=160e-3,
                rotational_frequency=1
            ),
            gap=2e-3,
        ),
        Transport(
            label="I => II",
            duration=1
        ),
        ThreeRollPass(
            label="Round II",
            roll=Roll(
                groove=RoundGroove(
                    r1=3e-3,
                    r2=25e-3,
                    depth=11e-3,
                    pad_angle=30
                ),
                nominal_radius=160e-3,
                rotational_frequency=1
            ),
            gap=2e-3,
        ),
    ])

    try:
        sequence.solve(in_profile)

        assert sequence[0].roll.neutral_point < 0
        assert sequence[2].roll.neutral_point < 0
    finally:
        root_hooks.remove(Roll.neutral_point)

        print("\nLog:")
        print(caplog.text)

    try:
        import pyroll.report

        report = pyroll.report.report(sequence)

        report_file = tmp_path / "report.html"
        report_file.write_text(report, encoding="utf-8")
        print(report_file)
        webbrowser.open(report_file.as_uri())

    except ImportError:
        pass
