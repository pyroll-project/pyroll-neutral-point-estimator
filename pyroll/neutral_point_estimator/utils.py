from pyroll.core import RollPass


def chosen_estimator(estimator: str, current_estimator: str):
    """Helper function to chose between different neutral point estimators."""
    if estimator.lower() is current_estimator:
        return True
    return False
