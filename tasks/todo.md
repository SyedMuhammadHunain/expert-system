# Tasks: Partial-Matching Fallback & Single-Symptom Resolution

## Task 1: Complete Partial-Matching Scoring in Inference Engine
**Description:** Ensure `_partial_match_score` in `inference_engine.py` handles all condition keys correctly (`symptoms`, `weather`, `plant_zone`, `damage`, `sightings`, `discoloration`, `stage`, `ph_min`, `ph_max`). Return proportional match ratio and captured conditions.
**Acceptance criteria:**
- [x] Disease rules with 2+ conditions fire as partial matches when 1 symptom is asserted.
- [x] Pest rules fire as partial matches when only plant zone and 1 damage sign or 1 sighting is asserted.
- [x] Nutrient rules fire as partial matches when only discoloration is asserted without specific pH.
- [x] Partial CF is scaled proportionally and hard-capped at 0.50 (50%).
**Verification:**
- [x] `pytest tests/test_rules.py` passes with dedicated partial matching assertions.
**Dependencies:** None
**Files likely touched:**
- `inference_engine.py`
- `tests/test_rules.py`
**Estimated scope:** Small (2 files)

---

## Task 2: Refine Explanation Trace & Boundary Explanations
**Description:** Enhance `ExplanationTrace` generation for partial matches so the user sees which conditions matched, which conditions were missing, and specific next observational steps.
**Acceptance criteria:**
- [ ] Trace includes an explicit limitation notice for partial matches.
- [ ] Diagnosis string appends `(Possible)` to prevent overconfidence.
- [ ] `remedies` are preserved and include advice to inspect missing symptoms.
**Verification:**
- [ ] Unit tests verify `res.limitation_notice` is populated on partial match.
**Dependencies:** Task 1
**Files likely touched:**
- `inference_engine.py`
- `tests/test_rules.py`
**Estimated scope:** Small (2 files)

---

## Checkpoint 1: Engine Logic Verification
- [ ] Unit tests pass: `pytest -v tests/test_rules.py`
- [ ] Latency remains < 10ms

---

## Task 3: Update Streamlit UI for Partial Confidence Feedback
**Description:** Update `app.py` diagnostic cards (Disease, Pest, and Nutrient tabs) to render a distinct status banner (`st.warning` with informative caption) when `result.limitation_notice` indicates a partial match.
**Acceptance criteria:**
- [ ] Tab 1 (Disease) shows an alert and guidance when a partial match is diagnosed.
- [ ] Tab 2 (Pest) handles partial pest matches cleanly with the pre-harvest safety guard intact.
- [ ] Tab 3 (Nutrient) displays partial deficiency suggestions when only discoloration is provided.
**Verification:**
- [ ] Visual verification and test run in `tests/test_ui.py`.
**Dependencies:** Task 1, 2
**Files likely touched:**
- `app.py`
**Estimated scope:** Small (1 file)

---

## Task 4: Add Automated UI Regression Tests for Single-Symptom Scenarios
**Description:** Add headless Streamlit AppTests in `tests/test_ui.py` simulating a user selecting exactly 1 symptom with default weather across crops to guarantee no unexpected "Unknown Condition" failure.
**Acceptance criteria:**
- [ ] AppTest simulates single-symptom selection (e.g., cotton `leaf_curling_upward`) and asserts valid diagnosis is rendered.
- [ ] AppTest tests pest tab with only 1 visible damage selected.
- [ ] All 26+ tests pass cleanly.
**Verification:**
- [ ] `pytest -v tests/` completes in < 3s with 100% passing tests.
**Dependencies:** Task 3
**Files likely touched:**
- `tests/test_ui.py`
**Estimated scope:** Small (1 file)

---

## Checkpoint 2: Complete System Verification
- [ ] Full test suite green (`pytest -v tests/`)
- [ ] Single-symptom inputs reliably produce actionable advice
- [ ] Code committed and pushed to git
