"""Smoke tests for pyfarm-water."""

import pytest

from pyfarm.water import (
    WaterBehavior,
    WaterCalculator,
    WaterQualityTarget,
    WaterSourceProfile,
    WaterSourceType,
    TreatmentPlan,
    TreatmentAction,
)


def test_water_source_profile():
    p = WaterSourceProfile(tds_ppm=300, ph=7.5)
    assert p.tds_ppm == 300
    assert p.ph == 7.5


def test_water_source_validation():
    with pytest.raises(ValueError):
        WaterSourceProfile(ph=15)
    with pytest.raises(ValueError):
        WaterSourceProfile(tds_ppm=-1)


def test_ro_blend_ratio():
    ratio = WaterCalculator.ro_blend_ratio(400, 50)
    assert ratio == pytest.approx(0.875)


def test_ro_blend_ratio_already_clean():
    ratio = WaterCalculator.ro_blend_ratio(50, 50)
    assert ratio == 0.0


def test_acid_dose():
    dose = WaterCalculator.acid_dose_ml_per_litre(8.0, 6.5)
    assert dose > 0


def test_acid_dose_no_change():
    dose = WaterCalculator.acid_dose_ml_per_litre(6.0, 6.5)
    assert dose == 0.0


@pytest.mark.asyncio
async def test_compute_treatment_high_tds():
    behavior = WaterBehavior()
    source = WaterSourceProfile(tds_ppm=400, ph=7.0)
    target = WaterQualityTarget(tds_ppm=50, ph_min=5.8, ph_max=6.5)
    plan = await behavior.compute_treatment(source, target)
    assert isinstance(plan, TreatmentPlan)
    actions = [s.action for s in plan.steps]
    assert TreatmentAction.RO_DILUTION in actions
    assert plan.estimated_result_tds == 50


@pytest.mark.asyncio
async def test_compute_treatment_high_ph():
    behavior = WaterBehavior()
    source = WaterSourceProfile(tds_ppm=50, ph=8.0)
    target = WaterQualityTarget(tds_ppm=50, ph_min=5.8, ph_max=6.5)
    plan = await behavior.compute_treatment(source, target)
    actions = [s.action for s in plan.steps]
    assert TreatmentAction.ACID_DOSE in actions


@pytest.mark.asyncio
async def test_validate_source_warnings():
    behavior = WaterBehavior()
    source = WaterSourceProfile(tds_ppm=600, ph=9.0, alkalinity_ppm=250)
    warnings = await behavior.validate_source(source)
    assert len(warnings) >= 2


@pytest.mark.asyncio
async def test_validate_source_clean():
    behavior = WaterBehavior()
    source = WaterSourceProfile(tds_ppm=50, ph=6.5, alkalinity_ppm=20, hardness_ppm=30)
    warnings = await behavior.validate_source(source)
    assert warnings == []
