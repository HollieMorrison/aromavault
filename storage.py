from __future__ import annotations
from dataclasses import asdict
from pathlib import Path
import csv
import json
from typing import Dict, List, Optional


from models import Perfume, UserProfile


# File‑based storage configuration
DATA_DIR = Path("data")
DB_PATH = DATA_DIR / "db.json"
DEFAULT_DB: Dict[str, List[dict]] = {"perfumes": [], "profiles": []}




def _ensure_db() -> None:
"""Create the data directory and JSON DB file if they don't exist."""
DATA_DIR.mkdir(exist_ok=True)
if not DB_PATH.exists():
DB_PATH.write_text(json.dumps(DEFAULT_DB, indent=2))




def load_db() -> Dict[str, List[dict]]:
"""Load the entire JSON DB into memory as a Python dict."""
_ensure_db()
return json.loads(DB_PATH.read_text())




def save_db(db: Dict[str, List[dict]]) -> None:
"""Persist the in‑memory DB back to disk in a human‑readable format."""
DB_PATH.write_text(json.dumps(db, indent=2))

# ---------- Perfumes ----------


def add_perfume(p: Perfume) -> None:
"""Append a new perfume record to the JSON array and save."""
db = load_db()
db["perfumes"].append(asdict(p))
save_db(db)




def list_perfumes() -> List[dict]:
"""Return all perfume dicts from the DB."""
return load_db()["perfumes"]




def get_perfume(pid: str) -> Optional[dict]:
"""Fetch a single perfume by exact UUID."""
return next((p for p in list_perfumes() if p["id"] == pid), None)




def update_perfume(pid: str, **updates) -> bool:
"""Update specific fields of a perfume by UUID and save the DB."""
db = load_db()
for i, p in enumerate(db["perfumes"]):
if p["id"] == pid:
p.update(updates)
db["perfumes"][i] = p
save_db(db)
return True
return False




def delete_perfume(pid: str) -> bool:
"""Remove a perfume by UUID and persist the change."""
db = load_db()
before = len(db["perfumes"])
db["perfumes"] = [p for p in db["perfumes"] if p["id"] != pid]
changed = len(db["perfumes"]) != before
if changed:
save_db(db)
return changed