"""Kisan Rahbar (کسان رہبر) - Pakistan Agriculture Expert System
Automated Crop Disease, Pest Management, and Fertilizer Advisory Portal.
Built for Pakistani Farmers and University CCP Viva Evaluation.
"""

import time
from typing import Dict, List, Tuple
import streamlit as st

from knowledge_base import Category, InferenceResult, RULES
from inference_engine import InferenceEngine
from working_memory import WorkingMemory
from explanation_module import ExplanationModule

# Page Configuration
st.set_page_config(
    page_title="Kisan Rahbar | Pakistan Agriculture Expert System",
    page_icon="🌾",
    layout="wide",
    initial_sidebar_state="expanded"
)


# Cached resource initialization
@st.cache_resource
def get_system_components() -> Tuple[InferenceEngine, ExplanationModule]:
    """Initialize rule engine and explanation module once for session."""
    engine = InferenceEngine(RULES)
    explainer = ExplanationModule()
    return engine, explainer


engine, explainer = get_system_components()

# Crop Display Mapping
CROPS_DISPLAY: Dict[str, str] = {
    "wheat": "Wheat (گندم - Gandum)",
    "cotton": "Cotton (کپاس - Kapas)",
    "rice": "Rice (دھان / چاول - Dhan)",
    "sugarcane": "Sugarcane (کماد / گنا - Kamad)",
    "maize": "Maize (مکئی - Makai)",
}

# Symptom Dictionaries per Crop
CROP_SYMPTOMS: Dict[str, Dict[str, str]] = {
    "wheat": {
        "yellow_pustules_stripes": "Yellow powdery pustules in parallel stripes on leaves (Peeli Kungi)",
        "brown_oval_pustules": "Scattered brown/orange oval pustules without striping (Bhoori Kungi)",
        "black_powdery_heads": "Entire ear head transformed into black sooty powder (Loose Smut / Kani)",
        "fishy_smell_grains": "Blackened kernels with rotten fishy smell (Karnal Bunt)",
        "blackened_kernels": "Partially shriveled blackened grain seeds"
    },
    "cotton": {
        "leaf_curling_upward": "Upward curling and cupping of young leaves (CLCuV)",
        "thickened_veins": "Thickened, swollen green veins and underside leafy outgrowths (Enations)",
        "angular_water_soaked_spots": "Angular water-soaked leaf spots bounded by veins (Bacterial Blight)",
        "black_veins": "Blackened leaf veinles (Black Arm phase)",
        "sudden_plant_wilting": "Sudden dropping and wilting of entire plant canopy in patches",
        "rotted_taproot": "Shredded, decayed dark bark on taproot (Root Rot)"
    },
    "rice": {
        "spindle_eye_shaped_lesions": "Spindle/eye-shaped elliptical lesions with ash-grey center (Rice Blast)",
        "brown_margin_grey_center": "Brown necrotic lesion margins with gray inner core",
        "water_soaked_leaf_margins": "Wavy yellowish-white marginal lesions starting from leaf tips (BLB)",
        "milky_bacterial_ooze": "Oozing microscopic bacterial drops along leaf edge",
        "circular_brown_spots_leaf": "Dark brown oval sesame-like spots with yellow halos (Brown Spot)"
    },
    "sugarcane": {
        "reddened_internal_pith": "Internal stalk split showing deep red tissue with white cross-bands (Red Rot)",
        "alcohol_sour_smell": "Strong sour alcoholic fermentation odor from cut canes",
        "black_whip_structure_shoot": "Terminal shoot transformed into a long curved black dusty whip (Smut)",
        "yellow_white_stripes_leaf": "Discontinuous yellow and whitish chlorotic stripes on foliage (Mosaic)"
    },
    "maize": {
        "long_elliptical_grey_green_lesions": "Large cigar-shaped grayish-green lesions (2-15 cm) parallel to leaves (Turcicum)",
        "golden_brown_pustules_scattered": "Circular to elongate golden-brown powdery pustules (Common Rust)",
        "small_rectangular_lesions": "Small rectangular lesions restricted between leaf veins (Maydis Blight)"
    }
}

WEATHER_CONDITIONS: Dict[str, str] = {
    "normal": "Normal / Dry Clear Weather",
    "cool_humid": "Cool & Humid (Heavy Morning Dew)",
    "hot_dry": "Hot & Dry Spell",
    "cool_nights_rain": "Cool Nights with Intermittent Rain",
    "waterlogged_humid": "Waterlogged Soil with High Humidity",
    "cool_damp_overcast": "Cool, Damp & Overcast Days"
}


# Header
st.title("🌾 Kisan Rahbar | کسان رہبر")
st.caption(
    "Automated Agronomy Expert System for Pakistan's Major Crops: "
    "Wheat, Cotton, Rice, Sugarcane, and Maize."
)

# Sidebar System Health & Architecture Info
with st.sidebar:
    st.header("⚙️ Expert System Info")
    st.success("● Engine Status: Online & Certified")
    st.metric(label="Loaded Rules", value=len(RULES), delta="Exceeds 50 required")
    st.metric(label="Targeted Crops", value=5, delta="Pakistani Major Crops")
    st.markdown("---")
    st.subheader("System Architecture")
    st.markdown(
        "- **Inference:** Pure Python Forward-Chaining\n"
        "- **Certainty Factors:** 0.0 - 1.0\n"
        "- **Safety Guard:** Pre-Harvest Interval (PHI)\n"
        "- **Audit Trail:** Working Memory Trace"
    )
    st.markdown("---")
    st.caption("Developed for Academic CCP Viva & National Farmer Extension.")


