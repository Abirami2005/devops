import requests
import os
from typing import Dict, Optional, List


class APIClient:
    def __init__(self):
        self.base_url = os.getenv("API_BASE_URL", "http://localhost:8000")

    def create_patient(self, patient_data: Dict) -> Dict:
        response = requests.post(f"{self.base_url}/patients/", json=patient_data)
        response.raise_for_status()
        return response.json()

    def get_patient(self, patient_id: str) -> Dict:
        response = requests.get(f"{self.base_url}/patients/{patient_id}")
        response.raise_for_status()
        return response.json()

    def list_patients(self, limit: int = 50) -> Dict:
        response = requests.get(f"{self.base_url}/patients/", params={"limit": limit})
        response.raise_for_status()
        return response.json()

    def extract_symptoms(self, symptom_data: Dict) -> Dict:
        response = requests.post(f"{self.base_url}/symptoms/extract", json=symptom_data)
        response.raise_for_status()
        return response.json()

    def get_symptom(self, symptom_id: str) -> Dict:
        response = requests.get(f"{self.base_url}/symptoms/{symptom_id}")
        response.raise_for_status()
        return response.json()

    def predict_condition(self, symptom_id: str) -> Dict:
        response = requests.post(f"{self.base_url}/predictions/predict/{symptom_id}")
        response.raise_for_status()
        return response.json()

    def get_prediction(self, prediction_id: str) -> Dict:
        response = requests.get(f"{self.base_url}/predictions/{prediction_id}")
        response.raise_for_status()
        return response.json()

    def get_appointment_queue(self, status: Optional[str] = "Pending") -> Dict:
        params = {"status": status} if status else {}
        response = requests.get(f"{self.base_url}/appointments/queue", params=params)
        response.raise_for_status()
        return response.json()

    def get_appointment(self, appointment_id: str) -> Dict:
        response = requests.get(f"{self.base_url}/appointments/{appointment_id}")
        response.raise_for_status()
        return response.json()

    def schedule_appointment(self, appointment_id: str, scheduled_date: str, doctor_id: Optional[str] = None) -> Dict:
        params = {"scheduled_date": scheduled_date}
        if doctor_id:
            params["doctor_id"] = doctor_id
        response = requests.patch(f"{self.base_url}/appointments/{appointment_id}/schedule", params=params)
        response.raise_for_status()
        return response.json()

    def update_appointment_status(self, appointment_id: str, status: str) -> Dict:
        response = requests.patch(
            f"{self.base_url}/appointments/{appointment_id}/status",
            params={"status": status}
        )
        response.raise_for_status()
        return response.json()

    def create_consultation_log(self, consultation_data: Dict) -> Dict:
        response = requests.post(f"{self.base_url}/consultations/", json=consultation_data)
        response.raise_for_status()
        return response.json()

    def get_prediction_accuracy(self) -> Dict:
        response = requests.get(f"{self.base_url}/consultations/analytics/accuracy")
        response.raise_for_status()
        return response.json()

    def transcribe_audio(self, audio_file, patient_id: str) -> Dict:
        files = {"audio": audio_file}
        data = {"patient_id": patient_id}
        response = requests.post(f"{self.base_url}/voice/transcribe", files=files, data=data)
        response.raise_for_status()
        return response.json()


api_client = APIClient()
