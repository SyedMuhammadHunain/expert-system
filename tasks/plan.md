# Implementation Plan: UI Professionalization, Accessibility & Visualization

## Overview
Transform Kisan Rahbar into an enterprise-grade, accessible, academic-grade agronomy expert system UI. Purge all emojis and Urdu text across the entire user interface and documentation. Maximize readability and WCAG accessibility (semantic typography, high contrast, clean card borders, aria labels). Add clean, native charts and graphs using Streamlit native charts and Altair (already installed with zero extra dependencies) to visually display Certainty Factor distributions, soil pH spectrum, and rule coverage metrics.

---

## Recommended Visualizations: Charts & Graphs Analysis

Since `streamlit`, `pandas`, `altair`, and `numpy` are installed out of the box in the virtualenv:

1. **Tab 1 & 2: Diagnosis Certainty Score Bar / Gauge (`altair` or `st.progress`)**
   - Horizontal confidence indicator chart comparing current diagnosis certainty against system threshold (0.50 threshold to 1.0 peak).
   - Color coding: Muted Blue / Dark Teal for high certainty, Amber for partial suspicion.
2. **Tab 3: Soil pH Chemistry Spectrum Bar Chart (`altair`)**
   - Visual band showing Acidic (<6.0, Coral/Amber), Optimal (6.0 - 7.5, Emerald Green), Alkaline / Calcareous (>7.5, Steel Blue).
   - A vertical needle or highlighted bar pinpointing the selected field pH (e.g. 7.8) with deficiency trigger ranges.
3. **Tab 3: Prescribed NPK Nutrient Ratio Bar Chart (`st.bar_chart` or `altair`)**
   - Visual comparison of Nitrogen (N), Phosphorus (P2O5), Potassium (K2O), and Zinc (Zn) kg/acre dosage recommendations based on crop and soil stage.
4. **Sidebar: Knowledge Base Domain Distribution Donut/Bar (`altair`)**
   - Clean breakdown of the 60 rules: Plant Pathology (25), Entomology (20), Soil Science (15) with modal classification (Hardcoded: 34, May/May Not: 15, Extended: 11).

---

## Architecture Decisions
- **Decision 1: Zero External Dependencies for Visualization.** Use `altair` and `streamlit` native primitives (`st.altair_chart`, `st.bar_chart`, `st.progress`). Keeps zero-footprint deployment on Streamlit Community Cloud.
- **Decision 2: Strict Monolingual English.** Replace all transliterated Urdu (e.g., "Gandum", "Kungi", "Makai") and Arabic-script Urdu ("کسان رہبر", "گندم") with standardized agronomic English and accepted botanical/taxonomic nomenclature.
- **Decision 3: Zero Emoji Iconography.** Strip all Unicode emojis from `page_icon`, headers, tabs, expanders, buttons, and status boxes. Replace with clean CSS indicators, semantic Material/Streamlit icons (`:material/check_circle:`, `:material/warning:`), or crisp typographic labeling.
- **Decision 4: WCAG 2.1 AA Accessibility & Contrast.** Use semantic markdown headings (`h1`-`h4`), high-contrast label formatting, explicit placeholder texts, accessible form field associations, and structured table/metric layouts.

---

## Task List

### Phase 1: Text & Iconography Cleanup
- [ ] Task 1: Complete Emoji Removal from UI & Code
- [ ] Task 2: Complete Urdu Language & Transliteration Purge to Clean English

### Checkpoint 1: Visual & Text Sanitization
- [ ] Run grep/regex verification: 0 emojis and 0 Urdu characters in `app.py`.
- [ ] All 23 automated pytest cases pass without regressions.

### Phase 2: Readability & Accessibility Enhancements
- [ ] Task 3: Improve UI Typography, Semantic Hierarchy & Accessibility (WCAG 2.1 AA)

### Phase 3: Visual Analytics (Charts & Graphs)
- [ ] Task 4: Add Rule Distribution Chart in Sidebar & Certainty Factor Meter in Tabs 1/2
- [ ] Task 5: Add Soil pH Chemistry Spectrum & NPK Ratio Chart in Tab 3

### Checkpoint 2: Final Verification & Test Integrity
- [ ] Headless `pytest -v tests/` 100% green.
- [ ] Verify clean, professional UI layout via Playwright/Browser inspection.

---

## Risks and Mitigations
| Risk | Impact | Mitigation |
|:---|:---|:---|
| Test suite relies on emoji or Urdu string assertions | High | Checked `tests/test_ui.py`: it asserts `"Brown Rust"`, `"Pink Bollworm"`, `"at least one observed symptom"`. No tests depend on emojis or Urdu. |
| Plotting library overhead slows down Streamlit rerun | Med | Use lightweight Altair charts with pre-aggregated tidy DataFrames, keeping reruns < 30ms. |
| Contrast failure on dark/light Streamlit themes | Med | Use theme-adaptive Altair color specs or neutral high-contrast hex codes (`#1f77b4`, `#2ca02c`, `#d62728`). |
