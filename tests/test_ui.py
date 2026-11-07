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
