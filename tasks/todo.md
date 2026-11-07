# Tasks: Pakistan Agriculture Expert System

## Task 1: Environment Setup & Data Contracts
**Description:** Create project dependencies in `requirements.txt` and define core domain data structures (`Rule`, `Fact`, `InferenceResult`, `ExplanationTrace`).
**Acceptance criteria:**
- [x] `requirements.txt` contains `streamlit` and `pytest`.
- [x] Core classes defined with type hints.
**Verification:**
- [x] Dependencies installable via `pip`.
- [x] Class definitions importable without syntax error.
**Dependencies:** None
**Files likely touched:**
- `requirements.txt`
- `knowledge_base.py`
**Estimated scope:** Small (1-2 files)

---

## Task 2: 50+ Agricultural Rules Codification
**Description:** Codify minimum 50 realistic agricultural rules for Pakistan across 5 crops (Wheat, Cotton, Rice, Sugarcane, Maize) covering diseases, pests, and nutrient deficiencies. Include hardcoded (1.0 CF), may-or-may-not (0.4-0.85 CF), and extended rule variants.
**Acceptance criteria:**
- [x] Total rule count >= 50.
- [x] All 5 crops have coverage across Disease, Pest, and Nutrient categories.
- [x] Each rule specifies remedies, severity, or fertilizer formulas.
**Verification:**
- [x] Python assertion script confirms `len(RULES) >= 50`.
**Dependencies:** Task 1
**Files likely touched:**
- `knowledge_base.py`
**Estimated scope:** Medium (1-2 files)

---

## Checkpoint 1: Foundation Checkpoint
- [x] `requirements.txt` ready
- [x] >= 50 valid rules loaded in `knowledge_base.py` (60 rules codified)

---

## Task 3: Working Memory & State Management
**Description:** Implement `working_memory.py` to maintain asserted user facts, active hypotheses, matched rules stack, and current query parameters per user session.
**Acceptance criteria:**
- [x] Supports asserting facts, clearing memory, querying asserted facts, and logging rule firings.
- [x] Pure Python without external state dependencies.
**Verification:**
- [x] Unit test creating working memory, asserting facts, and verifying query lookups.
**Dependencies:** Task 1
**Files likely touched:**
- `working_memory.py`
**Estimated scope:** Small (1 file)

---

## Task 4: Pure Python Inference Engine
**Description:** Implement forward-chaining rule inference engine in `inference_engine.py` that evaluates facts against knowledge base rules, resolves Certainty Factors, executes rule extensions, and handles conflict resolution.
**Acceptance criteria:**
- [x] Evaluates exact matches (hardcoded), uncertain matches (may or may not), and extended rules.
- [x] Returns structured `InferenceResult` in < 1.0s.
- [x] Gracefully handles unrecognized input with safe empty/boundary flag rather than throwing unhandled exceptions.
**Verification:**
- [x] Python tests executing queries for known and unknown cases.
**Dependencies:** Tasks 2, 3
**Files likely touched:**
- `inference_engine.py`
**Estimated scope:** Small (1-2 files)

---

## Task 5: Explanation & Limitations Facility
**Description:** Implement `explanation_module.py` to produce human-readable reasoning traces, explain why a conclusion was reached, display certainty factor math, and detail system boundary limitations when symptoms do not match.
**Acceptance criteria:**
- [x] Generates step-by-step reasoning trace from fired rules.
- [x] Explains why treatment/fertilizer was prescribed.
- [x] Formulates clear limitation notice when user inputs fall outside known rule database.
**Verification:**
- [x] Unit test verifying trace generation on positive and negative inference outcomes.
**Dependencies:** Tasks 3, 4
**Files likely touched:**
- `explanation_module.py`
**Estimated scope:** Small (1 file)

---

