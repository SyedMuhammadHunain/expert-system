"""Pakistan Agriculture Expert System
Automated Crop Disease, Pest Management, and Fertilizer Advisory Portal.
Built for Academic Evaluation and Agricultural Extension.
"""

import time
from typing import Any, Dict, List, Tuple
import altair as alt
import pandas as pd
import streamlit as st

from knowledge_base import Category, InferenceResult, RULES
from inference_engine import InferenceEngine
from working_memory import WorkingMemory
from explanation_module import ExplanationModule

st.set_page_config(
    page_title="Pakistan Agriculture Expert System",
    layout="wide",
    initial_sidebar_state="expanded"
)


@st.cache_resource
def get_system_components() -> Tuple[InferenceEngine, ExplanationModule]:
    """Initialize rule engine and explanation module once for session."""
    engine = InferenceEngine(RULES)
    explainer = ExplanationModule()
    return engine, explainer


engine, explainer = get_system_components()


def render_modality_badge(rule_type: str, confidence: float) -> None:
    """Render informative badge explaining rule modality."""
    if rule_type == "partial":
        st.caption(f"**Rule modality:** Partial match ({confidence}% Certainty Factor — corroborating signs recommended)")
    elif rule_type == "hardcoded":
        st.caption("**Rule modality:** Hardcoded deterministic (100% textbook match)")
    elif rule_type == "may_or_may_not":
        st.caption(f"**Rule modality:** Probabilistic inference ({confidence}% Certainty Factor)")
    elif rule_type == "extended":
        st.caption("**Rule modality:** Extended rule (Weather/Harvest/Safety Escalation)")


def render_confidence_meter(confidence: float) -> None:
    """Render visual certainty factor progress bar with color-coded classification."""
    val = max(0.0, min(1.0, confidence / 100.0))
    st.progress(val, text=f"Certainty factor: {confidence}% confidence score")


def render_soil_ph_spectrum(current_ph: float) -> None:
    """Render an Altair soil chemistry spectrum chart highlighting measured field pH."""
    spectrum_data = [
        {"Zone": "Acidic (Al/Mn Toxicity)", "Start": 4.5, "End": 6.0, "Color": "#d9534f"},
        {"Zone": "Optimal Agronomic Range", "Start": 6.0, "End": 7.5, "Color": "#5cb85c"},
        {"Zone": "Alkaline / Calcareous (Indus)", "Start": 7.5, "End": 8.5, "Color": "#0275d8"}
    ]
    df_spec = pd.DataFrame(spectrum_data)
    zones = alt.Chart(df_spec).mark_bar(opacity=0.6).encode(
        x=alt.X("Start:Q", scale=alt.Scale(domain=[4.5, 8.5]), title="Soil pH"),
        x2="End:Q",
        color=alt.Color(
            "Zone:N",
            scale=alt.Scale(
                domain=[s["Zone"] for s in spectrum_data],
                range=[s["Color"] for s in spectrum_data]
            ),
            legend=alt.Legend(orient="bottom", title=None)
        )
    ).properties(height=65)

    marker_df = pd.DataFrame([{"ph": current_ph}])
    marker = alt.Chart(marker_df).mark_rule(color="#111111", strokeWidth=3).encode(
        x="ph:Q"
    )

    chart = (zones + marker)
    st.altair_chart(chart, width="stretch", alt=f"Soil pH spectrum showing current measured pH at {current_ph}")


