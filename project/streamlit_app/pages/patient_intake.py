import streamlit as st
from utils.api_client import api_client
import time


def show():
    st.markdown('<div class="sub-header">Patient Intake & Symptom Analysis</div>', unsafe_allow_html=True)

    tab1, tab2 = st.tabs(["New Patient", "Existing Patient"])

    with tab1:
        show_new_patient_form()

    with tab2:
        show_existing_patient_form()


def show_new_patient_form():
    st.markdown("### Register New Patient")

    with st.form("new_patient_form"):
        col1, col2 = st.columns(2)

        with col1:
            age = st.number_input("Age", min_value=1, max_value=150, value=30)
            gender = st.selectbox("Gender", ["Male", "Female", "Other"])

        with col2:
            contact = st.text_input("Contact Phone (Optional)")

        medical_history = st.text_area(
            "Medical History (Optional)",
            placeholder="Previous conditions, allergies, current medications..."
        )

        st.markdown("---")
        st.markdown("### Symptom Description")

        symptom_input_method = st.radio("Input Method", ["Text", "Voice Recording"])

        symptom_text = ""
        if symptom_input_method == "Text":
            symptom_text = st.text_area(
                "Describe your symptoms",
                placeholder="Example: I have severe pain in my right knee for the past 2 weeks. The pain is about 8 out of 10 and there is swelling. I have difficulty walking.",
                height=150
            )
        else:
            st.info("Voice recording feature requires microphone access. For this demo, please use text input or upload a pre-recorded audio file.")

        submitted = st.form_submit_button("Submit Patient Data", use_container_width=True)

        if submitted:
            if not symptom_text:
                st.error("Please provide symptom description")
                return

            with st.spinner("Processing patient data..."):
                try:
                    medical_history_list = []
                    if medical_history:
                        medical_history_list = [{"note": medical_history}]

                    patient_data = {
                        "age": age,
                        "gender": gender,
                        "contact_phone": contact if contact else None,
                        "medical_history": medical_history_list
                    }

                    patient_result = api_client.create_patient(patient_data)
                    patient_id = patient_result["id"]

                    st.success(f"Patient registered: {patient_result['patient_code']}")

                    with st.spinner("Extracting symptoms using NLP..."):
                        symptom_data = {
                            "patient_id": patient_id,
                            "symptom_text": symptom_text
                        }
                        symptom_result = api_client.extract_symptoms(symptom_data)
                        symptom_id = symptom_result["symptom_id"]

                    st.success("Symptoms extracted successfully")

                    with st.spinner("Predicting conditions using ML models..."):
                        prediction_result = api_client.predict_condition(symptom_id)

                    st.success("Analysis complete!")

                    display_results(patient_result, symptom_result, prediction_result)

                except Exception as e:
                    st.error(f"Error processing patient: {str(e)}")


def show_existing_patient_form():
    st.markdown("### Existing Patient Symptom Input")

    try:
        patients_data = api_client.list_patients(limit=100)
        patients = patients_data.get("patients", [])

        if not patients:
            st.warning("No patients found. Please register a new patient first.")
            return

        patient_options = {f"{p['patient_code']} - Age {p['age']}, {p['gender']}": p["id"] for p in patients}

        selected_patient = st.selectbox("Select Patient", list(patient_options.keys()))
        patient_id = patient_options[selected_patient]

        with st.form("existing_patient_symptoms"):
            symptom_text = st.text_area(
                "Describe symptoms",
                placeholder="Example: Sharp pain in left shoulder when raising arm, intensity 7/10, started 3 days ago",
                height=150
            )

            submitted = st.form_submit_button("Analyze Symptoms", use_container_width=True)

            if submitted:
                if not symptom_text:
                    st.error("Please describe the symptoms")
                    return

                with st.spinner("Processing symptoms..."):
                    try:
                        symptom_data = {
                            "patient_id": patient_id,
                            "symptom_text": symptom_text
                        }
                        symptom_result = api_client.extract_symptoms(symptom_data)
                        symptom_id = symptom_result["symptom_id"]

                        prediction_result = api_client.predict_condition(symptom_id)

                        patient_result = api_client.get_patient(patient_id)

                        st.success("Analysis complete!")
                        display_results(patient_result, symptom_result, prediction_result)

                    except Exception as e:
                        st.error(f"Error: {str(e)}")

    except Exception as e:
        st.error(f"Error loading patients: {str(e)}")


def display_results(patient, symptom_result, prediction_result):
    st.markdown("---")
    st.markdown("### Analysis Results")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown('<div class="info-box">', unsafe_allow_html=True)
        st.markdown("#### Patient Information")
        st.write(f"**Patient Code:** {patient['patient_code']}")
        st.write(f"**Age:** {patient['age']}")
        st.write(f"**Gender:** {patient['gender']}")
        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        extraction = symptom_result.get("extraction", {})
        st.markdown('<div class="info-box">', unsafe_allow_html=True)
        st.markdown("#### Extracted Information")
        st.write(f"**Affected Body Part:** {extraction.get('affected_body_part', 'Not identified')}")
        st.write(f"**Pain Level:** {extraction.get('pain_level', 'Not specified')}/10")
        st.write(f"**Duration:** {extraction.get('duration', 'Not specified')}")
        st.write(f"**Confidence:** {extraction.get('extraction_confidence', 0):.0%}")
        st.markdown('</div>', unsafe_allow_html=True)

    severity = prediction_result.get("severity", {})
    severity_level = severity.get("level", "Unknown")

    if severity_level == "High":
        box_class = "danger-box"
    elif severity_level == "Medium":
        box_class = "warning-box"
    else:
        box_class = "success-box"

    st.markdown(f'<div class="{box_class}">', unsafe_allow_html=True)
    st.markdown(f"### Severity: {severity_level}")
    st.markdown(f"**Severity Score:** {severity.get('score', 0):.2f}")
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("#### Predicted Conditions")
    predictions = prediction_result.get("predictions", [])

    for idx, pred in enumerate(predictions[:5]):
        with st.expander(f"#{idx+1}: {pred['condition']} - {pred['probability']:.1%} probability"):
            st.write(f"**Probability:** {pred['probability']:.1%}")
            st.write(f"**Explanation:** {pred['explanation']}")

    recommendations = prediction_result.get("recommendations", {})

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("#### Recommended Diagnostic Tests")
        tests = recommendations.get("diagnostic_tests", [])
        for test in tests:
            st.write(f"- {test}")

    with col2:
        st.markdown("#### Initial Treatment Suggestions")
        treatments = recommendations.get("initial_treatment", [])
        for treatment in treatments:
            st.write(f"- {treatment}")

    if recommendations.get("referral_needed"):
        st.warning(f"**Referral Recommended:** {recommendations.get('referral_specialty', 'Specialist')}")

    appointment = prediction_result.get("appointment", {})
    st.info(f"**Appointment Priority Score:** {appointment.get('priority_score', 0)}/100")

    st.markdown('<div class="warning-box">', unsafe_allow_html=True)
    st.markdown("""
    **Clinical Review Required**

    These predictions are AI-generated and must be reviewed by a qualified medical professional
    before any clinical decisions are made.
    """)
    st.markdown('</div>', unsafe_allow_html=True)
