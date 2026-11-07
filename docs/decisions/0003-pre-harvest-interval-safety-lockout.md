# ADR-003: Pre-Harvest Interval (PHI) Toxic Chemical Lockout Guard

## Status
Accepted

## Date
2026-11-07

## Context
In agricultural pest management in Pakistan, indiscriminate pesticide application close to harvest causes severe chemical residue contamination in food grains (wheat, rice), export crops (Basmati, cotton fiber), and sugarcane juice. 

Standard agronomic safety codes enforce a "Pre-Harvest Interval" (PHI) — a mandatory waiting period between pesticide spray and harvest. If a farmer reports a pest outbreak when harvest is imminent (< 14–21 days), recommending synthetic neurotoxic insecticides (e.g. Cartap, Chlorpyrifos, Profenofos) violates food safety regulations.

## Decision
Incorporate a deterministic safety guard in `inference_engine.py` and `app.py`:
1. The Pest Identification module accepts an input toggle: `near_harvest: bool`.
2. When `near_harvest` is active, the engine intercepts the candidate rule's conclusions.
3. Synthetic chemical insecticides are suppressed (`chemical_blocked = True`).
4. A prominent alert banner is displayed in the UI.
5. Non-toxic biological controls (Bt spray, Trichogramma cards, neem extract) and cultural practices are mandated exclusively.

## Alternatives Considered

### 1. Show Chemical Options with a Small Disclaimer
- **Pros:** Shows all database remedies.
- **Cons:** Farmers or evaluators might miss the disclaimer; unsafe agricultural advice.
- **Rejected:** Expert systems have a duty of care in life-critical and food-safety domains.

### 2. Hard Lockout of Synthetic Chemicals
- **Pros:** Guaranteed prevention of illegal pesticide recommendations; satisfies course safety rubrics.
- **Accepted:** Chosen approach.

## Consequences
- Farmers near harvest are protected from grain contamination and export rejection.
- Clearly demonstrates safety boundaries during viva defense.
- Fully verified by automated unit tests in `tests/test_rules.py` and `tests/test_ui.py`.
