import streamlit as st


def show():
    st.markdown('<div class="sub-header">Welcome to the Orthopaedic Expert System</div>', unsafe_allow_html=True)

    st.markdown("""
    This intelligent system assists orthopaedic clinics by:

    - **Analyzing patient symptoms** using advanced NLP techniques
    - **Predicting possible conditions** with machine learning models
    - **Prioritizing appointments** based on severity and urgency
    - **Recommending diagnostic tests** and initial treatments
    - **Supporting clinical decisions** with explainable AI
    """)

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown('<div class="info-box">', unsafe_allow_html=True)
        st.markdown("### Patient Intake")
        st.markdown("""
        - Voice or text symptom input
        - Automatic medical NLP extraction
        - Real-time condition prediction
        """)
        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="info-box">', unsafe_allow_html=True)
        st.markdown("### Doctor Dashboard")
        st.markdown("""
        - View AI predictions
        - Review recommendations
        - Log consultations
        """)
        st.markdown('</div>', unsafe_allow_html=True)

    with col3:
        st.markdown('<div class="info-box">', unsafe_allow_html=True)
        st.markdown("### Appointment Queue")
        st.markdown("""
        - Priority-based ordering
        - Severity indicators
        - Schedule management
        """)
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("---")

    st.markdown('<div class="warning-box">', unsafe_allow_html=True)
    st.markdown("""
    **Important Disclaimer:**

    This system provides AI-assisted recommendations for clinical decision support only.
    All predictions and recommendations MUST be reviewed and approved by a qualified medical professional.
    The system does not replace clinical judgment and should be used as an advisory tool only.
    """)
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("---")

    st.markdown("### System Features")

    features = [
        ("Speech Recognition", "Convert patient voice input to text using OpenAI Whisper"),
        ("Medical NLP", "Extract symptoms, body parts, pain levels using spaCy + MedSpaCy"),
        ("ML Prediction", "Predict conditions using trained Random Forest/XGBoost models"),
        ("Severity Ranking", "Classify cases as Low, Medium, or High severity"),
        ("Smart Prioritization", "Calculate priority scores for appointment scheduling"),
        ("Clinical Recommendations", "Suggest diagnostic tests and initial treatments"),
        ("Performance Tracking", "Monitor AI prediction accuracy over time"),
    ]

    for feature, description in features:
        st.markdown(f"**{feature}:** {description}")

    st.markdown("---")

    st.info("Use the sidebar navigation to access different modules of the system.")
