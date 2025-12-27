from __future__ import annotations
from typing import List
import typer
from typer.main import get_command
import storage

# Build the Typer app (no_args_is_help avoids bare-run confusion)
_typer = typer.Typer(help="AromaVault CLI", no_args_is_help=True)

@_typer.command("seed-minimal")
def seed_minimal() -> None:
    """Seed 3 sample perfumes into the current DB."""
    items = [
        {"name": "Rose Dusk", "brand": "Floral", "price": 55.0, "notes": ["rose", "musk"]},
        {"name": "Citrus Bloom", "brand": "Citrico", "price": 45.0, "notes": ["orange", "neroli"]},
        {"name": "Woody Path", "brand": "Terra", "price": 60.0, "notes": ["cedar", "vetiver"]},
    ]
    for it in items:
        p = storage.Perfume.new(it["name"], it["brand"], it["price"], it["notes"], [])
        storage.add_perfume(p.__dict__)
    typer.echo("Seeded 3 perfumes")

@_typer.command("add-perf")
def add_perf(
    name: str,
    brand: str = typer.Option(..., "--brand"),
    price: float = typer.Option(..., "--price"),
    notes: str = typer.Option("", "--notes", help="Comma-separated list"),
) -> None:
    """Add a perfume (NAME is positional; others are options)."""
    notes_list = [n.strip() for n in notes.split(",") if n.strip()] if notes else []
    p = storage.Perfume.new(name, brand, price, notes_list, [])
    storage.add_perfume(p.__dict__)
    typer.echo(f"Added: {name}")

@_typer.command("list")
def list_cmd() -> None:
    """List perfumes."""
    for it in storage.list_perfumes():
        typer.echo(f"{it['name']} — {it['brand']}")

@_typer.command("find")
def find_cmd(query: str) -> None:
    """Find perfumes whose name/brand contains QUERY (case-insensitive)."""
    q = query.lower()
    for it in storage.list_perfumes():
        if q in it["name"].lower() or q in it["brand"].lower():
            typer.echo(f"{it['name']} — {it['brand']}")

# Export a real Click command (what pytest's CliRunner expects)
app = get_command(_typer)
# Give it a stable program name so Click can infer it under pytest
app.name = "aromavault"

__all__ = ["app"]
