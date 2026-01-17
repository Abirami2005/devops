# Project Structure

## Complete Folder Structure

```
orthopaedic-expert-system/
├── backend/                                # FastAPI Backend
│   ├── main.py                             # FastAPI application entry point
│   ├── config.py                           # Configuration and settings
│   ├── database.py                         # Supabase database client
│   ├── requirements.txt                    # Python dependencies
│   ├── .env.example                        # Environment variables template
│   │
│   ├── models/                             # Data models
│   │   └── schemas.py                      # Pydantic schemas
│   │
│   ├── routes/                             # API endpoints
│   │   ├── patients.py                     # Patient management endpoints
│   │   ├── symptoms.py                     # Symptom extraction endpoints
│   │   ├── predictions.py                  # ML prediction endpoints
│   │   ├── appointments.py                 # Appointment queue endpoints
│   │   ├── consultations.py                # Consultation log endpoints
│   │   ├── voice.py                        # Speech-to-text endpoints
│   │   └── evaluation.py                   # Model evaluation endpoints
│   │
│   └── services/                           # Business logic services
│       ├── speech_service.py               # OpenAI Whisper integration
│       ├── nlp_service.py                  # Medical NLP with spaCy
│       ├── ml_service.py                   # ML predictions & severity
│       ├── recommendation_service.py       # Clinical recommendations
│       └── evaluation_service.py           # Model evaluation & metrics
│
├── streamlit_app/                          # Streamlit Frontend
│   ├── app.py                              # Main Streamlit application
│   ├── requirements.txt                    # Streamlit dependencies
│   ├── .env.example                        # Environment variables template
│   │
│   ├── utils/                              # Utility modules
│   │   └── api_client.py                   # REST API client
│   │
│   └── pages/                              # Streamlit pages
│       ├── home.py                         # Home page
│       ├── patient_intake.py               # Patient registration & intake
│       ├── doctor_dashboard.py             # Doctor interface
│       ├── appointment_queue.py            # Queue management
│       ├── analytics.py                    # Performance metrics
│       └── about.py                        # System information
│
├── data/                                   # Data and datasets
│   └── generate_dataset.py                # Synthetic data generator
│
├── README.md                               # Main documentation
├── DEPLOYMENT.md                           # Deployment instructions
└── PROJECT_STRUCTURE.md                    # This file
```

## Module Descriptions

### Backend Modules

#### `main.py`
- FastAPI application initialization
- CORS middleware configuration
- Router registration
- Health check endpoints
- API documentation setup

#### `config.py`
- Environment variable management
- Settings configuration using Pydantic
- Singleton pattern for settings

#### `database.py`
- Supabase client initialization
- Database connection management
- Dependency injection for database access

#### `models/schemas.py`
Pydantic models for:
- PatientCreate, PatientResponse
- SymptomInput, SymptomExtraction
- ConditionPrediction, PredictionResult
- RecommendationCreate
- AppointmentCreate, AppointmentResponse
- ConsultationLogCreate
- VoiceTranscriptionRequest

#### `routes/patients.py`
Endpoints:
- POST `/patients/` - Create patient
- GET `/patients/{patient_id}` - Get patient details
- GET `/patients/` - List patients

#### `routes/symptoms.py`
Endpoints:
- POST `/symptoms/extract` - Extract symptoms from text using NLP
- GET `/symptoms/{symptom_id}` - Get symptom details
- GET `/symptoms/patient/{patient_id}` - Get patient's symptoms

#### `routes/predictions.py`
Endpoints:
- POST `/predictions/predict/{symptom_id}` - Predict condition using ML
- GET `/predictions/{prediction_id}` - Get prediction details
- GET `/predictions/patient/{patient_id}` - Get patient's predictions

#### `routes/appointments.py`
Endpoints:
- GET `/appointments/queue` - Get priority-sorted appointment queue
- PATCH `/appointments/{id}/schedule` - Schedule appointment
- PATCH `/appointments/{id}/status` - Update appointment status
- GET `/appointments/{id}` - Get full appointment details
- GET `/appointments/doctor/{doctor_id}` - Get doctor's appointments

