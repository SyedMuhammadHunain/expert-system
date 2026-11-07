"""Automated headless AppTest verifying Streamlit UI tabs and components."""

from streamlit.testing.v1 import AppTest


def test_app_loads_cleanly():
    at = AppTest.from_file("../app.py")
    at.run(timeout=10)
    assert not at.exception, f"App raised exception on initial load: {at.exception}"


def test_disease_tab_diagnosis():
    at = AppTest.from_file("../app.py")
    at.run(timeout=10)

    # Wheat Brown Rust (May or may not rule)
    at.multiselect("dis_symptoms_select").select("brown_oval_pustules")
    at.button("dis_submit_btn").click().run(timeout=10)

    assert not at.exception
    success_texts = [s.value for s in at.success]
    assert any("Brown Rust" in s for s in success_texts)


def test_disease_tab_unknown_boundary():
    at = AppTest.from_file("../app.py")
    at.run(timeout=10)

    # Empty symptoms trigger warning
    at.button("dis_submit_btn").click().run(timeout=10)
    assert not at.exception
    warning_texts = [w.value for w in at.warning]
    assert any("at least one observed symptom" in w for w in warning_texts)


def test_pest_tab_identification():
    at = AppTest.from_file("../app.py")
    at.run(timeout=10)

    # Cotton Pink Bollworm
    at.selectbox("pest_crop_select").select("cotton")
    at.selectbox("pest_zone_select").select("fruit")
    at.multiselect("pest_damage_multiselect").select("bore_holes")
    at.radio("pest_sighting_radio").set_value("caterpillars")
    at.button("pest_submit_btn").click().run(timeout=10)

    assert not at.exception
    success_texts = [s.value for s in at.success]
    assert any("Pink Bollworm" in s for s in success_texts)


def test_pest_tab_pre_harvest_lockout():
    at = AppTest.from_file("../app.py")
    at.run(timeout=10)

    # Near harvest toggle ON
    at.selectbox("pest_crop_select").select("cotton")
    at.selectbox("pest_zone_select").select("fruit")
    at.multiselect("pest_damage_multiselect").select("bore_holes")
    at.radio("pest_sighting_radio").set_value("caterpillars")
    at.toggle("pest_harvest_toggle").set_value(True)
    at.button("pest_submit_btn").click().run(timeout=10)

    assert not at.exception
    # Check that error/alert lockout banner appeared
    error_texts = [e.value for e in at.error]
    assert any("PRE-HARVEST SAFETY LOCKOUT" in e for e in error_texts)


def test_nutrient_tab_deficiency_prescription():
    at = AppTest.from_file("../app.py")
    at.run(timeout=10)

    # Wheat vegetative lower leaves yellowing -> Nitrogen
    at.selectbox("nut_crop_select").select("wheat")
    at.selectbox("nut_stage_select").select("vegetative")
    at.selectbox("nut_discoloration_select").select("lower_leaves_yellowing")
    at.slider("nut_ph_slider").set_value(8.0)
    at.button("nut_submit_btn").click().run(timeout=10)

    assert not at.exception
    info_texts = [i.value for i in at.info]
    assert any("Nitrogen" in i for i in info_texts)


def test_nutrient_tab_soil_acidity_fix():
    at = AppTest.from_file("../app.py")
    at.run(timeout=10)

    # Universal acidic soil (pH 5.0)
    at.selectbox("nut_crop_select").select("all")
    at.slider("nut_ph_slider").set_value(5.0)
    at.button("nut_submit_btn").click().run(timeout=10)

    assert not at.exception
    info_texts = [i.value for i in at.info]
    assert any("Soil Acidity Fix" in i for i in info_texts)


