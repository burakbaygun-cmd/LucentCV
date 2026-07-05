"""
UygunCV - Basit Hafiza (Memory) Katmani

Kullanicinin gecmis analizlerini yerel bir JSON dosyasinda saklar.
Ileride SQLite/Supabase'e tasinabilir; MVP icin dosya tabanli yeterli.
"""

import json
import os
from datetime import datetime

MEMORY_FILE = "memory_store.json"


def load_memory() -> list:
    if not os.path.exists(MEMORY_FILE):
        return []
    with open(MEMORY_FILE, "r", encoding="utf-8") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []


def save_analysis(cv_snippet: str, job_snippet: str, result: dict) -> None:
    """Yeni bir analiz sonucunu hafizaya ekler."""
    memory = load_memory()
    entry = {
        "timestamp": datetime.now().isoformat(timespec="seconds"),
        "cv_snippet": cv_snippet[:100],
        "job_snippet": job_snippet[:100],
        "match_score": result.get("match_result", {}).get("match_score"),
        "result": result,
    }
    memory.append(entry)
    with open(MEMORY_FILE, "w", encoding="utf-8") as f:
        json.dump(memory, f, ensure_ascii=False, indent=2)


def get_history() -> list:
    """Gecmis analizlerin ozet listesini dondurur (en yeni once)."""
    memory = load_memory()
    return list(reversed(memory))
