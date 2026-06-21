"""Water treatment behavior."""

from __future__ import annotations

from pyfarm.water.calculator import WaterCalculator
from pyfarm.water.models import (
    TreatmentAction,
    TreatmentPlan,
    TreatmentStep,
    WaterQualityTarget,
    WaterSourceProfile,
)


class WaterBehavior:

    def __init__(self):
        self.calculator = WaterCalculator()

    async def compute_treatment(
        self,
        source: WaterSourceProfile,
        target: WaterQualityTarget,
    ) -> TreatmentPlan:
        """Compute a treatment plan to bring source water to target quality."""
        steps: list[TreatmentStep] = []
        result_tds = source.tds_ppm
        result_ph = source.ph

        if source.tds_ppm > target.tds_ppm:
            ratio = self.calculator.ro_blend_ratio(source.tds_ppm, target.tds_ppm)
            steps.append(TreatmentStep(
                action=TreatmentAction.RO_DILUTION,
                notes=f"Blend {ratio*100:.1f}% RO water",
            ))
            result_tds = target.tds_ppm

        if source.ph > target.ph_max:
            dose = self.calculator.acid_dose_ml_per_litre(source.ph, target.ph_max)
            steps.append(TreatmentStep(
                action=TreatmentAction.ACID_DOSE,
                dose_ml_per_l=dose,
                notes="Lower pH with phosphoric acid",
            ))
            result_ph = target.ph_max

        if source.ph < target.ph_min:
            steps.append(TreatmentStep(
                action=TreatmentAction.BASE_DOSE,
                notes="Raise pH with potassium hydroxide",
            ))
            result_ph = target.ph_min

        return TreatmentPlan(
            steps=steps,
            estimated_result_tds=result_tds,
            estimated_result_ph=result_ph,
        )

    async def validate_source(self, source: WaterSourceProfile) -> list[str]:
        """Return quality warnings for the source profile."""
        warnings: list[str] = []
        if source.tds_ppm > 500:
            warnings.append(f"High TDS ({source.tds_ppm} ppm) — RO recommended")
        if source.alkalinity_ppm > 200:
            warnings.append(f"High alkalinity ({source.alkalinity_ppm} ppm)")
        if source.hardness_ppm > 300:
            warnings.append(f"Very hard water ({source.hardness_ppm} ppm)")
        if source.ph > 8.5:
            warnings.append(f"High pH ({source.ph})")
        if source.ph < 5.0:
            warnings.append(f"Low pH ({source.ph})")
        return warnings
