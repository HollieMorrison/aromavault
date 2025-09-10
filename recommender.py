from typing import List, Dict, Tuple

# Basic set-based similarities between notes.
# Jaccard = |intersection| / |union|
# Returns 0..1 where 1 means identical sets.

def jaccard(a: List[str], b: List[str]) -> float:
  sa, sb, = set(a), set(b)
  if not sa and not sb:
    return 0.0
  inter = sa & sb
  union = sa | sb
  return len(inter) / len(union)

# compute a recommendation score for a single perfume depending on users choices.
# Score = similarity(preferred_notes, perfume.notes) - penalty if the perfume has avoided allergies.

def score_perfume(perfume: Dict, preferred: List[str], avoid_allergens: List[str]) -> float:
    base = jaccard([n.lower() for n in preferred], [n.lower() for n in perfume.get("notes", [])])
    penalty = 0.5 if set(a.lower() for a in perfume.get("allergens", [])) & set(a.lower() for a in avoid_allergens) else 0.0
    return max(0.0, base - penalty)

def recommend(perfumes: List[Dict], preferred: List[str], avoid_allergens: List[str], k: int = 5) -> List[Tuple[Dict, float]]:
    scored = [(p, score_perfume(p, preferred, avoid_allergens)) for p in perfumes]
    scored = [t for t in scored if t[1] > 0.0] # drop zero scores
    scored.sort(key=lambda x: x[1], reverse=True)
    return scored [:k]