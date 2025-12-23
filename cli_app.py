from __future__ import annotations
from pathlib import Path
import json
from typing import List
import typer

# Tests monkeypatch storage.DEFAULT_DB, so we **must** import storage and use that path.
import storage  # must expose DEFAULT_DB as a Path-like

# Build the Typer app internally...
_typer_app = typer.Typer(
    help="AromaVault command-line interface.",
    no_args_is_help=True,
)

def _ensure_parent(p: Path) -> None:
    p.parent.mkdir(parents=True, exist_ok=True)

def _read_list(p: Path) -> List[dict]:
    if not p.exists():
        return []
    with p.open("r", encoding="utf-8") as f:
        data = json.load(f)
    # Accept either {"perfumes":[...]} or a bare list [...]
    return data.get("perfumes", data) if isinstance(data, dict) else data

def _write_list(p: Path, items: List[dict]) -> None:
    _ensure_parent(p)
    with p.open("w", encoding="utf-8") as f:
        json.dump(items, f, ensure_ascii=False, indent=2)

@_typer_app.command("seed-minimal")
def seed_minimal() -> None:
    """Seed 3 sample perfumes into storage.DEFAULT_DB (used by tests)."""
    db_path = Path(storage.DEFAULT_DB)
    items = [
        {
            "id": "seed-woodland-trail",
            "name": "Woodland Trail",
            "brand": "Earth&Oak",
            "price": 79.0,
            "notes": ["oakmoss", "cedar", "vetiver"],
            "allergens": ["oakmoss"],
            "stock": 4,
            "rating": 4.6,
        },
        {
            "id": "seed-night-bloom-xl",
            "name": "Night Bloom XL",
            "brand": "Nocturne",
            "price": 65.0,
            "notes": ["jasmine", "amber", "musk"],
            "allergens": ["coumarin"],
            "stock": 7,
            "rating": 4.4,
        },
        {
            "id": "seed-rose-dusk",
            "name": "Rose Dusk",
            "brand": "Floral",
            "price": 55.0,
            "notes": ["rose", "musk"],
            "allergens": [],
            "stock": 0,
            "rating": 4.0,
        },
    ]
    _write_list(db_path, items)
    typer.echo(f"Seeded {len(items)} perfumes into {db_path}")

@_typer_app.command("add-perf")
def add_perf(
    name: str = typer.Argument(..., help="Perfume name (positional)"),
    brand: str = typer.Option(..., "--brand", help="Brand name"),
    price: float = typer.Option(..., "--price", help="Price"),
    notes: str = typer.Option("", "--notes", help="Comma-separated notes"),
) -> None:
    """Add a perfume to storage.DEFAULT_DB (used by tests)."""
    db_path = Path(storage.DEFAULT_DB)
    items = _read_list(db_path)
    item = {
        "id": f"cli-{brand.lower().replace(' ', '-')}-{name.lower().replace(' ', '-')}",
        "name": name,
        "brand": brand,
        "price": float(price),
        "notes": [n.strip() for n in notes.split(",") if n.strip()],
        "allergens": [],
        "stock": 0,
        "rating": 0.0,
    }
    items.append(item)
    _write_list(db_path, items)
    typer.echo(f"Added '{name}' by {brand} (£{price}) to {db_path}")

# ...and export a Click command as `app` for tests/CliRunner:
# (This avoids the 'Typer object has no attribute name' error.)
from typer.main import get_command as _get_click_command
app = _get_click_command(_typer_app)

if __name__ == "__main__":
    # Running directly: execute the Click command
    app()
