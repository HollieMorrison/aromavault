from __future__ import annotations

import sys as _sys

import click

import storage


@click.group(name="aromavault")
def app() -> None:
    """AromaVault CLI"""


# Use default autohyphenation (seed_minimal -> seed-minimal)
@app.command()
def seed_minimal() -> None:
    """Write 3 sample perfumes (overwrites current DB)."""
    n = storage.seed_minimal()
    click.echo(f"Seeded {n} perfumes")


@app.command()
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


# Make both hyphen and underscore names available defensively
if "seed-minimal" not in app.commands and "seed_minimal" in app.commands:
    app.add_command(app.commands["seed_minimal"], name="seed-minimal")
if "seed_minimal" not in app.commands and "seed-minimal" in app.commands:
    app.add_command(app.commands["seed-minimal"], name="seed_minimal")

if "add-perf" not in app.commands and "add_perf" in app.commands:
    app.add_command(app.commands["add_perf"], name="add-perf")
if "add_perf" not in app.commands and "add-perf" in app.commands:
    app.add_command(app.commands["add-perf"], name="add_perf")

# Import-time breadcrumb (shows in pytest -s if anything is weird)
try:
    _sys.stderr.write(f"[cli_core import] commands={sorted(app.commands.keys())}\n")
except Exception:
    pass
