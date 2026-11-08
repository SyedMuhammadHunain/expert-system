# Implementation Plan: Dynamic Crop Option Reactivity Across All Tabs

## Overview
Currently, in all three tabs (`Tab 1: Disease`, `Tab 2: Pest`, `Tab 3: Nutrient`), inputs are nested inside `st.form(...)`. In Streamlit, forms suppress all client-to-server reruns on widget interaction until form submission. As a result, selecting a new crop never triggers a rerun, leaving the symptom multiselect frozen on the previously loaded crop (Wheat). We will replace `st.form(...)` with reactive `st.container(border=True)` and standard `st.button(...)` controls, enabling instantaneous dropdown reactivity while maintaining the click-to-diagnose workflow and clearing stale selections upon crop switch.

## Architecture Decisions
- **Eliminate `st.form` in Favor of `st.container(border=True)`**: Replaces form buffering with native Streamlit reactive state loops so crop selection triggers instant reactive re-rendering of all dependent dropdowns.
- **Crop-Scoped Widget State Keys**: Use dynamic keys or change detection to clear stale selections (e.g. wheat symptoms selected while on wheat) when switching to another crop (cotton), preventing cross-crop symptom leakage.
- **Maintain Action-Button Gating**: Diagnostic inference remains explicitly gated behind the action button (`Diagnose disease`, `Identify pest`, `Prescribe fertilizer`) so execution only occurs on user demand.
- **Preserve Button Indices**: Retain the exact order of action buttons so headless `AppTest` suites (`at.button[0]`, `at.button[1]`, `at.button[2]`) remain 100% compliant and passing.

## Task List

### Phase 1: Tab 1 Dynamic Crop Reactivity
- [x] Task 1: Refactor Tab 1 (Disease) to reactive container and implement crop-change auto-reset for symptom multiselect.

### Phase 2: Tab 2 & Tab 3 Audit and Reactivity
- [x] Task 2: Refactor Tab 2 (Pest) and Tab 3 (Nutrient) to reactive containers and audit dependent field updates.

### Phase 3: Automated Verification & UI Regression Testing
- [x] Task 3: Add automated headless AppTests verifying dynamic crop selection updates symptom options in real-time without page reload.

## Checkpoint: Final Verification
- [x] Automated test suite green (`pytest -v tests/`).
- [x] Manual verification on live server: selecting Cotton immediately shows Cotton symptoms.

## Risks and Mitigations
| Risk | Impact | Mitigation |
|------|--------|------------|
| Cross-crop symptom pollution in session state | Med | Reset symptom selection whenever crop dropdown changes. |
| Test suite button index mismatch | High | Keep button hierarchy unchanged so `at.button[0..2]` match exactly. |
