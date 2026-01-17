from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime


class PatientCreate(BaseModel):
    age: int = Field(..., ge=1, le=150)
    gender: str = Field(..., pattern="^(Male|Female|Other)$")
    contact_phone: Optional[str] = None
    medical_history: List[Dict[str, Any]] = Field(default_factory=list)


class PatientResponse(BaseModel):
    id: str
    patient_code: str
    age: int
    gender: str
    created_at: datetime


class SymptomInput(BaseModel):
    patient_id: str
    symptom_text: str
    voice_recording_url: Optional[str] = None


class SymptomExtraction(BaseModel):
    affected_body_part: Optional[str] = None
    pain_level: Optional[int] = Field(None, ge=0, le=10)
    duration: Optional[str] = None
    additional_symptoms: List[str] = Field(default_factory=list)
    extraction_confidence: float = Field(..., ge=0, le=1)


class ConditionPrediction(BaseModel):
    condition: str
    probability: float
    explanation: str


class PredictionResult(BaseModel):
    symptom_id: str
    patient_id: str
    predicted_conditions: List[ConditionPrediction]
    top_condition: str
    top_condition_probability: float
    severity_level: str
    severity_score: float
    features_used: Dict[str, Any]


class RecommendationCreate(BaseModel):
    prediction_id: str
    diagnostic_tests: List[str]
    initial_treatment: List[str]
    referral_needed: bool
    referral_specialty: Optional[str] = None
    urgency_level: str = Field(..., pattern="^(Routine|Urgent|Emergency)$")


class AppointmentCreate(BaseModel):
    patient_id: str
    symptom_id: str
    prediction_id: str
    appointment_type: str = Field(..., pattern="^(Initial|Follow-up|Emergency)$")


class AppointmentResponse(BaseModel):
    id: str
    patient_id: str
    priority_score: int
    scheduled_date: Optional[datetime]
    status: str
    queue_position: Optional[int]
    created_at: datetime


class ConsultationLogCreate(BaseModel):
    appointment_id: str
    patient_id: str
    doctor_id: str
    actual_diagnosis: str
    ai_prediction_accuracy: bool
    treatments_prescribed: List[Dict[str, Any]]
    tests_ordered: List[Dict[str, Any]]
    follow_up_needed: bool
    follow_up_date: Optional[datetime] = None
    consultation_notes: str
    consultation_duration: int


class VoiceTranscriptionRequest(BaseModel):
    audio_file_path: str
    patient_id: str
