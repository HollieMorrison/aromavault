from __future__ import annotations

import json
from pathlib import Path

# Default data file (you can override by passing a Path to functions)
DEFAULT_DB = Path("data.json")


def _read_json(path: Path) -> list[dict]:
    """
    Read a JSON file that stores a list of perfume dicts.
    Returns an empty list if the file doesn't exist or is empty/invalid.
    """
    try:
        if not path.exists():
            return []
        text = path.read_text(encoding="utf-8").strip()
        if not text:
            return []
        data = json.loads(text)
        if isinstance(data, list):
            return [x for x in data if isinstance(x, dict)]
        return []
    except (OSError, json.JSONDecodeError):
        # Friendly failure: treat as empty dataset
        return []


def _write_json(path: Path, data: list[dict]) -> None:
    """
    Write list of dicts to JSON file, creating parent dirs if needed.
    """
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


def load_all(path: Path | None = None) -> list[dict]:
    """
    Load the entire dataset from JSON.
    """
    return _read_json(path or DEFAULT_DB)


def save_all(items: list[dict], path: Path | None = None) -> None:
    """
    Overwrite the dataset with the provided list of dicts.
    """
    _write_json(path or DEFAULT_DB, items)


def get_by_id(pid: str, path: Path | None = None) -> dict | None:
    """
    Return the perfume dict with matching id, or None if not found.
    """
    items = load_all(path)
    for it in items:
        if str(it.get("id")) == str(pid):
            return it
    return None


def upsert(item: dict, path: Path | None = None) -> dict:
    """
    Insert or update a perfume by its 'id' field.
    Returns the stored item.
    """
    if "id" not in item:
        raise ValueError("Item must contain an 'id' field")
    db_path = path or DEFAULT_DB
    items = load_all(db_path)
    updated = False
    for idx, it in enumerate(items):
        if str(it.get("id")) == str(item["id"]):
            items[idx] = {**it, **item}
            updated = True
            break
    if not updated:
        items.append(item)
    save_all(items, db_path)
    return item


def delete(pid: str, path: Path | None = None) -> bool:
    """
    Delete an item by id. Returns True if something was removed.
    """
    db_path = path or DEFAULT_DB
    items = load_all(db_path)
    new_items = [it for it in items if str(it.get("id")) != str(pid)]
    removed = len(new_items) != len(items)
    if removed:
        save_all(new_items, db_path)
    return removed


def search(
    query: str | None = None,
    brand: str | None = None,
    notes_any: list[str] | None = None,
    price_max: float | None = None,
    path: Path | None = None,
) -> list[dict]:
    """
    Simple search across the catalog.
    - query: substring match on name (case-insensitive)
    - brand: exact (case-insensitive)
    - notes_any: at least one note must match (case-insensitive)
    - price_max: price <= price_max
    """
    items = load_all(path)

    def norm(s: str) -> str:
        return s.casefold()

    results: list[dict] = []
    for it in items:
        name = str(it.get("name", ""))
        it_brand = str(it.get("brand", ""))
        it_notes = it.get("notes") or []
        it_price = it.get("price")

        if query and norm(query) not in norm(name):
            continue
        if brand and norm(brand) != norm(it_brand):
            continue
        if notes_any:
            s_notes = {norm(x) for x in it_notes if isinstance(x, str)}
            if not any(norm(n) in s_notes for n in notes_any):
                continue
        if price_max is not None:
            try:
                p = float(it_price)
            except (TypeError, ValueError):
                continue
            if p > float(price_max):
                continue
        results.append(it)
    return results


# --- Compatibility wrappers so existing app.py imports keep working ---


def add_perfume(item: dict, path: Path | None = None) -> dict:
    """Legacy name: insert a perfume (or update if id exists)."""
    return upsert(item, path)


def update_perfume(pid: str, changes: dict, path: Path | None = None) -> dict:
    """Legacy name: update by id with partial changes."""
    existing = get_by_id(pid, path)
    if existing is None:
        raise ValueError(f"Perfume with id '{pid}' not found")
    merged = {**existing, **changes, "id": existing.get("id")}
    return upsert(merged, path)


