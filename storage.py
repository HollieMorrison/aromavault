from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List

# Test suite monkeypatches this, so keep the name and type.
DEFAULT_DB: Path = Path("db.json")


def _load(path: Path | None = None) -> List[Dict[str, Any]]:
    p = path or DEFAULT_DB
    if not p.exists():
        return []
    try:
        with p.open("r", encoding="utf-8") as f:
            data = json.load(f)
        if isinstance(data, list):
            return data
        return []
    except Exception:
        return []


def _save(items: List[Dict[str, Any]], path: Path | None = None) -> None:
    p = path or DEFAULT_DB
    p.parent.mkdir(parents=True, exist_ok=True)
    with p.open("w", encoding="utf-8") as f:
        json.dump(items, f, ensure_ascii=False, indent=2)


def list_perfumes() -> List[Dict[str, Any]]:
    return _load()


def add_perfume(item: Dict[str, Any]) -> Dict[str, Any]:
    items = _load()
    # Ensure required fields with reasonable defaults
    out = {
        "id": item.get("id") or item.get("name") or "",
        "name": item.get("name", ""),
        "brand": item.get("brand", ""),
        "price": float(item.get("price", 0.0)),
        "notes": list(item.get("notes", [])),
        "allergens": list(item.get("allergens", [])),
        "rating": float(item.get("rating", 0.0)),
        "stock": int(item.get("stock", 0)),
    }
    # If id still empty, derive a simple one
    if not out["id"]:
        from uuid import uuid4

        out["id"] = str(uuid4())
    items.append(out)
    _save(items)
    return out


def update_perfume(perfume_id: str, changes: Dict[str, Any]) -> bool:
    items = _load()
    found = False
    for i, it in enumerate(items):
        if it.get("id") == perfume_id:
            it.update(changes or {})
            # Normalize types on updates
            if "price" in it:
                it["price"] = float(it["price"])
            if "rating" in it:
                it["rating"] = float(it["rating"])
            if "stock" in it:
                it["stock"] = int(it["stock"])
            if "notes" in it and not isinstance(it["notes"], list):
                it["notes"] = [
                    str(x).strip() for x in str(it["notes"]).split(",") if str(x).strip()
                ]
            if "allergens" in it and not isinstance(it["allergens"], list):
                it["allergens"] = [
                    str(x).strip() for x in str(it["allergens"]).split(",") if str(x).strip()
                ]
            items[i] = it
            found = True
            break
    if found:
        _save(items)
    return found


def delete_perfume(perfume_id: str) -> bool:
    items = _load()
    new_items = [it for it in items if it.get("id") != perfume_id]
    changed = len(new_items) != len(items)
    if changed:
        _save(new_items)
    return changed


def seed_minimal() -> int:
    """Write a tiny seed set to the current DEFAULT_DB. Overwrites existing content."""
    samples = [
        {
            "id": "seed-rose-dusk",
            "name": "Rose Dusk",
            "brand": "Floral",
            "price": 55.0,
            "notes": ["rose", "musk"],
            "allergens": [],
            "rating": 4.2,
            "stock": 5,
        },
        {
            "id": "seed-citrus-day",
            "name": "Citrus Day",
            "brand": "FreshCo",
            "price": 42.0,
            "notes": ["lemon", "neroli"],
            "allergens": [],
            "rating": 4.0,
            "stock": 8,
        },
        {
            "id": "seed-night-bloom-xl",
            "name": "Night Bloom XL",
            "brand": "Nocturne",
            "price": 65.0,
            "notes": ["jasmine", "amber", "musk"],
            "allergens": ["coumarin"],
            "rating": 4.4,
            "stock": 7,
        },
    ]
    _save(samples)
    return len(samples)


# Helper used by web API (/api/admin/add)
def add_or_update_perfume(item: Dict[str, Any]) -> tuple[bool, str | None]:
    """Idempotent upsert by 'id'."""
    pid = item.get("id")
    if not pid:
        return False, "Missing id"
    items = _load()
    for i, it in enumerate(items):
        if it.get("id") == pid:
            items[i] = {**it, **item}
            # normalize
            items[i]["price"] = float(items[i].get("price", 0.0))
            items[i]["rating"] = float(items[i].get("rating", 0.0))
            items[i]["stock"] = int(items[i].get("stock", 0))
            if "notes" in items[i] and not isinstance(items[i]["notes"], list):
                items[i]["notes"] = [
                    s.strip() for s in str(items[i]["notes"]).split(",") if s.strip()
                ]
            if "allergens" in items[i] and not isinstance(items[i]["allergens"], list):
                items[i]["allergens"] = [
                    s.strip() for s in str(items[i]["allergens"]).split(",") if s.strip()
                ]
            _save(items)
            return True, None
    # not found -> add
    add_perfume(item)
    return True, None


# === BEGIN: test-friendly JSON storage helpers (idempotent) =================
import json
from dataclasses import asdict
from pathlib import Path


def _db_path():
    # DEFAULT_DB is already defined in this module; fall back to db.json
    return str(globals().get("DEFAULT_DB", Path("db.json")))


