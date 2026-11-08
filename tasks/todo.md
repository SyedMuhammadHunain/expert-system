# Tasks: UI Professionalization, Accessibility & Visualization

## Task 1: Complete Emoji Removal from UI & Code
**Description:** Remove every emoji character (e.g., 🌾, 🔬, 🐛, 🌱, 📋, 🔍, 🩺, 🚨, 🛑, 📦, ⏱️, ⚙️, 🔖, 🔎) from `app.py`, page config, headers, tab labels, form buttons, expanders, and cards. Replace with clean textual indicators or native Streamlit material icons (`:material/...:`).
**Acceptance criteria:**
- [x] `st.set_page_config` uses no emoji icon (clean SVG or title).
- [x] Tab titles contain no emojis: `1. Crop Disease Diagnosis`, `2. Pest Management & Safety Lock`, `3. Soil Chemistry & Fertilizer Prescription`.
- [x] All button labels, card headers, and expander titles are free of emojis.
- [x] Regex check confirms 0 emojis in `app.py`.
**Verification:**
- [x] Python unicode regex test confirms zero emoji characters in `app.py`.
- [x] `pytest -v tests/` passes.
**Dependencies:** None
**Files likely touched:**
- `app.py`
**Estimated scope:** Small (1 file)

---

## Task 2: Complete Urdu Language & Transliteration Purge
**Description:** Remove all Urdu script (`[\u0600-\u06ff]`) and romanized Urdu terms (e.g., `Gandum`, `Kapas`, `Dhan`, `Kamad`, `Makai`, `Peeli Kungi`, `Bhoori Kungi`, `Kani`, `تشخیص کریں`) from `app.py`. Standardize all labels and symptoms into precise agronomic English and accepted scientific nomenclature.
**Acceptance criteria:**
- [x] Crop dropdown labels use clean English: `Wheat`, `Cotton`, `Rice`, `Sugarcane`, `Maize`.
- [x] Symptom dictionary values use standard pathological and anatomical English descriptions.
- [x] UI title, sidebar, headers, and form inputs contain 0 Urdu characters or transliterations.
**Verification:**
- [x] Python unicode regex confirms 0 characters in range `\u0600-\u06ff` in `app.py`.
- [x] `pytest -v tests/` passes.
**Dependencies:** Task 1
**Files likely touched:**
- `app.py`
**Estimated scope:** Small (1 file)

---

## Checkpoint 1: Visual & Text Sanitization
- [x] Zero emojis in `app.py`
- [x] Zero Urdu script in `app.py`
- [x] Automated tests pass (`pytest -v tests/`)

---

## Task 3: Improve Readability & Accessibility (WCAG 2.1 AA)
**Description:** Enhance visual hierarchy, typography, contrast, and form semantics. Improve helper descriptions, add structured tables/cards for diagnostic outputs, ensure field labels have descriptive help popovers, and optimize color contrast across alert containers (`st.info`, `st.success`, `st.warning`, `st.error`).
**Acceptance criteria:**
- [x] Semantic heading structure (`h1` -> `h2` -> `h3` -> `h4`) throughout.
- [x] Input widgets feature explicit `help` parameters explaining expected observations to assist screen readers and field users.
- [x] Prescriptions and chemical lockout warnings use high-contrast, structured callouts with clear visual hierarchy.
**Verification:**
- [x] Headless UI tests in `tests/test_ui.py` verify all components render cleanly without exceptions.
**Dependencies:** Tasks 1, 2
**Files likely touched:**
- `app.py`
- `tests/test_ui.py`
**Estimated scope:** Small (1-2 files)

---

## Task 4: Add Sidebar Rule Distribution Chart & Diagnosis Certainty Meter
**Description:** Implement clean, responsive visual analytics using `altair` and `streamlit`. Add a Knowledge Base composition chart (rule counts by crop and domain category) to the sidebar, and render a Certainty Factor gauge/progress bar in the diagnosis cards for Tabs 1 and 2.
**Acceptance criteria:**
- [x] Sidebar displays an Altair horizontal bar chart showing rule distribution across Disease, Pest, and Soil categories.
- [x] Diagnostic reports in Tab 1 and Tab 2 include a visual Certainty Factor bar with calibrated color bands (e.g. Amber <70%, Green >=70%).
- [x] Charts are fully responsive and adapt to dark/light modes.
**Verification:**
- [x] Chart generation runs in < 5ms without rendering errors.
- [x] AppTest in `tests/test_ui.py` verifies charts render without exceptions.
**Dependencies:** Task 3
**Files likely touched:**
- `app.py`
- `tests/test_ui.py`
**Estimated scope:** Medium (1-2 files)

---

## Task 5: Add Soil pH Chemistry Spectrum & NPK Dosage Chart
**Description:** In Tab 3 (Soil & Fertilizer), implement an interactive Soil pH Spectrum Chart (illustrating Acidic, Neutral, and Alkaline zones with an indicator marker for the user's selected pH) and an NPK Macronutrient Recommendation Bar Chart (showing relative kg/acre application rates).
**Acceptance criteria:**
- [ ] Altair pH spectrum chart visually marks acidic (<6.0), optimal (6.0 - 7.5), and alkaline/calcareous (>7.5) ranges with a pointer at the current soil pH.
- [ ] Diagnostic output in Tab 3 displays an NPK dosage breakdown bar chart when nutrient deficiency is identified.
- [ ] Zero external dependencies added (pure `altair` + `pandas`).
**Verification:**
- [ ] AppTest tests verify Tab 3 execution with new charts.
- [ ] `pytest -v tests/` passes completely.
**Dependencies:** Task 4
**Files likely touched:**
- `app.py`
- `tests/test_ui.py`
**Estimated scope:** Medium (1-2 files)

---

## Checkpoint 2: System Sign-Off & Verification
- [ ] 23+ automated tests pass (`pytest -v tests/`)
- [ ] Browser review confirms 0 emojis, 0 Urdu, high readability, and clean responsive charts
- [ ] Changes committed cleanly to git repository
