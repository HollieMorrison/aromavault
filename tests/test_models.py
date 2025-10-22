from models import Perfume, UserProfile


def test_perfume_factory_normalises():
    p = Perfume.new("  Rose Dusk ", " Floral ", 55, [" rose ", "musk", ""], ["  "])
    assert p.name == "Rose Dusk"
    assert p.brand == "Floral"
    assert p.notes == ["rose", "musk"]
    assert p.allergens == []
    assert isinstance(p.id, str)


def test_userprofile_factory_normalises():
    u = UserProfile.new(" Hollie ", [" Rose "], ["  none  "])
    assert u.name == "Hollie"
    assert u.preferred_notes == ["rose"]
    assert u.avoid_allergens == ["none"]
