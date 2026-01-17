# NLP-Based Orthopaedics Appointment Expert System

An intelligent web-based system that assists orthopaedic doctors by collecting patient symptoms through voice or text input, extracting medical information using NLP, predicting possible orthopaedic conditions, ranking severity, and prioritizing appointments.

## Features

- **Voice & Text Input**: Convert patient speech to text using OpenAI Whisper
- **Medical NLP**: Extract symptoms, body parts, pain levels, and duration using spaCy
- **ML Prediction**: Predict orthopaedic conditions with confidence scores
- **Severity Ranking**: Classify cases as Low, Medium, or High severity
- **Smart Prioritization**: Calculate priority scores for appointment scheduling
- **Clinical Recommendations**: Suggest diagnostic tests and initial treatments
- **Doctor Dashboard**: View predictions, manage appointments, log consultations
- **Analytics**: Track AI prediction accuracy and system performance

## Technology Stack

### Frontend
- **Streamlit**: Interactive web interface
- **Plotly**: Data visualization

### Backend
- **FastAPI**: REST API framework
- **Python 3.8+**

### Database
- **PostgreSQL (Supabase)**: Secure cloud database with Row-Level Security

### AI/ML
- **spaCy**: Medical NLP and entity recognition
- **OpenAI Whisper**: Speech-to-text conversion
- **Custom ML Models**: Disease classification and severity prediction
- **scikit-learn**: Model evaluation

## Project Structure

```
project/
├── backend/
│   ├── main.py                 # FastAPI application
│   ├── config.py               # Configuration management
│   ├── database.py             # Supabase client
│   ├── requirements.txt        # Python dependencies
│   ├── models/
│   │   └── schemas.py          # Pydantic models
│   ├── routes/
│   │   ├── patients.py         # Patient management
│   │   ├── symptoms.py         # Symptom extraction
│   │   ├── predictions.py      # ML predictions
│   │   ├── appointments.py     # Appointment queue
│   │   ├── consultations.py    # Consultation logs
│   │   ├── voice.py            # Speech processing
│   │   └── evaluation.py       # Model evaluation
│   └── services/
│       ├── speech_service.py   # Whisper integration
│       ├── nlp_service.py      # Medical NLP
│       ├── ml_service.py       # ML predictions
│       ├── recommendation_service.py  # Clinical recommendations
│       └── evaluation_service.py      # Model evaluation
├── streamlit_app/
│   ├── app.py                  # Main Streamlit app
│   ├── requirements.txt        # Streamlit dependencies
│   ├── utils/
│   │   └── api_client.py       # API client
│   └── pages/
│       ├── home.py             # Home page
│       ├── patient_intake.py   # Patient registration
│       ├── doctor_dashboard.py # Doctor interface
│       ├── appointment_queue.py # Queue management
│       ├── analytics.py        # Performance metrics
│       └── about.py            # System information
├── data/
│   └── generate_dataset.py    # Synthetic data generator
└── README.md
```

## Database Schema

### Tables

1. **patients**: Anonymized patient information
2. **symptoms**: Extracted symptom data with NLP confidence scores
3. **predictions**: ML model predictions with explainability
4. **recommendations**: Diagnostic tests and treatment suggestions
5. **appointments**: Priority queue with scheduling
6. **consultation_logs**: Doctor consultation records
7. **model_performance**: ML model metrics tracking

## Installation & Setup

### Prerequisites

- Python 3.8 or higher
- PostgreSQL (via Supabase)
- OpenAI API key (optional, for Whisper)

### Backend Setup

1. Navigate to the backend directory:
```bash
cd backend
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Download spaCy model:
```bash
python -m spacy download en_core_web_sm
```

4. Create `.env` file:
```bash
cp .env.example .env
```

5. Configure environment variables in `.env`:
```
SUPABASE_URL=your_supabase_project_url
SUPABASE_ANON_KEY=your_supabase_anon_key
SUPABASE_SERVICE_KEY=your_supabase_service_role_key
OPENAI_API_KEY=your_openai_api_key (optional)
MODEL_VERSION=v1.0
ENVIRONMENT=development
```

6. The database schema is automatically created via Supabase migration

7. Start the FastAPI server:
```bash
python main.py
```

The API will be available at `http://localhost:8000`

API documentation: `http://localhost:8000/docs`

### Frontend Setup

1. Navigate to the Streamlit directory:
```bash
cd streamlit_app
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Create `.env` file:
```bash
cp .env.example .env
```

4. Configure the API URL in `.env`:
```
API_BASE_URL=http://localhost:8000
```

5. Run the Streamlit app:
```bash
streamlit run app.py
```

The web interface will be available at `http://localhost:8501`

### Generate Synthetic Dataset

To create a sample dataset for testing:

```bash
cd data
python generate_dataset.py
```

This generates:
- `orthopaedic_dataset.csv` (500 synthetic patient records)
- `orthopaedic_dataset.json` (JSON format)

## Usage Guide

### 1. Patient Intake

1. Navigate to "Patient Intake" in the sidebar
2. Choose "New Patient" or "Existing Patient"
3. Fill in patient information (age, gender, contact)
4. Provide medical history (optional)
5. Describe symptoms via text or voice
6. Submit for AI analysis