# Tabs
tab_disease, tab_pest, tab_nutrient = st.tabs([
    "🔬 1. Crop Disease Diagnosis",
    "🐛 2. Pest Identification & Safety Guard",
    "🌱 3. Nutrient Deficiency & Fertilizer"
])


# ============================================================================
# TAB 1: DISEASE IDENTIFICATION
# ============================================================================
with tab_disease:
    st.subheader("Crop Disease Identification & Management")
    st.info(
        "Select your crop, observed foliage symptoms, and recent weather. "
        "The expert system matches symptoms against agronomic rule chains in < 1.0s.",
        icon=":material/info:"
    )

    col_in, col_out = st.columns([1, 1], gap="medium")

    with col_in:
        with st.container(border=True):
            st.markdown("#### 📋 Field Disease Observation Form")
            selected_crop_key = st.selectbox(
                "Select Crop (فصل منتخب کریں)",
                options=list(CROPS_DISPLAY.keys()),
                format_func=lambda k: CROPS_DISPLAY[k],
                key="dis_crop_select"
            )

            # Retrieve crop-specific symptoms
            available_symptoms = CROP_SYMPTOMS.get(selected_crop_key, {})
            selected_symptom_keys = st.multiselect(
                "Select Observed Symptoms (علامات منتخب کریں)",
                options=list(available_symptoms.keys()),
                format_func=lambda k: available_symptoms[k],
                placeholder="Choose one or more observed leaf/ear signs...",
                key="dis_symptoms_select"
            )

            weather_choice = st.radio(
                "Current / Recent Field Weather Conditions (موسمی کیفیت)",
                options=list(WEATHER_CONDITIONS.keys()),
                format_func=lambda k: WEATHER_CONDITIONS[k],
                key="dis_weather_radio"
            )

            diagnose_disease_btn = st.button(
                "🔍 Diagnose Disease (تشخیص کریں)",
                width="stretch",
                type="primary",
                key="dis_submit_btn"
            )

    with col_out:
        with st.container(border=True):
            st.markdown("#### 🩺 Expert System Diagnostic Report")

            if diagnose_disease_btn:
                if not selected_symptom_keys:
                    st.warning("⚠️ Please select at least one observed symptom before diagnosing.")
                else:
                    # Initialize working memory for this query
                    wm = WorkingMemory()
                    wm.assert_fact("crop", selected_crop_key)
                    wm.assert_fact("symptoms", selected_symptom_keys)
                    if weather_choice != "normal":
                        wm.assert_fact("weather", weather_choice)

                    # Execute inference
                    t_start = time.perf_counter()
                    result: InferenceResult = engine.evaluate(wm, Category.DISEASE)
                    latency = (time.perf_counter() - t_start) * 1000

                    explanation = explainer.explain(result, wm)

                    if result.success:
                        st.success(f"### {result.diagnosis}")

                        # Metrics row
                        m1, m2, m3 = st.columns(3)
                        m1.metric("Certainty Score", f"{result.confidence}%")
                        m2.metric("Severity", result.details.get("severity", "Moderate"))
                        m3.metric("Latency", f"{latency:.2f} ms")

                        # Rule Category Badge
                        rule_type = result.details.get("rule_type", "hardcoded")
                        if rule_type == "hardcoded":
                            st.caption("🔖 **Rule Modality:** Hardcoded Deterministic (100% textbook match)")
                        elif rule_type == "may_or_may_not":
                            st.caption(f"🔖 **Rule Modality:** Probabilistic Inference ({result.confidence}% Certainty Factor)")
                        elif rule_type == "extended":
                            st.caption("🔖 **Rule Modality:** Extended Rule (Weather/Environmental Escalation)")

                        # Treatment Remedies
                        st.markdown("##### 💊 Prescribed Remedies & Solutions:")
                        for idx, remedy in enumerate(result.remedies, 1):
                            st.markdown(f"**{idx}.** {remedy}")

                        # Explanation Chain Expander
                        with st.expander("🔎 View Expert Decision Trail & Reasoning"):
                            for s in explanation.get("steps", []):
                                st.markdown(f"**{s['step']}**: {s['detail']}")
                            st.caption(f"System boundary: {explanation.get('limitations')}")

                    else:
                        st.warning(f"### {result.diagnosis}")
                        st.markdown(
                            "The expert system could not match these specific symptoms with high confidence. "
                            "To protect crop health, the system avoids speculative guessing."
                        )
                        st.markdown("##### 💡 Recommended Next Actions:")
                        for idx, rem in enumerate(result.remedies, 1):
                            st.markdown(f"**{idx}.** {rem}")

                        with st.expander("🔎 System Boundary Limitation Audit"):
                            for s in explanation.get("steps", []):
                                st.markdown(f"**{s['step']}**: {s['detail']}")
            else:
                st.caption("Select crop symptoms on the left and click **Diagnose Disease** to view findings.")


# ============================================================================
# TAB 2: PEST IDENTIFICATION (Placeholder for Task 8)
# ============================================================================
with tab_pest:
    st.subheader("Crop Pest Identification & Pre-Harvest Safety Guard")
    st.caption("Module will be loaded in Task 8.")


# ============================================================================
# TAB 3: NUTRIENT DEFICIENCY (Placeholder for Task 9)
# ============================================================================
with tab_nutrient:
    st.subheader("Nutrient Deficiency & Fertilizer Prescription")
    st.caption("Module will be loaded in Task 9.")
