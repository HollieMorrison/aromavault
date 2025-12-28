from __future__ import annotations
import click
import storage

# Root group exported as `app`
@click.group(name="aromavault")
def app() -> None:
    """AromaVault CLI"""

# ---- Commands (define, then register) --------------------------------------
@click.command(name="seed-minimal")
def seed_minimal() -> None:
    """Write 3 sample perfumes (overwrites current DB)."""
    n = storage.seed_minimal()
    click.echo(f"Seeded {n} perfumes")

@click.command(name="add-perf")
@click.argument("name", nargs=1)
@click.option("--brand", required=True, help="Brand name")
@click.option("--price", required=True, type=float, help="Price")
@click.option("--notes", required=False, help="Comma separated notes, e.g. 'rose,musk'")
def add_perf(name: str, brand: str, price: float, notes: str | None) -> None:
    """Add a single perfume entry."""
    notes_list = [s.strip() for s in (notes or "").split(",") if s.strip()]
    item = {
        "name": name,
        "brand": brand,
        "price": float(price),
        "notes": notes_list,
        "allergens": [],
        "rating": 0.0,
        "stock": 0,
    }
    storage.add_perfume(item)
    click.echo(f"Added: {name}")

# Explicit registration (no decorator stacking on `app`)
app.add_command(seed_minimal, name="seed-minimal")
app.add_command(add_perf, name="add-perf")

__all__ = ["app"]