def delete_perfume(pid: str, path: Path | None = None) -> bool:
    """Legacy name: delete by id."""
    return delete(pid, path)


def get_perfume_by_id(pid: str, path: Path | None = None) -> dict | None:
    """Legacy name: fetch by id."""
    return get_by_id(pid, path)


def list_perfumes(path: Path | None = None) -> list[dict]:
    """Legacy name: list all perfumes."""
    return load_all(path)


def search_perfumes(
    query: str | None = None,
    brand: str | None = None,
    notes_any: list[str] | None = None,
    price_max: float | None = None,
    path: Path | None = None,
) -> list[dict]:
    """Legacy name: search helper."""
    return search(query=query, brand=brand, notes_any=notes_any, price_max=price_max, path=path)


# ===== Profile compatibility (separate JSON file) =====

DEFAULT_PROFILES_DB = Path("profiles.json")


def list_profiles(path: Path | None = None) -> list[dict]:
    """Return all user profiles."""
    return load_all(path or DEFAULT_PROFILES_DB)


def get_profile_by_id(uid: str, path: Path | None = None) -> dict | None:
    """Fetch a user profile by id."""
    return get_by_id(uid, path or DEFAULT_PROFILES_DB)


def add_profile(profile: dict, path: Path | None = None) -> dict:
    """Insert or update a user profile (must contain 'id')."""
    return upsert(profile, path or DEFAULT_PROFILES_DB)


def update_profile(uid: str, changes: dict, path: Path | None = None) -> dict:
    """Partial update to a profile by id."""
    existing = get_profile_by_id(uid, path)
    if existing is None:
        raise ValueError(f"Profile with id '{uid}' not found")
    merged = {**existing, **changes, "id": existing.get("id")}
    return upsert(merged, path or DEFAULT_PROFILES_DB)


def delete_profile(uid: str, path: Path | None = None) -> bool:
    """Delete a profile by id."""
    return delete(uid, path or DEFAULT_PROFILES_DB)


# ===== CSV export (perfumes) =====
def export_csv(csv_path, path: Path | None = None) -> int:
    """
    Export the perfumes catalog to CSV.
    - csv_path: destination file path (str or Path)
    - path: optional JSON DB path (defaults to DEFAULT_DB)
    Returns the number of rows written.
    """
    import csv
    from pathlib import Path as _P

    db_path = path or DEFAULT_DB
    items = load_all(db_path)

    # Determine CSV headers: union of keys across items, with sensible ordering
    base_order = ["id", "name", "brand", "notes", "price"]
    keys = set().union(*(it.keys() for it in items)) if items else set(base_order)
    # Keep base_order first, then any extra keys
    fieldnames = [k for k in base_order if k in keys] + [
        k for k in sorted(keys) if k not in base_order
    ]

    # Ensure parent directory exists
    csv_path = _P(csv_path)
    csv_path.parent.mkdir(parents=True, exist_ok=True)

    written = 0
    with csv_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for it in items:
            row = dict(it)
            # Flatten notes (list -> semicolon-separated string)
            if isinstance(row.get("notes"), list):
                row["notes"] = ";".join(map(str, row["notes"]))
            writer.writerow(row)
            written += 1
    return written


# --- Alias for legacy import name expected by app.py ---
def get_profile(uid: str, path: Path | None = None):
    """Legacy alias: get_profile -> get_profile_by_id."""
    return get_profile_by_id(uid, path)


