"""
Script untuk konversi CSV ke JSON knowledge base.
Jalankan sekali untuk generate knowledge_base.json dari file CSV.
"""

import csv
import json
from pathlib import Path


def load_kerusakan(csv_path: str) -> list[dict]:
    symptoms = []
    with open(csv_path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            symptoms.append({
                "code": row["Kode"].strip(),
                "description": row["Kerusakan"].strip()
            })
    return symptoms


def load_gejala(csv_path: str) -> list[dict]:
    rules = []
    with open(csv_path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            conditions = [c.strip() for c in row["Gejala yang dihadapi"].split(",")]
            rules.append({
                "code": row["Kode"].strip(),
                "conditions": conditions,
                "diagnosis": row["THEN"].strip(),
                "solution": ""
            })
    return rules


def main():
    base_path = Path(__file__).parent.parent

    symptoms = load_kerusakan(base_path / "kerusakan.csv")
    rules = load_gejala(base_path / "gejala.csv")

    knowledge_base = {
        "symptoms": symptoms,
        "rules": rules
    }

    output_path = base_path / "data" / "knowledge_base.json"
    output_path.parent.mkdir(exist_ok=True)

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(knowledge_base, f, ensure_ascii=False, indent=2)

    print(f"Knowledge base saved to: {output_path}")
    print(f"Total symptoms: {len(symptoms)}")
    print(f"Total rules: {len(rules)}")


if __name__ == "__main__":
    main()
