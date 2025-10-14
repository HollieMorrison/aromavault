from __future__ import annotations
from dataclasses import asdict
from pathlib import Path
import csv
import json
from typing import Optional

from models import Perfume, UserProfile

# File-based storage configuration
DATA_DIR = Path("data")
DB_PATH = DATA_DIR / "db.json"
DEFAULT_DB: dict[str, list[dict]] = {"perfumes": [], "profiles": []}


def _ensure_db() -> None:
    """Create the data directory and JSON DB file if they don't exist."""
    DATA_DIR.mkdir(exist_ok=True)
    if not DB_PATH.exists():
        DB_PATH.write_text(json.dumps(DEFAULT_DB, indent=2))


def load_db() -> dict[str, list[dict]]:
    """Load the entire JSON DB into memory as a Python dict."""
    _ensure_db()
    return json.loads(DB_PATH.read_text())


def save_db(db: dict[str, list[dict]]) -> None:
    """Persist the in-memory DB back to disk in a human-readable format."""
    DB_PATH.write_text(json.dumps(db, indent=2))


# ---------- Perfumes ----------


def add_perfume(p: Perfume) -> None:
    """Append a new perfume record to the JSON array and save."""
    db = load_db()
    db["perfumes"].append(asdict(p))
    save_db(db)


def list_perfumes() -> list[dict]:
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


# ---------- Profiles ----------


def add_profile(profile: UserProfile) -> None:
    """Append a new user profile to the DB and save."""
    db = load_db()
    db["profiles"].append(asdict(profile))
    save_db(db)


def list_profiles() -> list[dict]:
    """Return all user profiles from the DB."""
    return load_db()["profiles"]


def get_profile(pid: str) -> Optional[dict]:
    """Fetch a single profile by exact UUID."""
    return next((p for p in list_profiles() if p["id"] == pid), None)


# ---------- CSV import/export ----------

CSV_FIELDS = ["name", "brand", "price", "notes", "allergens", "rating", "stock"]


def export_csv(path: str) -> int:
    """Write the perfume collection to a CSV file and return the number of rows."""
    perfumes = list_perfumes()
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=CSV_FIELDS)
        writer.writeheader()
        for p in perfumes:
            row = {k: p.get(k, "") for k in CSV_FIELDS}
            # Join list fields into comma-separated strings for CSV
            row["notes"] = ", ".join(p.get("notes", []))
            row["allergens"] = ", ".join(p.get("allergens", []))
            writer.writerow(row)
    return len(perfumes)


def import_csv(path: str) -> int:
    """Read perfumes from a CSV and merge, skipping duplicates by (name, brand)."""
    db = load_db()
    existing = {(p["name"].strip().lower(), p["brand"].strip().lower()) for p in db["perfumes"]}
    added = 0
    with open(path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            key = (
                row.get("name", "").strip().lower(),
                row.get("brand", "").strip().lower(),
            )
            if key in existing:
                continue  # Skip duplicates based on name+brand
            p = Perfume.new(
                name=row.get("name", ""),
                brand=row.get("brand", ""),
                price=float(row.get("price", 0) or 0),
                notes=[n.strip() for n in (row.get("notes", "").split(",") if row.get("notes") else []) if n.strip()],
                allergens=[
                    a.strip()
                    for a in (row.get("allergens", "").split(",") if row.get("allergens") else [])
                    if a.strip()
                ],
                rating=float(row.get("rating") or 0) if row.get("rating") else None,
                stock=int(row.get("stock", 0) or 0),
            )
            db["perfumes"].append(asdict(p))
            existing.add(key)
            added += 1
    save_db(db)
    return added
