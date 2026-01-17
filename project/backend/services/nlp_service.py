import spacy
from typing import Dict, List, Optional, Tuple
import re


class MedicalNLPService:
    def __init__(self):
        try:
            self.nlp = spacy.load("en_core_web_sm")
        except OSError:
            import subprocess
            subprocess.run(["python", "-m", "spacy", "download", "en_core_web_sm"])
            self.nlp = spacy.load("en_core_web_sm")

        self.orthopaedic_body_parts = {
            "knee", "knees", "shoulder", "shoulders", "hip", "hips",
            "ankle", "ankles", "wrist", "wrists", "elbow", "elbows",
            "back", "spine", "neck", "leg", "legs", "arm", "arms",
            "hand", "hands", "foot", "feet", "finger", "fingers",
            "toe", "toes", "jaw", "pelvis", "rib", "ribs"
        }

        self.symptom_keywords = {
            "pain", "ache", "aching", "hurt", "hurting", "sore", "soreness",
            "swelling", "swollen", "inflammation", "stiff", "stiffness",
            "weakness", "weak", "numbness", "numb", "tingling", "burning",
            "sharp", "dull", "throbbing", "radiating", "limited", "difficulty",
            "fracture", "broken", "sprain", "strain", "tear", "injury"
        }

        self.duration_pattern = re.compile(
            r'(\d+)\s*(day|days|week|weeks|month|months|year|years)',
            re.IGNORECASE
        )

        self.pain_level_pattern = re.compile(
            r'(pain|severity|level|intensity).*?(\d{1,2})\s*(?:out of|\/|\s)?\s*10',
            re.IGNORECASE
        )

    def extract_symptoms(self, text: str) -> Dict:
        doc = self.nlp(text.lower())

        affected_parts = []
        symptoms = []
        pain_level = None
        duration = None
        confidence = 0.0

        for token in doc:
            if token.lemma_ in self.orthopaedic_body_parts:
                affected_parts.append(token.text)
            if token.lemma_ in self.symptom_keywords:
                symptoms.append(token.text)

        pain_match = self.pain_level_pattern.search(text)
        if pain_match:
            try:
                pain_level = int(pain_match.group(2))
                if pain_level > 10:
                    pain_level = 10
            except (ValueError, IndexError):
                pass

        duration_match = self.duration_pattern.search(text)
        if duration_match:
            duration = duration_match.group(0)

        found_entities = len(affected_parts) + len(symptoms)
        if pain_level:
            found_entities += 1
        if duration:
            found_entities += 1

        max_possible = 6
        confidence = min(found_entities / max_possible, 1.0)

        return {
            "affected_body_part": affected_parts[0] if affected_parts else None,
            "all_affected_parts": list(set(affected_parts)),
            "pain_level": pain_level,
            "duration": duration,
            "additional_symptoms": list(set(symptoms)),
            "extraction_confidence": round(confidence, 2),
            "processed_text": text.lower().strip()
        }

    def extract_medical_entities(self, text: str) -> List[Dict]:
        doc = self.nlp(text)
        entities = []

        for ent in doc.ents:
            entities.append({
                "text": ent.text,
                "label": ent.label_,
                "start": ent.start_char,
                "end": ent.end_char
            })

        return entities


nlp_service = MedicalNLPService()
