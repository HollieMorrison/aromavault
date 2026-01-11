import storage

samples = [
    {
        "name": "Rose Dusk",
        "brand": "Floral",
        "price": 55,
        "notes": ["rose", "musk"],
        "rating": 4.5,
    },
    {
        "name": "Amber Trail",
        "brand": "Nocturne",
        "price": 72,
        "notes": ["amber", "vanilla", "tonka"],
        "rating": 4.6,
    },
    {
        "name": "Ocean Mist",
        "brand": "Aqua",
        "price": 49,
        "notes": ["marine", "citrus", "salt"],
        "rating": 4.0,
    },
    {
        "name": "Vetiver Line",
        "brand": "Terra",
        "price": 67,
        "notes": ["vetiver", "grapefruit", "pepper"],
        "rating": 4.3,
    },
    {
        "name": "Jasmine Night",
        "brand": "Floral",
        "price": 58,
        "notes": ["jasmine", "white musk"],
        "rating": 4.4,
    },
]
for p in samples:
    storage.add_perfume(p)
print(f"Seeded {len(samples)} perfumes")
