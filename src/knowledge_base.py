import json
from pathlib import Path
from typing import Optional


class KnowledgeBase:
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
