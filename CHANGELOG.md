# Changelog

All notable changes to the **Kisan Rahbar (Pakistan Agriculture Expert System)** project are documented in this file.
The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/), and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [1.0.0] - 2026-11-07

### Added
- **Knowledge Base:** 60 validated agricultural rules covering Pakistan's top 5 crops (Wheat, Cotton, Rice, Sugarcane, Maize).
- **Rule Modalities:** Deterministic hardcoded rules (1.0 CF), probabilistic inference (0.50–0.85 CF), and rule extension override mechanisms.
- **Inference Engine:** Pure Python forward-chaining rule engine evaluating in 0.011 ms (< 1.0s target).
- **Working Memory:** Dynamic fact assertion, retraction, and audit logging.
- **Explanation Module:** 4-step reasoning trace and system boundary limitation fallback.
- **Safety Lockout Guard:** Automated Pre-Harvest Interval (PHI) suppressing toxic chemical insecticides near harvest.
- **Streamlit Web Portal:**
  - Tab 1: Crop Disease Identification & Management.
  - Tab 2: Pest Identification & IPM with pre-harvest safety lock.
  - Tab 3: Nutrient Deficiency & Soil Fertilizer Prescription (NPK + Lime/Gypsum).
- **Test Suite:** 23 automated unit and headless UI tests in `tests/test_rules.py` and `tests/test_ui.py`.
- **Architecture Documentation:** Architecture Decision Records (`ADR-001`, `ADR-002`, `ADR-003`) in `docs/decisions/`.
- **Theme Configuration:** Production agricultural theme and disabled telemetry in `.streamlit/config.toml`.
