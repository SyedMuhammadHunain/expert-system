"""Comprehensive unit tests for Pakistan Agriculture Expert System.
Verifies:
- Minimum 50 rules requirement.
- Full 5-crop coverage (Wheat, Cotton, Rice, Sugarcane, Maize).
- 3 rule modalities (Hardcoded, May-or-May-Not, Extended).
- Pre-harvest chemical safety lockout.
- Zero-crash fault tolerance and explanation limits.
- Sub-second latency.
"""

import time
import pytest

from knowledge_base import (
    Category,
    ExplanationTrace,
    InferenceResult,
    Rule,
    RuleType,
    RULES,
)
from working_memory import WorkingMemory
from inference_engine import InferenceEngine
from explanation_module import ExplanationModule


@pytest.fixture
def engine() -> InferenceEngine:
    return InferenceEngine()


@pytest.fixture
def explainer() -> ExplanationModule:
    return ExplanationModule()


@pytest.fixture
def memory() -> WorkingMemory:
    return WorkingMemory()


# ============================================================================
# 1. ACADEMIC RUBRIC & KNOWLEDGE BASE VERIFICATIONS
# ============================================================================

def test_rule_count_minimum():
    """Instructor requirement: Minimum 50 rules."""
    assert len(RULES) >= 50, f"Expected at least 50 rules, found {len(RULES)}"


def test_crop_coverage():
    """Must cover 5 major Pakistani crops across all 3 functional modules."""
    crops = {"wheat", "cotton", "rice", "sugarcane", "maize"}
    for crop in crops:
        crop_rules = [r for r in RULES if r.crop == crop]
        assert len(crop_rules) >= 9, f"Crop {crop} has insufficient rules: {len(crop_rules)}"

        categories = {r.category for r in crop_rules}
        assert Category.DISEASE in categories, f"Missing disease rules for {crop}"
        assert Category.PEST in categories, f"Missing pest rules for {crop}"
        assert Category.NUTRIENT in categories, f"Missing nutrient rules for {crop}"


def test_rule_modalities():
    """Course concept: Hardcoded, May or May Not, and Extended rules."""
    hardcoded = [r for r in RULES if r.rule_type == RuleType.HARDCODED]
    may_or_not = [r for r in RULES if r.rule_type == RuleType.MAY_OR_MAY_NOT]
    extended = [r for r in RULES if r.rule_type == RuleType.EXTENDED]

    assert len(hardcoded) >= 20, "Expected robust set of deterministic hardcoded rules"
    assert len(may_or_not) >= 10, "Expected probabilistic may-or-may-not rules with CF"
    assert len(extended) >= 5, "Expected extended rules refining base rules"

    for r in hardcoded:
        assert r.certainty_factor == 1.0, f"Hardcoded rule {r.rule_id} must have CF=1.0"

    for r in may_or_not:
        assert 0.4 <= r.certainty_factor < 1.0, f"May-or-May-Not rule {r.rule_id} CF out of range"

    for r in extended:
        assert r.extended_from is not None, f"Extended rule {r.rule_id} must cite extended_from"


# ============================================================================
# 2. WORKING MEMORY TESTS
# ============================================================================

def test_working_memory_state_operations(memory: WorkingMemory):
    memory.assert_fact("crop", "wheat")
    memory.assert_fact("stage", "flowering", confidence=0.85)

    assert memory.has_fact("crop")
    assert memory.get_fact_value("crop") == "wheat"
    assert memory.get_fact("stage").confidence == 0.85
    assert memory.get_fact_value("nonexistent", "default_val") == "default_val"

    memory.log_rule_firing("TEST-001", "hardcoded", {"test": True})
    assert len(memory.get_fired_rules()) == 1

    memory.retract_fact("crop")
    assert not memory.has_fact("crop")

    memory.clear()
    assert len(memory.all_facts()) == 0
    assert len(memory.get_fired_rules()) == 0


# ============================================================================
# 3. DISEASE IDENTIFICATION TESTS
# ============================================================================

def test_disease_wheat_yellow_rust(engine: InferenceEngine, memory: WorkingMemory):
    memory.assert_fact("crop", "wheat")
    memory.assert_fact("symptoms", ["yellow_pustules_stripes"])
    memory.assert_fact("weather", "cool_humid")

    res = engine.evaluate(memory, Category.DISEASE)
    assert res.success is True
    assert "Yellow Rust" in res.diagnosis
    assert res.confidence == 100.0
    assert len(res.remedies) >= 1


