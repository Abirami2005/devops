import streamlit as st
from utils.api_client import api_client
import plotly.graph_objects as go
import plotly.express as px


def show():
    st.markdown('<div class="sub-header">System Analytics & Performance</div>', unsafe_allow_html=True)

    try:
        accuracy_data = api_client.get_prediction_accuracy()

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric(
                "AI Accuracy",
                f"{accuracy_data.get('accuracy', 0):.1f}%",
                delta=None
            )

        with col2:
            st.metric(
                "Total Consultations",
                accuracy_data.get('total_consultations', 0)
            )

        with col3:
            st.metric(
                "Correct Predictions",
                accuracy_data.get('correct_predictions', 0),
                delta=None
            )

        with col4:
            st.metric(
                "Incorrect Predictions",
                accuracy_data.get('incorrect_predictions', 0),
                delta=None
            )

        st.markdown("---")

        col1, col2 = st.columns(2)

        with col1:
            st.markdown("### Prediction Accuracy")
            fig = go.Figure(data=[go.Pie(
                labels=['Correct', 'Incorrect'],
                values=[
                    accuracy_data.get('correct_predictions', 0),
                    accuracy_data.get('incorrect_predictions', 0)
                ],
                marker=dict(colors=['#28a745', '#dc3545']),
                hole=0.4
            )])
            fig.update_layout(height=300)
            st.plotly_chart(fig, use_container_width=True)

        with col2:
            st.markdown("### Performance Gauge")
            fig = go.Figure(go.Indicator(
                mode="gauge+number",
                value=accuracy_data.get('accuracy', 0),
                domain={'x': [0, 1], 'y': [0, 1]},
                gauge={
                    'axis': {'range': [None, 100]},
                    'bar': {'color': "#1f77b4"},
                    'steps': [
                        {'range': [0, 50], 'color': "#f8d7da"},
                        {'range': [50, 75], 'color': "#fff3cd"},
                        {'range': [75, 100], 'color': "#d4edda"}
                    ],
                    'threshold': {
                        'line': {'color': "red", 'width': 4},
                        'thickness': 0.75,
                        'value': 90
                    }
                }
            ))
            fig.update_layout(height=300)
            st.plotly_chart(fig, use_container_width=True)

        st.markdown("---")
        st.markdown("### System Statistics")

        try:
            patients_data = api_client.list_patients(limit=1000)
            total_patients = len(patients_data.get("patients", []))

            queue_data = api_client.get_appointment_queue(status=None)
            total_appointments = len(queue_data.get("queue", []))

            pending_data = api_client.get_appointment_queue(status="Pending")
            pending_appointments = len(pending_data.get("queue", []))

            col1, col2, col3 = st.columns(3)

            with col1:
                st.metric("Total Patients", total_patients)

            with col2:
                st.metric("Total Appointments", total_appointments)

            with col3:
                st.metric("Pending Appointments", pending_appointments)

        except Exception as e:
            st.warning(f"Could not load additional statistics: {str(e)}")

        st.markdown("---")
        st.markdown("### Model Information")

        st.info("""
        **Current Model Version:** v1.0

        **ML Algorithms:**
        - Disease Classification: Rule-based + Probabilistic Matching
        - Severity Prediction: Weighted Scoring System
        - Priority Calculation: Multi-factor Algorithm

        **NLP Components:**
        - Medical Entity Recognition: spaCy
        - Text Processing: Custom Medical NLP Pipeline
        """)

    except Exception as e:
        st.error(f"Error loading analytics: {str(e)}")
