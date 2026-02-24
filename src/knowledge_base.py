import json
from pathlib import Path
from typing import Optional


class KnowledgeBase:
    """Knowledge base loader untuk data gejala, aturan, dan kasus printer."""

    def __init__(self, json_path: str):
        self._data = self._load_data(json_path)

    def _load_data(self, json_path: str) -> dict:
        path = Path(json_path)
        if not path.exists():
            raise FileNotFoundError(f"Knowledge base tidak ditemukan: {json_path}")
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)

    def get_symptoms(self) -> list[dict]:
        return self._data.get("symptoms", [])

    def get_rules(self) -> list[dict]:
        return self._data.get("rules", [])

    def get_symptom_by_code(self, code: str) -> Optional[dict]:
        for symptom in self.get_symptoms():
            if symptom["code"] == code:
                return symptom
        return None

    def get_rule_by_code(self, code: str) -> Optional[dict]:
        for rule in self.get_rules():
            if rule["code"] == code:
                return rule
        return None

    def get_symptom_categories(self) -> list[str]:
        categories = set()
        for symptom in self.get_symptoms():
            cat = symptom.get("category", "other")
            categories.add(cat)
        return sorted(list(categories))

    def get_symptoms_by_category(self, category: str) -> list[dict]:
        return [s for s in self.get_symptoms() if s.get("category") == category]

    def get_symptom_weight(self, code: str) -> float:
        symptom = self.get_symptom_by_code(code)
        if symptom:
            return symptom.get("weight", 0.5)
        return 0.5