# ===== CSV import (perfumes) =====
def import_csv(csv_path, path: Path | None = None, overwrite: bool = False) -> int:
    """
    Import perfumes from a CSV file into the JSON catalog.
    - csv_path: source CSV (str or Path)
    - path: destination JSON DB (defaults to DEFAULT_DB)
    - overwrite: if True, replace the DB with the CSV rows; otherwise upsert by 'id'
    Returns number of rows ingested.
    """
    import csv
    from pathlib import Path as _P

    db_path = path or DEFAULT_DB
    csv_path = _P(csv_path)

    if not csv_path.exists():
        raise FileNotFoundError(f"CSV not found: {csv_path}")

    # Read existing data (for upsert mode)
    existing = [] if overwrite else load_all(db_path)
    by_id = {str(x.get("id")): x for x in existing if "id" in x}

    ingested = 0
    with csv_path.open("r", encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if not row:
                continue
            # Normalize keys and fields
            item = {
                k.strip(): (v.strip() if isinstance(v, str) else v) for k, v in row.items() if k
            }

            # Ensure required fields exist
            if not item.get("id"):
                # skip rows without an id
                continue

            # notes: string -> list[str]
            notes_val = item.get("notes", "")
            if isinstance(notes_val, str) and notes_val:
                # split on ';' primarily, fall back to ','
                sep = ";" if ";" in notes_val else ("," if "," in notes_val else None)
                item["notes"] = [
                    s.strip() for s in (notes_val.split(sep) if sep else [notes_val]) if s.strip()
                ]
            elif isinstance(notes_val, list):
                # already a list
                pass
            else:
                item["notes"] = []

            # price: to float if possible
            if "price" in item and item["price"] != "":
                try:
                    item["price"] = float(item["price"])
                except (TypeError, ValueError):
                    # leave as-is if not convertible
                    pass

            # Upsert or collect for overwrite
            if overwrite:
                by_id[str(item["id"])] = item
            else:
                upsert(item, db_path)
            ingested += 1

    if overwrite:
        # Replace DB with imported items
        save_all(list(by_id.values()), db_path)

    return ingested


# ---- Aromavault in-memory store helpers (for web API) -----------------------
try:
    PERFUMES  # may already exist
except NameError:
    PERFUMES = []

# If there’s a seed list present, populate once on import.
if not PERFUMES:
    for _seed_name in ("SEED_PERFUMES", "DEFAULT_PERFUMES"):
        if _seed_name in globals() and isinstance(globals()[_seed_name], list):
            PERFUMES = list(globals()[_seed_name])
            break

def _num(v, t=float, default=0.0):
    try:
        if isinstance(v, (int, float)): return t(v)
        s = str(v).strip()
        if s == "": return default
        return t(float(s))
    except Exception:
        return default

def _normalize_item(item: dict) -> dict:
    it = dict(item or {})
    it["id"] = str(it.get("id") or "").strip()
    it["name"] = str(it.get("name") or "").strip()
    it["brand"] = str(it.get("brand") or "").strip()

    notes = it.get("notes")
    if isinstance(notes, list):
        it["notes"] = [str(n).strip() for n in notes if str(n).strip()]
    else:
        s = str(notes or "").strip()
        it["notes"] = [t.strip() for t in s.split(",")] if s else []

    it["price"]  = _num(it.get("price"),  float, 0.0)
    it["rating"] = _num(it.get("rating"), float, 0.0)
    it["stock"]  = int(_num(it.get("stock"), int, 0))

    al = it.get("allergens", [])
    if isinstance(al, list):
        it["allergens"] = [str(a).strip() for a in al if str(a).strip()]
    elif al:
        it["allergens"] = [t.strip() for t in str(al).split(",") if t.strip()]
    else:
        it["allergens"] = []
    return it

def add_or_update_perfume(item: dict):
    """Insert or update by 'id'. Returns (True, None) or (False, 'message')."""
    it = _normalize_item(item)
    if not it.get("id"):
        return False, "Missing 'id'"
    for i, x in enumerate(PERFUMES):
        if isinstance(x, dict) and x.get("id") == it["id"]:
            PERFUMES[i] = it
            return True, None
    PERFUMES.append(it)
    return True, None

def delete_perfume(pid: str):
    pid = str(pid or "").strip()
    if not pid:
        return False, "Missing id"
    before = len(PERFUMES)
    PERFUMES[:] = [x for x in PERFUMES if not (isinstance(x, dict) and x.get("id") == pid)]
    return (len(PERFUMES) < before), (None if len(PERFUMES) < before else "Not found")

def get_all_perfumes():
    return list(PERFUMES)
# -----------------------------------------------------------------------------
