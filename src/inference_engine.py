from src.knowledge_base import KnowledgeBase


class InferenceEngine:
    def __init__(self, knowledge_base: KnowledgeBase):
        self._kb = knowledge_base

    def diagnose(self, selected_symptoms: list[str]) -> list[dict]:
        """
        Forward chaining dengan AND logic.
        Mengembalikan list diagnosis yang semua kondisinya terpenuhi.
        """
        results = []
        selected_set = set(selected_symptoms)

        for rule in self._kb.get_rules():
            conditions = set(rule["conditions"])
            if conditions.issubset(selected_set):
                results.append({
                    "code": rule["code"],
                    "diagnosis": rule["diagnosis"],
                    "solution": rule["solution"],
                    "matched_conditions": rule["conditions"]
                })

        return results

    def get_matching_rules_partial(self, selected_symptoms: list[str]) -> list[dict]:
        """
        Mengembalikan rules dengan minimal satu kondisi terpenuhi (untuk info).
        """
        results = []
        selected_set = set(selected_symptoms)

        for rule in self._kb.get_rules():
            conditions = set(rule["conditions"])
            matched = conditions.intersection(selected_set)
            if matched:
                results.append({
                    "code": rule["code"],
                    "diagnosis": rule["diagnosis"],
                    "matched": len(matched),
                    "total": len(conditions),
                    "complete": conditions.issubset(selected_set)
                })

        return results
