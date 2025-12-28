from __future__ import annotations
import click
import sys
import storage

# Minimal Click group exported as `app`
@click.group(name="aromavault")
def app() -> None:
    """AromaVault CLI"""

# Define commands WITHOUT stacking decorators on the group
@click.command(name="seed-minimal")
def seed_minimal() -> None:
    """Write 3 sample perfumes (overwrites current DB)."""
    n = storage.seed_minimal()  # must return 3
    click.echo(f"Seeded {n} perfumes")

@click.command(name="add-perf")
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

# Explicit registration
app.add_command(seed_minimal, name="seed-minimal")
app.add_command(add_perf, name="add-perf")

# Redundant safety: if CI somehow missed, re-add with explicit names
for _name, _cmd in (("seed-minimal", seed_minimal), ("add-perf", add_perf)):
    if _name not in app.commands:
        app.add_command(_cmd, name=_name)

# Tiny import debug to stderr (pytest captures this on failure)
try:
    sys.stderr.write(
        f"[cli_app import] commands={sorted(app.commands.keys())}\\n"
    )
except Exception:
    pass

__all__ = ["app"]
