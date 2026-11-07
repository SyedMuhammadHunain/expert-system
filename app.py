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
# TAB 2: PEST IDENTIFICATION & PRE-HARVEST SAFETY GUARD
# ============================================================================
with tab_pest:
    st.subheader("Crop Pest Identification & Integrated Pest Management (IPM)")
    st.info(
        "Locate plant damage zone, observed feeding symptoms, and insect sightings. "
        "The expert system enforces Pre-Harvest Interval (PHI) safety by blocking toxic insecticides if harvest is imminent.",
        icon=":material/pest_control:"
    )

    col_pest_in, col_pest_out = st.columns([1, 1], gap="medium")

    with col_pest_in:
        with st.container(border=True):
            st.markdown("#### 🐛 Pest Observation Form")
            pest_crop_key = st.selectbox(
                "Select Crop (فصل)",
                options=list(CROPS_DISPLAY.keys()),
                format_func=lambda k: CROPS_DISPLAY[k],
                key="pest_crop_select"
            )

            plant_zone = st.selectbox(
                "Target Plant Zone (نقصان کا حصہ)",
                options=["leaves", "stems", "roots", "fruit"],
                format_func=lambda z: {
                    "leaves": "🍃 Leaves (پتے)",
                    "stems": "🎋 Stems / Tillers (تنے)",
                    "roots": "🌱 Roots / Underground (جڑیں)",
                    "fruit": "🌾 Fruit / Bolls / Ears / Cobs (پھل / پھٹی / سٹے / چھلی)"
                }.get(z, z.title()),
                key="pest_zone_select"
            )

            visible_damage_list = st.multiselect(
                "Visible Damage Checklist (نقصان کی علامات)",
                options=[
                    "chewed_leaf_margins",
                    "fine_silky_webbing",
                    "sticky_honeydew",
                    "bore_holes",
                    "dry_wilted_plants"
                ],
                format_func=lambda d: {
                    "chewed_leaf_margins": "Chewed leaf margins / shot-holes (کترے ہوئے پتے)",
                    "fine_silky_webbing": "Fine silky webbing under leaves (باریک جالا)",
                    "sticky_honeydew": "Sticky honeydew with black sooty mold (چپچپا مواد)",
                    "bore_holes": "Bore holes with frass / sawdust (سوراخ اور فضلے کے ذرات)",
                    "dry_wilted_plants": "Dry, wilted or dead hearts (خشک سوکھے ہوئے پودے)"
                }.get(d, d.replace("_", " ").title()),
                key="pest_damage_multiselect"
            )

            pest_sighting = st.radio(
                "Pest Sightings (دیکھا گیا کیڑا)",
                options=[
                    "none_seen",
                    "tiny_green_insects",
                    "white_flying_flies",
                    "caterpillars",
                    "white_waxy_clusters",
                    "tiny_brown_hoppers",
                    "jumping_leafhoppers",
                    "tiny_red_mites"
                ],
                format_func=lambda s: {
                    "none_seen": "None seen directly (کوئی نظر نہیں آیا)",
                    "tiny_green_insects": "Tiny soft green insects (چھوٹا سبز کیڑا / تیلہ)",
                    "white_flying_flies": "White flying flies (سفید مکھی)",
                    "caterpillars": "Caterpillars / Larvae / Worms (سنڈیاں / کیڑے)",
                    "white_waxy_clusters": "White waxy clusters on stems (سفید گدی دار کیڑا)",
                    "tiny_brown_hoppers": "Tiny brown hoppers near base (بھورا تیلا)",
                    "jumping_leafhoppers": "Active jumping leafhoppers (پتے کا ٹڈا)",
                    "tiny_red_mites": "Tiny reddish moving specks / mites (سرخ مکڑی)"
                }.get(s, s.replace("_", " ").title()),
                key="pest_sighting_radio"
            )

            st.markdown("---")
            near_harvest_val = st.toggle(
                "🚨 Harvest is Close (< 14 - 21 Days to Harvest)",
                help="Activating this triggers the Pre-Harvest Interval (PHI) safety guard, blocking hazardous chemicals to protect human food safety.",
                key="pest_harvest_toggle"
            )

            diagnose_pest_btn = st.button(
                "🛡️ Identify Pest & Get Solutions",
                width="stretch",
                type="primary",
                key="pest_submit_btn"
            )

    with col_pest_out:
        with st.container(border=True):
            st.markdown("#### 🔍 Pest Identification & IPM Advisory")

            if diagnose_pest_btn:
                if not visible_damage_list and pest_sighting == "none_seen":
                    st.warning("⚠️ Please select visible plant damage signs or observed insect sightings.")
                else:
                    wm_pest = WorkingMemory()
                    wm_pest.assert_fact("crop", pest_crop_key)
                    wm_pest.assert_fact("plant_zone", plant_zone)
                    if visible_damage_list:
                        wm_pest.assert_fact("damage", visible_damage_list)
                    if pest_sighting != "none_seen":
                        wm_pest.assert_fact("sightings", pest_sighting)
                    if near_harvest_val:
                        wm_pest.assert_fact("near_harvest", True)

                    t_start = time.perf_counter()
                    pest_result: InferenceResult = engine.evaluate(wm_pest, Category.PEST)
                    latency = (time.perf_counter() - t_start) * 1000

                    pest_explanation = explainer.explain(pest_result, wm_pest)

                    if pest_result.success:
                        st.success(f"### {pest_result.diagnosis}")

                        p1, p2, p3 = st.columns(3)
                        p1.metric("Certainty Score", f"{pest_result.confidence}%")
                        p2.metric("Severity Tier", pest_result.details.get("severity_tier", "Moderate"))
                        p3.metric("Latency", f"{latency:.2f} ms")

                        # Pre-Harvest Lockout Warning Callout
                        if pest_result.chemical_blocked:
                            st.error(
                                "🚨 **PRE-HARVEST SAFETY LOCKOUT TRIGGERED:**\n\n"
                                "Crop harvest is imminent. Synthetic chemical sprays are **STRICTLY BLOCKED** "
                                "to avoid toxic pesticide residue in grains and fiber. Only non-toxic biological "
                                "and cultural controls are permitted.",
                                icon=":material/gavel:"
                            )

                        # Biological Controls Column vs Chemical Insecticides
                        st.markdown("##### 🐞 Biological & Cultural Controls:")
                        bio_remedies = [r for r in pest_result.remedies if "BLOCKED" not in r and "SAFETY WARNING" not in r and "EC" not in r and "SC" not in r and "SL" not in r and "WG" not in r and "4G" not in r and "3G" not in r]
                        for b in bio_remedies:
                            st.markdown(f"- {b}")

                        if not pest_result.chemical_blocked:
                            st.markdown("##### 🧪 Chemical Insecticide Options (Apply with protective gear):")
                            chem_remedies = [r for r in pest_result.remedies if r not in bio_remedies]
                            for c in chem_remedies:
                                st.markdown(f"- {c}")

                        with st.expander("🔎 View Expert Decision Trail & IPM Reasoning"):
                            for s in pest_explanation.get("steps", []):
                                st.markdown(f"**{s['step']}**: {s['detail']}")
                            st.caption(f"System boundary: {pest_explanation.get('limitations')}")

                    else:
                        st.warning(f"### {pest_result.diagnosis}")
                        st.markdown(
                            "The observed pest signature does not match any recognized pest pattern in the database. "
                            "Please inspect the field with your local extension agent."
                        )
                        with st.expander("🔎 System Boundary Limitation Audit"):
                            for s in pest_explanation.get("steps", []):
                                st.markdown(f"**{s['step']}**: {s['detail']}")
            else:
                st.caption("Provide pest observation signs on the left and click **Identify Pest & Get Solutions**.")



# ============================================================================
# TAB 3: NUTRIENT DEFICIENCY (Placeholder for Task 9)
# ============================================================================
with tab_nutrient:
    st.subheader("Nutrient Deficiency & Fertilizer Prescription")
    st.caption("Module will be loaded in Task 9.")
