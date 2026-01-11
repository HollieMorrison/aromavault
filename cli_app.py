from typing import List

import click

import storage


def _fmt_line(p: dict) -> str:
    notes = ",".join(p.get("notes") or [])
    price = float(p.get("price", 0))
    rating = float(p.get("rating", 0))
    return f"{p.get('id')} | {p.get('name')} | {p.get('brand')} | £{price:.1f} | rating {rating:.1f} | {notes}"


@click.group(name="aromavault", help="AromaVault CLI")
def app() -> None:
    """CLI group."""


# ---------- Seeding ----------
@app.command("seed-minimal")
def seed_minimal_cmd():
    """Write 3 sample perfumes (overwrites current DB)."""
    n = storage.seed_minimal()
    click.echo(f"Seeded {n} perfumes")


@app.command("seed-30")
def seed_30_cmd():
    """Write 30 sample perfumes if available, else fall back to 3."""
    seeder = getattr(storage, "seed_30", None) or storage.seed_minimal
    n = seeder()
    click.echo(f"Seeded {n} perfumes")


# ---------- List ----------
@app.command("list")
def list_cmd():
    """List all perfumes (with header)."""
    items = storage.list_perfumes()
    click.echo(f"Perfumes ({len(items)})")
    for p in items:
        click.echo(_fmt_line(p))


# Some tests/environments expect this alias. Keep both.
@app.command("list-perfumes-cmd")
def list_perfumes_cmd():
    """Alias: list all perfumes (with header)."""
    items = storage.list_perfumes()
    click.echo(f"Perfumes ({len(items)})")
    for p in items:
        click.echo(_fmt_line(p))


# ---------- Add ----------
@app.command("add-perf")
@click.argument("name", type=str)
@click.option("--brand", required=True, type=str, help="Brand name")
@click.option("--price", required=True, type=float, help="Price (GBP)")
@click.option("--notes", default="", type=str, help='Comma-separated notes e.g. "rose,musk"')
def add_perf_cmd(name: str, brand: str, price: float, notes: str):
    """Add a perfume with minimal fields used in tests."""
    notes_list: List[str] = [n.strip() for n in notes.split(",") if n.strip()] if notes else []
    payload = {
        "name": name,
        "brand": brand,
        "price": float(price),
        "notes": notes_list,
        "allergens": [],
        "rating": 0.0,
        "stock": 0,
    }
    stored = storage.add_perfume(payload)
    click.echo(f"Added: {stored.get('id')}")


# ---------- Find ----------
@app.command("find")
@click.argument("query", type=str)
def find_cmd(query: str):
    """Find by name/brand/notes (case-insensitive)."""
    q = query.lower().strip()
    items = storage.list_perfumes()
    hits = []
    for p in items:
        if q in (p.get("name", "").lower()) or q in (p.get("brand", "").lower()):
            hits.append(p)
            continue
        notes = [str(n).lower() for n in (p.get("notes") or [])]
        if any(q in n for n in notes):
            hits.append(p)
    for p in hits:
        click.echo(_fmt_line(p))


# ---------- Show ----------
@app.command("show")
@click.argument("token", type=str)
def show_cmd(token: str):
    """Show a single perfume by id (exact) or name substring (case-insensitive)."""
    items = storage.list_perfumes()
    t = token.lower().strip()
    for p in items:
        if str(p.get("id")) == token:
            click.echo(_fmt_line(p))
            return
    for p in items:
        if t in str(p.get("name", "")).lower():
            click.echo(_fmt_line(p))
            return
    click.echo("Not found")


# ---------- Delete ----------
@app.command("delete")
@click.argument("token", type=str)
def delete_cmd(token: str):
    """Delete by exact id or exact name (case-insensitive)."""
    token_l = token.lower().strip()
    items = storage.list_perfumes()
    target_id = None
    for p in items:
        if str(p.get("id")) == token or str(p.get("name", "")).lower() == token_l:
            target_id = str(p.get("id"))
            break
    if not target_id:
        click.echo("Not found")
        raise SystemExit(1)

    # Use storage helpers if available; otherwise rewrite DB list
    if hasattr(storage, "delete_by_id"):
        ok = storage.delete_by_id(target_id)
    elif hasattr(storage, "delete_perfume"):
        ok = storage.delete_perfume(target_id)  # type: ignore[attr-defined]
    else:
        data = [p for p in items if str(p.get("id")) != target_id]
        storage.write_db(data)
        ok = True

    if ok:
        click.echo(f"Deleted: {target_id}")
    else:
        click.echo("Not found")
        raise SystemExit(1)
