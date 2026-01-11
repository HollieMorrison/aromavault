from __future__ import annotations

import json
import uuid
from pathlib import Path
from typing import Dict, List, Optional

# -------- settings you can tune --------
DEFAULT_DB = Path("data/db.json")
NAME_MAX = 60
BRAND_MAX = 40
NOTE_MAX = 40
MAX_PRICE = 2000.0  # change if you want a different cap
# ---------------------------------------


def _ensure_file():
    DEFAULT_DB.parent.mkdir(parents=True, exist_ok=True)
    if not DEFAULT_DB.exists():
        DEFAULT_DB.write_text("[]", encoding="utf-8")


def _load() -> List[Dict]:
    _ensure_file()
    try:
        return json.loads(DEFAULT_DB.read_text(encoding="utf-8"))
    except Exception:
        return []


def _save(items: List[Dict]) -> None:
    DEFAULT_DB.write_text(json.dumps(items, indent=2, ensure_ascii=False), encoding="utf-8")


def _ci(s: str) -> str:
    return (s or "").strip().casefold()


def _normalize_new(data: Dict) -> Dict:
    """Validate/normalize a perfume for creation (no rating)."""
    name = str(data.get("name", "")).strip()
    brand = str(data.get("brand", "")).strip()
    price = data.get("price", None)
    notes = data.get("notes", [])
    stock = data.get("stock", 0)

    if not name:
        raise ValueError("name is required")
    if len(name) > NAME_MAX:
        raise ValueError(f"name too long (max {NAME_MAX})")

    if not brand:
        raise ValueError("brand is required")
    if len(brand) > BRAND_MAX:
        raise ValueError(f"brand too long (max {BRAND_MAX})")

    try:
        price = float(price)
    except Exception:
        raise ValueError("price must be a number")
    if not (0 <= price <= MAX_PRICE):
        raise ValueError(f"price must be between 0 and {MAX_PRICE}")

    if isinstance(notes, str):
        notes = [s.strip() for s in notes.split(",") if s.strip()]
    if not isinstance(notes, list):
        raise ValueError("notes must be a list (or comma-separated string)")
    notes = [str(n).strip() for n in notes if str(n).strip()]
    for n in notes:
        if len(n) > NOTE_MAX:
            raise ValueError(f"note '{n}' too long (max {NOTE_MAX})")

    try:
        stock = int(stock)
    except Exception:
        raise ValueError("stock must be an integer")
    if stock < 0:
        raise ValueError("stock must be >= 0")

    return {
        "id": str(uuid.uuid4()),
        "name": name,
        "brand": brand,
        "price": price,
        "notes": notes,
        "allergens": data.get("allergens", []),  # kept as-is if present
        "stock": stock,
    }


def list_perfumes(
    brand: Optional[str] = None, name: Optional[str] = None, notes_sub: Optional[str] = None
) -> List[Dict]:
    """List all, or filter with optional substrings (case-insensitive)."""
    items = _load()
    b = _ci(brand) if brand else None
    n = _ci(name) if name else None
    q = _ci(notes_sub) if notes_sub else None

    def match(it: Dict) -> bool:
        if b and b not in _ci(it.get("brand", "")):
            return False
        if n and n not in _ci(it.get("name", "")):
            return False
        if q:
            note_hit = any(q in _ci(x) for x in it.get("notes", []))
            if not note_hit:
                return False
        return True

    if any([b, n, q]):
        return [it for it in items if match(it)]
    return items


def _get_by_id(items: List[Dict], pid: str) -> Optional[Dict]:
    for it in items:
        if it.get("id") == pid:
            return it
    return None


def _get_by_name_ci(items: List[Dict], name: str) -> Optional[Dict]:
    target = _ci(name)
    for it in items:
        if _ci(it.get("name", "")) == target:
            return it
    return None


def get_by_id_or_name(identifier: str) -> Optional[Dict]:
    items = _load()
    hit = _get_by_id(items, identifier)
    if hit:
        return hit
    return _get_by_name_ci(items, identifier)


def add_perfume(data: Dict) -> Dict:
    """Add (name must be unique case-insensitively)."""
    items = _load()
    norm = _normalize_new(data)
    if _get_by_name_ci(items, norm["name"]):
        raise ValueError(f"name '{norm['name']}' already exists")
    items.append(norm)
    _save(items)
    return norm


def delete_perfume(id_or_name: str) -> bool:
    items = _load()
    hit = _get_by_id(items, id_or_name) or _get_by_name_ci(items, id_or_name)
    if not hit:
        return False
    items = [x for x in items if x is not hit]
    _save(items)
    return True


def update_perfume(id_or_name: str, changes: Dict) -> bool:
    """Allowed fields: name, brand, price, notes, stock (no rating)."""
    items = _load()
    hit = _get_by_id(items, id_or_name) or _get_by_name_ci(items, id_or_name)
    if not hit:
        return False

    # validate field-by-field
    if "name" in changes:
        new_name = str(changes["name"]).strip()
        if not new_name:
            raise ValueError("name cannot be empty")
        if len(new_name) > NAME_MAX:
            raise ValueError(f"name too long (max {NAME_MAX})")
        other = _get_by_name_ci(items, new_name)
        if other and other is not hit:
            raise ValueError(f"name '{new_name}' already exists")
        hit["name"] = new_name

    if "brand" in changes:
        brand = str(changes["brand"]).strip()
        if not brand:
            raise ValueError("brand cannot be empty")
        if len(brand) > BRAND_MAX:
            raise ValueError(f"brand too long (max {BRAND_MAX})")
        hit["brand"] = brand

    if "price" in changes:
        try:
            price = float(changes["price"])
        except Exception:
            raise ValueError("price must be a number")
        if not (0 <= price <= MAX_PRICE):
            raise ValueError(f"price must be between 0 and {MAX_PRICE}")
        hit["price"] = price

    if "notes" in changes:
        notes = changes["notes"]
        if isinstance(notes, str):
            notes = [s.strip() for s in notes.split(",") if s.strip()]
        if not isinstance(notes, list):
            raise ValueError("notes must be a list (or comma-separated string)")
        notes = [str(n).strip() for n in notes if str(n).strip()]
        for n in notes:
            if len(n) > NOTE_MAX:
                raise ValueError(f"note '{n}' too long (max {NOTE_MAX})")
        hit["notes"] = notes

    if "stock" in changes:
        try:
            stock = int(changes["stock"])
        except Exception:
            raise ValueError("stock must be an integer")
        if stock < 0:
            raise ValueError("stock must be >= 0")
        hit["stock"] = stock

    _save(items)
    return True
