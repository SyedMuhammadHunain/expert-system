# Kisan Rahbar (کسان رہبر) - Pakistan Agriculture Expert System

An intelligent, fault-tolerant agronomy expert system in pure Python and Streamlit designed for Pakistani farmers and university CCP course viva evaluation. It provides automated diagnosis and prescriptions across Pakistan's top five agricultural crops: **Wheat (گندم)**, **Cotton (کپاس)**, **Rice (دھان)**, **Sugarcane (کماد)**, and **Maize (مکئی)**.

---

## 🏛️ System Architecture

The architecture strictly follows the modular expert system design pattern:

```
Streamlit UI (app.py)
   │  ▲
 1 │  │ 5
   ▼  │
Inference Engine (inference_engine.py) ◄────► Knowledge Base (knowledge_base.py)
   │  ▲                                              (60 Rules)
 3 │  │
   ▼  │
Working Memory (working_memory.py)
   │
 4 │
   ▼
Explanation Module (explanation_module.py)
```

1. **Streamlit UI (`app.py`)**: Three operational tabs (Disease Diagnosis, Pest Identification, Soil & Fertilizer Prescription).
2. **Inference Engine (`inference_engine.py`)**: Pure Python forward-chaining engine supporting Certainty Factors and rule extensions.
3. **Knowledge Base (`knowledge_base.py`)**: 60 validated agricultural rules covering diseases, pests, and soil nutrients.
4. **Working Memory (`working_memory.py`)**: Manages session state, asserted facts, and rule firing audit trails.
5. **Explanation Module (`explanation_module.py`)**: Translates inference decisions into transparent, step-by-step reasoning steps and explains boundary limitations.

---

## 📋 Course & Viva Requirements Checklist

| Requirement | Rubric | Kisan Rahbar Status |
|-------------|--------|---------------------|
| **Rule Count** | Minimum 50 conditions | **60 Validated Rules** codified |
| **Language & Engine** | Pure Python | **100% Pure Python** (No Prolog / SWI dependencies) |
| **Rule Modalities** | Hardcoded, May/May Not, Extended | **34 Hardcoded**, **15 May or May Not**, **11 Extended** |
| **Explanation Facility** | Explains decisions & limitations | **Full step-by-step trace & boundary alerts** |
| **Safety Guard** | Farm safety | **Pre-Harvest Interval (PHI) toxic chemical lockout** |
| **Fault Tolerance** | No unhandled Python tracebacks | **Zero crashes on malformed/unmapped inputs** |
| **Inference Latency** | < 1.0 second | **~0.012 ms** (Benchmarked) |
| **UI Responsiveness** | < 500ms | **Instantaneous Streamlit reload** |
| **Public Deployment** | WAN accessible | **Streamlit Community Cloud ready** |

---

## 🚀 How to Run Locally

### 1. Clone & Setup Environment
```bash
git clone <your-repo-url>
cd expert-system

# Create virtual environment with uv or python3-venv
python3 -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Run Test Suite
```bash
pytest -v tests/
```
All 23 unit and headless UI tests will pass in < 1 second.

### 3. Launch Web Application
```bash
streamlit run app.py
```
Open your browser at `http://localhost:8501`.

---

## 🌐 Deploying Live to the Internet (WAN) for Viva

To fulfill the university requirement that the portal be live and accessible over the internet:

1. Push this repository to your GitHub account:
   ```bash
   git remote add origin https://github.com/<your-username>/expert-system.git
   git branch -M main
   git push -u origin main
   ```
2. Go to [share.streamlit.io](https://share.streamlit.io) and log in with your GitHub account.
3. Click **"New app"**.
4. Select your repository (`expert-system`), branch (`main`), and main file path (`app.py`).
5. Click **"Deploy!"**.
6. Streamlit Community Cloud will automatically build and give you a public URL (e.g., `https://kisan-rahbar.streamlit.app`) to submit on Google Classroom and present during viva.

---

## 🎓 Key Viva Concepts for Instructor Defense

1. **What is the difference between Hardcoded, May or May Not, and Extended rules?**
   - **Hardcoded:** Deterministic rule with 1.0 Certainty Factor. E.g., when leaf symptoms and weather exactly match Wheat Yellow Rust, the diagnosis is 100% certain.
   - **May or May Not:** Probabilistic rule with 0.50 - 0.85 Certainty Factor representing incomplete symptom footprints.
   - **Extended:** A rule that extends or overrides an existing base rule when secondary environmental triggers occur (e.g. humid weather turning mild blight into an epidemic, or harvest proximity locking out chemical pesticides).
2. **How does the system handle limitations?**
   - When unrecognized symptoms are entered, the system refuses to guess randomly. Instead, it activates the explanation module's boundary defense, explains that the input falls outside calibrated profiles, and refers the farmer to local district extension officers.
3. **Why pure Python over Prolog?**
   - Pure Python avoids binary runtime dependencies like SWI-Prolog, guaranteeing 100% portability, zero deployment crashes, and microsecond evaluation speed on Streamlit Cloud.
