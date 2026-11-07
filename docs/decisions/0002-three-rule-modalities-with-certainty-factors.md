# ADR-002: Three Rule Modalities (Hardcoded, May-or-May-Not, Extended) with Certainty Factors

## Status
Accepted

## Date
2026-11-07

## Context
The university course instructor explicitly evaluated students on their ability to design expert systems that recognize uncertainty and evolutionary rule refinement. The instructor taught three specific modalities:
1. **Hardcoded:** Exact match where facts yield 100% deterministic conclusion.
2. **May or May Not:** Probabilistic partial matches with Certainty Factors (0.50 - 0.85).
3. **Extended:** Rules that take a base hardcoded rule and modify/escalate the diagnosis or remedy when secondary facts emerge.

## Decision
Codify 60 rules in `knowledge_base.py` categorized by `RuleType` enum (`HARDCODED`, `MAY_OR_MAY_NOT`, `EXTENDED`):
- **34 Hardcoded rules** ($CF = 1.0$) for textbook crop symptoms.
- **15 May-or-May-Not rules** ($CF \in [0.50, 0.85]$) for ambiguous/early-stage symptoms.
- **11 Extended rules** ($CF \ge 0.90$) linked to parent rules via `extended_from`, prioritizing escalation during adverse weather or harvest proximity.

In conflict resolution (`inference_engine.py`), `EXTENDED` rules supersede their parent rules and inherit higher priority.

## Alternatives Considered

### 1. Pure Boolean Logic
- **Pros:** Simpler code.
- **Cons:** Cannot represent real-world agricultural uncertainty (e.g. leaf spots that could be either rust or nutrient scorch).
- **Rejected:** Fails instructor viva requirement.

### 2. Full Bayesian Network
- **Pros:** Mathematically rigorous conditional probabilities.
- **Cons:** Requires extensive prior joint probability tables that Pakistani local field conditions lack.
- **Rejected:** Disproportionate complexity for a 60-rule expert system.

### 3. MYCIN-Style Certainty Factors with Modality Classification
- **Pros:** Directly aligns with university lecture concepts; simple combination algebra ($CF_{combined} = CF_{rule} \times \min(CF_{facts})$); reviewable by instructors.
- **Accepted:** Chosen approach.

## Consequences
- Every rule firing explains its exact modality in the UI audit card.
- Demonstrates mastery of academic AI course concepts during viva.
- Conflict resolution gives predictable precedence to specific environmental extensions.
