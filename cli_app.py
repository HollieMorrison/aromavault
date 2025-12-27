from __future__ import annotations
import click
import storage

@click.group(name="aromavault")
def app() -> None:
    """AromaVault CLI"""

@app.command("seed-minimal")
def seed_minimal() -> None:
    """Write 3 sample perfumes (overwrites current DB)."""
    n = storage.seed_minimal()
    click.echo(f"Seeded {n} perfumes")

@app.command("add-perf")
@click.argument("name", metavar="NAME")
@click.option("--brand", "-b", required=True, help="Brand")
@click.option("--price", "-p", required=True, type=float, help="Price")
@click.option("--notes", "-n", default="", help="CSV notes e.g. rose,musk")
def add_perf(name: str, brand: str, price: float, notes: str) -> None:
    """Add a perfume entry."""
    notes_list = [s.strip() for s in notes.split(",") if s.strip()] if notes else []
    created = storage.add_perfume({
        "name": name,
        "brand": brand,
        "price": price,
        "notes": notes_list,
        "rating": 0.0,
        "stock": 0,
        "allergens": [],
    })
    click.echo(f"Added: {created['id']}")