#### `routes/consultations.py`
Endpoints:
- POST `/consultations/` - Log consultation
- GET `/consultations/{id}` - Get consultation details
- GET `/consultations/patient/{patient_id}` - Get patient consultations
- GET `/consultations/doctor/{doctor_id}` - Get doctor consultations
- GET `/consultations/analytics/accuracy` - Get AI accuracy metrics

#### `routes/voice.py`
Endpoints:
- POST `/voice/transcribe` - Transcribe audio to text

#### `routes/evaluation.py`
Endpoints:
- POST `/evaluation/predict` - Evaluate prediction accuracy
- POST `/evaluation/severity` - Evaluate severity predictions
- GET `/evaluation/report` - Get evaluation report
- GET `/evaluation/explainability/{id}` - Get prediction explanation

#### `services/speech_service.py`
- OpenAI Whisper model integration
- Audio transcription
- Medical terminology normalization
- Speech-to-text conversion

#### `services/nlp_service.py`
- spaCy NLP pipeline
- Medical entity recognition
- Body part extraction
- Pain level extraction
- Duration parsing
- Symptom classification
- Confidence scoring

#### `services/ml_service.py`
- Condition prediction algorithm
- Probability calculation
- Severity assessment (Low/Medium/High)
- Priority score calculation
- Feature engineering
- Explainability generation

#### `services/recommendation_service.py`
- Diagnostic test recommendations
- Initial treatment suggestions
- Referral determination
- Urgency level classification (Routine/Urgent/Emergency)
- Clinical decision support

#### `services/evaluation_service.py`
- Model performance metrics (accuracy, precision, recall, F1)
- Confusion matrix calculation
- Per-class metrics
- Severity prediction evaluation
- Explainability metrics
- Evaluation report generation

### Frontend Modules

#### `app.py`
- Streamlit app configuration
- Page routing and navigation
- Custom CSS styling
- Sidebar menu

#### `utils/api_client.py`
- REST API client wrapper
- HTTP request handling
- Error management
- Response parsing

#### `pages/home.py`
- System overview
- Feature descriptions
- Important disclaimers
- Navigation guidance

#### `pages/patient_intake.py`
- New patient registration form
- Existing patient selection
- Symptom input (text/voice)
- Real-time NLP extraction
- Condition prediction display
- Results visualization

#### `pages/doctor_dashboard.py`
- Appointment list view
- AI prediction review
- Consultation logging form
- Patient history
- Accuracy tracking

#### `pages/appointment_queue.py`
- Priority-sorted patient queue
- Color-coded severity indicators
- Appointment scheduling
- Queue position management
- Detailed patient information

#### `pages/analytics.py`
- AI accuracy metrics
- Performance gauges
- Statistical visualizations
- System statistics
- Model information

#### `pages/about.py`
- Technology stack details
- System architecture
- Security & privacy information
- Clinical disclaimers
- Contact information

### Data Modules

#### `data/generate_dataset.py`
- Synthetic patient data generation
- 500+ sample records
- Realistic symptom descriptions
- Multiple orthopaedic conditions
- CSV and JSON export
- Statistical analysis

## Database Schema (Supabase)

### Tables

1. **patients**
   - Patient demographics (anonymized)
   - Medical history
   - Created/updated timestamps

2. **symptoms**
   - Original symptom text
   - Processed/normalized text
   - Extracted information (body part, pain, duration)
   - NLP confidence scores

3. **predictions**
   - AI predictions with probabilities
   - Severity assessments
   - Model version tracking
   - Feature importance

4. **recommendations**
   - Diagnostic test suggestions
   - Treatment recommendations
   - Referral decisions
   - Doctor approval status

5. **appointments**
   - Priority scores
   - Scheduling information
   - Status tracking
   - Doctor assignments

6. **consultation_logs**
   - Actual diagnosis
   - AI accuracy tracking
   - Treatments prescribed
   - Follow-up information

7. **model_performance**
   - Accuracy metrics
   - Performance tracking over time
   - Model version history

