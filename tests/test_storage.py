import json
from pathlib import Path
from storage import JSONStorage  # adjust to your API


def test_crud_roundtrip(tmp_path: Path):
    db_path = tmp_path / "data.json"
    store = JSONStorage(db_path)

    # Create
    item = {"id": "p1", "name": "Citrus Test", "brand": "Demo", "notes": ["citrus"]}
    store.save_item(item)
    assert store.get_item("p1")["name"] == "Citrus Test"

    # Update
    store.update_item("p1", {"brand": "DemoX"})
    assert store.get_item("p1")["brand"] == "DemoX"

    # Delete
    store.delete_item("p1")
    assert store.get_item("p1") is None
