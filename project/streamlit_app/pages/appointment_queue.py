import streamlit as st
from utils.api_client import api_client
import pandas as pd
from datetime import datetime, timedelta


def show():
    st.markdown('<div class="sub-header">Appointment Queue Management</div>', unsafe_allow_html=True)

    try:
        queue_data = api_client.get_appointment_queue(status="Pending")
        appointments = queue_data.get("queue", [])

        if not appointments:
            st.info("No pending appointments in queue")
            return

        st.markdown(f"### Priority Queue ({len(appointments)} patients)")

        queue_df = []
        for appt in appointments:
            patient = appt.get("patients", {})
            prediction = appt.get("predictions", {})

            queue_df.append({
                "Position": appt.get("queue_position", 0),
                "Priority": appt.get("priority_score", 0),
                "Patient": patient.get("patient_code", "N/A"),
                "Age": patient.get("age", "N/A"),
                "Condition": prediction.get("top_condition", "N/A"),
                "Severity": prediction.get("severity_level", "N/A"),
                "Status": appt.get("status", "N/A"),
                "ID": appt.get("id")
            })

        df = pd.DataFrame(queue_df)

        def highlight_severity(row):
            if row["Severity"] == "High":
                return ['background-color: #f8d7da'] * len(row)
            elif row["Severity"] == "Medium":
                return ['background-color: #fff3cd'] * len(row)
            else:
                return ['background-color: #d4edda'] * len(row)

        st.dataframe(
            df.style.apply(highlight_severity, axis=1),
            hide_index=True,
            use_container_width=True
        )

        st.markdown("---")
        st.markdown("### Schedule Appointment")

        selected_patient = st.selectbox(
            "Select Patient",
            [f"{row['Patient']} (Priority: {row['Priority']})" for _, row in df.iterrows()]
        )

        selected_index = int(selected_patient.split("Priority: ")[1].split(")")[0])
        selected_appointment = next(a for a in appointments if a.get("priority_score") == selected_index)

        col1, col2 = st.columns(2)

        with col1:
            schedule_date = st.date_input(
                "Appointment Date",
                min_value=datetime.now().date(),
                value=datetime.now().date() + timedelta(days=1)
            )

        with col2:
            schedule_time = st.time_input("Appointment Time")

        doctor_id = st.text_input("Assign Doctor ID (optional)")

        if st.button("Schedule Appointment", use_container_width=True):
            try:
                scheduled_datetime = datetime.combine(schedule_date, schedule_time)

                result = api_client.schedule_appointment(
                    selected_appointment["id"],
                    scheduled_datetime.isoformat(),
                    doctor_id if doctor_id else None
                )

                st.success("Appointment scheduled successfully!")
                st.rerun()

            except Exception as e:
                st.error(f"Error scheduling appointment: {str(e)}")

        st.markdown("---")
        st.markdown("### Appointment Details")

        selected_id = st.selectbox(
            "View Details",
            [appt["id"] for appt in appointments],
            format_func=lambda x: next(
                f"{a.get('patients', {}).get('patient_code', 'N/A')} - {a.get('predictions', {}).get('top_condition', 'N/A')}"
                for a in appointments if a["id"] == x
            )
        )

        if st.button("Load Details"):
            try:
                full_appointment = api_client.get_appointment(selected_id)

                col1, col2 = st.columns(2)

                with col1:
                    st.json(full_appointment.get("patients", {}))

                with col2:
                    st.json(full_appointment.get("predictions", {}))

                st.json(full_appointment.get("recommendations", {}))

            except Exception as e:
                st.error(f"Error loading details: {str(e)}")

    except Exception as e:
        st.error(f"Error loading appointment queue: {str(e)}")
