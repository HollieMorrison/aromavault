from __future__ import annotations
from pathlib import Path
from typing import List
import json
import typer

# The tests (and our CLI) use this path from your storage module
import storage  # must define DEFAULT_DB (Path-like)

app = typer.Typer(
    name="aromavault",
    help="AromaVault CLI: manage your perfume catalogue (list, add, delete, seed).",
)

# ---------- helpers ----------
def _db_path() -> Path:
    p = Path(storage.DEFAULT_DB)
    p.parent.mkdir(parents=True, exist_ok=True)
    return p

def _load() -> List[dict]:
    p = _db_path()
    if not p.exists():
        return []
    try:
        return json.loads(p.read_text(encoding="utf-8"))
    except Exception:
        return []

def _save(items: List[dict]) -> None:
    _db_path().write_text(json.dumps(items, indent=2, ensure_ascii=False), encoding="utf-8")

def _parse_notes(notes_csv: str | None) -> List[str]:
    if not notes_csv:
        return []
    return [n.strip() for n in notes_csv.split(",") if n.strip()]

# ---------- commands already used by tests ----------
@app.command("seed-minimal")
def seed_minimal() -> None:
    """Seed 3 example perfumes (used by tests). Overwrites the DB."""
    data = [
        {"name": "Citrus Spark", "brand": "AromaVault", "price": 39.0, "notes": ["citrus", "bergamot", "fresh"]},
        {"name": "Midnight Oud", "brand": "AromaVault", "price": 79.0, "notes": ["oud", "smoke", "amber"]},
        {"name": "Vanilla Veil", "brand": "AromaVault", "price": 49.0, "notes": ["vanilla", "tonka", "warm"]},
    ]
    _save(data)
    typer.echo(f"Seeded 3 perfumes into {Path(storage.DEFAULT_DB).name}")

@app.command("add-perf")
def add_perf(
    name: str = typer.Argument(..., help="Perfume name"),
    brand: str = typer.Option(..., "--brand", help="Brand name"),
    price: float = typer.Option(..., "--price", help="Price in £"),
    notes: str = typer.Option("", "--notes", help="Comma-separated notes, e.g. 'rose,musk'"),
) -> None:
    """Add a single perfume (used by tests and users)."""
    data = _load()
    if any(p["name"].lower() == name.lower() for p in data):
        typer.echo(f"'{name}' already exists — updating details.")
        data = [p for p in data if p["name"].lower() != name.lower()]
    data.append({"name": name, "brand": brand, "price": float(price), "notes": _parse_notes(notes)})
    _save(data)
    typer.echo(f"Added '{name}' by {brand} (£{float(price)}) to {Path(storage.DEFAULT_DB).name}")

# ---------- user-facing convenience commands ----------
@app.command("list")
def list_perfumes() -> None:
    """List all perfumes in the catalogue."""
    data = _load()
    if not data:
        typer.echo("No perfumes found. Try: aromavault add-perf \"Name\" --brand Brand --price 49.0 --notes rose,musk")
        raise typer.Exit(code=0)

    header = f"{'NAME':30} {'BRAND':20} {'PRICE':>7}  NOTES"
    typer.echo(header)
    typer.echo("-" * len(header))
    for p in sorted(data, key=lambda x: (x["brand"].lower(), x["name"].lower())):
        notes = ", ".join(p.get("notes", []))
        typer.echo(f"{p['name'][:30]:30} {p['brand'][:20]:20} £{p['price']:>6.2f}  {notes}")

@app.command("del-perf")
def delete_perf(name: str = typer.Argument(..., help="Perfume name to delete")) -> None:
    """Delete a perfume by name (case-insensitive)."""
    data = _load()
    before = len(data)
    data = [p for p in data if p["name"].lower() != name.lower()]
    _save(data)
    removed = before - len(data)
    if removed:
        typer.echo(f"Deleted {removed} item(s) named '{name}'.")
    else:
        typer.echo(f"No perfume named '{name}' was found.")

# Export Click command for Click/CliRunner compatibility (tests, etc.)
cli = typer.main.get_command(app)

if __name__ == "__main__":
    app()
