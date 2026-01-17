from fastapi import APIRouter, HTTPException
from database import supabase
from datetime import datetime
from typing import Optional

router = APIRouter(prefix="/appointments", tags=["appointments"])


@router.get("/queue")
async def get_appointment_queue(status: Optional[str] = "Pending"):
    try:
        query = supabase.table("appointments").select(
            "*, patients(patient_code, age, gender), predictions(top_condition, severity_level)"
        ).order("priority_score", desc=True)

        if status:
            query = query.eq("status", status)

        result = query.execute()

        queue = []
        for idx, appointment in enumerate(result.data):
            queue.append({
                **appointment,
                "queue_position": idx + 1
            })

        return {"queue": queue, "total": len(queue)}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.patch("/{appointment_id}/schedule")
async def schedule_appointment(
    appointment_id: str,
    scheduled_date: datetime,
    doctor_id: Optional[str] = None
):
    try:
        update_data = {
            "scheduled_date": scheduled_date.isoformat(),
            "status": "Scheduled"
        }

        if doctor_id:
            update_data["assigned_doctor_id"] = doctor_id

        result = supabase.table("appointments").update(update_data).eq("id", appointment_id).execute()

        if not result.data:
            raise HTTPException(status_code=404, detail="Appointment not found")

        return {"message": "Appointment scheduled successfully", "appointment": result.data[0]}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.patch("/{appointment_id}/status")
async def update_appointment_status(appointment_id: str, status: str):
    try:
        valid_statuses = ["Pending", "Scheduled", "Completed", "Cancelled"]
        if status not in valid_statuses:
            raise HTTPException(status_code=400, detail=f"Invalid status. Must be one of {valid_statuses}")

        result = supabase.table("appointments").update({"status": status}).eq("id", appointment_id).execute()

        if not result.data:
            raise HTTPException(status_code=404, detail="Appointment not found")

        return {"message": "Status updated successfully", "appointment": result.data[0]}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{appointment_id}")
async def get_appointment(appointment_id: str):
    try:
        result = supabase.table("appointments").select(
            "*, patients(*), symptoms(*), predictions(*), recommendations(*)"
        ).eq("id", appointment_id).maybeSingle().execute()

        if not result.data:
            raise HTTPException(status_code=404, detail="Appointment not found")

        return result.data

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/doctor/{doctor_id}")
async def get_doctor_appointments(doctor_id: str):
    try:
        result = supabase.table("appointments").select(
            "*, patients(patient_code, age, gender), predictions(top_condition, severity_level)"
        ).eq("assigned_doctor_id", doctor_id).order("scheduled_date", desc=True).execute()

        return {"appointments": result.data, "count": len(result.data)}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