## Data Flow

```
1. Patient Input (Voice/Text)
   ↓
2. Speech-to-Text (Whisper) [if voice]
   ↓
3. NLP Extraction (spaCy)
   ↓
4. ML Prediction (Custom Models)
   ↓
5. Severity Assessment
   ↓
6. Recommendation Generation
   ↓
7. Priority Calculation
   ↓
8. Appointment Queue
   ↓
9. Doctor Review
   ↓
10. Consultation Logging
    ↓
11. Accuracy Tracking
```

## API Architecture

```
Frontend (Streamlit)
    ↓ HTTP Requests
API Layer (FastAPI)
    ↓ Service Calls
Business Logic (Services)
    ↓ Database Queries
Data Layer (Supabase)
```

## Technology Stack Summary

### Backend
- **Framework**: FastAPI 0.109.0
- **Language**: Python 3.8+
- **Database**: PostgreSQL (Supabase)
- **ORM**: Supabase Python Client
- **Validation**: Pydantic 2.5.3
- **Server**: Uvicorn

### AI/ML
- **NLP**: spaCy 3.7.2, scispacy 0.5.4, medspacy 1.0.0
- **Speech**: OpenAI Whisper
- **ML**: scikit-learn 1.4.0, XGBoost 2.0.3
- **Deep Learning**: PyTorch 2.1.2, Transformers 4.37.0
- **Data**: pandas 2.2.0, numpy 1.26.3

### Frontend
- **Framework**: Streamlit 1.30.0
- **Visualization**: Plotly 5.18.0
- **HTTP Client**: requests 2.31.0

### DevOps
- **ASGI Server**: Uvicorn with workers
- **Reverse Proxy**: Nginx (production)
- **Process Manager**: systemd
- **SSL**: Let's Encrypt (Certbot)
- **Monitoring**: Logs, Sentry (optional)

## Environment Variables

### Backend `.env`
```
SUPABASE_URL=your_supabase_url
SUPABASE_ANON_KEY=your_anon_key
SUPABASE_SERVICE_KEY=your_service_key
OPENAI_API_KEY=your_openai_key
MODEL_VERSION=v1.0
ENVIRONMENT=development|production
```

### Frontend `.env`
```
API_BASE_URL=http://localhost:8000
```

## Key Features by Module

### NLP Service
- Medical entity recognition
- Body part identification
- Pain level extraction (1-10 scale)
- Duration parsing (days/weeks/months)
- Symptom keyword detection
- Confidence scoring

### ML Service
- Multi-condition prediction
- Probability-based classification
- Severity scoring (0-1 scale)
- Priority calculation (1-100)
- Feature importance tracking
- Explainable predictions

### Recommendation Service
- Diagnostic test mapping (X-ray, MRI, CT, etc.)
- Treatment protocol suggestions
- Specialty referral logic
- Urgency classification
- Evidence-based recommendations

### Evaluation Service
- Accuracy, precision, recall, F1 metrics
- Per-class performance analysis
- Confusion matrix generation
- Historical performance tracking
- Explainability scoring

## Security Features

- Row-Level Security (RLS) on all tables
- Patient data anonymization
- Environment variable protection
- HTTPS/SSL in production
- Input validation
- SQL injection prevention
- CORS configuration
- Authentication support

## Performance Optimizations

- Database indexing on frequently queried columns
- Connection pooling
- Async request handling
- Caching for frequent predictions
- Batch processing support
- Lazy loading of models

## Testing Strategy

1. **Unit Tests**: Individual service functions
2. **Integration Tests**: API endpoint testing
3. **Performance Tests**: Load and stress testing
4. **Accuracy Tests**: ML model validation
5. **Security Tests**: Penetration testing
6. **User Acceptance Tests**: Clinical validation

## Future Enhancements

- Real-time voice recording in browser
- Multi-language support
- Advanced ML models (BioBERT, ClinicalBERT)
- EHR integration
- Mobile applications
- Telemedicine features
- Imaging analysis
- Automated model retraining

---

**Last Updated**: December 2024
**Version**: 1.0.0
