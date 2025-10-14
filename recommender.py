from __future__ import annotations

from typing import Optional


def _norm_set(values: Optional[list[str]]) -> set[str]:
    if not values:
        return set()
    return {str(v).casefold().strip() for v in values if isinstance(v, str) and v.strip()}


def score_perfume(
    perfume: dict,
    preferred_notes: Optional[list[str]] = None,
    avoid_notes: Optional[list[str]] = None,
    brand_bias: Optional[str] = None,
    price_max: Optional[float] = None,
) -> float:
    """
    Return a relevance score for a single perfume.

    Heuristic:
      +2 per matching preferred note
      -2 per matching avoided note
      +1 if brand matches preferred brand
      Small bonus if price <= price_max (scaled)
    """
    notes = _norm_set(perfume.get("notes"))
    prefs = _norm_set(preferred_notes)
    avoid = _norm_set(avoid_notes)
    score = 0.0

    # Preferred notes
    score += 2.0 * len(notes.intersection(prefs))

    # Avoid notes
    score -= 2.0 * len(notes.intersection(avoid))

    # Brand bias
    if brand_bias:
        if str(perfume.get("brand", "")).casefold().strip() == brand_bias.casefold().strip():
            score += 1.0

    # Price consideration
    if price_max is not None:
        try:
            price = float(perfume.get("price"))
            # If within budget, add a small bonus that grows as price is lower than max
            if price <= float(price_max):
                # e.g., price_max 100, price 80 -> (100-80)/100 = 0.2
                score += max(0.0, (float(price_max) - price) / max(1.0, float(price_max)))
            else:
                # over budget slightly penalized
                score -= 0.5
        except (TypeError, ValueError):
            pass

    return score


def recommend(
    catalog: list[dict],
    preferred_notes: Optional[list[str]] = None,
    avoid_notes: Optional[list[str]] = None,
    brand_bias: Optional[str] = None,
    price_max: Optional[float] = None,
    k: int = 5,
) -> list[dict]:
    """
    Rank perfumes in `catalog` by a simple heuristic score and return top-k.
    """
    ranked = sorted(
        catalog,
        key=lambda p: score_perfume(
            p,
            preferred_notes=preferred_notes,
            avoid_notes=avoid_notes,
            brand_bias=brand_bias,
            price_max=price_max,
        ),
        reverse=True,
    )
    return ranked[: max(1, int(k))]
