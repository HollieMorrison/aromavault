#!/usr/bin/env python3
"""
AromaVault – Interactive CLI (PP3)

Features:
- Seed (3 or 30 if available)
- List all (with count)
- Find (name/brand/notes, case-insensitive)
- Show (by id or name substring)
- Add (name, brand, price, notes)
- Update (by exact id or exact name)
- Delete (by exact id or exact name)

Uses the same JSON DB as the web app (storage.DEFAULT_DB).
"""

from __future__ import annotations

import json
import sys
import uuid
from pathlib import Path

DEFAULT_DB = Path("db.json")
seeders: dict[str, callable] = {}

# Prefer your project's storage module if present
try:
    import storage  # type: ignore

    DEFAULT_DB = getattr(storage, "DEFAULT_DB", DEFAULT_DB)
    if hasattr(storage, "seed_minimal"):
        seeders["minimal"] = storage.seed_minimal  # returns count
    if hasattr(storage, "seed_30"):
        seeders["seed_30"] = storage.seed_30  # returns count
except Exception:
    # storage is optional; fallback used if missing
    pass


def load_db(path: Path = DEFAULT_DB) -> list[dict]:
    if not path.exists():
        return []
    try:
        with path.open("r", encoding="utf-8") as f:
            data = json.load(f)
        return data if isinstance(data, list) else []
    except Exception:
        return []


def save_db(items: list[dict], path: Path = DEFAULT_DB) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        json.dump(items, f, indent=2, ensure_ascii=False)


def ensure_seeded() -> None:
    """If DB is empty, seed with 30 (if available) else 3 else internal 3."""
    items = load_db()
    if items:
        return
    if "seed_30" in seeders:
        n = seeders["seed_30"]()
        print(f"[auto-seed] wrote {n} perfumes (seed_30)")
    elif "minimal" in seeders:
        n = seeders["minimal"]()
        print(f"[auto-seed] wrote {n} perfumes (minimal)")
    else:
        fallback = [
            {
                "id": str(uuid.uuid4()),
                "name": "Citrus Aurora",
                "brand": "Sole",
                "price": 48.0,
                "notes": ["bergamot", "lemon", "neroli"],
                "rating": 0.0,
                "stock": 0,
            },
            {
                "id": str(uuid.uuid4()),
                "name": "Rose Dusk",
                "brand": "Floral",
                "price": 55.0,
                "notes": ["rose", "musk"],
                "rating": 0.0,
                "stock": 0,
            },
            {
                "id": str(uuid.uuid4()),
                "name": "Vetiver Line",
                "brand": "Terra",
                "price": 67.0,
                "notes": ["vetiver", "grapefruit", "pepper"],
                "rating": 0.0,
                "stock": 0,
            },
        ]
        save_db(fallback)
        print("[auto-seed] wrote 3 perfumes (fallback)")


def input_nonempty(prompt: str) -> str:
    while True:
        s = input(prompt).strip()
        if s:
            return s
        print("Please enter a value.")


def as_float(s: str, default: float | None = None) -> float:
    try:
        return float(s)
    except Exception:
        if default is not None:
            return default
        raise


def show_perfume(x: dict) -> None:
    notes = ", ".join(x.get("notes") or [])
    print("-" * 72)
    print(f"ID:     {x.get('id')}")
    print(f"Name:   {x.get('name')}")
    print(f"Brand:  {x.get('brand')}")
    print(f"Price:  £{x.get('price', 0):.2f}")
    print(f"Rating: {x.get('rating', 0)}")
    print(f"Stock:  {x.get('stock', 0)}")
    print(f"Notes:  {notes}")
    print("-" * 72)


def pick_by_id_or_exact_name():
    key = input_nonempty("Enter exact ID or exact Name: ").strip()
    items = load_db()
    by_id = [x for x in items if x.get("id") == key]
    if by_id:
        return items, by_id[0]
    by_name = [x for x in items if (x.get("name") or "").strip().lower() == key.lower()]
    if by_name:
        return items, by_name[0]
    print("Not found (need exact ID or exact Name).")
    return items, None


# --- menu actions -------------------------------------------------------------


def menu_list():
    items = load_db()
    print(f"Perfumes ({len(items)})")
    for x in items:
        notes = ",".join(x.get("notes") or [])
        print(
            f"{x.get('id')} | {x.get('name')} | {x.get('brand')} | £{x.get('price',0):.2f} | rating {x.get('rating',0)} | {notes}"
        )


def menu_find():
    q = input_nonempty("Keyword (name/brand/notes): ").lower()
    items = load_db()
    results = []
    for x in items:
        name = (x.get("name") or "").lower()
        brand = (x.get("brand") or "").lower()
        notes = [n.lower() for n in (x.get("notes") or [])]
        if q in name or q in brand or any(q in n for n in notes):
            results.append(x)
    if not results:
        print("No matches.")
        return
    print(f"Found {len(results)}:")
    for x in results:
        show_perfume(x)


