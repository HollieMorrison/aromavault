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