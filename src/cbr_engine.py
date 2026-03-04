import json
from pathlib import Path
from datetime import datetime
from typing import Optional

from src.knowledge_base import KnowledgeBase


class CBREngine:
    """
    Case-Based Reasoning (CBR) Engine.

    Menggunakan siklus CBR (Retrieve-Reuse-Revise-Retain) untuk mendiagnosis
    masalah printer berdasarkan kasus-kasus sebelumnya.

    Metode similarity menggunakan Weighted Nearest Neighbor:
        Similarity(C_new, C_old) = Σ (w_i * sim(f_i_new, f_i_old)) / Σ w_i

    di mana:
        - w_i = bobot fitur ke-i (dari symptom weight di knowledge base)
        - sim(f_i_new, f_i_old) = 1 jika fitur cocok, 0 jika tidak
        - Σ w_i = total bobot semua fitur yang relevan

    Referensi:
    - Aamodt, A., & Plaza, E. (1994). Case-Based Reasoning: Foundational
      Issues, Methodological Variations, and System Approaches. AI Communications, 7(1), 39-59.
    - Kolodner, J. (1993). Case-Based Reasoning. Morgan Kaufmann Publishers.
    - Watson, I. (1997). Applying Case-Based Reasoning: Techniques for
      Enterprise Systems. Morgan Kaufmann Publishers.
    """

    SIMILARITY_THRESHOLD = 0.4

    def __init__(self, case_library_path: str, knowledge_base: KnowledgeBase):
        self._kb = knowledge_base
        self._case_library_path = case_library_path
        self._cases = self._load_cases(case_library_path)

    def _load_cases(self, path: str) -> list[dict]:
        p = Path(path)
        if not p.exists():
            return []
        with open(p, "r", encoding="utf-8") as f:
            return json.load(f)

    def _save_cases(self):
        with open(self._case_library_path, "w", encoding="utf-8") as f:
            json.dump(self._cases, f, ensure_ascii=False, indent=2)

    def get_all_cases(self) -> list[dict]:
        return self._cases

    def get_case_by_id(self, case_id: str) -> Optional[dict]:
        for case in self._cases:
            if case["case_id"] == case_id:
                return case
        return None

    def compute_similarity(self, new_symptoms: list[str], case_symptoms: list[str]) -> float:
        """
        Menghitung similarity menggunakan Weighted Nearest Neighbor.

        Formula:
            Similarity = Σ (w_i * match_i) / Σ w_i

        di mana match_i = 1 jika gejala ada di kedua kasus, 0 jika tidak.
        Bobot w_i diambil dari knowledge base (symptom weight).

        Args:
            new_symptoms: Gejala kasus baru (input user).
            case_symptoms: Gejala kasus lama (dari case library).

        Returns:
            Nilai similarity antara 0.0 dan 1.0.
        """
        all_symptom_codes = set(new_symptoms) | set(case_symptoms)

        if not all_symptom_codes:
            return 0.0

        total_weighted_match = 0.0
        total_weight = 0.0

        for code in all_symptom_codes:
            weight = self._kb.get_symptom_weight(code)
            total_weight += weight

            in_new = code in new_symptoms
            in_case = code in case_symptoms

            if in_new and in_case:
                total_weighted_match += weight
            # Tidak cocok → 0 kontribusi

        if total_weight == 0:
            return 0.0

        return round(total_weighted_match / total_weight, 4)

    def retrieve(self, new_symptoms: list[str], top_k: int = 5) -> list[dict]:
        """
        RETRIEVE: Mengambil kasus-kasus paling mirip dari case library.

        Menghitung similarity antara kasus baru dan semua kasus di library,
        lalu mengembalikan top-K kasus dengan similarity tertinggi.

        Args:
            new_symptoms: Gejala kasus baru.
            top_k: Jumlah kasus teratas yang dikembalikan.

        Returns:
            List kasus teratas dengan skor similarity.
        """
        scored_cases = []

        for case in self._cases:
            similarity = self.compute_similarity(new_symptoms, case["symptoms"])

            if similarity >= self.SIMILARITY_THRESHOLD:
                scored_case = case.copy()
                scored_case["similarity"] = similarity

                # Detail breakdown fitur yang cocok dan tidak
                matched_symptoms = set(new_symptoms) & set(case["symptoms"])
                unmatched_new = set(new_symptoms) - set(case["symptoms"])
                unmatched_case = set(case["symptoms"]) - set(new_symptoms)

                scored_case["matched_symptoms"] = list(matched_symptoms)
                scored_case["unmatched_in_new"] = list(unmatched_new)
                scored_case["unmatched_in_case"] = list(unmatched_case)

                # Enriched symptom details
                scored_case["matched_details"] = []
                for code in matched_symptoms:
                    symptom = self._kb.get_symptom_by_code(code)
                    if symptom:
                        scored_case["matched_details"].append({
                            "code": code,
                            "description": symptom["description"]
                        })

                scored_cases.append(scored_case)

        scored_cases.sort(key=lambda x: x["similarity"], reverse=True)
        return scored_cases[:top_k]

    def reuse(self, retrieved_cases: list[dict]) -> Optional[dict]:
        """
        REUSE: Mengadaptasi solusi dari kasus yang paling mirip.

        Mengambil kasus dengan similarity tertinggi dan mengusulkan
        solusinya sebagai solusi awal untuk kasus baru.

        Args:
            retrieved_cases: List kasus yang di-retrieve, sudah diurutkan.

        Returns:
            Proposed solution berdasarkan kasus teratas, atau None.
        """
        if not retrieved_cases:
            return None

        best_case = retrieved_cases[0]

        proposed = {
            "source_case_id": best_case["case_id"],
            "source_case_title": best_case["title"],
            "similarity": best_case["similarity"],
            "proposed_diagnosis": best_case["diagnosis"],
            "proposed_solution": best_case["solution"],
            "severity": best_case.get("severity", "medium"),
            "adaptation_notes": self._generate_adaptation_notes(best_case),
            "confidence_level": self._similarity_to_confidence(best_case["similarity"])
        }

        return proposed

    def retain(self, new_case: dict) -> str:
        """
        RETAIN: Menyimpan kasus baru ke dalam case library.

        Kasus yang berhasil diselesaikan disimpan agar bisa direferensikan
        untuk kasus-kasus serupa di masa depan.

        Args:
            new_case: Dict berisi informasi kasus baru (symptoms, diagnosis, solution, dll).

        Returns:
            Case ID yang diberikan untuk kasus baru.
        """
        next_id = self._generate_next_id()

        case_entry = {
            "case_id": next_id,
            "title": new_case.get("title", f"Kasus baru {next_id}"),
            "description": new_case.get("description", ""),
            "printer_type": new_case.get("printer_type", "Unknown"),
            "brand": new_case.get("brand", "Unknown"),
            "symptoms": new_case.get("symptoms", []),
            "diagnosis": new_case.get("diagnosis", ""),
            "solution": new_case.get("solution", ""),
            "severity": new_case.get("severity", "medium"),
            "outcome": new_case.get("outcome", "pending"),
            "date": datetime.now().strftime("%Y-%m-%d"),
            "technician_notes": new_case.get("technician_notes", ""),
            "references": new_case.get("references", [])
        }

        self._cases.append(case_entry)
        self._save_cases()

        return next_id

    def get_similarity_breakdown(self, new_symptoms: list[str], case: dict) -> dict:
        """
        Mengembalikan breakdown detail perhitungan similarity per gejala
        beserta total numerator dan denominator untuk formula WNN.

        Formula WNN:
            Similarity(C_new, C_old) = Σ (w_i * sim(f_i)) / Σ w_i

        Args:
            new_symptoms: Gejala kasus baru.
            case: Kasus dari library.

        Returns:
            Dict berisi:
            - "features": list detail per fitur
            - "total_weighted_match": Σ (w_i * sim_i) -- numerator
            - "total_weight": Σ w_i -- denominator
            - "similarity": hasil akhir
        """
        case_symptoms = case.get("symptoms", [])
        all_codes = sorted(set(new_symptoms) | set(case_symptoms))
        features = []

        total_weighted_match = 0.0
        total_weight = 0.0

        for code in all_codes:
            symptom = self._kb.get_symptom_by_code(code)
            weight = self._kb.get_symptom_weight(code)
            in_new = code in new_symptoms
            in_case = code in case_symptoms
            matched = in_new and in_case

            sim_fi = 1 if matched else 0
            wi_x_sim = weight * sim_fi

            total_weighted_match += wi_x_sim
            total_weight += weight

            features.append({
                "code": code,
                "description": symptom["description"] if symptom else code,
                "weight": weight,
                "in_new_case": in_new,
                "in_old_case": in_case,
                "matched": matched,
                "sim_fi": sim_fi,
                "wi_x_sim": round(wi_x_sim, 4),
            })

        similarity = round(total_weighted_match / total_weight, 4) if total_weight > 0 else 0.0

        return {
            "features": features,
            "total_weighted_match": round(total_weighted_match, 4),
            "total_weight": round(total_weight, 4),
            "similarity": similarity,
        }

    def get_case_statistics(self) -> dict:
        """Statistik ringkasan dari case library."""
        if not self._cases:
            return {"total_cases": 0}

        brands = {}
        severities = {"low": 0, "medium": 0, "high": 0}
        outcomes = {"success": 0, "failed": 0, "pending": 0}

        for case in self._cases:
            brand = case.get("brand", "Unknown")
            brands[brand] = brands.get(brand, 0) + 1

            sev = case.get("severity", "medium")
            severities[sev] = severities.get(sev, 0) + 1

            out = case.get("outcome", "pending")
            outcomes[out] = outcomes.get(out, 0) + 1

        return {
            "total_cases": len(self._cases),
            "brands": brands,
            "severities": severities,
            "outcomes": outcomes
        }

    def _generate_next_id(self) -> str:
        if not self._cases:
            return "C001"
        max_num = 0
        for case in self._cases:
            cid = case.get("case_id", "C000")
            try:
                num = int(cid[1:])
                if num > max_num:
                    max_num = num
            except (ValueError, IndexError):
                pass
        return f"C{max_num + 1:03d}"

    def _generate_adaptation_notes(self, best_case: dict) -> str:
        similarity = best_case.get("similarity", 0)
        if similarity >= 0.9:
            return "Kasus sangat mirip. Solusi dapat diterapkan langsung tanpa modifikasi."
        elif similarity >= 0.7:
            return "Kasus cukup mirip. Solusi dapat diadaptasi dengan sedikit penyesuaian sesuai kondisi spesifik printer."
        elif similarity >= 0.5:
            return "Kasus memiliki kemiripan parsial. Perlu evaluasi lebih lanjut dan kemungkinan modifikasi solusi."
        else:
            return "Kemiripan rendah. Solusi hanya sebagai referensi awal, perlu investigasi lebih mendalam."

    @staticmethod
    def _similarity_to_confidence(similarity: float) -> str:
        if similarity >= 0.9:
            return "Sangat Tinggi"
        elif similarity >= 0.7:
            return "Tinggi"
        elif similarity >= 0.5:
            return "Sedang"
        else:
            return "Rendah"
