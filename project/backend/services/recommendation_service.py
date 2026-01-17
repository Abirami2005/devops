from typing import Dict, List, Tuple


class RecommendationService:
    def __init__(self):
        self.diagnostic_tests_map = {
            "Osteoarthritis": ["X-Ray", "MRI"],
            "Meniscus Tear": ["MRI", "Physical Examination"],
            "ACL Tear": ["MRI", "Physical Examination"],
            "Rotator Cuff Tear": ["MRI", "Ultrasound"],
            "Herniated Disc": ["MRI", "CT Scan"],
            "Spinal Stenosis": ["MRI", "CT Scan", "X-Ray"],
            "Fracture": ["X-Ray", "CT Scan"],
            "Carpal Tunnel Syndrome": ["Nerve Conduction Study", "EMG"],
            "Arthritis": ["X-Ray", "Blood Tests", "MRI"],
        }

        self.initial_treatment_map = {
            "Osteoarthritis": [
                "NSAIDs for pain management",
                "Physical therapy",
                "Weight management counseling"
            ],
            "Meniscus Tear": [
                "RICE protocol (Rest, Ice, Compression, Elevation)",
                "Physical therapy",
                "Anti-inflammatory medication"
            ],
            "ACL Tear": [
                "Immediate immobilization",
                "RICE protocol",
                "Referral to orthopedic surgeon"
            ],
            "Rotator Cuff Tear": [
                "Physical therapy",
                "Pain management with NSAIDs",
                "Corticosteroid injection consideration"
            ],
            "Herniated Disc": [
                "Pain management",
                "Physical therapy",
                "Activity modification"
            ],
            "Fracture": [
                "Immediate immobilization",
                "Pain management",
                "Urgent orthopedic consultation"
            ],
            "Carpal Tunnel Syndrome": [
                "Wrist splinting",
                "Ergonomic modifications",
                "NSAIDs for symptom relief"
            ],
        }

        self.referral_specialties = {
            "surgery_keywords": ["tear", "fracture", "rupture", "severe"],
            "neurology_keywords": ["nerve", "radiculopathy", "neuropathy"],
            "rheumatology_keywords": ["arthritis", "inflammatory"],
            "pain_management_keywords": ["chronic", "persistent"]
        }

    def generate_recommendations(
        self,
        top_condition: str,
        severity_level: str,
        symptom_data: Dict
    ) -> Dict:
        diagnostic_tests = self._get_diagnostic_tests(top_condition)

        initial_treatment = self._get_initial_treatment(top_condition)

        referral_needed, referral_specialty = self._determine_referral(
            top_condition,
            severity_level
        )

        urgency_level = self._determine_urgency(
            severity_level,
            symptom_data.get("pain_level", 0),
            top_condition
        )

        return {
            "diagnostic_tests": diagnostic_tests,
            "initial_treatment": initial_treatment,
            "referral_needed": referral_needed,
            "referral_specialty": referral_specialty,
            "urgency_level": urgency_level
        }

    def _get_diagnostic_tests(self, condition: str) -> List[str]:
        for key, tests in self.diagnostic_tests_map.items():
            if key.lower() in condition.lower():
                return tests

        if "pain" in condition.lower():
            return ["X-Ray", "Physical Examination"]
        return ["Physical Examination", "X-Ray"]

    def _get_initial_treatment(self, condition: str) -> List[str]:
        for key, treatments in self.initial_treatment_map.items():
            if key.lower() in condition.lower():
                return treatments

        return [
            "Pain management with appropriate analgesics",
            "Physical therapy evaluation",
            "Activity modification guidance"
        ]

    def _determine_referral(
        self,
        condition: str,
        severity_level: str
    ) -> Tuple[bool, str]:
        condition_lower = condition.lower()

        if severity_level == "High":
            if any(kw in condition_lower for kw in self.referral_specialties["surgery_keywords"]):
                return True, "Orthopedic Surgery"
            return True, "Orthopedic Specialist"

        if any(kw in condition_lower for kw in self.referral_specialties["neurology_keywords"]):
            return True, "Neurology"

        if any(kw in condition_lower for kw in self.referral_specialties["rheumatology_keywords"]):
            return True, "Rheumatology"

        if severity_level == "Medium":
            return True, "Orthopedic Specialist"

        return False, None

    def _determine_urgency(
        self,
        severity_level: str,
        pain_level: int,
        condition: str
    ) -> str:
        condition_lower = condition.lower()

        emergency_keywords = ["fracture", "dislocation", "rupture", "acute"]
        if any(kw in condition_lower for kw in emergency_keywords):
            if severity_level == "High" or pain_level >= 8:
                return "Emergency"

        if severity_level == "High" or pain_level >= 7:
            return "Urgent"

        return "Routine"


recommendation_service = RecommendationService()