def _read_all():
    path = _db_path()
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
            if isinstance(data, list):
                return data
    except FileNotFoundError:
        pass
    return []


def _write_all(items):
    path = _db_path()
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(items, f, ensure_ascii=False, indent=2)


def list_perfumes():
    """Return list of dicts from the JSON DB."""
    return _read_all()


def add_perfume(item: dict):
    """Append item and persist."""
    items = _read_all()
    items.append(item)
    _write_all(items)
    return item


def update_perfume(perfume_id: str, changes: dict):
    """Update item by id; return True if found."""
    items = _read_all()
    updated = False
    for it in items:
        if it.get("id") == perfume_id:
            it.update(changes)
            updated = True
            break
    if updated:
        _write_all(items)
    return updated


def delete_perfume(perfume_id: str):
    """Delete item by id; return True if something was removed."""
    items = _read_all()
    new_items = [it for it in items if it.get("id") != perfume_id]
    removed = len(new_items) != len(items)
    if removed:
        _write_all(new_items)
    return removed


# === END: test-friendly JSON storage helpers =================================

# ---- simple JSON storage helpers -------------------------------------------
try:
    DEFAULT_DB
except NameError:
    DEFAULT_DB = Path("db.json")


def _load_db():
    try:
        data = json.loads(Path(DEFAULT_DB).read_text(encoding="utf-8"))
        if isinstance(data, list):
            return data
        return []
    except FileNotFoundError:
        return []
    except Exception:
        return []


def _save_db(items):
    Path(DEFAULT_DB).write_text(json.dumps(items, ensure_ascii=False, indent=2), encoding="utf-8")


def list_perfumes():
    return _load_db()


def add_perfume(item):
    items = _load_db()
    items.append(item)
    _save_db(items)
    return item


def update_perfume(pid, patch):
    items = _load_db()
    ok = False
    for it in items:
        if it.get("id") == pid or it.get("name") == pid:
            it.update(patch)
            ok = True
            break
    if ok:
        _save_db(items)
    return ok


def delete_perfume(pid):
    items = _load_db()
    new = [it for it in items if it.get("id") != pid and it.get("name") != pid]
    changed = len(new) != len(items)
    if changed:
        _save_db(new)
    return changed


def seed_minimal() -> int:
    items = [
        {
            "name": "Citrus Aurora",
            "brand": "Sole",
            "price": 48.0,
            "notes": ["bergamot", "lemon", "neroli"],
            "allergens": [],
            "rating": 0.0,
            "stock": 0,
        },
        {
            "name": "Rose Dusk",
            "brand": "Floral",
            "price": 55.0,
            "notes": ["rose", "musk"],
            "allergens": [],
            "rating": 0.0,
            "stock": 0,
        },
        {
            "name": "Vetiver Line",
            "brand": "Terra",
            "price": 67.0,
            "notes": ["vetiver", "grapefruit", "pepper"],
            "allergens": [],
            "rating": 0.0,
            "stock": 0,
        },
    ]
    _save_db(items)
    return 3

# ---- minimal JSON storage helpers used by CLI/tests ----
from pathlib import Path
import json
from typing import Any, Dict, List

try:
    DEFAULT_DB
except NameError:
    DEFAULT_DB = Path("db.json")

def _load() -> List[Dict[str, Any]]:
    try:
        data = json.loads(Path(DEFAULT_DB).read_text(encoding="utf-8"))
        return data if isinstance(data, list) else []
    except FileNotFoundError:
        return []
    except Exception:
        return []

def _save(items: List[Dict[str, Any]]) -> None:
    Path(DEFAULT_DB).write_text(json.dumps(items, ensure_ascii=False, indent=2), encoding="utf-8")

def list_perfumes() -> List[Dict[str, Any]]:
    return _load()

def add_perfume(item: Dict[str, Any]) -> Dict[str, Any]:
    items = _load()
    # assign an id if not present
    if "id" not in item or not item["id"]:
        import uuid
        item["id"] = str(uuid.uuid4())
    items.append(item)
    _save(items)
    return item

def update_perfume(pid: str, patch: Dict[str, Any]) -> bool:
    items = _load()
    ok = False
    for it in items:
        if it.get("id") == pid or it.get("name") == pid:
            it.update(patch); ok = True; break
    if ok: _save(items)
    return ok

def delete_perfume(pid: str) -> bool:
    items = _load()
    new = [it for it in items if it.get("id") != pid and it.get("name") != pid]
    changed = len(new) != len(items)
    if changed: _save(new)
    return changed

def seed_minimal() -> int:
    items = [
        {"name":"Citrus Aurora","brand":"Sole","price":48.0,"notes":["bergamot","lemon","neroli"],"allergens":[],"rating":0.0,"stock":0},
        {"name":"Rose Dusk","brand":"Floral","price":55.0,"notes":["rose","musk"],"allergens":[],"rating":0.0,"stock":0},
        {"name":"Vetiver Line","brand":"Terra","price":67.0,"notes":["vetiver","grapefruit","pepper"],"allergens":[],"rating":0.0,"stock":0},
    ]
    _save(items)
    return 3
