from typing import Dict, List, Tuple
import pandas as pd
import numpy as np
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix
import json


class ModelEvaluationService:
    def __init__(self):
        self.evaluation_history = []

    def evaluate_predictions(
        self,
        y_true: List[str],
        y_pred: List[str],
        model_name: str = "orthopaedic_classifier"
    ) -> Dict:
        if len(y_true) != len(y_pred):
            raise ValueError("True labels and predictions must have same length")

        if len(y_true) == 0:
            return {
                "accuracy": 0.0,
                "precision": 0.0,
                "recall": 0.0,
                "f1_score": 0.0,
                "sample_size": 0
            }

        unique_labels = list(set(y_true + y_pred))

        accuracy = accuracy_score(y_true, y_pred)

        precision = precision_score(
            y_true,
            y_pred,
            average='weighted',
            labels=unique_labels,
            zero_division=0
        )

        recall = recall_score(
            y_true,
            y_pred,
            average='weighted',
            labels=unique_labels,
            zero_division=0
        )

        f1 = f1_score(
            y_true,
            y_pred,
            average='weighted',
            labels=unique_labels,
            zero_division=0
        )

        conf_matrix = confusion_matrix(y_true, y_pred, labels=unique_labels)

        per_class_metrics = {}
        for idx, label in enumerate(unique_labels):
            y_true_binary = [1 if y == label else 0 for y in y_true]
            y_pred_binary = [1 if y == label else 0 for y in y_pred]

            if sum(y_true_binary) > 0:
                per_class_metrics[label] = {
                    "precision": precision_score(y_true_binary, y_pred_binary, zero_division=0),
                    "recall": recall_score(y_true_binary, y_pred_binary, zero_division=0),
                    "f1_score": f1_score(y_true_binary, y_pred_binary, zero_division=0),
                    "support": sum(y_true_binary)
                }

        evaluation_result = {
            "model_name": model_name,
            "accuracy": round(accuracy, 4),
            "precision": round(precision, 4),
            "recall": round(recall, 4),
            "f1_score": round(f1, 4),
            "sample_size": len(y_true),
            "confusion_matrix": conf_matrix.tolist(),
            "per_class_metrics": per_class_metrics,
            "unique_classes": unique_labels
        }

        self.evaluation_history.append(evaluation_result)

        return evaluation_result

    def evaluate_severity_prediction(
        self,
        y_true_severity: List[str],
        y_pred_severity: List[str]
    ) -> Dict:
        severity_mapping = {"Low": 0, "Medium": 1, "High": 2}

        y_true_numeric = [severity_mapping.get(s, 1) for s in y_true_severity]
        y_pred_numeric = [severity_mapping.get(s, 1) for s in y_pred_severity]

        exact_matches = sum(1 for t, p in zip(y_true_numeric, y_pred_numeric) if t == p)
        accuracy = exact_matches / len(y_true_numeric) if len(y_true_numeric) > 0 else 0

        off_by_one = sum(1 for t, p in zip(y_true_numeric, y_pred_numeric) if abs(t - p) <= 1)
        tolerance_accuracy = off_by_one / len(y_true_numeric) if len(y_true_numeric) > 0 else 0

        mae = np.mean([abs(t - p) for t, p in zip(y_true_numeric, y_pred_numeric)])

        return {
            "accuracy": round(accuracy, 4),
            "tolerance_accuracy": round(tolerance_accuracy, 4),
            "mean_absolute_error": round(mae, 4),
            "sample_size": len(y_true_severity)
        }

    def calculate_explainability_metrics(
        self,
        prediction_data: Dict
    ) -> Dict:
        features = prediction_data.get("features_used", {})
        predictions = prediction_data.get("predicted_conditions", [])

        top_condition = predictions[0] if predictions else {}
        top_prob = top_condition.get("probability", 0)

        confidence_level = "High" if top_prob >= 0.7 else "Medium" if top_prob >= 0.5 else "Low"

        feature_importance = {
            "body_part": 0.30,
            "pain_level": 0.25,
            "duration": 0.20,
            "symptoms": 0.25
        }

        explanation = {
            "confidence_level": confidence_level,
            "top_probability": top_prob,
            "prediction_diversity": len(predictions),
            "feature_importance": feature_importance,
            "key_factors": []
        }

        if features.get("pain_level", 0) >= 7:
            explanation["key_factors"].append("High pain level (>= 7/10)")

        if features.get("duration_category") == "chronic":
            explanation["key_factors"].append("Chronic condition (long duration)")

        if features.get("symptom_count", 0) >= 3:
            explanation["key_factors"].append("Multiple symptoms present")

        return explanation

    def generate_evaluation_report(self) -> Dict:
        if not self.evaluation_history:
            return {"message": "No evaluations performed yet"}

        latest_eval = self.evaluation_history[-1]

        avg_metrics = {
            "avg_accuracy": np.mean([e["accuracy"] for e in self.evaluation_history]),
            "avg_precision": np.mean([e["precision"] for e in self.evaluation_history]),
            "avg_recall": np.mean([e["recall"] for e in self.evaluation_history]),
            "avg_f1_score": np.mean([e["f1_score"] for e in self.evaluation_history]),
        }

        return {
            "latest_evaluation": latest_eval,
            "historical_averages": avg_metrics,
            "total_evaluations": len(self.evaluation_history)
        }

    def save_evaluation_report(self, filename: str = "evaluation_report.json"):
        report = self.generate_evaluation_report()

        with open(filename, 'w') as f:
            json.dump(report, f, indent=2)

        return f"Report saved to {filename}"


evaluation_service = ModelEvaluationService()
