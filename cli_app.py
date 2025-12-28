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
@click.argument("name", nargs=1)
@click.option("--brand", required=True, help="Brand name")
@click.option("--price", required=True, type=float, help="Price")
@click.option("--notes", required=False, help="Comma separated notes, e.g. 'rose,musk'")
def add_perf(name: str, brand: str, price: float, notes: str | None) -> None:
    """Add a single perfume with minimal fields used in tests."""
    notes_list = [s.strip() for s in (notes or "").split(",") if s.strip()]
    payload = {
        "name": name,
        "brand": brand,
        "price": float(price),
        "notes": notes_list,
        "allergens": [],
        "rating": 0.0,
        "stock": 0,
    }
    created = storage.add_perfume(payload)
    _id = created.get("id") or created.get("name") or name
    click.echo(f"Added: {_id}")

__all__ = ["app"]
