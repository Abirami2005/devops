from fastapi import APIRouter, UploadFile, File, HTTPException, Form
from services.speech_service import speech_service
import os
import uuid

router = APIRouter(prefix="/voice", tags=["voice"])


@router.post("/transcribe")
async def transcribe_audio(
    audio: UploadFile = File(...),
    patient_id: str = Form(...)
):
    try:
        temp_dir = "/tmp/audio_uploads"
        os.makedirs(temp_dir, exist_ok=True)

        file_extension = audio.filename.split(".")[-1] if audio.filename else "wav"
        temp_filename = f"{uuid.uuid4()}.{file_extension}"
        temp_path = os.path.join(temp_dir, temp_filename)

        with open(temp_path, "wb") as buffer:
            content = await audio.read()
            buffer.write(content)

        transcription_result = speech_service.transcribe_audio(temp_path)

        normalized_text = speech_service.normalize_medical_text(
            transcription_result["text"]
        )

        os.remove(temp_path)

        return {
            "patient_id": patient_id,
            "original_text": transcription_result["text"],
            "normalized_text": normalized_text,
            "language": transcription_result["language"],
            "message": "Audio transcribed successfully"
        }

    except FileNotFoundError as e:
        raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Transcription failed: {str(e)}")
