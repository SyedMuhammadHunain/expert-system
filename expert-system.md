This software is for Pakistani Farmers. 
This software should cover "Pakistan Major Agricultural Crops" in which "Pakistan's Economy" is mostly dependent.

1. Functional Requirements
    i. Disease Identification - App identifies disease of crop.
    ii. Disease Solution - App provides disease solution after identification.
    iii. Disease Input Form - App takes crop disease information from farmer.
    iv. Pest Identification - App identifies pest.
    v. Pest Solution - App provides pest solution after identification.
    vi. Input Form - App takes pest information from the farmer.
    v. Nutrient Deficiency - App identifies soil deficiencies from foliage signs.
    vi. Fertilizer Prescription - App calculates exact fertilizer dosage (NPK) and soil fix.
    vii. Nutrient Input Form - App takes leaf discoloration patterns, crop stage, and soil pH.

2. Non-Functional Requirements
    i. Performance & Latency - Inference engine evaluates rule chain in < 1.0 second.
    ii. Fault Tolerance & Robustness - Malformed inputs trigger friendly error alerts without Python traceback crashes.
    iii. UI Responsiveness - Streamlit page reloads in < 500ms.
    iv. Scalable - In future, if new features planned, easy to scale.

3. High Level Design
    The high level design present in: ~/Projects/expert-system/high-level-design.png

4. Language
    Streamlit: Python
    Knowledge Base & Inference: Pure Python

5. Streamlit UI
    In streamlit, three sections are there:
    i. Disease Identification Tab - Initial: Show Input Form (Crop dropdown, Symptoms multi-select, weather radio. Output: Identified Disease name + confidence + Columns + Solutions 
    ii. Pest Identification Tab - Initial: Show Input Form (Target plant zone selectbox (Leaves, Stems, Roots, Fruit), Visible damage checklist(Chewed leaf margins, fine silky webbing, sticky honeydew, bore holes) multiselect, Pest Sightings radio(None seen, tiny green insects, white flying flies, caterpillars)), Output: Pest species name + severity tier (Low / Moderate / Severe), Warning if harvest is close (blocks toxic chemicals), Recommended biological controls (ladybugs, BT spray) vs chemical insecticides. 
    iii. Nutricient Deficiency & Fertilizer - Initial:  Crop growth stage (Vegetative, Flowering, Fruiting), Leaf discoloration map (Lower leaves yellowing, leaf edges scorched brown, purple leaf undersides, interveinal chlorosis). Soil pH slider (4.5 to 8.5). Output: • Missing nutrient badge (st.info("Deficiency: Nitrogen (N)" or Potassium (K)), Prescribed NPK fertilizer ratio card (e.g., Urea 46-0-0 @ 30kg/acre or Lime required to raise pH), Recovery timeline estimate (st.caption("Expected foliage recovery: 7-10 days")).


6. Estimated Files
    i. app.py - Streamlit User Interface.
    ii. inference_engine.py - Pure Python inference engine (evaluates rules & confidence).
    iii. working_memory.py - Working memory state management.
    iv. knowledge_base.py - Rule definitions, facts, and certainty factors in Python (50+ rules).
    v. explanation_module.py - Explains decision chain and limitations.

7. Reference
    Always use the following skill for streamlit related app.
    /developing-with-streamlit

8. Course Requirements and What I know
    What our Instructor said:
    i. Minimum 50 rules.
    ii. Deployment is must.
    iii. If sir receive any error in project evaluation day then marks will be deducted.
    What he taught me in office:
    i. Expert system knows its limitations.
    ii. It explains it decisions.
    iii. Expert system has hardcoded, may or may not, extended category.
        a. Hardcoded - Exact same fact and the expert system gives me output.
        b. May or May Not - 50%, 60%, 70% means not 100% sure, so we can use if-else conditions.
        c. Extended - Expert system identifies hardcoded rule but on new infromation extends the hardcoded rule.
    Google Classroom Requirements for CCP
    Here it is:
    "Make an expert system in python, with minimum 50 conditions, and a unique niche. UI is mandatory (use Streamlit only). The     streamlit portal must be live i.e. accessible over the internet (WAN). Viva will be conducted, students will be called for     viva as per the teacher's availability on any day of the week 14. Submission Requirements: Project zip folder (with python     code files and other relevant files), a .pdf file with code explanation along with the streamlit live link."
