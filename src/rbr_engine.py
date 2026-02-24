from src.knowledge_base import KnowledgeBase


class RBREngine:
    """
    Rule-Based Reasoning (RBR) Engine.

    Menggunakan metode Forward Chaining untuk mencocokkan gejala yang dipilih
    dengan aturan (rules) yang ada di knowledge base.

    Referensi:
    - Turban, E., Aronson, J.E., & Liang, T.P. (2005). Decision Support Systems
      and Intelligent Systems (7th ed.). Pearson Prentice Hall.
    - Giarratano, J.C., & Riley, G.D. (2005). Expert Systems: Principles and
      Programming (4th ed.). Thomson Course Technology.
    """

    def __init__(self, knowledge_base: KnowledgeBase):
        self._kb = knowledge_base

    def forward_chaining(self, selected_symptoms: list[str]) -> list[dict]:
        """
        Forward Chaining dengan AND logic.

        Cara kerja:
        1. Ambil semua gejala yang dipilih oleh user (fakta).
        2. Untuk setiap rule di knowledge base, cek apakah SEMUA kondisi
           (antecedent) terpenuhi oleh fakta yang ada.
        3. Jika semua kondisi terpenuhi, rule tersebut "fire" dan
           diagnosisnya ditambahkan ke hasil.

        Args:
            selected_symptoms: List kode gejala yang dipilih user.

        Returns:
            List diagnosis yang cocok, lengkap dengan detail.
        """
        results = []
        selected_set = set(selected_symptoms)
        all_symptoms = self._kb.get_symptoms()

        for rule in self._kb.get_rules():
            conditions = set(rule["conditions"])
            matched = conditions.intersection(selected_set)

            if conditions.issubset(selected_set):
                matched_details = []
                for code in rule["conditions"]:
                    symptom = self._kb.get_symptom_by_code(code)
                    if symptom:
                        matched_details.append({
                            "code": code,
                            "description": symptom["description"]
                        })

                results.append({
                    "code": rule["code"],
                    "diagnosis": rule["diagnosis"],
                    "solution": rule["solution"],
                    "severity": rule.get("severity", "medium"),
                    "category": rule.get("category", "other"),
                    "references": rule.get("references", []),
                    "matched_conditions": rule["conditions"],
                    "matched_details": matched_details,
                    "confidence": 1.0,
                    "match_type": "exact"
                })

        return sorted(results, key=lambda x: self._severity_score(x["severity"]), reverse=True)

    def partial_matching(self, selected_symptoms: list[str]) -> list[dict]:
        """
        Mengembalikan rules dengan partial match (minimal satu kondisi terpenuhi).

        Berguna untuk memberikan saran kemungkinan diagnosis ketika
        tidak ada rule yang 100% cocok.

        Args:
            selected_symptoms: List kode gejala yang dipilih user.

        Returns:
            List kemungkinan diagnosis dengan persentase kecocokkan.
        """
        results = []
        selected_set = set(selected_symptoms)

        for rule in self._kb.get_rules():
            conditions = set(rule["conditions"])
            matched = conditions.intersection(selected_set)

            if matched and not conditions.issubset(selected_set):
                confidence = len(matched) / len(conditions)

                matched_details = []
                for code in matched:
                    symptom = self._kb.get_symptom_by_code(code)
                    if symptom:
                        matched_details.append({
                            "code": code,
                            "description": symptom["description"]
                        })

                unmatched_details = []
                unmatched = conditions - matched
                for code in unmatched:
                    symptom = self._kb.get_symptom_by_code(code)
                    if symptom:
                        unmatched_details.append({
                            "code": code,
                            "description": symptom["description"]
                        })

                results.append({
                    "code": rule["code"],
                    "diagnosis": rule["diagnosis"],
                    "solution": rule["solution"],
                    "severity": rule.get("severity", "medium"),
                    "category": rule.get("category", "other"),
                    "references": rule.get("references", []),
                    "matched_conditions": list(matched),
                    "matched_details": matched_details,
                    "unmatched_conditions": list(unmatched),
                    "unmatched_details": unmatched_details,
                    "confidence": round(confidence, 2),
                    "total_conditions": len(conditions),
                    "match_type": "partial"
                })

        return sorted(results, key=lambda x: x["confidence"], reverse=True)

    def get_inference_trace(self, selected_symptoms: list[str]) -> list[dict]:
        """
        Mengembalikan jejak inferensi (trace) langkah demi langkah
        proses forward chaining.

        Berguna untuk transparansi dan penjelasan proses penalaran sistem.

        Args:
            selected_symptoms: List kode gejala yang dipilih user.

        Returns:
            List langkah inferensi, menunjukkan rule mana yang diperiksa
            dan hasilnya.
        """
        trace = []
        selected_set = set(selected_symptoms)

        for i, rule in enumerate(self._kb.get_rules(), 1):
            conditions = set(rule["conditions"])
            matched = conditions.intersection(selected_set)
            is_fired = conditions.issubset(selected_set)

            step = {
                "step": i,
                "rule_code": rule["code"],
                "rule_diagnosis": rule["diagnosis"],
                "conditions_required": list(conditions),
                "conditions_matched": list(matched),
                "conditions_unmatched": list(conditions - matched),
                "match_ratio": f"{len(matched)}/{len(conditions)}",
                "fired": is_fired,
                "status": "FIRE" if is_fired else f"TIDAK FIRE ({len(matched)}/{len(conditions)} terpenuhi)"
            }
            trace.append(step)

        return trace

    @staticmethod
    def _severity_score(severity: str) -> int:
        mapping = {"low": 1, "medium": 2, "high": 3}
        return mapping.get(severity, 0)
