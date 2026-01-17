from fastapi import APIRouter, HTTPException
from models.schemas import SymptomInput
from database import supabase
from services.nlp_service import nlp_service

router = APIRouter(prefix="/symptoms", tags=["symptoms"])


@router.post("/extract")
async def extract_symptoms(symptom_input: SymptomInput):
    try:
        extraction_result = nlp_service.extract_symptoms(symptom_input.symptom_text)

        symptom_record = {
            "patient_id": symptom_input.patient_id,
            "symptom_text": symptom_input.symptom_text,
            "processed_text": extraction_result["processed_text"],
            "affected_body_part": extraction_result["affected_body_part"],
            "pain_level": extraction_result["pain_level"],
            "duration": extraction_result["duration"],
            "additional_symptoms": extraction_result["additional_symptoms"],
            "voice_recording_url": symptom_input.voice_recording_url,
            "extraction_confidence": extraction_result["extraction_confidence"]
        }

        result = supabase.table("symptoms").insert(symptom_record).execute()

        if not result.data:
            raise HTTPException(status_code=500, detail="Failed to save symptom data")

        return {
            "symptom_id": result.data[0]["id"],
            "extraction": extraction_result,
            "message": "Symptoms extracted and saved successfully"
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{symptom_id}")
async def get_symptom(symptom_id: str):
    try:
        result = supabase.table("symptoms").select("*").eq("id", symptom_id).maybeSingle().execute()

        if not result.data:
            raise HTTPException(status_code=404, detail="Symptom record not found")

        return result.data

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/patient/{patient_id}")
async def get_patient_symptoms(patient_id: str):
    try:
        result = supabase.table("symptoms").select("*").eq("patient_id", patient_id).order("created_at", desc=True).execute()

        return {"symptoms": result.data, "count": len(result.data)}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
