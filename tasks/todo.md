# Tasks: Generate Project Report Word Document (.docx)

## Task 1: Environment Setup
**Description:** Install `python-docx` into the local virtual environment (`.venv`) so Python can programmatically build the `.docx` document.
**Acceptance criteria:**
- [x] `python-docx` installed in `.venv`.
- [x] `.venv/bin/python3 -c "import docx"` succeeds.
**Verification:**
- [x] Exit code 0 on python import test.
**Dependencies:** None
**Files likely touched:** None
**Estimated scope:** Small

---

## Task 2: Build and Execute Report Generation Script
**Description:** Create `scripts/generate_docx_report.py` to construct `Project_Report_Expert_System.docx` strictly fulfilling:
1. Dotted Table of Contents with page references.
2. Introduction: 1 simple paragraph.
3. Problem Statement: Exactly 4 lines in one paragraph.
4. Requirements:
   - Subheading Functional Requirements: 2-column table (`Requirement` | `Description`) from `expert-system.md`.
   - Subheading Non-Functional Requirements: 2-column table (`Requirement` | `Description`) from `expert-system.md`.
5. High Level Design: Blank placeholder area.
6. Code Explanation: Blank placeholder area.
7. Results: Blank placeholder area.
8. Summary: Exactly 5 lines in one paragraph.
9. Format: Main headings Bold + Italic + Underlined; 100% black font, zero colors, zero table fills.
**Acceptance criteria:**
- [ ] Document generated at `Project_Report_Expert_System.docx`.
- [ ] All main headings are bold, italic, and underlined.
- [ ] Tables use only black text and white cells (no blue, light blue, or colored shading).
- [ ] Requirements extracted from `expert-system.md`.
**Verification:**
- [ ] Python script runs cleanly and inspects generated docx structure.
**Dependencies:** Task 1
**Files likely touched:**
- `scripts/generate_docx_report.py`
- `Project_Report_Expert_System.docx`
**Estimated scope:** Medium (1 script + 1 docx)

---

## Checkpoint: Sign-off and Delivery
- [ ] Document verified and confirmed on disk.
- [ ] Ready for user editing and viva submission.
