import whisper
import os
from typing import Optional


class SpeechToTextService:
    def __init__(self, model_size: str = "base"):
        self.model = whisper.load_model(model_size)

    def transcribe_audio(self, audio_file_path: str, language: str = "en") -> dict:
        if not os.path.exists(audio_file_path):
            raise FileNotFoundError(f"Audio file not found: {audio_file_path}")

        result = self.model.transcribe(
            audio_file_path,
            language=language,
            task="transcribe",
            fp16=False
        )

        return {
            "text": result["text"].strip(),
            "language": result.get("language", language),
            "segments": result.get("segments", [])
        }

    def normalize_medical_text(self, text: str) -> str:
        replacements = {
            "nee": "knee",
            "bac": "back",
            "sholder": "shoulder",
            "ancle": "ankle",
            "rist": "wrist",
            "elbo": "elbow",
            "hip": "hip",
            "payn": "pain",
            "aik": "ache",
            "swell": "swelling",
        }

        normalized = text.lower()
        for wrong, correct in replacements.items():
            normalized = normalized.replace(wrong, correct)

        return normalized


speech_service = SpeechToTextService()
