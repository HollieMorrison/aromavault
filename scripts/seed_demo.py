#!/usr/bin/env python
import json
import sys
from pathlib import Path

import storage

QUIET = "--quiet" in sys.argv


def seed_items():
    # simple demo catalog (unique names)
    items = [
        {"name": "Amber Sky", "brand": "Noctis", "price": 72.0, "notes": "amber,vanilla"},
        {"name": "Azure Mist", "brand": "Noctis", "price": 59.0, "notes": "citrus,musk"},
        {"name": "Rose Dusk", "brand": "Floral", "price": 55.0, "notes": "rose,musk"},
        {"name": "Cedar Lake", "brand": "Nord", "price": 64.0, "notes": "cedar,wood"},
        {"name": "Citrus Bloom", "brand": "Verde", "price": 49.0, "notes": "citrus,floral"},
        {"name": "Velvet Night", "brand": "Noctis", "price": 80.0, "notes": "vanilla,tonka"},
    ]
    return items


def main():
    try:
        if storage.list_perfumes():
            if not QUIET:
                print("DB already has data; skipping seeding")
            return 0
        n = 0
        for it in seed_items():
            storage.add_perfume(it)
            n += 1
        if not QUIET:
            print(f"Seeded {n} perfumes")
        return 0
    except Exception as e:
        if not QUIET:
            print("Seed error:", e)
        # don't fail the deploy because of seed
        return 0


if __name__ == "__main__":
    raise SystemExit(main())
