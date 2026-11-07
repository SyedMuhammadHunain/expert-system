# Spec: Pakistan Agriculture Expert System (Kisan Rahbar)

## Objective
Build a fault-tolerant, rule-based agronomy expert system in pure Python and Streamlit for Pakistani farmers and university CCP viva evaluation. It identifies diseases, detects pests, and prescribes fertilizer/soil remedies across Pakistan's 5 major cash/staple crops (Wheat, Cotton, Rice, Sugarcane, Maize) using 50+ deterministic and certainty-factor rules with an explanation facility.

## Tech Stack
- Python 3.10+
- Streamlit >= 1.30 (UI framework)
- Pure Python standard library (no SWI-Prolog / `pyswip` dependency)
- Pytest (rule engine validation and test suite)

## Commands
- Run UI: `streamlit run app.py`
- Run Tests: `pytest -v tests/`
- Lint/Check: `python -m py_compile app.py inference_engine.py working_memory.py knowledge_base.py explanation_module.py`

## Project Structure
```
├── app.py                  # Streamlit interface (3 tabs, alerts, zero raw stack traces)
├── inference_engine.py     # Pure Python forward/rule-chaining engine with Certainty Factors
├── working_memory.py       # Working memory state management (facts, traces, query context)
├── knowledge_base.py       # 50+ rules (Crops: Wheat, Cotton, Rice, Sugarcane, Maize)
├── explanation_module.py   # Decision chain explanations, fired rules trace, system limits
├── tests/
│   └── test_rules.py       # Automated unit tests verifying 50+ rules and edge cases
├── requirements.txt        # Deployment dependencies (streamlit, pytest)
├── high-level-design.png   # Architecture diagram reference
└── expert-system.md        # Original problem statement & academic rubric
```

## Code Style & Conventions
- Pure Python dataclasses or typed dictionaries for Rule and Fact structures.
- No `eval()` or dynamic string execution.
- Graceful error boundary: functions return result objects with success/error states; UI displays friendly `st.warning` / `st.info` on out-of-boundary inputs instead of bubbling tracebacks.

Example:
```python
@dataclass
class Rule:
    rule_id: str
    category: str  # 'disease' | 'pest' | 'nutrient'
    crop: str
    conditions: dict
    conclusion: dict
    rule_type: str  # 'hardcoded' | 'may_or_may_not' | 'extended'
    certainty_factor: float  # 0.0 to 1.0
```

## Testing Strategy
- Framework: `pytest`.
- Test location: `tests/test_rules.py`.
- Criteria:
  1. Verify total rule count >= 50.
  2. Test every crop has disease, pest, and nutrient rules.
  3. Verify certainty factor calculations for "may or may not" rules.
  4. Test edge cases: unrecognized symptoms trigger explanation limitation without crashing.
  5. Test harvest time proximity safety trigger in pest module.

## Boundaries
- **Always:** Keep code 100% pure Python; validate inputs against allowed domains; keep Streamlit reload latency < 500ms; maintain zero unhandled exception traces.
- **Ask first:** Adding new external package dependencies beyond `streamlit` and `pytest`.
- **Never:** Use SWI-Prolog/system binaries; commit personal secrets or university credentials; alter existing user reference diagrams.

## Success Criteria
1. Exactly 50+ verifiable rules codified in `knowledge_base.py`.
2. All 5 crops (Wheat, Cotton, Rice, Sugarcane, Maize) covered across 3 operational tabs:
   - Tab 1: Disease Diagnosis (Crop, symptoms, weather -> Disease name, confidence %, remedies).
   - Tab 2: Pest Management (Plant zone, damage signs, sightings -> Pest species, severity tier, pre-harvest safety guard, bio vs chemical controls).
   - Tab 3: Nutrient Deficiency & Soil Prescription (Growth stage, leaf discoloration, soil pH -> Missing nutrient, NPK dosage card, recovery timeline).
3. Explanation module generates human-readable reasoning trace and explicitly states when input falls outside known facts.
4. Evaluation engine responds in < 1.0 second.
5. All automated tests pass (`pytest tests/`).
6. Streamlit Cloud deployable out-of-the-box via `requirements.txt`.

## Assumptions
1. Deployment target is Streamlit Community Cloud linked to a GitHub repository.
2. English language UI tailored to Pakistani agricultural contexts (local crop names, recognized local treatments).
3. No persistent SQL database needed; session state is managed via Streamlit and `working_memory.py`.

## Open Questions
- None. Intent confirmed.
