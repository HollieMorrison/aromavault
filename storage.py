from __future__ import annotations

import json
from pathlib import Path
from typing import Optional


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


def load_all(path: Optional[Path] = None) -> list[dict]:
    """
    Load the entire dataset from JSON.
    """
    return _read_json(path or DEFAULT_DB)


def save_all(items: list[dict], path: Optional[Path] = None) -> None:
    """
    Overwrite the dataset with the provided list of dicts.
    """
    _write_json(path or DEFAULT_DB, items)


def get_by_id(pid: str, path: Optional[Path] = None) -> Optional[dict]:
    """
    Return the perfume dict with matching id, or None if not found.
    """
    items = load_all(path)
    for it in items:
        if str(it.get("id")) == str(pid):
            return it
    return None


def upsert(item: dict, path: Optional[Path] = None) -> dict:
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


def delete(pid: str, path: Optional[Path] = None) -> bool:
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
    query: Optional[str] = None,
    brand: Optional[str] = None,
    notes_any: Optional[list[str]] = None,
    price_max: Optional[float] = None,
    path: Optional[Path] = None,
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

def add_perfume(item: dict, path: Optional[Path] = None) -> dict:
    """Legacy name: insert a perfume (or update if id exists)."""
    return upsert(item, path)

def update_perfume(pid: str, changes: dict, path: Optional[Path] = None) -> dict:
    """Legacy name: update by id with partial changes."""
    existing = get_by_id(pid, path)
    if existing is None:
        raise ValueError(f"Perfume with id '{pid}' not found")
    merged = {**existing, **changes, "id": existing.get("id")}
    return upsert(merged, path)

def delete_perfume(pid: str, path: Optional[Path] = None) -> bool:
    """Legacy name: delete by id."""
    return delete(pid, path)

def get_perfume_by_id(pid: str, path: Optional[Path] = None) -> Optional[dict]:
    """Legacy name: fetch by id."""
    return get_by_id(pid, path)

def list_perfumes(path: Optional[Path] = None) -> list[dict]:
    """Legacy name: list all perfumes."""
    return load_all(path)

def search_perfumes(
    query: Optional[str] = None,
    brand: Optional[str] = None,
    notes_any: Optional[list[str]] = None,
    price_max: Optional[float] = None,
    path: Optional[Path] = None,
) -> list[dict]:
    """Legacy name: search helper."""
    return search(query=query, brand=brand, notes_any=notes_any, price_max=price_max, path=path)
