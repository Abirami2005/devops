from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List
from services.evaluation_service import evaluation_service

router = APIRouter(prefix="/evaluation", tags=["evaluation"])


class EvaluationRequest(BaseModel):
    y_true: List[str]
    y_pred: List[str]
    model_name: str = "orthopaedic_classifier"


class SeverityEvaluationRequest(BaseModel):
    y_true_severity: List[str]
    y_pred_severity: List[str]


@router.post("/predict")
async def evaluate_predictions(request: EvaluationRequest):
    try:
        result = evaluation_service.evaluate_predictions(
            request.y_true,
            request.y_pred,
            request.model_name
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/severity")
async def evaluate_severity(request: SeverityEvaluationRequest):
    try:
        result = evaluation_service.evaluate_severity_prediction(
            request.y_true_severity,
            request.y_pred_severity
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/report")
async def get_evaluation_report():
    try:
        report = evaluation_service.generate_evaluation_report()
        return report
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/explainability/{prediction_id}")
async def get_explainability(prediction_id: str):
    try:
        from database import supabase

        result = supabase.table("predictions").select("*").eq("id", prediction_id).maybeSingle().execute()

        if not result.data:
            raise HTTPException(status_code=404, detail="Prediction not found")

        explanation = evaluation_service.calculate_explainability_metrics(result.data)

        return {
            "prediction_id": prediction_id,
            "explainability": explanation,
            "prediction_data": result.data
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
