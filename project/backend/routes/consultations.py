from fastapi import APIRouter, HTTPException
from models.schemas import ConsultationLogCreate
from database import supabase

router = APIRouter(prefix="/consultations", tags=["consultations"])


@router.post("/")
async def create_consultation_log(consultation: ConsultationLogCreate):
    try:
        result = supabase.table("consultation_logs").insert(consultation.model_dump()).execute()

        if not result.data:
            raise HTTPException(status_code=500, detail="Failed to create consultation log")

        supabase.table("appointments").update({"status": "Completed"}).eq("id", consultation.appointment_id).execute()

        return {
            "consultation_id": result.data[0]["id"],
            "message": "Consultation logged successfully"
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{consultation_id}")
async def get_consultation(consultation_id: str):
    try:
        result = supabase.table("consultation_logs").select("*").eq("id", consultation_id).maybeSingle().execute()

        if not result.data:
            raise HTTPException(status_code=404, detail="Consultation not found")

        return result.data

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/patient/{patient_id}")
async def get_patient_consultations(patient_id: str):
    try:
        result = supabase.table("consultation_logs").select("*").eq("patient_id", patient_id).order("created_at", desc=True).execute()

        return {"consultations": result.data, "count": len(result.data)}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/doctor/{doctor_id}")
async def get_doctor_consultations(doctor_id: str):
    try:
        result = supabase.table("consultation_logs").select("*").eq("doctor_id", doctor_id).order("created_at", desc=True).execute()

        return {"consultations": result.data, "count": len(result.data)}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/analytics/accuracy")
async def get_prediction_accuracy():
    try:
        result = supabase.table("consultation_logs").select("ai_prediction_accuracy").execute()

        if not result.data:
            return {"accuracy": 0, "total_consultations": 0, "correct_predictions": 0}

        total = len(result.data)
        correct = sum(1 for log in result.data if log.get("ai_prediction_accuracy") is True)

        accuracy = (correct / total * 100) if total > 0 else 0

        return {
            "accuracy": round(accuracy, 2),
            "total_consultations": total,
            "correct_predictions": correct,
            "incorrect_predictions": total - correct
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
