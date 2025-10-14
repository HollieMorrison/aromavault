import uuid
from dataclasses import dataclass, field
from typing import Optional


# Dataclass for a perfume record stored in our JSON database
@dataclass
class Perfume:
    id: str  # UUID string used as unique identifier
    name: str
    brand: str
    price: float
    notes: list[str] = field(default_factory=list)
    allergens: list[str] = field(default_factory=list)
    rating: Optional[float] = None
    stock: int = 0

    @staticmethod
    def new(
        name: str,
        brand: str,
        price: float,
        notes: list[str],
        allergens: list[str],
        rating: Optional[float] = None,
        stock: int = 0,
    ) -> "Perfume":
        """Factory method that normalises and validates fields before creating a Perfume."""
        return Perfume(
            id=str(uuid.uuid4()),
            name=name.strip(),
            brand=brand.strip(),
            price=float(price),
            notes=[n.strip().lower() for n in notes if n.strip()],
            allergens=[a.strip().lower() for a in allergens if a.strip()],
            rating=float(rating) if rating is not None else None,
            stock=int(stock),
        )


# Dataclass for a user profile that drives personalised recommendations
@dataclass
class UserProfile:
    id: str
    name: str
    preferred_notes: list[str] = field(default_factory=list)
    avoid_allergens: list[str] = field(default_factory=list)

    @staticmethod
    def new(
        name: str, preferred_notes: list[str], avoid_allergens: list[str]
    ) -> "UserProfile":
        """Factory that lowercases and trims list values to keep the data clean."""
        return UserProfile(
            id=str(uuid.uuid4()),
            name=name.strip(),
            preferred_notes=[n.strip().lower() for n in preferred_notes if n.strip()],
            avoid_allergens=[a.strip().lower() for a in avoid_allergens if a.strip()],
        )
