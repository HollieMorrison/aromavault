from __future__ import annotations

import json
import math
import uuid
from pathlib import Path
from typing import Dict, Iterable, List, Optional

# Single JSON file "DB"
DEFAULT_DB: Path = Path("db.json")

# Soft limits (mentor notes)
MAX_NAME = 80
MAX_BRAND = 80
MAX_NOTE_LEN = 80
MAX_PRICE = 1_000_000.0  # generous upper bound


def _load() -> List[Dict]:
    if not DEFAULT_DB.exists():
        return []
    try:
        return json.loads(DEFAULT_DB.read_text(encoding="utf-8"))
    except Exception:
        return []


def _save(items: Iterable[Dict]) -> None:
    DEFAULT_DB.write_text(json.dumps(list(items), ensure_ascii=False, indent=2), encoding="utf-8")


def _clean(s: str) -> str:
    return " ".join(s.split()).strip()


def _validate_name(name: str) -> str:
    name = _clean(name)
    if not name:
        raise ValueError("name is required")
    if len(name) > MAX_NAME:
        raise ValueError(f"name must be ≤ {MAX_NAME} chars")
    return name


def _validate_brand(brand: str) -> str:
    brand = _clean(brand)
    if not brand:
        raise ValueError("brand is required")
    if len(brand) > MAX_BRAND:
        raise ValueError(f"brand must be ≤ {MAX_BRAND} chars")
    return brand


def _validate_price(price: float) -> float:
    try:
        price = float(price)
    except Exception:
        raise ValueError("price must be a number")
    if not math.isfinite(price) or price < 0 or price > MAX_PRICE:
        raise ValueError(f"price must be between 0 and {MAX_PRICE}")
    return round(price, 2)


def _parse_notes(notes: Optional[Iterable[str] | str]) -> List[str]:
    if notes is None:
        return []
    if isinstance(notes, str):
        parts = [p.strip() for p in notes.split(",")]
    else:
        parts = [str(p).strip() for p in notes]
    cleaned = []
    for p in parts:
        if not p:
            continue
        if len(p) > MAX_NOTE_LEN:
            raise ValueError(f"note too long (>{MAX_NOTE_LEN})")
        cleaned.append(p)
    # keep order; drop dupes while preserving order
    seen = set()
    dedup = []
    for n in cleaned:
        key = n.lower()
        if key not in seen:
            seen.add(key)
            dedup.append(n)
    return dedup


def _find_index(items: List[Dict], id_or_name: str) -> int:
    key = id_or_name.strip()
    # id exact
    for i, it in enumerate(items):
        if it.get("id") == key:
            return i
    # name exact, case-insensitive
    lower = key.lower()
    for i, it in enumerate(items):
        if it.get("name", "").lower() == lower:
            return i
    return -1


def list_perfumes(
    brand_sub: Optional[str] = None,
    notes_sub: Optional[str] = None,
    name_sub: Optional[str] = None,
) -> List[Dict]:
    items = _load()

    def ok(it: Dict) -> bool:
        if brand_sub and brand_sub.lower() not in it.get("brand", "").lower():
            return False
        if name_sub and name_sub.lower() not in it.get("name", "").lower():
            return False
        if notes_sub:
            hay = ",".join(it.get("notes", [])).lower()
            if notes_sub.lower() not in hay:
                return False
        return True

    out = [it for it in items if ok(it)]
    # stable alphabetical by name
    return sorted(out, key=lambda d: d.get("name", "").lower())


def get_one(id_or_name: str) -> Optional[Dict]:
    items = _load()
    idx = _find_index(items, id_or_name)
    return items[idx].copy() if idx >= 0 else None


def add_perfume(data: Dict) -> Dict:
    items = _load()
    name = _validate_name(data.get("name", ""))
    brand = _validate_brand(data.get("brand", ""))
    price = _validate_price(data.get("price", 0))
    notes = _parse_notes(data.get("notes", []))

    # unique name (case-insensitive)
    if any(it.get("name", "").lower() == name.lower() for it in items):
        raise ValueError("name must be unique")

    item = {
        "id": uuid.uuid4().hex,
        "name": name,
        "brand": brand,
        "price": price,
        "notes": notes,
    }
    items.append(item)
    _save(items)
    return item.copy()


def update_perfume(id_or_name: str, changes: Dict) -> bool:
    items = _load()
    idx = _find_index(items, id_or_name)
    if idx < 0:
        return False

    allowed = {"name", "brand", "price", "notes"}
    changes = {k: v for k, v in (changes or {}).items() if k in allowed}
    if not changes:
        return True

    # validate each and apply
    it = items[idx]
    if "name" in changes:
        new = _validate_name(changes["name"])
        if new.lower() != it["name"].lower() and any(
            x.get("name", "").lower() == new.lower() for j, x in enumerate(items) if j != idx
        ):
            raise ValueError("name must be unique")
        it["name"] = new
    if "brand" in changes:
        it["brand"] = _validate_brand(changes["brand"])
    if "price" in changes:
        it["price"] = _validate_price(changes["price"])
    if "notes" in changes:
        it["notes"] = _parse_notes(changes["notes"])

    _save(items)
    return True


def delete_perfume(id_or_name: str) -> bool:
    items = _load()
    idx = _find_index(items, id_or_name)
    if idx < 0:
        return False
    items.pop(idx)
    _save(items)
    return True