## Task 6: Comprehensive Unit Test Suite
**Description:** Build test suite in `tests/test_rules.py` covering rule count assertion (>= 50), rule firing across all 5 crops, certainty factor mechanics, safety constraints, and edge case resilience.
**Acceptance criteria:**
- [x] `pytest tests/` passes 100%.
- [x] `assert len(RULES) >= 50` passes.
- [x] Tests verify pre-harvest chemical restrictions and fault tolerance.
**Verification:**
- [x] Run `pytest -v tests/`.
**Dependencies:** Tasks 2, 3, 4, 5
**Files likely touched:**
- `tests/test_rules.py`
**Estimated scope:** Medium (1-2 files)

---

## Checkpoint 2: Engine & Core Logic Checkpoint
- [x] All unit tests pass with `pytest` (16/16 passed in 0.03s)
- [x] Latency verified < 1.0 second (measured ~0.012ms)
- [x] Explanation traces generated cleanly

---

## Task 7: Streamlit UI - Disease Diagnosis Tab
**Description:** Build Tab 1 in `app.py`: Crop selection dropdown, multi-select symptom checklist, weather conditions radio, and responsive diagnosis card displaying disease name, certainty %, and treatment recommendations.
**Acceptance criteria:**
- [x] Matches all Tab 1 specifications in `expert-system.md`.
- [x] Fast rendering (< 500ms) with clean layout and responsive columns.
**Verification:**
- [x] Syntax check and headless test of app module.
**Dependencies:** Tasks 4, 5
**Files likely touched:**
- `app.py`
**Estimated scope:** Medium (1 file)

---

## Task 8: Streamlit UI - Pest Management Tab with Pre-Harvest Guard
**Description:** Build Tab 2 in `app.py`: Plant zone selectbox, visible damage signs multiselect, pest sightings radio, harvest proximity toggle, and output card displaying pest species, severity tier, biological controls vs chemical insecticides, with chemical lockout when harvest is close.
**Acceptance criteria:**
- [x] Matches all Tab 2 specifications in `expert-system.md`.
- [x] Blocks toxic chemicals with a warning card when harvest is imminent.
**Verification:**
- [x] Interactive / programmatic validation of pre-harvest safety guard.
**Dependencies:** Tasks 4, 5
**Files likely touched:**
- `app.py`
**Estimated scope:** Small (1 file)

---

## Task 9: Streamlit UI - Soil & Fertilizer Prescription Tab
**Description:** Build Tab 3 in `app.py`: Growth stage selector, leaf discoloration map, soil pH slider (4.5 to 8.5), displaying missing nutrient badge, NPK fertilizer dosage card, and foliage recovery timeline.
**Acceptance criteria:**
- [x] Matches all Tab 3 specifications in `expert-system.md`.
- [x] Outputs exact NPK dosage per acre and pH remediation guidance.
**Verification:**
- [x] Verification of calculations against soil pH ranges and discoloration symptoms.
**Dependencies:** Tasks 4, 5
**Files likely touched:**
- `app.py`
**Estimated scope:** Small (1 file)

---

## Task 10: Fault-Tolerance, Latency Benchmark & Deployment Audit
**Description:** Perform whole-system hardening: wrap UI interactions in user-friendly error banners, ensure zero unhandled Python tracebacks, benchmark execution speed (< 500ms UI reload, < 1.0s inference), verify `requirements.txt` for Streamlit Cloud, and document WAN deployment steps.
**Acceptance criteria:**
- [x] Fault injection tests confirm no raw Python traceback is ever shown on malformed inputs.
- [x] Latency benchmarks pass.
- [x] System is ready for live Streamlit Community Cloud deployment.
**Verification:**
- [x] End-to-end test run and compile check.
**Dependencies:** Tasks 6, 7, 8, 9
**Files likely touched:**
- `app.py`
- `README.md`
**Estimated scope:** Small (1-2 files)

---

## Checkpoint 3: Complete System Sign-Off
- [x] All 10 tasks completed
- [x] 50+ rules verified (60 rules codified)
- [x] Zero viva crash vulnerabilities (100% boundary defended)
- [x] Live deployment instructions ready