### 2. AI Analysis Process

The system automatically:
1. Extracts symptoms using medical NLP
2. Identifies affected body parts, pain levels, duration
3. Predicts possible orthopaedic conditions
4. Calculates severity scores
5. Recommends diagnostic tests and treatments
6. Assigns priority score for appointment scheduling

### 3. Doctor Dashboard

1. View all appointments with AI predictions
2. Review recommendations and explanations
3. Log consultations with actual diagnosis
4. Mark AI prediction accuracy for model improvement

### 4. Appointment Queue

1. View priority-sorted patient queue
2. Schedule appointments for high-priority cases
3. Assign doctors to appointments
4. Track appointment status

### 5. Analytics

- Monitor AI prediction accuracy
- View system statistics
- Track model performance over time

## API Endpoints

### Patients
- `POST /patients/` - Create patient
- `GET /patients/{patient_id}` - Get patient details
- `GET /patients/` - List all patients

### Symptoms
- `POST /symptoms/extract` - Extract symptoms from text
- `GET /symptoms/{symptom_id}` - Get symptom details
- `GET /symptoms/patient/{patient_id}` - Get patient symptoms

### Predictions
- `POST /predictions/predict/{symptom_id}` - Predict condition
- `GET /predictions/{prediction_id}` - Get prediction details
- `GET /predictions/patient/{patient_id}` - Get patient predictions

### Appointments
- `GET /appointments/queue` - Get appointment queue
- `PATCH /appointments/{id}/schedule` - Schedule appointment
- `PATCH /appointments/{id}/status` - Update status
- `GET /appointments/{id}` - Get appointment details

### Consultations
- `POST /consultations/` - Log consultation
- `GET /consultations/{id}` - Get consultation details
- `GET /consultations/analytics/accuracy` - Get AI accuracy

### Voice
- `POST /voice/transcribe` - Transcribe audio to text

### Evaluation
- `POST /evaluation/predict` - Evaluate predictions
- `POST /evaluation/severity` - Evaluate severity predictions
- `GET /evaluation/report` - Get evaluation report
- `GET /evaluation/explainability/{id}` - Get prediction explanation

## Model Evaluation

The system tracks the following metrics:

- **Accuracy**: Percentage of correct predictions
- **Precision**: True positives / (True positives + False positives)
- **Recall**: True positives / (True positives + False negatives)
- **F1 Score**: Harmonic mean of precision and recall

To evaluate the model:

```python
from services.evaluation_service import evaluation_service

result = evaluation_service.evaluate_predictions(
    y_true=['Osteoarthritis', 'ACL Tear', 'Fracture'],
    y_pred=['Osteoarthritis', 'Meniscus Tear', 'Fracture'],
    model_name='orthopaedic_classifier'
)

print(f"Accuracy: {result['accuracy']}")
print(f"F1 Score: {result['f1_score']}")
```

## Security & Compliance

- **Patient Anonymization**: Unique patient codes instead of personal identifiers
- **Row-Level Security**: Database-level access control via Supabase RLS
- **Role-Based Access**: Authenticated medical staff only
- **Audit Logging**: All sensitive operations are logged
- **HIPAA Considerations**: Data handling follows best practices

## Clinical Disclaimer

**IMPORTANT**: This system is a clinical decision support tool and does NOT replace professional medical judgment.

- All AI predictions are advisory only
- Doctor confirmation is mandatory before clinical actions
- System cannot make autonomous medical decisions
- Regular accuracy monitoring required
- Model updates needed based on feedback

## Limitations

1. **AI Predictions**: Not 100% accurate, requires doctor review
2. **Voice Recognition**: May have errors with medical terminology
3. **Language Support**: Currently English only
4. **Training Data**: Based on synthetic data, needs real-world training
5. **Scope**: Limited to common orthopaedic conditions

## Future Enhancements

- Multi-language support
- Integration with Electronic Health Records (EHR)
- Advanced ML models (BioBERT, ClinicalBERT)
- Real-time voice recording in browser
- Mobile application
- Telemedicine integration
- Imaging analysis (X-ray, MRI)

## Troubleshooting

### Backend Issues

**Port already in use:**
```bash
lsof -ti:8000 | xargs kill -9
python main.py
```

**Database connection error:**
- Verify Supabase credentials in `.env`
- Check internet connection
- Ensure Supabase project is active

**Import errors:**
```bash
pip install -r requirements.txt --upgrade
python -m spacy download en_core_web_sm
```

### Frontend Issues

**API connection refused:**
- Ensure backend is running on `http://localhost:8000`
- Check `API_BASE_URL` in `.env`

**Streamlit crashes:**
```bash
pip install streamlit --upgrade
streamlit run app.py
```

## Contributing

This is an academic project. For improvements:
1. Test thoroughly with synthetic data
2. Document all changes
3. Follow existing code structure
4. Ensure security best practices

## License

For academic and clinical evaluation purposes.

## Contact

For technical support or clinical feedback:
- Email: support@orthoexpert.ai
- Documentation: See inline comments in code

## Version

**Version**: 1.0.0
**Last Updated**: December 2024
**Author**: AI Healthcare Systems Team
