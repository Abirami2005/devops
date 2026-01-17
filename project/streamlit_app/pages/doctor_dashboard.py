import streamlit as st
from utils.api_client import api_client
import pandas as pd


def show():
    st.markdown('<div class="sub-header">Doctor Dashboard</div>', unsafe_allow_html=True)

    tab1, tab2 = st.tabs(["View Appointments", "Log Consultation"])

    with tab1:
        show_appointments()

    with tab2:
        show_consultation_form()


def show_appointments():
    st.markdown("### Your Appointments")

    try:
        queue_data = api_client.get_appointment_queue(status=None)
        appointments = queue_data.get("queue", [])

        if not appointments:
            st.info("No appointments found")
            return

        status_filter = st.selectbox(
            "Filter by Status",
            ["All", "Pending", "Scheduled", "Completed", "Cancelled"]
        )

        filtered_appointments = appointments
        if status_filter != "All":
            filtered_appointments = [a for a in appointments if a.get("status") == status_filter]

        for appointment in filtered_appointments:
            with st.expander(
                f"Priority {appointment.get('priority_score', 0)} - "
                f"{appointment.get('patients', {}).get('patient_code', 'N/A')} - "
                f"{appointment.get('status', 'N/A')}"
            ):
                display_appointment_details(appointment)

    except Exception as e:
        st.error(f"Error loading appointments: {str(e)}")


def display_appointment_details(appointment):
    col1, col2 = st.columns(2)

    with col1:
        patient = appointment.get("patients", {})
        st.markdown("#### Patient Information")
        st.write(f"**Patient Code:** {patient.get('patient_code', 'N/A')}")
        st.write(f"**Age:** {patient.get('age', 'N/A')}")
        st.write(f"**Gender:** {patient.get('gender', 'N/A')}")

    with col2:
        prediction = appointment.get("predictions", {})
        st.markdown("#### AI Prediction")
        st.write(f"**Condition:** {prediction.get('top_condition', 'N/A')}")
        st.write(f"**Severity:** {prediction.get('severity_level', 'N/A')}")
        st.write(f"**Confidence:** {prediction.get('top_condition_probability', 0):.1%}")

    st.markdown("#### Appointment Details")
    st.write(f"**Priority Score:** {appointment.get('priority_score', 0)}/100")
    st.write(f"**Status:** {appointment.get('status', 'N/A')}")
    st.write(f"**Type:** {appointment.get('appointment_type', 'N/A')}")

    if st.button(f"View Full Details", key=f"view_{appointment['id']}"):
        try:
            full_appointment = api_client.get_appointment(appointment["id"])
            st.json(full_appointment)
        except Exception as e:
            st.error(f"Error: {str(e)}")


def show_consultation_form():
    st.markdown("### Log Consultation")

    try:
        queue_data = api_client.get_appointment_queue(status="Scheduled")
        appointments = queue_data.get("queue", [])

        if not appointments:
            st.warning("No scheduled appointments found")
            return

        appointment_options = {}
        for appt in appointments:
            patient = appt.get("patients", {})
            label = f"{patient.get('patient_code', 'N/A')} - {appt.get('predictions', {}).get('top_condition', 'N/A')}"
            appointment_options[label] = appt

        selected_label = st.selectbox("Select Appointment", list(appointment_options.keys()))
        selected_appointment = appointment_options[selected_label]

        st.markdown("---")

        prediction = selected_appointment.get("predictions", {})
        st.info(f"**AI Predicted:** {prediction.get('top_condition', 'N/A')} ({prediction.get('top_condition_probability', 0):.1%} confidence)")

        with st.form("consultation_form"):
            actual_diagnosis = st.text_input("Actual Diagnosis")

            ai_correct = st.radio(
                "Was the AI prediction accurate?",
                ["Yes", "No", "Partially"]
            )

            ai_prediction_accuracy = ai_correct == "Yes"

            col1, col2 = st.columns(2)

            with col1:
                tests_ordered = st.text_area(
                    "Tests Ordered",
                    placeholder="Enter tests, one per line"
                )

            with col2:
                treatments_prescribed = st.text_area(
                    "Treatments Prescribed",
                    placeholder="Enter treatments, one per line"
                )

            consultation_notes = st.text_area(
                "Consultation Notes",
                height=150
            )

            consultation_duration = st.number_input(
                "Consultation Duration (minutes)",
                min_value=1,
                max_value=300,
                value=30
            )

            follow_up_needed = st.checkbox("Follow-up Needed")

            follow_up_date = None
            if follow_up_needed:
                follow_up_date = st.date_input("Follow-up Date")

            doctor_id = st.text_input("Doctor ID", value="doc_001")

            submitted = st.form_submit_button("Save Consultation", use_container_width=True)

            if submitted:
                if not actual_diagnosis:
                    st.error("Actual diagnosis is required")
                    return

                try:
                    tests_list = [{"test": t.strip()} for t in tests_ordered.split("\n") if t.strip()]
                    treatments_list = [{"treatment": t.strip()} for t in treatments_prescribed.split("\n") if t.strip()]

                    consultation_data = {
                        "appointment_id": selected_appointment["id"],
                        "patient_id": selected_appointment["patient_id"],
                        "doctor_id": doctor_id,
                        "actual_diagnosis": actual_diagnosis,
                        "ai_prediction_accuracy": ai_prediction_accuracy,
                        "treatments_prescribed": treatments_list,
                        "tests_ordered": tests_list,
                        "follow_up_needed": follow_up_needed,
                        "follow_up_date": follow_up_date.isoformat() if follow_up_date else None,
                        "consultation_notes": consultation_notes,
                        "consultation_duration": consultation_duration
                    }

                    result = api_client.create_consultation_log(consultation_data)

                    st.success(f"Consultation logged successfully! ID: {result['consultation_id']}")

                except Exception as e:
                    st.error(f"Error saving consultation: {str(e)}")

    except Exception as e:
        st.error(f"Error loading appointments: {str(e)}")
