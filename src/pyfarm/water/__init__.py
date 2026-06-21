"""pyfarm-water: Source water treatment and quality management."""

from pyfarm.water.behavior import WaterBehavior
from pyfarm.water.calculator import WaterCalculator
from pyfarm.water.models import (
    TreatmentAction,
    TreatmentPlan,
    TreatmentStep,
    WaterQualityTarget,
    WaterSourceProfile,
    WaterSourceType,
)

__version__ = "0.1.0"

__all__ = [
    "WaterSourceType",
    "WaterSourceProfile",
    "WaterQualityTarget",
    "TreatmentAction",
    "TreatmentStep",
    "TreatmentPlan",
    "WaterCalculator",
    "WaterBehavior",
]
