from typing import list, dict, tuple

# Basic set-based similarities between notes.
# Jaccard = |intersection| / |union|
# Returns 0..1 where 1 means identical sets.


def jaccard(a: list[str], b: list[str]) -> float:
    (
        sa,
        sb,
    ) = set(
        a
    ), set(b)
    if not sa and not sb:
        return 0.0
    inter = sa & sb
    union = sa | sb
    return len(inter) / len(union)


# compute a recommendation score for a single perfume depending on users choices.
# Score = similarity(preferred_notes, perfume.notes) - penalty if the perfume has avoided allergies.


def score_perfume(perfume: dict, preferred: list[str], avoid_allergens: list[str]) -> float:
    base = jaccard([n.lower() for n in preferred], [n.lower() for n in perfume.get("notes", [])])
    penalty = (
        0.5 if set(a.lower() for a in perfume.get("allergens", [])) & set(a.lower() for a in avoid_allergens) else 0.0
    )
    return max(0.0, base - penalty)


def recommend(
    perfumes: list[dict], preferred: list[str], avoid_allergens: list[str], k: int = 5
) -> list[tuple[dict, float]]:
    scored = [(p, score_perfume(p, preferred, avoid_allergens)) for p in perfumes]
    scored = [t for t in scored if t[1] > 0.0]  # drop zero scores
    scored.sort(key=lambda x: x[1], reverse=True)
    return scored[:k]
