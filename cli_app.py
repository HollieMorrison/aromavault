from __future__ import annotations

import click

import storage


@click.group(help="AromaVault CLI")
def app():
    pass


@app.command("add-perf", help="Add a perfume (unique name).")
@click.argument("name")
@click.option("--brand", required=True, help="Brand (≤80 chars)")
@click.option("--price", required=True, type=float, help="Price (0..1e6)")
@click.option("--notes", default="", help="Comma-separated notes")
def add_perf(name, brand, price, notes):
    try:
        item = storage.add_perfume({"name": name, "brand": brand, "price": price, "notes": notes})
        click.echo(f"Added: {item['name']} ({item['id']})")
    except Exception as e:
        click.echo(f"Error: {e}")


@app.command("list", help="List perfumes (optionally filter).")
@click.option("--brand", default=None, help="Filter by brand substring")
@click.option("--notes", "notes_sub", default=None, help="Filter by note substring")
@click.option("--name", "name_sub", default=None, help="Filter by name substring")
def list_cmd(brand, notes_sub, name_sub):
    rows = storage.list_perfumes(brand_sub=brand, notes_sub=notes_sub, name_sub=name_sub)
    if not rows:
        click.echo("No perfumes found")
        return
    for r in rows:
        n = ",".join(r.get("notes", []))
        click.echo(f"{r['id']} | {r['name']} | {r['brand']} | £{r['price']:.2f} | {n}")


@app.command("show", help="Show exactly one perfume by ID or unique name.")
@click.argument("id_or_name")
def show_cmd(id_or_name):
    r = storage.get_one(id_or_name)
    if not r:
        click.echo("Not found")
        return
    click.echo(f"ID: {r['id']}")
    click.echo(f"Name: {r['name']}")
    click.echo(f"Brand: {r['brand']}")
    click.echo(f"Price: £{r['price']:.2f}")
    click.echo(f"Notes: {', '.join(r.get('notes', []))}")


@app.command("update", help="Update fields on a perfume.")
@click.argument("id_or_name")
@click.option("--name", default=None)
@click.option("--brand", default=None)
@click.option("--price", type=float, default=None)
@click.option("--notes", default=None, help="Comma-separated")
def update_cmd(id_or_name, name, brand, price, notes):
    payload = {}
    if name is not None:
        payload["name"] = name
    if brand is not None:
        payload["brand"] = brand
    if price is not None:
        payload["price"] = price
    if notes is not None:
        payload["notes"] = notes
    if not payload:
        click.echo("Nothing to update")
        return
    try:
        ok = storage.update_perfume(id_or_name, payload)
        click.echo("Updated" if ok else "Not found")
    except Exception as e:
        click.echo(f"Error: {e}")


@app.command("delete", help="Delete by ID or unique name.")
@click.argument("id_or_name")
def delete_cmd(id_or_name):
    ok = storage.delete_perfume(id_or_name)
    click.echo("Deleted" if ok else "Not found")


# Optional helper for tests/quick setup (no output besides a simple line)
@app.command("seed-minimal", help="Seed 3 sample perfumes if DB is empty.")
def seed_minimal():
    if storage.list_perfumes():
        click.echo("Already seeded")
        return
    samples = [
        {"name": "Rose Dusk", "brand": "Floral", "price": 55, "notes": "rose,musk"},
        {"name": "Citrus Glow", "brand": "Aurora", "price": 42.5, "notes": "citrus,bergamot"},
        {"name": "Amber Night", "brand": "Noctis", "price": 60, "notes": "amber,vanilla"},
    ]
    added = 0
    for s in samples:
        try:
            storage.add_perfume(s)
            added += 1
        except Exception:
            pass
    click.echo(f"Seeded {added}")
