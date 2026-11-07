# Implementation Plan: Pakistan Agriculture Expert System (Kisan Rahbar)

## Overview
A fault-tolerant, pure Python rule-based expert system and Streamlit web application providing disease identification, pest management, and fertilizer prescriptions for Pakistan's top 5 crops (Wheat, Cotton, Rice, Sugarcane, Maize). It satisfies all university CCP course requirements: 50+ rules, 3 rule modalities (hardcoded, may-or-may-not, extended), working memory, explanation facility, and sub-second zero-crash inference.

## Architecture Decisions
- **Pure Python Engine:** No external binary dependencies (no SWI-Prolog) to guarantee 100% stability on Streamlit Community Cloud.
- **Rule Categorization:**
  - *Hardcoded:* 1.0 certainty factor exact symptom-crop matches.
  - *May or May Not:* Partial symptom matches with explicit Certainty Factors (0.4 - 0.85).
  - *Extended:* Rules that take base condition and refine/override conclusion based on environmental/weather/crop-stage triggers.
- **Defensive Execution:** The inference engine and UI are wrapped in safe boundary handlers; unmatched inputs return informative diagnostic guidance rather than unhandled Python exceptions.
- **Modular Component Isolation:** Direct separation of concerns per high-level design: UI (`app.py`), Engine (`inference_engine.py`), Memory (`working_memory.py`), Rules (`knowledge_base.py`), Explanations (`explanation_module.py`).

## Task List

### Phase 1: Environment & Knowledge Base Foundation
- [ ] Task 1: Environment Setup & Data Contracts (`requirements.txt`, core classes)
- [ ] Task 2: 50+ Agricultural Rules Codification (`knowledge_base.py`)
- [ ] Checkpoint: Foundation & Rules verification (>= 50 rules defined across 5 crops)

### Phase 2: Engine, Working Memory & Explanation Module
- [ ] Task 3: Working Memory & State Management (`working_memory.py`)
- [ ] Task 4: Pure Python Inference Engine (`inference_engine.py`)
- [ ] Task 5: Explanation & Limitations Facility (`explanation_module.py`)
- [ ] Task 6: Comprehensive Unit Test Suite (`tests/test_rules.py`)
- [ ] Checkpoint: Engine & Logic verification (all tests pass, inference < 1.0s)

### Phase 3: Streamlit UI & End-to-End Verification
- [ ] Task 7: Streamlit UI - Disease Diagnosis Tab (`app.py`)
- [ ] Task 8: Streamlit UI - Pest Management Tab with Pre-Harvest Safety Guard (`app.py`)
- [ ] Task 9: Streamlit UI - Soil & Fertilizer Prescription Tab (`app.py`)
- [ ] Task 10: Fault-Tolerance & Deployment Audit (Streamlit reload < 500ms, zero tracebacks)
- [ ] Checkpoint: Complete System End-to-End Test and Viva Readiness

## Risks and Mitigations
| Risk | Impact | Mitigation |
|------|--------|------------|
| Rule count < 50 triggers marks deduction | High | Programmatic test assertion in `tests/test_rules.py` enforcing `len(RULES) >= 50`. |
| Unhandled exception during viva evaluation | High | Engine returns structured `InferenceResult` with error/boundary flags; UI never bubbles raw tracebacks. |
| Streamlit Cloud deployment failures | Medium | Keep dependencies minimal (`streamlit`, `pytest`) in standard `requirements.txt`. |
| Performance latency exceeding 1.0s | Low | Rules indexed by category and crop in memory; direct dict matching evaluates in < 5ms. |

## Open Questions
- None. Spec and requirements approved.
