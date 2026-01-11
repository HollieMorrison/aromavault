from __future__ import annotations
import storage

SAMPLES = [
    {"name": "Amber Sky",   "brand": "Noctis", "price": 72.0, "notes": "amber,vanilla"},
    {"name": "Azure Mist",  "brand": "Noctis", "price": 59.0, "notes": "citrus,musk"},
    {"name": "Rose Dusk",   "brand": "Floral", "price": 55.0, "notes": "rose,musk"},
    {"name": "Cedar Grove", "brand": "Terra",  "price": 64.0, "notes": "cedar,wood"},
    {"name": "Citrinella",  "brand": "Luma",   "price": 47.0, "notes": "citrus,herbal"},
    {"name": "Velvet Oud",  "brand": "Noctis", "price": 88.0, "notes": "oud,spice"},
]

def run():
    items = storage._load()
    if items:
        print("[seed] DB already has data, skipping")
        return
    for s in SAMPLES:
        storage.add_perfume(s)
    print(f"[seed] Inserted {len(SAMPLES)} perfumes")

if __name__ == "__main__":
    run()
