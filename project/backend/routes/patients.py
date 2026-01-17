from fastapi import APIRouter, HTTPException
from models.schemas import PatientCreate, PatientResponse
from database import supabase
from datetime import datetime

router = APIRouter(prefix="/patients", tags=["patients"])


@router.post("/", response_model=PatientResponse)
async def create_patient(patient: PatientCreate):
    try:
        existing_count = supabase.table("patients").select("id", count="exact").execute()
        count = existing_count.count if existing_count.count else 0

        patient_code = f"P-{datetime.now().year}-{str(count + 1).zfill(4)}"

        result = supabase.table("patients").insert({
            "patient_code": patient_code,
            "age": patient.age,
            "gender": patient.gender,
            "contact_phone": patient.contact_phone,
            "medical_history": patient.medical_history
        }).execute()

        if not result.data:
            raise HTTPException(status_code=500, detail="Failed to create patient")

        return result.data[0]

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{patient_id}", response_model=PatientResponse)
async def get_patient(patient_id: str):
    try:
        result = supabase.table("patients").select("*").eq("id", patient_id).maybeSingle().execute()

        if not result.data:
            raise HTTPException(status_code=404, detail="Patient not found")

        return result.data

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/")
async def list_patients(limit: int = 50, offset: int = 0):
    try:
        result = supabase.table("patients").select("*").range(offset, offset + limit - 1).order("created_at", desc=True).execute()

        return {"patients": result.data, "count": len(result.data)}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
