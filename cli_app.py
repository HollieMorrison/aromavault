import click

import storage


@click.group(name="aromavault")
def app():
    """AromaVault CLI — add, list (with filters), show, update, delete."""
    pass


@app.command("add-perf")
@click.argument("name")
@click.option("--brand", required=True, help="Brand (max length enforced)")
@click.option("--price", required=True, type=float, help="Price (0..MAX)")
@click.option("--notes", default="", help="Comma-separated notes")
@click.option("--stock", default=0, type=int, help="Initial stock (>=0)")
def add_perf(name, brand, price, notes, stock):
    """Add a perfume."""
    try:
        item = storage.add_perfume(
            {"name": name, "brand": brand, "price": price, "notes": notes, "stock": stock}
        )
        click.echo(f"Added: {item['name']} ({item['id']})")
    except Exception as e:
        click.echo(f"Error: {e}")


@app.command("list")
@click.option("--brand", default=None, help="Filter by brand (substring)")
@click.option("--name", "name_sub", default=None, help="Filter by name (substring)")
@click.option("--notes", "notes_sub", default=None, help="Filter by notes (substring)")
def list_cmd(brand, name_sub, notes_sub):
    """List all, or filter by --brand/--name/--notes."""
    items = storage.list_perfumes(brand=brand, name=name_sub, notes_sub=notes_sub)
    click.echo(f"Perfumes ({len(items)})")
    for it in items:
        click.echo(f"- {it['name']} — {it['brand']} — £{it['price']:.2f} — stock {it['stock']}")


@app.command("show")
@click.argument("id_or_name")
def show_cmd(id_or_name):
    """Show exactly one item by ID or exact Name."""
    it = storage.get_by_id_or_name(id_or_name)
    if not it:
        click.echo("Not found")
        return
    click.echo(f"ID: {it['id']}")
    click.echo(f"Name: {it['name']}")
    click.echo(f"Brand: {it['brand']}")
    click.echo(f"Price: £{it['price']:.2f}")
    click.echo(f"Notes: {', '.join(it['notes']) if it.get('notes') else '-'}")
    click.echo(f"Stock: {it['stock']}")


@app.command("update-perf")
@click.argument("id_or_name")
@click.option("--name", default=None)
@click.option("--brand", default=None)
@click.option("--price", type=float, default=None)
@click.option("--notes", default=None, help="Comma-separated")
@click.option("--stock", type=int, default=None)
def update_perf(id_or_name, name, brand, price, notes, stock):
    """Update fields on a perfume (no rating)."""
    payload = {}
    if name is not None:
        payload["name"] = name
    if brand is not None:
        payload["brand"] = brand
    if price is not None:
        payload["price"] = price
    if notes is not None:
        payload["notes"] = notes
    if stock is not None:
        payload["stock"] = stock
    if not payload:
        click.echo("Nothing to update")
        return
    try:
        ok = storage.update_perfume(id_or_name, payload)
        click.echo("Updated" if ok else "Not found")
    except Exception as e:
        click.echo(f"Error: {e}")


@app.command("delete")
@click.argument("id_or_name")
def delete_cmd(id_or_name):
    """Delete by exact ID or exact Name (names are unique)."""
    click.echo("Deleted" if storage.delete_perfume(id_or_name) else "Not found")