def render_npk_dosage_chart(remedies: List[str], crop: str) -> None:
    """Render NPK macronutrient application bar chart based on prescribed remedies."""
    import re
    fertilizers = []
    for r in remedies:
        kg_match = re.search(r"(\d+)\s*kg", r, re.IGNORECASE)
        dosage = int(kg_match.group(1)) if kg_match else None

        if "urea" in r.lower():
            fertilizers.append({"Fertilizer": "Urea (46% N)", "Dosage (kg/acre)": dosage or 50, "Nutrient": "Nitrogen"})
        elif "dap" in r.lower():
            fertilizers.append({"Fertilizer": "DAP (18% N, 46% P)", "Dosage (kg/acre)": dosage or 50, "Nutrient": "Phosphorus"})
        elif "sop" in r.lower() or "potassium" in r.lower():
            fertilizers.append({"Fertilizer": "SOP / MOP (50% K)", "Dosage (kg/acre)": dosage or 25, "Nutrient": "Potassium"})
        elif "zinc" in r.lower():
            fertilizers.append({"Fertilizer": "Zinc Sulphate (33% Zn)", "Dosage (kg/acre)": dosage or 6, "Nutrient": "Zinc"})
        elif "gypsum" in r.lower():
            fertilizers.append({"Fertilizer": "Agricultural Gypsum", "Dosage (kg/acre)": dosage or 500, "Nutrient": "Calcium/Sulfur"})
        elif "lime" in r.lower():
            fertilizers.append({"Fertilizer": "Agricultural Lime", "Dosage (kg/acre)": dosage or 1000, "Nutrient": "Calcium"})

    if fertilizers:
        df_fert = pd.DataFrame(fertilizers)
        chart_fert = (
            alt.Chart(df_fert)
            .mark_bar(cornerRadiusEnd=4)
            .encode(
                x=alt.X("Dosage (kg/acre):Q", title="Application Rate (kg / acre)"),
                y=alt.Y("Fertilizer:N", sort="-x", title=None),
                color=alt.Color("Nutrient:N", legend=None),
                tooltip=["Fertilizer", "Nutrient", "Dosage (kg/acre)"]
            )
            .properties(height=max(100, len(fertilizers) * 32))
        )
        st.markdown("##### Prescribed application rates by product:")
        st.altair_chart(chart_fert, width="stretch", alt="Prescribed fertilizer application rates in kg per acre")


def render_explanation_expander(
    explanation: Dict[str, Any], title: str = "View expert decision trail and reasoning"
) -> None:
    """Render reasoning steps and system boundary limitations."""
    with st.expander(title, icon=":material/visibility:"):
        for s in explanation.get("steps", []):
            st.markdown(f"**{s['step']}**: {s['detail']}")
        if limits := explanation.get("limitations"):
            st.caption(f"System boundary: {limits}")


CROPS_DISPLAY: Dict[str, str] = {
    "wheat": "Wheat",
    "cotton": "Cotton",
    "rice": "Rice",
    "sugarcane": "Sugarcane",
    "maize": "Maize",
}

