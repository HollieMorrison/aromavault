import pytest
from validators import non_empty_str, positive_float_or_none, non_empty_list_str

def test_non_empty_str_ok():
    assert non_empty_str("  hi  ", "field") == "hi"

def test_non_empty_str_fail():
    with pytest.raises(ValueError):
        non_empty_str("   ", "field")

def test_positive_float_ok():
    assert positive_float_or_none("12.5", "price") == 12.5

def test_positive_float_fail():
    with pytest.raises(ValueError):
        positive_float_or_none("-1", "price")

def test_list_normalization():
    assert non_empty_list_str(["  a ", "", "b "]) == ["a","b"]