def test_disease_cotton_clcuv_extended(engine: InferenceEngine, memory: WorkingMemory):
    """Hot dry weather escalates CLCuV into extended epidemic rule."""
    memory.assert_fact("crop", "cotton")
    memory.assert_fact("symptoms", ["leaf_curling_upward", "thickened_veins"])
    memory.assert_fact("weather", "hot_dry")

    res = engine.evaluate(memory, Category.DISEASE)
    assert res.success is True
    assert "CLCuV" in res.diagnosis
    assert res.details.get("rule_type") == "extended"
    assert res.confidence == 95.0


def test_disease_rice_blast(engine: InferenceEngine, memory: WorkingMemory):
    memory.assert_fact("crop", "rice")
    memory.assert_fact("symptoms", ["spindle_eye_shaped_lesions", "brown_margin_grey_center"])

    res = engine.evaluate(memory, Category.DISEASE)
    assert res.success is True
    assert "Rice Blast" in res.diagnosis


def test_disease_sugarcane_red_rot(engine: InferenceEngine, memory: WorkingMemory):
    memory.assert_fact("crop", "sugarcane")
    memory.assert_fact("symptoms", ["reddened_internal_pith", "alcohol_sour_smell"])

    res = engine.evaluate(memory, Category.DISEASE)
    assert res.success is True
    assert "Red Rot" in res.diagnosis


def test_disease_maize_turcicum(engine: InferenceEngine, memory: WorkingMemory):
    memory.assert_fact("crop", "maize")
    memory.assert_fact("symptoms", ["long_elliptical_grey_green_lesions"])

    res = engine.evaluate(memory, Category.DISEASE)
    assert res.success is True
    assert "Northern Corn Leaf Blight" in res.diagnosis


# ============================================================================
# 4. PEST MANAGEMENT & PRE-HARVEST SAFETY TESTS
# ============================================================================

def test_pest_cotton_pink_bollworm(engine: InferenceEngine, memory: WorkingMemory):
    memory.assert_fact("crop", "cotton")
    memory.assert_fact("plant_zone", "fruit")
    memory.assert_fact("damage", ["bore_holes"])
    memory.assert_fact("sightings", "caterpillars")
    memory.assert_fact("near_harvest", False)

    res = engine.evaluate(memory, Category.PEST)
    assert res.success is True
    assert "Pink Bollworm" in res.diagnosis
    assert res.chemical_blocked is False


def test_pest_pre_harvest_safety_lockout(engine: InferenceEngine, memory: WorkingMemory):
    """Crucial safety test: Near harvest blocks toxic chemicals."""
    memory.assert_fact("crop", "cotton")
    memory.assert_fact("plant_zone", "fruit")
    memory.assert_fact("damage", ["bore_holes"])
    memory.assert_fact("sightings", "caterpillars")
    memory.assert_fact("near_harvest", True)

    res = engine.evaluate(memory, Category.PEST)
    assert res.success is True
    assert res.chemical_blocked is True
    assert any("SAFETY WARNING" in r or "BLOCKED" in r for r in res.remedies)


# ============================================================================
# 5. NUTRIENT DEFICIENCY & SOIL pH TESTS
# ============================================================================

def test_soil_acidity_lime_fix(engine: InferenceEngine, memory: WorkingMemory):
    memory.assert_fact("crop", "all")
    memory.assert_fact("soil_ph", 5.0)

    res = engine.evaluate(memory, Category.NUTRIENT)
    assert res.success is True
    assert "Soil Acidity Fix" in res.diagnosis
    assert any("Limestone" in r for r in res.remedies)


def test_soil_alkalinity_gypsum_fix(engine: InferenceEngine, memory: WorkingMemory):
    memory.assert_fact("crop", "all")
    memory.assert_fact("soil_ph", 8.4)

    res = engine.evaluate(memory, Category.NUTRIENT)
    assert res.success is True
    assert "Soil Alkalinity" in res.diagnosis
    assert any("Gypsum" in r for r in res.remedies)


def test_nutrient_rice_khaira_zinc(engine: InferenceEngine, memory: WorkingMemory):
    memory.assert_fact("crop", "rice")
    memory.assert_fact("discoloration", "interveinal_chlorosis")
    memory.assert_fact("stage", "vegetative")
    memory.assert_fact("soil_ph", 8.0)

    res = engine.evaluate(memory, Category.NUTRIENT)
    assert res.success is True
    assert "Zinc" in res.diagnosis


