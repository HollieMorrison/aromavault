from __future__ import annotations
from pathlib import Path
import json, uuid
from typing import Any, Dict, List, Optional

# Test/CI monkeypatches this path sometimes; keep the name.
DEFAULT_DB = Path("db.json")

def _load_db() -> List[Dict[str, Any]]:
    try:
        data = json.loads(DEFAULT_DB.read_text(encoding="utf-8"))
        return data if isinstance(data, list) else []
    except FileNotFoundError:
        return []
    except Exception:
        return []

def _save_db(items: List[Dict[str, Any]]) -> None:
    DEFAULT_DB.write_text(json.dumps(items, ensure_ascii=False, indent=2), encoding="utf-8")

def list_perfumes() -> List[Dict[str, Any]]:
    return _load_db()

def get_perfume(pid: str) -> Optional[Dict[str, Any]]:
    for it in _load_db():
        if it.get("id") == pid or it.get("name") == pid:
            return it
    return None

def add_perfume(item: Dict[str, Any]) -> Dict[str, Any]:
    items = _load_db()
    if not item.get("id"):
        item["id"] = str(uuid.uuid4())
    items.append(item)
    _save_db(items)
    return item

def update_perfume(pid: str, patch: Dict[str, Any]) -> bool:
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

def delete_perfume(pid: str) -> bool:
    items = _load_db()
    new_items = [it for it in items if it.get("id") != pid and it.get("name") != pid]
    changed = len(new_items) != len(items)
    if changed:
        _save_db(new_items)
    return changed

def seed_minimal() -> int:
    items = [
        {"id": str(uuid.uuid4()), "name": "Citrus Aurora", "brand": "Sole", "price": 48.0, "notes": ["bergamot","lemon","neroli"], "allergens": [], "rating": 0.0, "stock": 0},
        {"id": str(uuid.uuid4()), "name": "Rose Dusk",     "brand": "Floral", "price": 55.0, "notes": ["rose","musk"],               "allergens": [], "rating": 0.0, "stock": 0},
        {"id": str(uuid.uuid4()), "name": "Vetiver Line",  "brand": "Terra",  "price": 67.0, "notes": ["vetiver","grapefruit","pepper"], "allergens": [], "rating": 0.0, "stock": 0},
    ]
    _save_db(items)
    return len(items)

