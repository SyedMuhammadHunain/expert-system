# Tasks: Code Comment Cleanup (Antislop-Code)

## Task 1: Clean comments in `knowledge_base.py` and `working_memory.py`
**Description:** Scan `knowledge_base.py` and `working_memory.py` for decorative separator banners, redundant field restatements, or empty category markers. Keep rule definitions, certainty factor documentation, and domain metadata unchanged.

**Acceptance criteria:**
- [x] No decorative box headers or banner lines (`# ====...`).
- [x] Obvious field echo comments removed.
- [x] Core domain rule docstrings and constraints preserved.
- [x] Code syntax and logic 100% untouched.

**Verification:**
- [x] `.venv/bin/pytest` passes.

**Dependencies:** None

**Files likely touched:**
- `knowledge_base.py`
- `working_memory.py`

**Estimated scope:** Small (2 files)

---

## Task 2: Clean comments in `inference_engine.py` and `explanation_module.py`
**Description:** Remove obvious line-by-line narrations or decorative comments in inference engine and explanation module while keeping algorithm notes (forward chaining, conflict resolution, MYCIN certainty factor formulas).

**Acceptance criteria:**
- [x] No empty labels or workflow narration comments.
- [x] Mathematical formulas and resolution logic explanations preserved.
- [x] Code syntax and logic 100% untouched.

**Verification:**
- [x] `.venv/bin/pytest` passes.

**Dependencies:** Task 1

**Files likely touched:**
- `inference_engine.py`
- `explanation_module.py`

**Estimated scope:** Small (2 files)

---

## Checkpoint: Core Engine Integrity
- [x] `.venv/bin/pytest` passes all tests.
- [x] Engine files free of comment slop.

---

## Task 3: Clean comments in `app.py`
**Description:** Remove decorative section headers (`# ============================================================================`), empty category headers (`# Tabs`, `# Metrics row`, `# Header`), and trivial narration comments. Keep UI safety warnings and chemical application explanations.

**Acceptance criteria:**
- [x] Section banners replaced or removed.
- [x] Empty UI labels removed.
- [x] Streamlit rendering code and layout completely untouched.

**Verification:**
- [x] `.venv/bin/pytest` passes.
- [x] `python3 -m py_compile app.py` succeeds.

**Dependencies:** Task 2

**Files likely touched:**
- `app.py`

**Estimated scope:** Medium (1 large file)

---

## Task 4: Clean comments in `tests/test_rules.py` and `tests/test_ui.py`
**Description:** Remove redundant step narration in tests (e.g. `# Arrange`, `# Act`, `# Assert` or repeated trivial notes) while preserving test fixture context or non-obvious assertion rationale.

**Acceptance criteria:**
- [x] Test comments concise, natural, and non-repetitive.
- [x] Zero changes to test assertions, logic, or fixtures.

**Verification:**
- [x] `.venv/bin/pytest` passes.

**Dependencies:** Task 3

**Files likely touched:**
- `tests/test_rules.py`
- `tests/test_ui.py`

**Estimated scope:** Small (2 files)

---

## Checkpoint: Final Delivery Gate
- [x] All 34 tests pass via `.venv/bin/pytest`.
- [x] `git diff` shows only comment deletions/modifications.
- [x] Code comment checklist verified.