CROP_SYMPTOMS: Dict[str, Dict[str, str]] = {
    "wheat": {
        "yellow_pustules_stripes": "Yellow powdery pustules in parallel stripes on leaves (Stripe Rust)",
        "brown_oval_pustules": "Scattered brown/orange oval pustules without striping (Leaf Rust)",
        "black_powdery_heads": "Entire ear head transformed into black sooty powder (Loose Smut)",
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


st.title("Pakistan Agriculture Expert System")
st.caption(
    "Automated Agronomy Expert System for Major Crops: "
    "Wheat, Cotton, Rice, Sugarcane, and Maize."
)

with st.sidebar:
    st.header("Expert System")
    st.metric(label="Loaded rules", value=len(RULES))
    st.metric(label="Targeted crops", value=5)

    st.subheader("Knowledge base distribution")
    rules_data = [
        {"Domain": r.category.value.title(), "Crop": r.crop.title()}
        for r in RULES
    ]
    df_rules = pd.DataFrame(rules_data)
    domain_counts = df_rules["Domain"].value_counts().reset_index()
    domain_counts.columns = ["Domain", "Rule count"]

    chart_kb = (
        alt.Chart(domain_counts)
        .mark_bar(cornerRadiusEnd=4)
        .encode(
            x=alt.X("Rule count:Q", title="Number of rules"),
            y=alt.Y("Domain:N", sort="-x", title="Domain"),
            color=alt.Color("Domain:N", legend=None)
        )
        .properties(height=140)
    )
    st.altair_chart(chart_kb, width="stretch", alt="Knowledge base rule count distribution across Disease, Pest, and Nutrient domains")

    


tab_disease, tab_pest, tab_nutrient = st.tabs([
    "1. Crop Disease Identification",
    "2. Pest identification",
    "3. Nutrient deficiency and fertilizer"
])


with tab_disease:
    st.subheader("Crop disease identification and management")
    st.info(
        "Select your crop, observed foliage symptoms, and recent weather. "
        "The expert system matches symptoms against agronomic rule chains in < 1.0s.",
        icon=":material/info:"
    )

    col_in, col_out = st.columns([1, 1], gap="medium")

    def _reset_disease_on_crop_change() -> None:
        st.session_state.pop("dis_symptoms_select", None)
        st.session_state.pop("dis_result", None)
        st.session_state.pop("dis_error", None)

    with col_in:
        with st.container(border=True):
            st.markdown("#### Field disease observation form")
            selected_crop_key = st.selectbox(
                "Select crop",
                options=list(CROPS_DISPLAY.keys()),
                format_func=lambda k: CROPS_DISPLAY[k],
                help="Choose the primary crop currently showing foliar or ear abnormalities.",
                key="dis_crop_select",
                on_change=_reset_disease_on_crop_change
            )

            available_symptoms = CROP_SYMPTOMS.get(selected_crop_key, {})
            selected_symptom_keys = st.multiselect(
                "Select observed symptoms",
                options=list(available_symptoms.keys()),
                format_func=lambda k: available_symptoms[k],
                placeholder="Choose one or more observed leaf, stalk, or grain signs...",
                help="Select all distinct visible lesion or tissue patterns present on the crop.",
                key="dis_symptoms_select"
            )

            weather_choice = st.radio(
                "Current or recent field weather conditions",
                options=list(WEATHER_CONDITIONS.keys()),
                format_func=lambda k: WEATHER_CONDITIONS[k],
                help="Microclimate conditions like high humidity and dew accelerate specific fungal pathogens.",
                key="dis_weather_radio"
            )

            diagnose_disease_btn = st.button(
                "Diagnose disease",
                icon=":material/biotech:",
                width="stretch",
                type="primary"
            )

            if diagnose_disease_btn:
                try:
                    if not selected_symptom_keys:
                        st.session_state["dis_error"] = "Please select at least one observed symptom before diagnosing."
                        st.session_state.pop("dis_result", None)
                    else:
                        st.session_state.pop("dis_error", None)
                        wm = WorkingMemory()
                        wm.assert_fact("crop", selected_crop_key)
                        wm.assert_fact("symptoms", selected_symptom_keys)
                        if weather_choice != "normal":
                            wm.assert_fact("weather", weather_choice)

                        t_start = time.perf_counter()
                        res: InferenceResult = engine.evaluate(wm, Category.DISEASE)
                        lat = (time.perf_counter() - t_start) * 1000
                        exp = explainer.explain(res, wm)
                        st.session_state["dis_result"] = {
                            "result": res,
                            "latency": lat,
                            "explanation": exp
                        }
                except Exception as e:
                    st.error(f"Inference error: {e}")

    with col_out:
        with st.container(border=True):
            st.markdown("#### Expert diagnostic report")

            if st.session_state.get("dis_error"):
                st.warning(f"{st.session_state['dis_error']}", icon=":material/warning:")
            elif "dis_result" in st.session_state:
                item = st.session_state["dis_result"]
                result: InferenceResult = item["result"]
                latency = item["latency"]
                explanation = item["explanation"]

                if result.success:
                    if result.limitation_notice:
                        st.warning(f"### {result.diagnosis}", icon=":material/help:")
                        st.caption(result.limitation_notice)
                    else:
                        st.success(f"### {result.diagnosis}", icon=":material/check_circle:")

                    m1, m2, m3 = st.columns(3)
                    m1.metric("Certainty score", f"{result.confidence}%")
                    m2.metric("Severity", result.details.get("severity", "Moderate"))
                    m3.metric("Latency", f"{latency:.2f} ms")

                    render_confidence_meter(result.confidence)
                    render_modality_badge(result.details.get("rule_type", "hardcoded"), result.confidence)

                    st.markdown("##### Prescribed remedies and agronomic treatments:")
                    for idx, remedy in enumerate(result.remedies, 1):
                        st.markdown(f"**{idx}.** {remedy}")

                    render_explanation_expander(explanation)

                else:
                    st.warning(f"### {result.diagnosis}", icon=":material/help:")
                    st.markdown(
                        "The expert system could not match these specific symptoms with high confidence. "
                        "To protect crop health, the system avoids speculative guessing."
                    )
                    st.markdown("##### Recommended next actions:")
                    for idx, rem in enumerate(result.remedies, 1):
                        st.markdown(f"**{idx}.** {rem}")

                    render_explanation_expander(explanation, title="System boundary limitation audit")
            else:
                st.caption("Select crop symptoms on the left and click **Diagnose disease** to view findings.")


with tab_pest:
    st.subheader("Crop pest identification and integrated pest management (IPM)")
    st.info(
        "Locate plant damage zone, observed feeding symptoms, and insect sightings. "
        "The expert system enforces Pre-Harvest Interval (PHI) safety by blocking toxic insecticides if harvest is imminent.",
        icon=":material/pest_control:"
    )

    col_pest_in, col_pest_out = st.columns([1, 1], gap="medium")

    def _reset_pest_on_crop_change() -> None:
        st.session_state.pop("pest_result", None)
        st.session_state.pop("pest_error", None)

    with col_pest_in:
        with st.container(border=True):
            st.markdown("#### Pest observation form")
            pest_crop_key = st.selectbox(
                "Select crop",
                options=list(CROPS_DISPLAY.keys()),
                format_func=lambda k: CROPS_DISPLAY[k],
                help="Select the host crop experiencing pest feeding or infestation.",
                key="pest_crop_select",
                on_change=_reset_pest_on_crop_change
            )

            plant_zone = st.selectbox(
                "Target plant zone",
                options=["leaves", "stems", "roots", "fruit"],
                format_func=lambda z: {
                    "leaves": "Leaves",
                    "stems": "Stems / Tillers",
                    "roots": "Roots / Underground",
                    "fruit": "Fruit / Bolls / Ears / Cobs"
                }.get(z, z.title()),
                help="Specify the primary plant organ or anatomical structure affected by pests.",
                key="pest_zone_select"
            )

            visible_damage_list = st.multiselect(
                "Visible damage checklist",
                options=[
                    "chewed_leaf_margins",
                    "fine_silky_webbing",
                    "sticky_honeydew",
                    "bore_holes",
                    "dry_wilted_plants"
                ],
                format_func=lambda d: {
                    "chewed_leaf_margins": "Chewed leaf margins / shot-holes",
                    "fine_silky_webbing": "Fine silky webbing under leaves",
                    "sticky_honeydew": "Sticky honeydew with black sooty mold",
                    "bore_holes": "Bore holes with frass / sawdust",
                    "dry_wilted_plants": "Dry, wilted or dead hearts"
                }.get(d, d.replace("_", " ").title()),
                placeholder="Select one or more observable physical crop damages...",
                help="Check all symptoms of physical feeding or excretion visible in the field.",
                key="pest_damage_multiselect"
            )

            pest_sighting = st.radio(
                "Observed insect pest sightings",
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
                    "none_seen": "None seen directly",
                    "tiny_green_insects": "Tiny soft green insects (Aphids)",
                    "white_flying_flies": "White flying flies (Whitefly)",
                    "caterpillars": "Caterpillars / Larvae / Borers",
                    "white_waxy_clusters": "White waxy clusters on stems (Mealybug)",
                    "tiny_brown_hoppers": "Tiny brown hoppers near base (Planthopper)",
                    "jumping_leafhoppers": "Active jumping leafhoppers (Jassids)",
                    "tiny_red_mites": "Tiny reddish moving specks / mites"
                }.get(s, s.replace("_", " ").title()),
                help="Direct visual observation of the pest or its larval/nymph stages.",
                key="pest_sighting_radio"
            )

            st.divider()
            near_harvest_val = st.toggle(
                "Harvest is close (< 14 - 21 days to harvest)",
                help="Activating this triggers the Pre-Harvest Interval (PHI) safety guard, blocking hazardous chemicals to protect human food safety.",
                key="pest_harvest_toggle"
            )

            diagnose_pest_btn = st.button(
                "Identify pest and retrieve IPM advisory",
                icon=":material/security:",
                width="stretch",
                type="primary"
            )

            if diagnose_pest_btn:
                if not visible_damage_list and pest_sighting == "none_seen":
                    st.session_state["pest_error"] = "Please select visible plant damage signs or observed insect sightings."
                    st.session_state.pop("pest_result", None)
                else:
                    st.session_state.pop("pest_error", None)
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
                    p_res: InferenceResult = engine.evaluate(wm_pest, Category.PEST)
                    p_lat = (time.perf_counter() - t_start) * 1000
                    p_exp = explainer.explain(p_res, wm_pest)
                    st.session_state["pest_result"] = {
                        "result": p_res,
                        "latency": p_lat,
                        "explanation": p_exp
                    }

    with col_pest_out:
        with st.container(border=True):
            st.markdown("#### Pest identification and IPM advisory")

            if st.session_state.get("pest_error"):
                st.warning(f"{st.session_state['pest_error']}", icon=":material/warning:")
            elif "pest_result" in st.session_state:
                p_item = st.session_state["pest_result"]
                pest_result: InferenceResult = p_item["result"]
                latency = p_item["latency"]
                pest_explanation = p_item["explanation"]

                if pest_result.success:
                    if pest_result.limitation_notice:
                        st.warning(f"### {pest_result.diagnosis}", icon=":material/help:")
                        st.caption(pest_result.limitation_notice)
                    else:
                        st.success(f"### {pest_result.diagnosis}", icon=":material/check_circle:")

                    p1, p2, p3 = st.columns(3)
                    p1.metric("Certainty score", f"{pest_result.confidence}%")
                    p2.metric("Severity tier", pest_result.details.get("severity_tier", "Moderate"))
                    p3.metric("Latency", f"{latency:.2f} ms")

                    render_confidence_meter(pest_result.confidence)
                    render_modality_badge(
                        "partial" if pest_result.details.get("match_type") == "partial" else pest_result.details.get("rule_type", "hardcoded"),
                        pest_result.confidence
                    )

                    if pest_result.chemical_blocked:
                        st.error(
                            "**PRE-HARVEST SAFETY LOCKOUT TRIGGERED:**\n\n"
                            "Crop harvest is imminent. Synthetic chemical sprays are **strictly blocked** "
                            "to avoid toxic pesticide residue in grains and fiber. Only non-toxic biological "
                            "and cultural controls are permitted.",
                            icon=":material/gavel:"
                        )

                    st.markdown("##### Biological and cultural controls:")
                    bio_remedies = [r for r in pest_result.remedies if "BLOCKED" not in r and "SAFETY WARNING" not in r and "EC" not in r and "SC" not in r and "SL" not in r and "WG" not in r and "4G" not in r and "3G" not in r]
                    for b in bio_remedies:
                        st.markdown(f"- {b}")

                    if not pest_result.chemical_blocked:
                        st.markdown("##### Chemical insecticide options (Apply with certified PPE):")
                        chem_remedies = [r for r in pest_result.remedies if r not in bio_remedies]
                        for c in chem_remedies:
                            st.markdown(f"- {c}")

                    render_explanation_expander(pest_explanation, title="View expert decision trail and IPM reasoning")

                else:
                    st.warning(f"### {pest_result.diagnosis}", icon=":material/help:")
                    st.markdown(
                        "The observed pest signature does not match any recognized pest pattern in the database. "
                        "Please inspect the field with your local extension agent."
                    )
                    render_explanation_expander(pest_explanation, title="System boundary limitation audit")
            else:
                st.caption("Provide pest observation signs on the left and click **Identify pest and retrieve IPM advisory**.")



with tab_nutrient:
    st.subheader("Nutrient deficiency identification and fertilizer prescription")
    st.info(
        "Analyze leaf discoloration patterns, crop growth stage, and soil pH to calculate exact "
        "NPK fertilizer dosages (Urea, DAP, SOP) and soil chemical remediation (Lime / Gypsum).",
        icon=":material/compost:"
    )

    col_nut_in, col_nut_out = st.columns([1, 1], gap="medium")

    def _reset_nutrient_on_crop_change() -> None:
        st.session_state.pop("nut_result", None)

    with col_nut_in:
        with st.container(border=True):
            st.markdown("#### Soil and foliage input form")

            nut_crop_options = ["all"] + list(CROPS_DISPLAY.keys())
            nut_crop_key = st.selectbox(
                "Target crop",
                options=nut_crop_options,
                format_func=lambda k: "All crops / universal soil check" if k == "all" else CROPS_DISPLAY[k],
                help="Select target crop or choose universal check for general soil pH guidance.",
                key="nut_crop_select",
                on_change=_reset_nutrient_on_crop_change
            )

            crop_stage = st.selectbox(
                "Crop growth stage",
                options=["vegetative", "flowering", "fruiting"],
                format_func=lambda s: {
                    "vegetative": "Vegetative / tillering stage",
                    "flowering": "Flowering / boot stage",
                    "fruiting": "Fruiting / boll-fill / grain formation"
                }.get(s, s.title()),
                help="Plant phenological stage dictates specific nutrient uptake demands.",
                key="nut_stage_select"
            )

            leaf_discoloration = st.selectbox(
                "Leaf discoloration map",
                options=[
                    "none",
                    "lower_leaves_yellowing",
                    "leaf_edges_scorched_brown",
                    "purple_leaf_undersides",
                    "interveinal_chlorosis"
                ],
                format_func=lambda d: {
                    "none": "No significant discoloration",
                    "lower_leaves_yellowing": "Lower / older leaves yellowing (Nitrogen/Potassium deficit)",
                    "leaf_edges_scorched_brown": "Leaf edges scorched brown / necrosis (Potassium deficit)",
                    "purple_leaf_undersides": "Purple leaf undersides / anthocyanin (Phosphorus deficit)",
                    "interveinal_chlorosis": "Interveinal chlorosis / bleached bands (Zinc/Iron deficit)"
                }.get(d, d.replace("_", " ").title()),
                help="Characteristic visual chlorosis patterns corresponding to mobility of nutrients.",
                key="nut_discoloration_select"
            )

            soil_ph = st.slider(
                "Measured soil pH",
                min_value=4.5,
                max_value=8.5,
                value=7.8,
                step=0.1,
                help="Typical Indus Basin soils are alkaline (pH 7.8 - 8.5). Acidic soils (< 6.0) require agricultural lime; sodic soils (> 8.2) require gypsum.",
                key="nut_ph_slider"
            )

            render_soil_ph_spectrum(soil_ph)

            if soil_ph < 5.5:
                st.error(f"Soil status: Strongly acidic (pH {soil_ph}) — High risk of Al/Mn toxicity.", icon=":material/report:")
            elif soil_ph > 8.2:
                st.warning(f"Soil status: Strongly alkaline / sodic (pH {soil_ph}) — Micronutrients locked.", icon=":material/warning:")
            else:
                st.success(f"Soil status: Optimal / moderately alkaline (pH {soil_ph}) — Standard Indus plain range.", icon=":material/check_circle:")

            diagnose_nut_btn = st.button(
                "Prescribe fertilizer and soil remediation",
                icon=":material/science:",
                width="stretch",
                type="primary"
            )

            if diagnose_nut_btn:
                wm_nut = WorkingMemory()
                wm_nut.assert_fact("crop", nut_crop_key)
                wm_nut.assert_fact("stage", crop_stage)
                wm_nut.assert_fact("soil_ph", soil_ph)
                if leaf_discoloration != "none":
                    wm_nut.assert_fact("discoloration", leaf_discoloration)

                t_start = time.perf_counter()
                n_res: InferenceResult = engine.evaluate(wm_nut, Category.NUTRIENT)
                n_lat = (time.perf_counter() - t_start) * 1000
                n_exp = explainer.explain(n_res, wm_nut)
                st.session_state["nut_result"] = {
                    "result": n_res,
                    "latency": n_lat,
                    "explanation": n_exp,
                    "soil_ph": soil_ph
                }

    with col_nut_out:
        with st.container(border=True):
            st.markdown("#### Expert soil and fertilizer prescription")

            if "nut_result" in st.session_state:
                n_item = st.session_state["nut_result"]
                nut_result: InferenceResult = n_item["result"]
                latency = n_item["latency"]
                nut_explanation = n_item["explanation"]
                recorded_ph = n_item["soil_ph"]

                if nut_result.success:
                    if nut_result.limitation_notice:
                        st.warning(f"### Deficiency identified: {nut_result.diagnosis}", icon=":material/help:")
                        st.caption(nut_result.limitation_notice)
                    else:
                        st.info(f"### Deficiency identified: {nut_result.diagnosis}", icon=":material/science:")

                    n1, n2, n3 = st.columns(3)
                    n1.metric("Certainty score", f"{nut_result.confidence}%")
                    n2.metric("Soil pH", f"{recorded_ph}")
                    n3.metric("Latency", f"{latency:.2f} ms")

                    render_confidence_meter(nut_result.confidence)
                    render_modality_badge(
                        "partial" if nut_result.details.get("match_type") == "partial" else nut_result.details.get("rule_type", "hardcoded"),
                        nut_result.confidence
                    )

                    st.markdown("##### Prescribed NPK and soil remediation schedule:")
                    for idx, rem in enumerate(nut_result.remedies, 1):
                        st.markdown(f"- **{rem}**")

                    render_npk_dosage_chart(nut_result.remedies, nut_crop_key)

                    timeline_val = nut_result.details.get("recovery_timeline", "7-14 days")
                    st.caption(f"**Expected foliage recovery timeline:** {timeline_val}")

                    render_explanation_expander(nut_explanation, title="View expert decision trail and soil chemistry reasoning")

                else:
                    st.warning(f"### {nut_result.diagnosis}", icon=":material/help:")
                    st.markdown(
                        "No acute nutrient deficit was detected for the provided combination. "
                        "Maintain standard NPK basal application for this crop."
                    )
                    render_explanation_expander(nut_explanation, title="System boundary limitation audit")
            else:
                st.caption("Adjust foliage discoloration, growth stage, and soil pH, then click **Prescribe fertilizer and soil remediation**.")

