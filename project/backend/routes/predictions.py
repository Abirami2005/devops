from fastapi import APIRouter, HTTPException
from database import supabase
from services.ml_service import ml_service
from services.recommendation_service import recommendation_service
from config import get_settings

router = APIRouter(prefix="/predictions", tags=["predictions"])
settings = get_settings()


@router.post("/predict/{symptom_id}")
async def predict_condition(symptom_id: str):
    try:
        symptom_result = supabase.table("symptoms").select("*").eq("id", symptom_id).maybeSingle().execute()

        if not symptom_result.data:
            raise HTTPException(status_code=404, detail="Symptom record not found")

        symptom_data = symptom_result.data

        patient_result = supabase.table("patients").select("*").eq("id", symptom_data["patient_id"]).maybeSingle().execute()

        if not patient_result.data:
            raise HTTPException(status_code=404, detail="Patient not found")

        patient_data = patient_result.data

        predictions, features = ml_service.predict_condition(symptom_data)

        severity_level, severity_score = ml_service.predict_severity(symptom_data)

        prediction_record = {
            "symptom_id": symptom_id,
            "patient_id": symptom_data["patient_id"],
            "predicted_conditions": predictions,
            "top_condition": predictions[0]["condition"],
            "top_condition_probability": predictions[0]["probability"],
            "severity_level": severity_level,
            "severity_score": severity_score,
            "model_version": settings.model_version,
            "features_used": features
        }

        pred_result = supabase.table("predictions").insert(prediction_record).execute()

        if not pred_result.data:
            raise HTTPException(status_code=500, detail="Failed to save prediction")

        prediction_id = pred_result.data[0]["id"]

        recommendations = recommendation_service.generate_recommendations(
            predictions[0]["condition"],
            severity_level,
            symptom_data
        )

        rec_record = {
            "prediction_id": prediction_id,
            **recommendations
        }

        rec_result = supabase.table("recommendations").insert(rec_record).execute()

        priority_score = ml_service.calculate_priority_score(
            severity_score,
            symptom_data.get("pain_level", 5),
            symptom_data.get("duration", ""),
            patient_data["age"]
        )

        appointment_record = {
            "patient_id": symptom_data["patient_id"],
            "symptom_id": symptom_id,
            "prediction_id": prediction_id,
            "priority_score": priority_score,
            "status": "Pending",
            "appointment_type": "Emergency" if recommendations["urgency_level"] == "Emergency" else "Initial"
        }

        appt_result = supabase.table("appointments").insert(appointment_record).execute()

        return {
            "prediction_id": prediction_id,
            "predictions": predictions,
            "severity": {
                "level": severity_level,
                "score": severity_score
            },
            "recommendations": recommendations,
            "appointment": {
                "id": appt_result.data[0]["id"] if appt_result.data else None,
                "priority_score": priority_score
            },
            "message": "Prediction completed successfully"
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{prediction_id}")
async def get_prediction(prediction_id: str):
    try:
        result = supabase.table("predictions").select("*").eq("id", prediction_id).maybeSingle().execute()

        if not result.data:
            raise HTTPException(status_code=404, detail="Prediction not found")

        return result.data

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/patient/{patient_id}")
async def get_patient_predictions(patient_id: str):
    try:
        result = supabase.table("predictions").select("*").eq("patient_id", patient_id).order("created_at", desc=True).execute()

        return {"predictions": result.data, "count": len(result.data)}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
