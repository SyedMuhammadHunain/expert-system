# Implementation Plan: Clean Code Comments via Antislop-Code

## Overview
Audit and clean code comments across the Python codebase (`app.py`, `inference_engine.py`, `knowledge_base.py`, `working_memory.py`, `explanation_module.py`, and test files). Remove decorative banner headers (`# ============`), narrating step-by-step markers, empty category labels, and obvious restatements. Preserve business logic, domain agrochemical rules, safety constraints (such as pre-harvest safety lockout rationale), and architectural/API contracts. Keep executable code completely untouched.

## Architecture Decisions
- Scope Guardrail: Modify comment lines and inline comments only. Never change executable code, logic, variable names, imports, or whitespace formatting.
- Preservation Rule: Maintain docstrings with actual specifications, rule explanations, and critical constraints (e.g., PHI lockouts, CF calculations).
- Targeted Patterns:
  - Banners: `# ============================================================================`
  - Empty Labels: `# Metrics row`, `# Header`, `# Tabs`, `# Certainty factor visual meter`
  - Workflow Narration: `# Step 1...`, trivial `# Retrieve crop-specific symptoms`

## Task List

### Phase 1: Core Engine & Domain Models
- [x] Task 1: Audit and clean comments in `knowledge_base.py` and `working_memory.py`
- [x] Task 2: Audit and clean comments in `inference_engine.py` and `explanation_module.py`

### Checkpoint: Engine Integrity
- [x] Run test suite `.venv/bin/pytest` to ensure 100% test pass and zero behavioral regression

### Phase 2: Application UI & Tests
- [x] Task 3: Audit and clean comments in `app.py`
- [x] Task 4: Audit and clean comments in `tests/test_rules.py` and `tests/test_ui.py`

### Checkpoint: Final Verification
- [x] All 34 tests pass via `.venv/bin/pytest`
- [x] Diff inspection confirms zero executable code changes (only `#` comment lines edited or deleted)
- [x] Checklist in `antislop-code` satisfied

## Risks and Mitigations
| Risk | Impact | Mitigation |
|------|--------|------------|
| Accidental removal of essential domain constraints | Medium | Strict check against `antislop-code` "Not a Ban" list before deleting any non-banner comment. |
| Code formatting or whitespace disruption | Low | Only remove or trim comment tokens; run pytest after every phase. |

## Open Questions
- None. Scope confirmed.
