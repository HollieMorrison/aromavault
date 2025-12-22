from typing import Iterable

def non_empty_str(value: str, field: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{field} must be a non-empty string.")
    return value.strip()

def positive_float_or_none(value, field: str):
    if value is None:
        return None
    try:
        v = float(value)
    except Exception:
        raise ValueError(f"{field} must be a number.")
    if v < 0:
        raise ValueError(f"{field} must be >= 0.")
    return v

def non_empty_list_str(values: Iterable[str] | None) -> list[str]:
    if not values:
        return []
    out = [v.strip() for v in values if isinstance(v, str) and v.strip()]
    return out
