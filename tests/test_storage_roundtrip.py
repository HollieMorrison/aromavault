from dataclasses import asdict
from models import Perfume
import storage


def test_add_list_update_delete_roundtrip(tmp_path, monkeypatch):
    # point DB to a temp file (no real data touched)
    monkeypatch.setattr(storage, "DEFAULT_DB", tmp_path / "db.json")

    # add
    p = Perfume.new("Test Scent", "BrandX", 12.5, ["citrus"], [], rating=4.0, stock=3)
    stored = storage.add_perfume(asdict(p))
    assert stored["name"] == "Test Scent"
    assert len(storage.list_perfumes()) == 1

    # update
    ok = storage.update_perfume(stored["id"], {"price": 15.0, "stock": 5})
    assert ok
    updated = storage.list_perfumes()[0]
    assert updated["price"] == 15.0 and updated["stock"] == 5

    # delete
    assert storage.delete_perfume(stored["id"])
    assert storage.list_perfumes() == []
