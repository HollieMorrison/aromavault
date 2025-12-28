from __future__ import annotations

import json
import uuid

import click

import storage


@click.group(name="aromavault")
def app() -> None:
    """AromaVault CLI"""


@app.command("seed-minimal")
def seed_minimal_cmd() -> None:
    """Write 3 sample perfumes (overwrites current DB)."""
    n = storage.seed_minimal()
    click.echo(f"Seeded {n} perfumes")


@app.command("seed-30")
def seed_30_cmd() -> None:
    """Write 30 sample perfumes (overwrites current DB)."""
    seeder = getattr(storage, "seed_30", None)
    n = seeder() if callable(seeder) else storage.seed_minimal()
    click.echo(f"Seeded {n} perfumes")


@app.command("add-perf")
@click.argument("name", nargs=1)
@click.option("--brand", required=True, help="Brand name")
@click.option("--price", required=True, type=float, help="Price")
@click.option("--notes", required=False, help="Comma separated notes, e.g. 'rose,musk'")
def add_perf(name: str, brand: str, price: float, notes: str | None) -> None:
    """Add a single perfume with minimal fields."""
    notes_list = [s.strip() for s in (notes or "").split(",") if s.strip()]
    payload = {
        "id": str(uuid.uuid4()),
        "name": name,
        "brand": brand,
        "price": float(price),
        "notes": notes_list,
        "allergens": [],
        "rating": 0.0,
        "stock": 0,
    }
    created = storage.add_perfume(payload)
    click.echo(f"Added: {created.get('id') or created.get('name') or name}")


@app.command("list")
def list_cmd() -> None:
    """List all perfumes."""
    items = storage.list_perfumes()
    if not items:
        click.echo("No perfumes found")
        return
    for i, it in enumerate(items, 1):
        click.echo(
            f"{i:02d}. {it.get('name')} | {it.get('brand')} | £{it.get('price')} | rating {it.get('rating', 0)}"
        )


@app.command("show")
@click.argument("query", nargs=1)
def show_cmd(query: str) -> None:
    """Show details by id or name substring."""
    q = query.lower()
    items = storage.list_perfumes()
    match = next(
        (it for it in items if it.get("id") == query or q in str(it.get("name", "")).lower()),
        None,
    )
    if not match:
        raise click.ClickException("Not found")
    click.echo(json.dumps(match, ensure_ascii=False, indent=2))


@app.command("find")
@click.argument("needle", nargs=1)
def find_cmd(needle: str) -> None:
    """Case-insensitive search over name/brand/notes."""
    n = needle.lower()
    items = storage.list_perfumes()
    hits: list[str] = []
    for it in items:
        hay = " ".join(
            [str(it.get("name", "")), str(it.get("brand", "")), ",".join(it.get("notes", []))]
        ).lower()
        if n in hay:
            hits.append(f"- {it.get('name')} ({it.get('brand')}) £{it.get('price')}")
    click.echo("\n".join(hits) if hits else "No matches")


@app.command("delete")
@click.argument("query", nargs=1)
def delete_cmd(query: str) -> None:
    """Delete by id or exact name (first match)."""
    items = storage.list_perfumes()
    pid = None
    for it in items:
        if it.get("id") == query or it.get("name") == query:
            pid = it.get("id") or it.get("name")
            break
    if not pid:
        raise click.ClickException("Not found")
    ok = storage.delete_perfume(pid)
    click.echo("Deleted" if ok else "No change")


__all__ = ["app"]
