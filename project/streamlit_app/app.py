import streamlit as st
import os
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(
    page_title="Orthopaedic Expert System",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
    <style>
    .main-header {
        font-size: 2.5rem;
        font-weight: 700;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .sub-header {
        font-size: 1.5rem;
        font-weight: 600;
        color: #2c3e50;
        margin-top: 1rem;
        margin-bottom: 1rem;
    }
    .info-box {
        padding: 1rem;
        border-radius: 0.5rem;
        background-color: #f0f2f6;
        border-left: 4px solid #1f77b4;
        margin: 1rem 0;
    }
    .warning-box {
        padding: 1rem;
        border-radius: 0.5rem;
        background-color: #fff3cd;
        border-left: 4px solid #ffc107;
        margin: 1rem 0;
    }
    .success-box {
        padding: 1rem;
        border-radius: 0.5rem;
        background-color: #d4edda;
        border-left: 4px solid #28a745;
        margin: 1rem 0;
    }
    .danger-box {
        padding: 1rem;
        border-radius: 0.5rem;
        background-color: #f8d7da;
        border-left: 4px solid #dc3545;
        margin: 1rem 0;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-header">🏥 Orthopaedic Expert System</div>', unsafe_allow_html=True)
st.markdown('<div class="info-box">AI-Powered Appointment Prioritization & Clinical Decision Support</div>', unsafe_allow_html=True)

st.sidebar.title("Navigation")
page = st.sidebar.radio(
    "Select Module",
    ["Home", "Patient Intake", "Doctor Dashboard", "Appointment Queue", "Analytics", "About"]
)

if page == "Home":
    from pages import home
    home.show()
elif page == "Patient Intake":
    from pages import patient_intake
    patient_intake.show()
elif page == "Doctor Dashboard":
    from pages import doctor_dashboard
    doctor_dashboard.show()
elif page == "Appointment Queue":
    from pages import appointment_queue
    appointment_queue.show()
elif page == "Analytics":
    from pages import analytics
    analytics.show()
elif page == "About":
    from pages import about
    about.show()
