import numpy as np
from typing import Dict, List, Tuple
import joblib
import os
from datetime import datetime


class MLPredictionService:
    def __init__(self):
        self.orthopaedic_conditions = {
            "knee": [
                "Osteoarthritis", "Meniscus Tear", "ACL Tear",
                "Patellar Tendinitis", "Bursitis"
            ],
            "shoulder": [
                "Rotator Cuff Tear", "Frozen Shoulder", "Shoulder Impingement",
                "Bursitis", "Arthritis"
            ],
            "back": [
                "Herniated Disc", "Spinal Stenosis", "Sciatica",
                "Muscle Strain", "Spondylolisthesis"
            ],
            "hip": [
                "Hip Osteoarthritis", "Hip Bursitis", "Hip Labral Tear",
                "Hip Fracture", "Avascular Necrosis"
            ],
            "ankle": [
                "Ankle Sprain", "Achilles Tendinitis", "Ankle Fracture",
                "Arthritis", "Tarsal Tunnel Syndrome"
            ],
            "wrist": [
                "Carpal Tunnel Syndrome", "Wrist Fracture", "Tendinitis",
                "Arthritis", "De Quervain's Tenosynovitis"
            ],
            "elbow": [
                "Tennis Elbow", "Golfer's Elbow", "Elbow Bursitis",
                "Elbow Fracture", "Arthritis"
            ],
            "neck": [
                "Cervical Spondylosis", "Herniated Cervical Disc",
                "Whiplash", "Muscle Strain", "Cervical Radiculopathy"
            ]
        }

        self.severity_weights = {
            "pain_level": 0.35,
            "duration": 0.25,
            "functional_impact": 0.20,
            "symptom_intensity": 0.20
        }

    def predict_condition(
        self,
        symptom_data: Dict
    ) -> Tuple[List[Dict], Dict]:
        body_part = symptom_data.get("affected_body_part", "").lower()
        pain_level = symptom_data.get("pain_level", 5)
        duration = symptom_data.get("duration", "")
        symptoms = symptom_data.get("additional_symptoms", [])

        possible_conditions = []
        for part_key in self.orthopaedic_conditions.keys():
            if part_key in body_part:
                possible_conditions = self.orthopaedic_conditions[part_key]
                break

        if not possible_conditions:
            possible_conditions = ["General Musculoskeletal Disorder"]

        base_probabilities = self._calculate_probabilities(
            possible_conditions,
            pain_level,
            duration,
            symptoms
        )

        predictions = []
        for condition, prob in base_probabilities.items():
            predictions.append({
                "condition": condition,
                "probability": round(prob, 3),
                "explanation": self._generate_explanation(
                    condition,
                    symptom_data
                )
            })

        predictions.sort(key=lambda x: x["probability"], reverse=True)

        features = {
            "body_part": body_part,
            "pain_level": pain_level,
            "duration_category": self._categorize_duration(duration),
            "symptom_count": len(symptoms),
            "primary_symptoms": symptoms[:3] if symptoms else []
        }

        return predictions, features

    def _calculate_probabilities(
        self,
        conditions: List[str],
        pain_level: int,
        duration: str,
        symptoms: List[str]
    ) -> Dict[str, float]:
        base_prob = 1.0 / len(conditions)
        probabilities = {}

        for condition in conditions:
            prob = base_prob

            if pain_level >= 7:
                if any(word in condition.lower() for word in ["tear", "fracture", "rupture"]):
                    prob *= 1.5
            elif pain_level <= 3:
                if any(word in condition.lower() for word in ["strain", "itis"]):
                    prob *= 1.3

            if "week" in duration.lower() or "month" in duration.lower():
                if "chronic" in condition.lower() or "itis" in condition.lower():
                    prob *= 1.2

            probabilities[condition] = prob

        total = sum(probabilities.values())
        probabilities = {k: v/total for k, v in probabilities.items()}

        return probabilities

    def predict_severity(self, symptom_data: Dict) -> Tuple[str, float]:
        pain_level = symptom_data.get("pain_level", 0)
        duration = symptom_data.get("duration", "")
        symptoms = symptom_data.get("additional_symptoms", [])

        pain_score = (pain_level / 10) * self.severity_weights["pain_level"]

        duration_score = 0
        if "year" in duration.lower():
            duration_score = 1.0
        elif "month" in duration.lower():
            duration_score = 0.7
        elif "week" in duration.lower():
            duration_score = 0.4
        else:
            duration_score = 0.2
        duration_score *= self.severity_weights["duration"]

        functional_keywords = ["cannot", "unable", "difficulty", "limited", "weakness"]
        functional_impact = any(kw in " ".join(symptoms).lower() for kw in functional_keywords)
        functional_score = (1.0 if functional_impact else 0.3) * self.severity_weights["functional_impact"]

        intense_symptoms = ["swelling", "numbness", "burning", "sharp"]
        symptom_intensity = sum(1 for s in symptoms if s in intense_symptoms) / max(len(symptoms), 1)
        symptom_score = symptom_intensity * self.severity_weights["symptom_intensity"]

        total_score = pain_score + duration_score + functional_score + symptom_score

        if total_score >= 0.7:
            severity_level = "High"
        elif total_score >= 0.4:
            severity_level = "Medium"
        else:
            severity_level = "Low"

        return severity_level, round(total_score, 3)

    def _categorize_duration(self, duration: str) -> str:
        if not duration:
            return "unknown"
        duration_lower = duration.lower()
        if "year" in duration_lower:
            return "chronic"
        elif "month" in duration_lower:
            return "subacute"
        else:
            return "acute"

    def _generate_explanation(self, condition: str, symptom_data: Dict) -> str:
        body_part = symptom_data.get("affected_body_part", "area")
        pain_level = symptom_data.get("pain_level", "moderate")

        return (
            f"Based on {body_part} involvement with pain level {pain_level}, "
            f"{condition} shows high correlation with reported symptoms."
        )

    def calculate_priority_score(
        self,
        severity_score: float,
        pain_level: int,
        duration: str,
        age: int
    ) -> int:
        base_score = int(severity_score * 40)

        pain_contribution = int((pain_level / 10) * 30)

        duration_contribution = 0
        if "day" in duration.lower():
            if "1" in duration or "2" in duration:
                duration_contribution = 15

        age_contribution = 0
        if age >= 65:
            age_contribution = 10
        elif age <= 18:
            age_contribution = 5

        priority_score = base_score + pain_contribution + duration_contribution + age_contribution

        return min(max(priority_score, 1), 100)


ml_service = MLPredictionService()
