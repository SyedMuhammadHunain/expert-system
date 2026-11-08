# Tasks: Dynamic Crop Option Reactivity Across All Tabs

## Task 1: Refactor Tab 1 (Disease) to Reactive Container
**Description:** Replace `with st.form("disease_form", border=True):` with `with st.container(border=True):` in `app.py`. Change `st.form_submit_button` to `st.button`. Clear previous symptom selections and diagnostic outputs when a new crop is chosen so symptom options immediately reflect the selected crop.
**Acceptance criteria:**
- [x] Selecting a crop in Tab 1 immediately triggers a rerun and updates the symptom multiselect options to match that crop.
- [x] Switching crops clears previous crop symptom selections.
- [x] "Diagnose disease" button remains the trigger for running the inference engine.
**Verification:**
- [x] Python test confirms selecting a different crop alters `dis_symptoms_select` options.
**Dependencies:** None
**Files likely touched:**
- `app.py`
**Estimated scope:** Small (1 file)

---

## Task 2: Refactor Tab 2 (Pest) and Tab 3 (Nutrient) to Reactive Containers
**Description:** Replace `st.form("pest_form")` and `st.form("nutrient_form")` with `st.container(border=True)` and standard `st.button`. Reset previous diagnostic results and dependent inputs when the target crop changes.
**Acceptance criteria:**
- [x] Tab 2 (Pest) switches reactively without requiring hard refresh; changing crop resets previous results and checklist selections.
- [x] Tab 3 (Nutrient) switches reactively; target crop change updates recommendation context immediately.
- [x] Action buttons `Identify pest and retrieve IPM advisory` and `Prescribe fertilizer and soil remediation` execute cleanly as standard buttons.
**Verification:**
- [x] `pytest tests/test_ui.py` passes all existing test cases.
**Dependencies:** Task 1
**Files likely touched:**
- `app.py`
**Estimated scope:** Small (1 file)

---

## Checkpoint 1: Reactive Container Migration
- [x] Tab 1, 2, and 3 use `st.container(border=True)` instead of `st.form`.
- [x] All 32 automated tests pass (`pytest -v tests/`).

---

## Task 3: Add Automated Headless AppTests for Dynamic Crop Switching
**Description:** In `tests/test_ui.py`, add dedicated `AppTest` test cases that programmatically switch `dis_crop_select` from Wheat to Cotton, Maize, Rice, Sugarcane and verify that the symptom options in `dis_symptoms_select` update dynamically to the correct crop's symptoms without hard refresh.
**Acceptance criteria:**
- [x] Headless test confirms `dis_symptoms_select` options switch from Wheat to Cotton after selectbox change.
- [x] Test confirms selecting Cotton symptom and clicking diagnose produces CLCuV or Bacterial Blight result.
- [x] Full test suite passes in < 3s.
**Verification:**
- [x] `pytest -v tests/` 100% passing.
**Dependencies:** Tasks 1, 2
**Files likely touched:**
- `tests/test_ui.py`
**Estimated scope:** Small (1 file)

---

## Checkpoint 2: Verification and Git Push
- [x] Test suite completely green.
- [x] Verify live Streamlit app running at `http://127.0.0.1:8501`.
- [x] Push atomic commits to GitHub `origin/main`.