def seed_30() -> int:
    brands = ["Floral","Terra","Sole","Urban","Aqua","Noir"]
    base_notes = [
        ["rose","musk"], ["vetiver","grapefruit"], ["bergamot","lemon"],
        ["amber","vanilla"], ["cedar","sage"], ["jasmine","pear"]
    ]
    items: List[Dict[str, Any]] = []
    for i in range(30):
        name = f"Scent {i+1:02d}"
        brand = brands[i % len(brands)]
        notes = base_notes[i % len(base_notes)]
        price = round(35.0 + (i % 10) * 3 + (i // 10) * 2, 2)
        items.append({
            "id": str(uuid.uuid4()),
            "name": name,
            "brand": brand,
            "price": price,
            "notes": notes,
            "allergens": [],
            "rating": 0.0,
            "stock": 0,
        })
    _save_db(items)
    return len(items)

def seed_30() -> int:
    items = [
        {"name":"Citrus Aurora","brand":"Sole","price":48.0,"notes":["bergamot","lemon","neroli"],"allergens":[],"rating":4.2,"stock":5},
        {"name":"Rose Dusk","brand":"Floral","price":55.0,"notes":["rose","musk"],"allergens":[],"rating":4.5,"stock":3},
        {"name":"Vetiver Line","brand":"Terra","price":67.0,"notes":["vetiver","grapefruit","pepper"],"allergens":[],"rating":4.3,"stock":2},
        {"name":"Amber Trail","brand":"Nocturne","price":72.0,"notes":["amber","vanilla","tonka"],"allergens":[],"rating":4.6,"stock":4},
        {"name":"Ocean Mist","brand":"Aqua","price":49.0,"notes":["marine","citrus","salt"],"allergens":[],"rating":4.0,"stock":6},
        {"name":"Sandal Shadow","brand":"Woods","price":60.0,"notes":["sandalwood","spice"],"allergens":[],"rating":4.1,"stock":1},
        {"name":"Lavender Field","brand":"Herba","price":44.0,"notes":["lavender","herbs"],"allergens":[],"rating":4.0,"stock":7},
        {"name":"Jasmine Night","brand":"Floral","price":58.0,"notes":["jasmine","white musk"],"allergens":[],"rating":4.4,"stock":3},
        {"name":"Cedar Smoke","brand":"Woods","price":63.0,"notes":["cedar","incense"],"allergens":[],"rating":4.2,"stock":2},
        {"name":"Vanilla Sky","brand":"Nocturne","price":52.0,"notes":["vanilla","amber"],"allergens":[],"rating":4.3,"stock":5},
        {"name":"Musk Noon","brand":"Sole","price":46.0,"notes":["musk","citrus"],"allergens":[],"rating":3.9,"stock":6},
        {"name":"Patchouli Drift","brand":"Terra","price":61.0,"notes":["patchouli","woods"],"allergens":[],"rating":4.1,"stock":2},
        {"name":"Bergamot Bloom","brand":"Citrus Co.","price":45.0,"notes":["bergamot"],"allergens":[],"rating":4.0,"stock":8},
        {"name":"Neroli Sun","brand":"Citrus Co.","price":50.0,"notes":["neroli","orange blossom"],"allergens":[],"rating":4.2,"stock":5},
        {"name":"Grapefruit Peel","brand":"Citrus Co.","price":43.0,"notes":["grapefruit","bitter citrus"],"allergens":[],"rating":3.8,"stock":9},
        {"name":"Pepper Noir","brand":"Spice Co.","price":59.0,"notes":["black pepper","woods"],"allergens":[],"rating":4.0,"stock":3},
        {"name":"Oud Mirage","brand":"Nocturne","price":95.0,"notes":["oud","saffron","rose"],"allergens":[],"rating":4.7,"stock":1},
        {"name":"Tea Garden","brand":"Herba","price":48.0,"notes":["green tea","jasmine"],"allergens":[],"rating":4.1,"stock":4},
        {"name":"Leather Bound","brand":"Terra","price":70.0,"notes":["leather","smoke"],"allergens":[],"rating":4.3,"stock":2},
        {"name":"Iris Veil","brand":"Floral","price":68.0,"notes":["iris","powder"],"allergens":[],"rating":4.4,"stock":2},
        {"name":"Fig Grove","brand":"Herba","price":57.0,"notes":["fig","green"],"allergens":[],"rating":4.2,"stock":3},
        {"name":"Apple Spice","brand":"Spice Co.","price":41.0,"notes":["apple","cinnamon"],"allergens":[],"rating":3.9,"stock":6},
        {"name":"Pear Drop","brand":"Sole","price":39.0,"notes":["pear","musk"],"allergens":[],"rating":3.8,"stock":7},
        {"name":"Cocoa Ember","brand":"Nocturne","price":64.0,"notes":["cacao","amber"],"allergens":[],"rating":4.3,"stock":2},
        {"name":"Tobacco Leaf","brand":"Terra","price":66.0,"notes":["tobacco","honey"],"allergens":[],"rating":4.2,"stock":2},
        {"name":"Pine Needle","brand":"Woods","price":53.0,"notes":["pine","resin"],"allergens":[],"rating":3.9,"stock":5},
        {"name":"Marine Blue","brand":"Aqua","price":51.0,"notes":["ozone","sea salt"],"allergens":[],"rating":4.0,"stock":6},
        {"name":"Cherry Blossom","brand":"Floral","price":56.0,"notes":["sakura","musk"],"allergens":[],"rating":4.1,"stock":4},
        {"name":"Lime Zest","brand":"Citrus Co.","price":42.0,"notes":["lime","ginger"],"allergens":[],"rating":3.8,"stock":9},
        {"name":"Mint Breeze","brand":"Herba","price":40.0,"notes":["mint","herbal"],"allergens":[],"rating":3.9,"stock":7},
    ]
    try:
        # Use same private helpers if present
        _save_db(items)  # type: ignore[name-defined]
        return len(items)
    except NameError:
        # Fallback if helpers were renamed (very unlikely here)
        from pathlib import Path, json as _json
        Path("db.json").write_text(_json.dumps(items, ensure_ascii=False, indent=2), encoding="utf-8")
        return len(items)

def seed_30() -> int:
    items = [
        {"name":"Citrus Aurora","brand":"Sole","price":48.0,"notes":["bergamot","lemon","neroli"],"allergens":[],"rating":4.2,"stock":5},
        {"name":"Rose Dusk","brand":"Floral","price":55.0,"notes":["rose","musk"],"allergens":[],"rating":4.5,"stock":3},
        {"name":"Vetiver Line","brand":"Terra","price":67.0,"notes":["vetiver","grapefruit","pepper"],"allergens":[],"rating":4.3,"stock":2},
        {"name":"Amber Trail","brand":"Nocturne","price":72.0,"notes":["amber","vanilla","tonka"],"allergens":[],"rating":4.6,"stock":4},
        {"name":"Ocean Mist","brand":"Aqua","price":49.0,"notes":["marine","citrus","salt"],"allergens":[],"rating":4.0,"stock":6},
        {"name":"Sandal Shadow","brand":"Woods","price":60.0,"notes":["sandalwood","spice"],"allergens":[],"rating":4.1,"stock":1},
        {"name":"Lavender Field","brand":"Herba","price":44.0,"notes":["lavender","herbs"],"allergens":[],"rating":4.0,"stock":7},
        {"name":"Jasmine Night","brand":"Floral","price":58.0,"notes":["jasmine","white musk"],"allergens":[],"rating":4.4,"stock":3},
        {"name":"Cedar Smoke","brand":"Woods","price":63.0,"notes":["cedar","incense"],"allergens":[],"rating":4.2,"stock":2},
        {"name":"Vanilla Sky","brand":"Nocturne","price":52.0,"notes":["vanilla","amber"],"allergens":[],"rating":4.3,"stock":5},
        {"name":"Musk Noon","brand":"Sole","price":46.0,"notes":["musk","citrus"],"allergens":[],"rating":3.9,"stock":6},
        {"name":"Patchouli Drift","brand":"Terra","price":61.0,"notes":["patchouli","woods"],"allergens":[],"rating":4.1,"stock":2},
        {"name":"Bergamot Bloom","brand":"Citrus Co.","price":45.0,"notes":["bergamot"],"allergens":[],"rating":4.0,"stock":8},
        {"name":"Neroli Sun","brand":"Citrus Co.","price":50.0,"notes":["neroli","orange blossom"],"allergens":[],"rating":4.2,"stock":5},
        {"name":"Grapefruit Peel","brand":"Citrus Co.","price":43.0,"notes":["grapefruit","bitter citrus"],"allergens":[],"rating":3.8,"stock":9},
        {"name":"Pepper Noir","brand":"Spice Co.","price":59.0,"notes":["black pepper","woods"],"allergens":[],"rating":4.0,"stock":3},
        {"name":"Oud Mirage","brand":"Nocturne","price":95.0,"notes":["oud","saffron","rose"],"allergens":[],"rating":4.7,"stock":1},
        {"name":"Tea Garden","brand":"Herba","price":48.0,"notes":["green tea","jasmine"],"allergens":[],"rating":4.1,"stock":4},
        {"name":"Leather Bound","brand":"Terra","price":70.0,"notes":["leather","smoke"],"allergens":[],"rating":4.3,"stock":2},
        {"name":"Iris Veil","brand":"Floral","price":68.0,"notes":["iris","powder"],"allergens":[],"rating":4.4,"stock":2},
        {"name":"Fig Grove","brand":"Herba","price":57.0,"notes":["fig","green"],"allergens":[],"rating":4.2,"stock":3},
        {"name":"Apple Spice","brand":"Spice Co.","price":41.0,"notes":["apple","cinnamon"],"allergens":[],"rating":3.9,"stock":6},
        {"name":"Pear Drop","brand":"Sole","price":39.0,"notes":["pear","musk"],"allergens":[],"rating":3.8,"stock":7},
        {"name":"Cocoa Ember","brand":"Nocturne","price":64.0,"notes":["cacao","amber"],"allergens":[],"rating":4.3,"stock":2},
        {"name":"Tobacco Leaf","brand":"Terra","price":66.0,"notes":["tobacco","honey"],"allergens":[],"rating":4.2,"stock":2},
        {"name":"Pine Needle","brand":"Woods","price":53.0,"notes":["pine","resin"],"allergens":[],"rating":3.9,"stock":5},
        {"name":"Marine Blue","brand":"Aqua","price":51.0,"notes":["ozone","sea salt"],"allergens":[],"rating":4.0,"stock":6},
        {"name":"Cherry Blossom","brand":"Floral","price":56.0,"notes":["sakura","musk"],"allergens":[],"rating":4.1,"stock":4},
        {"name":"Lime Zest","brand":"Citrus Co.","price":42.0,"notes":["lime","ginger"],"allergens":[],"rating":3.8,"stock":9},
        {"name":"Mint Breeze","brand":"Herba","price":40.0,"notes":["mint","herbal"],"allergens":[],"rating":3.9,"stock":7},
    ]
    try:
        # Use same private helpers if present
        _save_db(items)  # type: ignore[name-defined]
        return len(items)
    except NameError:
        # Fallback if helpers were renamed (very unlikely here)
        from pathlib import Path, json as _json
        Path("db.json").write_text(_json.dumps(items, ensure_ascii=False, indent=2), encoding="utf-8")
        return len(items)

def seed_30() -> int:
    items = [
        {"name":"Citrus Aurora","brand":"Sole","price":48.0,"notes":["bergamot","lemon","neroli"],"allergens":[],"rating":4.2,"stock":5},
        {"name":"Rose Dusk","brand":"Floral","price":55.0,"notes":["rose","musk"],"allergens":[],"rating":4.5,"stock":3},
        {"name":"Vetiver Line","brand":"Terra","price":67.0,"notes":["vetiver","grapefruit","pepper"],"allergens":[],"rating":4.3,"stock":2},
        {"name":"Amber Trail","brand":"Nocturne","price":72.0,"notes":["amber","vanilla","tonka"],"allergens":[],"rating":4.6,"stock":4},
        {"name":"Ocean Mist","brand":"Aqua","price":49.0,"notes":["marine","citrus","salt"],"allergens":[],"rating":4.0,"stock":6},
        {"name":"Sandal Shadow","brand":"Woods","price":60.0,"notes":["sandalwood","spice"],"allergens":[],"rating":4.1,"stock":1},
        {"name":"Lavender Field","brand":"Herba","price":44.0,"notes":["lavender","herbs"],"allergens":[],"rating":4.0,"stock":7},
        {"name":"Jasmine Night","brand":"Floral","price":58.0,"notes":["jasmine","white musk"],"allergens":[],"rating":4.4,"stock":3},
        {"name":"Cedar Smoke","brand":"Woods","price":63.0,"notes":["cedar","incense"],"allergens":[],"rating":4.2,"stock":2},
        {"name":"Vanilla Sky","brand":"Nocturne","price":52.0,"notes":["vanilla","amber"],"allergens":[],"rating":4.3,"stock":5},
        {"name":"Musk Noon","brand":"Sole","price":46.0,"notes":["musk","citrus"],"allergens":[],"rating":3.9,"stock":6},
        {"name":"Patchouli Drift","brand":"Terra","price":61.0,"notes":["patchouli","woods"],"allergens":[],"rating":4.1,"stock":2},
        {"name":"Bergamot Bloom","brand":"Citrus Co.","price":45.0,"notes":["bergamot"],"allergens":[],"rating":4.0,"stock":8},
        {"name":"Neroli Sun","brand":"Citrus Co.","price":50.0,"notes":["neroli","orange blossom"],"allergens":[],"rating":4.2,"stock":5},
        {"name":"Grapefruit Peel","brand":"Citrus Co.","price":43.0,"notes":["grapefruit","bitter citrus"],"allergens":[],"rating":3.8,"stock":9},
        {"name":"Pepper Noir","brand":"Spice Co.","price":59.0,"notes":["black pepper","woods"],"allergens":[],"rating":4.0,"stock":3},
        {"name":"Oud Mirage","brand":"Nocturne","price":95.0,"notes":["oud","saffron","rose"],"allergens":[],"rating":4.7,"stock":1},
        {"name":"Tea Garden","brand":"Herba","price":48.0,"notes":["green tea","jasmine"],"allergens":[],"rating":4.1,"stock":4},
        {"name":"Leather Bound","brand":"Terra","price":70.0,"notes":["leather","smoke"],"allergens":[],"rating":4.3,"stock":2},
        {"name":"Iris Veil","brand":"Floral","price":68.0,"notes":["iris","powder"],"allergens":[],"rating":4.4,"stock":2},
        {"name":"Fig Grove","brand":"Herba","price":57.0,"notes":["fig","green"],"allergens":[],"rating":4.2,"stock":3},
        {"name":"Apple Spice","brand":"Spice Co.","price":41.0,"notes":["apple","cinnamon"],"allergens":[],"rating":3.9,"stock":6},
        {"name":"Pear Drop","brand":"Sole","price":39.0,"notes":["pear","musk"],"allergens":[],"rating":3.8,"stock":7},
        {"name":"Cocoa Ember","brand":"Nocturne","price":64.0,"notes":["cacao","amber"],"allergens":[],"rating":4.3,"stock":2},
        {"name":"Tobacco Leaf","brand":"Terra","price":66.0,"notes":["tobacco","honey"],"allergens":[],"rating":4.2,"stock":2},
        {"name":"Pine Needle","brand":"Woods","price":53.0,"notes":["pine","resin"],"allergens":[],"rating":3.9,"stock":5},
        {"name":"Marine Blue","brand":"Aqua","price":51.0,"notes":["ozone","sea salt"],"allergens":[],"rating":4.0,"stock":6},
        {"name":"Cherry Blossom","brand":"Floral","price":56.0,"notes":["sakura","musk"],"allergens":[],"rating":4.1,"stock":4},
        {"name":"Lime Zest","brand":"Citrus Co.","price":42.0,"notes":["lime","ginger"],"allergens":[],"rating":3.8,"stock":9},
        {"name":"Mint Breeze","brand":"Herba","price":40.0,"notes":["mint","herbal"],"allergens":[],"rating":3.9,"stock":7},
    ]
    try:
        _save_db(items)  # uses your existing helper
        return len(items)
    except NameError:
        from pathlib import Path as _P, json as _J
        _P("db.json").write_text(_J.dumps(items, ensure_ascii=False, indent=2), encoding="utf-8")
        return len(items)
