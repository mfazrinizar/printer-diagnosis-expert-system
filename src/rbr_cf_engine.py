from src.knowledge_base import KnowledgeBase


class RBRCFEngine:
    """
    Rule-Based Reasoning Engine with Certainty Factor (CF).

    Implementasi lengkap metode Certainty Factor berdasarkan teori MYCIN
    oleh Shortliffe & Buchanan (1975).

    Konsep dasar:
        CF(H, E) = MB(H, E) - MD(H, E)

    di mana:
        - CF = Certainty Factor (nilai akhir keyakinan)
        - MB = Measure of Belief (ukuran kepercayaan)
        - MD = Measure of Disbelief (ukuran ketidakpercayaan)

    Perhitungan per rule:
        CF(Rule) = MB(Rule) - MD(Rule)
            di mana MB dan MD ditetapkan oleh pakar

    CF evidence (untuk kondisi AND):
        CF(E) = min(CF(E1), CF(E2), ..., CF(En))

    CF hipotesis berdasarkan evidence:
        CF(H, E) = CF(E) * CF(Rule)    jika CF(E) > 0
        CF(H, E) = CF(E) * CF(Rule)    jika CF(E) < 0 (menambah disbelief)

    Formula kombinasi (dua rule menghasilkan diagnosis sama):
        Jika CF1 >= 0 dan CF2 >= 0: CF1 + CF2 * (1 - CF1)
        Jika CF1 < 0 dan CF2 < 0:  CF1 + CF2 * (1 + CF1)
        Lainnya: (CF1 + CF2) / (1 - min(|CF1|, |CF2|))

    Skala Nilai Ketidakpastian (Uncertain Terms):
        +1.0 = Pasti (Definitely)
        +0.8 = Hampir Pasti (Almost Certainly)
        +0.6 = Kemungkinan Besar (Probably)
        +0.4 = Mungkin (Maybe)
        +0.2 = Tidak Tahu (Unknown) ... -0.2
        -0.4 = Mungkin Tidak (Maybe Not)
        -0.6 = Kemungkinan Besar Tidak (Probably Not)
        -0.8 = Hampir Pasti Tidak (Almost Certainly Not)
        -1.0 = Pasti Tidak (Definitely Not)

    Referensi:
    - Shortliffe, E.H., & Buchanan, B.G. (1975). A model of inexact
      reasoning in medicine. Mathematical Biosciences, 23(3-4), 351-379.
    - Turban, E., Aronson, J.E., & Liang, T.P. (2005). Decision Support
      Systems and Intelligent Systems (7th ed.). Pearson Prentice Hall.
    """

    # Skala lengkap Uncertain Terms sesuai PPT MYCIN
    # Meliputi rentang -1.0 (Pasti Tidak) hingga +1.0 (Pasti)
    USER_CF_OPTIONS = [
        ("Pasti", 1.0),
        ("Hampir Pasti", 0.8),
        ("Kemungkinan Besar", 0.6),
        ("Mungkin", 0.4),
        ("Tidak Tahu", 0.2),
        ("Tidak Tahu (Netral)", 0.0),
        ("Tidak Tahu (Cenderung Tidak)", -0.2),
        ("Mungkin Tidak", -0.4),
        ("Kemungkinan Besar Tidak", -0.6),
        ("Hampir Pasti Tidak", -0.8),
        ("Pasti Tidak", -1.0),
    ]

    def __init__(self, knowledge_base: KnowledgeBase):
        self._kb = knowledge_base

    def calculate_cf(
        self, user_cf_values: dict[str, float]
    ) -> list[dict]:
        """
        Menghitung Certainty Factor untuk semua rule menggunakan
        formula lengkap MB-MD dari MYCIN.

        Args:
            user_cf_values: Dict mapping symptom code -> user CF value.
                            Contoh: {"B1": 1.0, "B2": 0.8, "B3": -0.6}

        Returns:
            List diagnosis dengan nilai CF final, diurutkan dari CF
            tertinggi ke terendah.
        """
        rules = self._kb.get_rules()
        diagnosis_results = {}  # group by diagnosis name

        for rule in rules:
            mb_expert = rule.get("mb", 0.5)
            md_expert = rule.get("md", 0.0)
            cf_expert = mb_expert - md_expert
            conditions = rule["conditions"]

            # Hitung CF evidence: untuk AND logic, ambil minimum
            cf_evidences = []
            condition_details = []
            for code in conditions:
                symptom = self._kb.get_symptom_by_code(code)
                user_cf = user_cf_values.get(code, 0.0)
                cf_evidences.append(user_cf)
                condition_details.append({
                    "code": code,
                    "description": symptom["description"] if symptom else code,
                    "user_cf": user_cf,
                })

            cf_evidence = min(cf_evidences) if cf_evidences else 0.0

            # CF(H, E) = CF(E) * CF(Rule)
            cf_result = cf_evidence * cf_expert

            entry = {
                "rule_code": rule["code"],
                "diagnosis": rule["diagnosis"],
                "solution": rule["solution"],
                "severity": rule.get("severity", "medium"),
                "category": rule.get("category", "other"),
                "references": rule.get("references", []),
                "mb_expert": mb_expert,
                "md_expert": md_expert,
                "cf_expert": round(cf_expert, 4),
                "cf_evidence": round(cf_evidence, 4),
                "cf_result": round(cf_result, 4),
                "conditions": condition_details,
            }

            diag_key = rule["diagnosis"]
            if diag_key in diagnosis_results:
                # Combine CFs for same diagnosis
                existing = diagnosis_results[diag_key]
                combined_cf = self._combine_cf(
                    existing["cf_final"], cf_result
                )
                existing["cf_final"] = round(combined_cf, 4)
                existing["contributing_rules"].append(entry)
            else:
                diagnosis_results[diag_key] = {
                    "diagnosis": rule["diagnosis"],
                    "solution": rule["solution"],
                    "severity": rule.get("severity", "medium"),
                    "category": rule.get("category", "other"),
                    "references": rule.get("references", []),
                    "cf_final": round(cf_result, 4),
                    "contributing_rules": [entry],
                }

        results = list(diagnosis_results.values())
        # Filter: tampilkan yang CF > 0 (ada keyakinan)
        results = [r for r in results if r["cf_final"] > 0]
        results.sort(key=lambda x: x["cf_final"], reverse=True)

        return results

    def get_inference_trace(
        self, user_cf_values: dict[str, float]
    ) -> list[dict]:
        """
        Mengembalikan jejak inferensi (trace) langkah demi langkah
        proses perhitungan Certainty Factor dengan detail MB dan MD.

        Args:
            user_cf_values: Dict mapping symptom code -> user CF value.

        Returns:
            List langkah inferensi detail.
        """
        trace = []
        rules = self._kb.get_rules()

        for i, rule in enumerate(rules, 1):
            mb_expert = rule.get("mb", 0.5)
            md_expert = rule.get("md", 0.0)
            cf_expert = mb_expert - md_expert
            conditions = rule["conditions"]

            condition_cfs = []
            for code in conditions:
                symptom = self._kb.get_symptom_by_code(code)
                user_cf = user_cf_values.get(code, 0.0)
                condition_cfs.append({
                    "code": code,
                    "description": symptom["description"] if symptom else code,
                    "user_cf": user_cf,
                })

            cf_evidence = min(c["user_cf"] for c in condition_cfs) if condition_cfs else 0.0
            cf_result = cf_evidence * cf_expert

            cf_values_str = ", ".join(
                str(c["user_cf"]) for c in condition_cfs
            )

            trace.append({
                "step": i,
                "rule_code": rule["code"],
                "diagnosis": rule["diagnosis"],
                "mb_expert": mb_expert,
                "md_expert": md_expert,
                "cf_expert": round(cf_expert, 4),
                "conditions": condition_cfs,
                "cf_evidence": round(cf_evidence, 4),
                "cf_result": round(cf_result, 4),
                "formula_mb_md": (
                    f"CF(Rule) = MB - MD = {mb_expert} - {md_expert} "
                    f"= {cf_expert:.2f}"
                ),
                "formula_cf": (
                    f"CF(H,E) = CF(E) x CF(Rule) = "
                    f"min({cf_values_str}) x {cf_expert:.2f} "
                    f"= {cf_evidence:.2f} x {cf_expert:.2f} "
                    f"= {cf_result:.4f}"
                ),
                "fired": cf_result > 0,
            })

        return trace

    @staticmethod
    def _combine_cf(cf1: float, cf2: float) -> float:
        """
        Kombinasi dua CF berdasarkan formula Shortliffe & Buchanan.

        Digunakan ketika dua rule berbeda menghasilkan diagnosis yang sama.

        Formula (sesuai PPT):
            - CF1 >= 0 dan CF2 >= 0: CF1 + CF2 * (1 - CF1)
            - CF1 < 0 dan CF2 < 0:  CF1 + CF2 * (1 + CF1)
            - Lainnya: (CF1 + CF2) / (1 - min(|CF1|, |CF2|))
        """
        if cf1 >= 0 and cf2 >= 0:
            return cf1 + cf2 * (1 - cf1)
        elif cf1 < 0 and cf2 < 0:
            return cf1 + cf2 * (1 + cf1)
        else:
            denominator = 1 - min(abs(cf1), abs(cf2))
            if denominator == 0:
                return 0.0
            return (cf1 + cf2) / denominator

    @staticmethod
    def cf_to_label(cf: float) -> str:
        """Konversi nilai CF ke label tingkat keyakinan (Uncertain Terms)."""
        if cf >= 0.8:
            return "Pasti / Hampir Pasti"
        elif cf >= 0.6:
            return "Kemungkinan Besar"
        elif cf >= 0.4:
            return "Mungkin"
        elif cf >= 0.2:
            return "Tidak Tahu"
        elif cf > 0:
            return "Tidak Tahu (Rendah)"
        elif cf == 0:
            return "Tidak Ada Keyakinan"
        elif cf >= -0.4:
            return "Mungkin Tidak"
        elif cf >= -0.6:
            return "Kemungkinan Besar Tidak"
        elif cf >= -0.8:
            return "Hampir Pasti Tidak"
        else:
            return "Pasti Tidak"
