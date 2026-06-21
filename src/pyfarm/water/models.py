"""Data models for water quality."""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Optional


class WaterSourceType(str, Enum):
    MAINS = "mains"
    RAINWATER = "rainwater"
    WELL = "well"
    RO = "ro"
    BORE = "bore"


class TreatmentAction(str, Enum):
    RO_DILUTION = "ro_dilution"
    ACID_DOSE = "acid_dose"
    BASE_DOSE = "base_dose"
    UV = "uv"
    CARBON_FILTER = "carbon_filter"


@dataclass
class WaterSourceProfile:
    tds_ppm: float = 200.0
    ph: float = 7.0
    temp_c: float = 20.0
    alkalinity_ppm: float = 100.0
    hardness_ppm: float = 150.0
    source_type: WaterSourceType = WaterSourceType.MAINS

    def __post_init__(self):
        if self.tds_ppm < 0:
            raise ValueError("tds_ppm must be non-negative")
        if not 0 <= self.ph <= 14:
            raise ValueError("ph must be 0-14")
        if self.alkalinity_ppm < 0:
            raise ValueError("alkalinity_ppm must be non-negative")
        if self.hardness_ppm < 0:
            raise ValueError("hardness_ppm must be non-negative")


@dataclass
class WaterQualityTarget:
    tds_ppm: float = 50.0
    ph_min: float = 5.8
    ph_max: float = 6.5
    max_alkalinity_ppm: float = 30.0
    max_hardness_ppm: float = 80.0


@dataclass
class TreatmentStep:
    action: TreatmentAction = TreatmentAction.RO_DILUTION
    dose_ml_per_l: Optional[float] = None
    notes: str = ""


@dataclass
class TreatmentPlan:
    steps: list[TreatmentStep] = field(default_factory=list)
    estimated_result_tds: float = 0.0
    estimated_result_ph: float = 7.0
    notes: str = ""
