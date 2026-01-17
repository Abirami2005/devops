import streamlit as st


def show():
    st.markdown('<div class="sub-header">About the System</div>', unsafe_allow_html=True)

    st.markdown("""
    ## NLP-Based Orthopaedics Appointment Expert System

    This intelligent system combines Natural Language Processing, Machine Learning,
    and Clinical Decision Support to assist orthopaedic clinics in managing patient
    appointments and providing preliminary diagnostic insights.
    """)

    st.markdown("---")

    st.markdown("### Technology Stack")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
        **Frontend:**
        - Streamlit (Interactive UI)
        - Plotly (Data Visualization)

        **Backend:**
        - FastAPI (REST API)
        - Python 3.8+

        **Database:**
        - PostgreSQL (Supabase)
        - Row-Level Security
        """)

    with col2:
        st.markdown("""
        **AI/ML:**
        - spaCy (Medical NLP)
        - OpenAI Whisper (Speech Recognition)
        - Custom ML Models (Classification)

        **Key Features:**
        - Medical Entity Recognition
        - Condition Prediction
        - Severity Ranking
        - Priority Scoring
        """)

    st.markdown("---")

    st.markdown("### System Architecture")

    st.markdown("""
    1. **Voice Input Module**
       - Speech-to-text conversion
       - Medical terminology normalization

    2. **NLP Symptom Extraction**
       - Body part identification
       - Pain level extraction
       - Duration parsing
       - Symptom classification

    3. **ML Prediction Engine**
       - Condition probability calculation
       - Severity assessment
       - Feature engineering

    4. **Recommendation System**
       - Diagnostic test suggestions
       - Treatment recommendations
       - Referral decisions

    5. **Priority Calculation**
       - Multi-factor scoring
       - Queue management
       - Urgency classification

    6. **Doctor Dashboard**
       - Appointment management
       - Consultation logging
       - Performance tracking
    """)

    st.markdown("---")

    st.markdown("### Data Privacy & Security")

    st.markdown('<div class="info-box">', unsafe_allow_html=True)
    st.markdown("""
    - Patient data is anonymized using unique patient codes
    - All database access is protected by Row-Level Security
    - Role-based access control for medical staff
    - HIPAA-compliant data handling practices
    - Audit logging for all sensitive operations
    """)
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("---")

    st.markdown("### Clinical Disclaimer")

    st.markdown('<div class="warning-box">', unsafe_allow_html=True)
    st.markdown("""
    **Important Notice:**

    This system is designed as a **clinical decision support tool** and does NOT replace
    professional medical judgment. All AI predictions and recommendations must be reviewed
    and approved by qualified healthcare professionals before any clinical action is taken.

    - AI predictions are advisory only
    - Doctor confirmation is mandatory
    - System cannot make autonomous medical decisions
    - Regular accuracy monitoring and model updates required
    """)
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("---")

    st.markdown("### Evaluation Metrics")

    st.markdown("""
    The system tracks the following performance metrics:

    - **Accuracy:** Percentage of correct condition predictions
    - **Precision:** True positives / (True positives + False positives)
    - **Recall:** True positives / (True positives + False negatives)
    - **F1 Score:** Harmonic mean of precision and recall
    - **Priority Correlation:** Alignment of AI priority scores with actual urgency
    """)

    st.markdown("---")

    st.markdown("### Contact & Support")

    st.info("""
    For technical support or clinical feedback, please contact:
    - Email: support@orthoexpert.ai
    - Phone: +1 (555) 123-4567
    - Documentation: https://docs.orthoexpert.ai
    """)

    st.markdown("---")

    st.markdown("""
    **Version:** 1.0.0
    **Last Updated:** December 2024
    **License:** For academic and clinical use
    """)
