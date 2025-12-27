import typer

from storage import add_perfume, delete_perfume, export_csv, list_perfumes, search, update_perfume
from validators import non_empty_list_str, non_empty_str, positive_float_or_none

app = typer.Typer(help="AromaVault demo commands for assessment")


@app.command()
def listall():
    """List all perfumes."""
    items = list_perfumes()
    typer.echo(f"Total: {len(items)}")
    for it in items[:50]:
        typer.echo(
            f"- {it.get('id','?')} | {it.get('brand','?')} | {it.get('name','?')} | £{it.get('price','?')}"
        )


@app.command()
def find(
    q: str | None = typer.Option(None, "--q", help="Free text"),
    brand: str | None = None,
    notes: list[str] = typer.Option(None, "--note", help="Match any of these notes"),
    price_max: float | None = None,
):
    """Search the catalog (any of q/brand/notes/price_max)."""
    q = q.strip() if q else None
    brand = non_empty_str(brand, "brand") if brand else None
    notes_any = non_empty_list_str(notes)
    price = positive_float_or_none(price_max, "price_max")
    results = search(query=q, brand=brand, notes_any=notes_any, price_max=price)
    typer.echo(f"Found: {len(results)}")
    for r in results[:50]:
        typer.echo(f"- {r.get('id')} | {r.get('brand')} | {r.get('name')}")


@app.command()
def add(
    id: str,
    name: str,
    brand: str,
    price: float = typer.Option(..., "--price"),
    note: list[str] = typer.Option(None, "--note"),
):
    """Add a perfume (id, name, brand, price, notes)."""
    item = {
        "id": non_empty_str(id, "id"),
        "name": non_empty_str(name, "name"),
        "brand": non_empty_str(brand, "brand"),
        "price": positive_float_or_none(price, "price"),
        "notes": non_empty_list_str(note),
    }
    saved = add_perfume(item)
    typer.echo(f"Added/updated: {saved.get('id')}")


@app.command()
def patch(id: str, name: str | None = None, brand: str | None = None, price: float | None = None):
    """Update part of a perfume by id."""
    changes = {}
    if name:
        changes["name"] = non_empty_str(name, "name")
    if brand:
        changes["brand"] = non_empty_str(brand, "brand")
    if price is not None:
        changes["price"] = positive_float_or_none(price, "price")
    updated = update_perfume(id, changes)
    typer.echo(f"Updated: {updated.get('id')}")


@app.command()
def remove(id: str):
    """Delete a perfume by id."""
    ok = delete_perfume(id)
    typer.echo("Deleted" if ok else "Not found")


@app.command()
def csvout(path: str = "export.csv"):
    """Export catalog to CSV."""
    count = export_csv(path)
    typer.echo(f"Exported {count} items to {path}")


if __name__ == "__main__":
    app()
