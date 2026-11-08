# Implementation Plan: Partial-Matching Fallback & Single-Symptom Resolution

## Overview
Enable the expert system to provide meaningful, calibrated advisory responses when users select single symptoms, without returning "Unknown Condition" 80% of the time. When full condition sets are unmet, the engine falls back to partial matching with proportionally scaled Certainty Factors (capped at 50%), transparently labeling conclusions as "Possible" and guiding farmers toward precise verification.

## Architecture Decisions
- **Proportional Condition Scoring**: Rules with $N$ conditions match partially if $K \ge 1$ conditions are satisfied. Score = $\frac{K}{N} \times \text{Rule CF}$, strictly capped at 0.50 (50%).
- **Prioritize Strict Matches**: Full matches always take absolute precedence. Partial matches only evaluate if candidate count for strict matches is zero.
- **Transparent Labelling**: Partial matches append "(Possible)" to diagnosis, display a warning callout, and include explicit limitation notes in the explanation trace.
- **Zero Extra Dependencies**: Handled purely in existing `inference_engine.py` and rendered with native Streamlit components in `app.py`.

## Task List

### Phase 1: Engine Core & Evaluation Logic
- [ ] Task 1: Complete partial match scoring across Disease, Pest, and Nutrient domains in `InferenceEngine`.
- [ ] Task 2: Implement explanation trace and limitation notices for partial match candidates.

### Checkpoint: Engine Verification
- [ ] All unit tests in `tests/test_rules.py` pass with >90% coverage on partial matching logic.

### Phase 2: UI Transparency & Guidance
- [ ] Task 3: Update `app.py` diagnostic cards to render distinct "Possible match (partial confidence)" indicators for Tabs 1, 2, and 3.
- [ ] Task 4: Add headless AppTest test cases in `tests/test_ui.py` covering single-symptom selections for all 5 crops.

### Checkpoint: UI & Integration Complete
- [ ] Automated test suite clean (`pytest -v tests/`).
- [ ] Verify latency remains < 1.0s.

## Risks and Mitigations
| Risk | Impact | Mitigation |
|------|--------|------------|
| Speculative false diagnosis | Med | Cap CF at 50%, add prominent disclaimer and next verification steps. |
| Performance degradation from evaluating partial sets | Low | Partial matching only runs on failure of exact matching cycle; latency stays < 5ms. |
| Test suite regressions | High | Maintain existing strict test fixtures and add dedicated partial match test suites. |

## Open Questions
- None. User approved partial matching fallback approach.