# ============================================================================
# 6. EXPLANATION & SYSTEM BOUNDARY TESTS
# ============================================================================

def test_system_knows_its_limitations(
    engine: InferenceEngine, explainer: ExplanationModule, memory: WorkingMemory
):
    """Instructor requirement: System knows its limitations when signs are outside knowledge base."""
    memory.assert_fact("crop", "wheat")
    memory.assert_fact("symptoms", ["strange_silver_spots_from_space"])

    res = engine.evaluate(memory, Category.DISEASE)
    assert res.success is False
    assert res.confidence == 0.0

    exp = explainer.explain(res, memory)
    assert exp["success"] is False
    assert "limitations" in exp
    assert len(exp["steps"]) >= 2
    assert any("Boundary" in s["step"] for s in exp["steps"])


def test_partial_match_single_symptom_for_multi_symptom_rule(
    engine: InferenceEngine, memory: WorkingMemory
):
    """When user provides 1 of 2 required symptoms, engine returns a partial match
    instead of 'Unknown Condition'."""
    memory.assert_fact("crop", "cotton")
    # CLCuV rule C-DIS-001 requires ["leaf_curling_upward", "thickened_veins"]
    # Providing only one symptom should trigger partial match fallback
    memory.assert_fact("symptoms", ["leaf_curling_upward"])

    res = engine.evaluate(memory, Category.DISEASE)
    assert res.success is True
    assert "Possible" in res.diagnosis
    assert res.confidence > 0.0
    assert res.confidence <= 50.0  # Capped at PARTIAL_MATCH_CF_CAP
    assert res.limitation_notice is not None
    assert "partial" in res.limitation_notice.lower()


def test_partial_match_does_not_override_exact_match(
    engine: InferenceEngine, memory: WorkingMemory
):
    """When an exact match exists, partial match path is not used."""
    memory.assert_fact("crop", "cotton")
    memory.assert_fact("symptoms", ["leaf_curling_upward", "thickened_veins"])

    res = engine.evaluate(memory, Category.DISEASE)
    assert res.success is True
    assert "Possible" not in res.diagnosis
    assert res.limitation_notice is None


def test_pest_partial_match_damage_without_sighting(
    engine: InferenceEngine, memory: WorkingMemory
):
    """Pest rule requiring zone + damage + sighting still matches partially when only zone + damage provided."""
    memory.assert_fact("crop", "wheat")
    memory.assert_fact("plant_zone", "leaves")
    memory.assert_fact("damage", ["sticky_honeydew"])
    # Omitting "sightings": "tiny_green_insects"

    res = engine.evaluate(memory, Category.PEST)
    assert res.success is True
    assert "Possible" in res.diagnosis
    assert "Aphid" in res.diagnosis
    assert res.confidence <= 50.0
    assert res.limitation_notice is not None


def test_nutrient_partial_match_discoloration_without_ph(
    engine: InferenceEngine, memory: WorkingMemory
):
    """Nutrient rule requiring discoloration + pH range matches partially when only discoloration is known."""
    memory.assert_fact("crop", "wheat")
    memory.assert_fact("discoloration", "interveinal_chlorosis")
    memory.assert_fact("stage", "vegetative")
    # Omitting ph_min/ph_max

    res = engine.evaluate(memory, Category.NUTRIENT)
    assert res.success is True
    assert "Possible" in res.diagnosis
    assert "Zinc" in res.diagnosis
    assert res.confidence <= 50.0


def test_passive_facts_alone_do_not_trigger_partial_match(
    engine: InferenceEngine, memory: WorkingMemory
):
    """Asserting only contextual facts (like plant_zone or stage) with NO symptoms/damage must NOT trigger a false diagnosis."""
    memory.assert_fact("crop", "cotton")
    memory.assert_fact("plant_zone", "leaves")

    res = engine.evaluate(memory, Category.PEST)
    assert res.success is False
    assert "Unknown" in res.diagnosis


def test_inference_latency_benchmark(engine: InferenceEngine, memory: WorkingMemory):
    """Instructor requirement: Inference engine evaluates rule chain in < 1.0 second."""
    memory.assert_fact("crop", "wheat")
    memory.assert_fact("symptoms", ["yellow_pustules_stripes"])
    memory.assert_fact("weather", "cool_humid")

    t0 = time.perf_counter()
    res = engine.evaluate(memory, Category.DISEASE)
    duration = time.perf_counter() - t0

    assert res.success is True
    assert duration < 1.0, f"Evaluation took {duration:.4f}s (must be < 1.0s)"
