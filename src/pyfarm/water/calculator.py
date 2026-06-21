"""Water quality calculations."""

from __future__ import annotations


class WaterCalculator:

    @staticmethod
    def ro_blend_ratio(source_tds: float, target_tds: float) -> float:
        """Fraction of RO water (0 ppm) to blend to hit target TDS."""
        if source_tds <= 0:
            return 0.0
        ratio = 1.0 - (target_tds / source_tds)
        return max(0.0, min(1.0, ratio))

    @staticmethod
    def bicarbonate_adjustment(alkalinity_ppm: float, target_ph: float) -> float:
        """Estimate acid dose (ml/L of 85% phosphoric acid) to neutralise alkalinity."""
        if alkalinity_ppm <= 0:
            return 0.0
        meq_per_l = alkalinity_ppm / 50.0
        dose = meq_per_l * 0.074
        return max(0.0, round(dose, 4))

    @staticmethod
    def acid_dose_ml_per_litre(
        ph_current: float, ph_target: float, buffer_strength: float = 1.0
    ) -> float:
        """Estimate phosphoric acid dose (ml/L) to lower pH."""
        if ph_target >= ph_current:
            return 0.0
        delta_ph = ph_current - ph_target
        dose = delta_ph * 0.1 * buffer_strength
        return max(0.0, round(dose, 4))