def menu_show():
    key = input_nonempty("Enter ID or Name substring: ").lower()
    items = load_db()
    results = [
        x for x in items if key in (x.get("id", "").lower()) or key in (x.get("name", "").lower())
    ]
    if not results:
        print("Not found.")
        return
    for x in results:
        show_perfume(x)


def menu_add():
    name = input_nonempty("Name: ")
    brand = input_nonempty("Brand: ")
    price = as_float(input("Price (e.g. 49.99): ").strip() or "0")
    notes_raw = input("Notes (comma separated): ").strip()
    notes = [n.strip() for n in notes_raw.split(",") if n.strip()]
    item = {
        "id": str(uuid.uuid4()),
        "name": name,
        "brand": brand,
        "price": price,
        "notes": notes,
        "rating": 0.0,
        "stock": 0,
    }
    items = load_db()
    items.append(item)
    save_db(items)
    print("Added.")
    show_perfume(item)


def menu_update():
    items, target = pick_by_id_or_exact_name()
    if not target:
        return
    print("Updating (leave blank to keep current value).")
    show_perfume(target)

    new_name = input(f"Name [{target.get('name')}]: ").strip() or target.get("name")
    new_brand = input(f"Brand [{target.get('brand')}]: ").strip() or target.get("brand")
    price_in = input(f"Price [{target.get('price',0)}]: ").strip()
    new_price = (
        target.get("price", 0) if not price_in else as_float(price_in, target.get("price", 0))
    )
    notes_in = input(f"Notes comma [{','.join(target.get('notes') or [])}]: ").strip()
    new_notes = (
        target.get("notes")
        if not notes_in
        else [n.strip() for n in notes_in.split(",") if n.strip()]
    )
    rating_in = input(f"Rating [{target.get('rating',0)}]: ").strip()
    new_rating = (
        target.get("rating", 0) if not rating_in else as_float(rating_in, target.get("rating", 0))
    )
    stock_in = input(f"Stock [{target.get('stock',0)}]: ").strip()
    new_stock = (
        target.get("stock", 0) if not stock_in else int(as_float(stock_in, target.get("stock", 0)))
    )

    target.update(
        {
            "name": new_name,
            "brand": new_brand,
            "price": new_price,
            "notes": new_notes,
            "rating": new_rating,
            "stock": new_stock,
        }
    )
    save_db(items)
    print("Updated.")
    show_perfume(target)


def menu_delete():
    items, target = pick_by_id_or_exact_name()
    if not target:
        return
    show_perfume(target)
    ok = input("Delete this? (y/N): ").strip().lower()
    if ok != "y":
        print("Cancelled.")
        return
    new_items = [x for x in items if x is not target]
    save_db(new_items)
    print("Deleted.")


def menu_seed():
    print("1) Seed 3 sample perfumes")
    print("2) Seed 30 sample perfumes (if available)")
    choice = input("Choice [1/2]: ").strip() or "1"

    if choice == "2" and "seed_30" in seeders:
        n = seeders["seed_30"]()
        print(f"Seeded {n}.")
    elif "minimal" in seeders:
        n = seeders["minimal"]()
        print(f"Seeded {n}.")
    else:
        ensure_seeded()  # fallback path writes 3
    menu_list()


def main():
    ensure_seeded()
    while True:
        print("\n==== AromaVault (CLI) ====")
        print("1) List all")
        print("2) Find")
        print("3) Show (by id/name)")
        print("4) Add")
        print("5) Update (by exact id/name)")
        print("6) Delete (by exact id/name)")
        print("7) Seed data")
        print("0) Exit")
        choice = input("Select: ").strip()

        try:
            if choice == "1":
                menu_list()
            elif choice == "2":
                menu_find()
            elif choice == "3":
                menu_show()
            elif choice == "4":
                menu_add()
            elif choice == "5":
                menu_update()
            elif choice == "6":
                menu_delete()
            elif choice == "7":
                menu_seed()
            elif choice == "0":
                print("Goodbye!")
                break
            else:
                print("Invalid choice.")
        except KeyboardInterrupt:
            print("\nInterrupted. Returning to menu.")
        except Exception as e:
            print(f"[Error] {e}")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nGoodbye!")
        sys.exit(0)

if __name__ == "__main__":
    import sys

    # If CLI args are provided, delegate to the Click CLI (prints help etc.)
    if len(sys.argv) > 1:
        from click.testing import CliRunner

        from cli_app import app as _click_app

        r = CliRunner().invoke(_click_app, sys.argv[1:])
        if r.stdout:
            print(r.stdout, end="")
        if r.stderr:
            print(r.stderr, end="")
        raise SystemExit(r.exit_code)
    # Otherwise, fall back to interactive menu (existing code will run)
