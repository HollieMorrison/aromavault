import json
from pathlib import Path
import importlib

storage = importlib.import_module("storage")
recommender = importlib.import_module("recommender")


def test_storage_crud_roundtrip(tmp_path: Path):
    db = tmp_path / "mini.json"
    # Start empty
    assert storage.load_all(db) == []

    # Upsert one item
    item = {"id": "p1", "name": "Citrus Splash", "brand": "Demo", "notes": ["citrus", "fresh"], "price": 45.0}
    storage.upsert(item, db)

    # Read it back
    items = storage.load_all(db)
    assert len(items) == 1
    assert items[0]["id"] == "p1"

    # Update
    storage.upsert({"id": "p1", "price": 40.0}, db)
    updated = storage.get_by_id("p1", db)
    assert updated and updated["price"] == 40.0

    # Search by note and price
    results = storage.search(notes_any=["citrus"], price_max=50, path=db)
    assert results and results[0]["id"] == "p1"

    # Delete
    assert storage.delete("p1", db) is True
    assert storage.load_all(db) == []


def test_recommender_basic():
    catalog = [
        {"id": "a", "name": "Green Leaf", "brand": "BrandA", "notes": ["green", "herbal"], "price": 70},
        {"id": "b", "name": "Citrus Pop", "brand": "BrandB", "notes": ["citrus", "fresh"], "price": 40},
        {"id": "c", "name": "Vanilla Dream", "brand": "BrandC", "notes": ["vanilla", "sweet"], "price": 60},
    ]
    top = recommender.recommend(
        catalog,
        preferred_notes=["citrus", "fresh"],
        avoid_notes=["smoky"],
        brand_bias="BrandB",
        price_max=50,
        k=1,
    )
    assert len(top) == 1
    assert top[0]["id"] == "b"
