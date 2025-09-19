# Main entry for my aromavault CLI application and also uses Typer to manage commands, and Rich to make outputs look better.
from typing import Optional, List
import sys
import typer
from rich.console import Console
from rich.table import Table

# Importing dataclasses and functions from other modules.
from models import Perfume, UserProfile
from storage import (
  add_perfume,
  add_profile,
  list_perfumes,
  get_perfume,
  get_profile,
  update_perfume,
  delete_perfume,
  import_csv,
  export_csv,
)
from recommender import recommend
from utils import parse_csv_list, human_money, error, info

#If fuzzy search library is installed.
try:
    from rapidfuzz import fuzz
    HAVE_FUZZ = True
except Exception:
    HAVE_FUZZ = False

# Typer app object to register commands
app = typer.Typer(add_completion=False)
console = Console()

@app.command()
def add_perf(
    name: str = typer.Argument(..., help="Perfume name"),
    brand: str = typer.Option(..., "--brand", prompt=True),
    price: float = typer.Option(..., "--price", prompt=True),
    notes: str = typer.Option("", "--notes", help="Comma-separated notes"),
    allergens: str = typer.Option("", "--allergens", help="Comma-separated allergens"),
    rating: Optional[float] = typer.Option(None, "--rating"),
    stock: int = typer.Option(0, "--stock"),
):
    """Add a new perfume to the catalogue"""
    # Creates a new perfume and saves it to the JSON database using storage helpers.
    p = Perfume.new(
        name=name,
        brand=brand,
        price=price,
        notes=parse_csv_list(notes),
        allergens=parse_csv_list(allergens),
        rating=rating,
        stock=stock,
    )
    add_perfume(p)
    info(f"Added: {p.name} by {p.brand} ({human_money(p.price)})")

@app.command()
def list_perfumes_cmd(
    brand: Optional[str] = typer.Option(None, "--brand"),
    note: Optional[str] = typer.Option(None, "--note"),
    sort_by: str = typer.Option("name", "--sort", case_sensitive=False),
    # Filtering perfumes by brands or notes.
):
    """List of perfumes with optional filters and sorting method"""
    perfumes = list_perfumes() # This reads all perfumes from json storage.

    # Applies optional filters from the CLI
    if brand:
        perfumes = [p for p in perfumes if p["brand"].lower() == brand.lower()]
    if note:
        note_l = note.lower()
        perfumes = [p for p in perfumes if note_l in [n.lower() for n in p.get("notes", [])]]

    key = (lambda p: p.get("name", "").lower() if sort_by == "name" else ( lambda p: p.get("brand", "").lower() if sort_by == "brand" else ( lambda p: p.get("price", 0.0) if sort_by == "price" else ( lambda p: p.get("rating", 0.0)
       )
      )
     )
    )

    perfumes.sort(key=key)

    # Build a table with Rich

    table = Table(title=f"Perfumes ({len(perfumes)})")
    table.add_column("ID", no_wrap=True)
    table.add_column("Name")
    table.add_column("Brand")
    table.add_column("Price")
    table.add_column("Notes")
    table.add_column("Allergens")
    table.add_column("Rating")
    table.add_column("Stock")

    for p in perfumes: 
        table.add_row(
            p["id"][:8],
            p.get("name", ""),
            p.get("brand", ""),
            human_money(p.get("price", 0.0)),
            ", ".join(p.get("notes", [])),
            ", ".join(p.get("allergens", [])),
            str(p.get("rating", "")),
            str(p.get("stock", 0)),
        )

console.print(table)

@app.command()
def find(query: str = typer.Argument(..., help="Search name/brand")):
    """Fuzzy search across name and brand."""
    perfumes = list_perfumes()
    q = query.lower()
    
    # Perfume Score function.
    def score(p):
        text = f"{p.get('name', '')} {p.get('brand', '')}".lower()
        if HAVE_FUZZ:
            return max(
                fuzz.partial_ratio(q, text),
            )
        return 100 if q in text else (50 if any(w in text for w in q.split()) else 0)
    
    ranked = sorted(((p, score(p)) for p in perfumes), key=lambda t: t[1], reverse=True)
    top = [t for t in ranked if t[1] > 0][:10]

    # Shows top matches in perfumes table.

    table = Table(title=f"Search results for '{query}' ({len(top)} )")
    table.add_column("Match")
    table.add_column("Name")
    table.add_column("Brand")
    table.add_column("Price")
    for p, sc in top:
        table.add_row(str(sc), p.get("name", ""), p.get("brand", ""), human_money(p.get("price", 0.0)))
    console.print(table)


@app.command()
def update(
    pid: str = typer.Argument(..., help="Perfume ID (first 8 chars accepted)"),
    field: str = typer.Argument(..., help="Field to update: name|brand|price|notes|allergens|rating|stock"),
    value: str = typer.Argument(..., help="New value (use comma-separated for notes/allergens)"),
):
    """Update a perfume field by ID"""
    # Allows the user to update any single field and includes input validation for numbers
    full = _resolve_id(pid)
    if not full: 
        return error("No perfume found for that ID.")
    
    # Convert CLI string 'value' into the correct Python type depending on the field
    updates = {}
    if field in {"name", "brand"}:
        updates[field] = value
    elif field in {"price", "rating"}:
       try: 
           updates[field] = float(value)
       except ValueError: 
           return error("Value must be a number.")
    elif field == "stock":
       try: 
           updates[field] = int(value)
       except ValueError:
           return error("Stock must be an integer.")
    elif field in {"notes", "allergens"}:
        updates[field] = parse_csv_list(value)
    else:
        return error("unknown field.")
    
    ok = updated_perfume(full, **updates)
    if ok:
        info("Updated successfully.")
    else:
        error("Update failed, please try again.")
        
    

@app.command()
def remove(pid: str):
    """Delete a perfume by ID"""
    # This will remove a perfume from the database.
    full = _resolve_id(pid)
    if not full:
        return error("No perfume found for that ID.")
    if delete_perfume(full):
        info("Deleted.")
    else:
        error("Delete perfume failed.")

@app.command()
def add_profile_cmd(
    name: str = typer.Argument(...),
    preferred_notes: str = typer.Option("", "--preferred", help="Comma-separated"),
    avoid_allergens: str = typer.Option("", "--avoid", help="Comma-separated"),
):
    """Create a user profile"""
    # Shows profiles that are stored and relevant allergy information.
    profile = UserProfile.new(
   name=name,
   preferred_notes=parse_csv_list(preferred_notes),
   avoid_allergens=parse_csv_list(avoid_allergens),
)
add_profile(profile)
info(f"Profile created: {profile.name}")

@app.command("profiles")
def list_profiles_cmd():
    """List user Profiles"""
    # Displays all saved profiles in a rich table.
    profiles = list_profiles()
    table = Table(title=f"Profiles ({len(profiles)})")
    table.add_column("ID", no_wrap=True)
    table.add_column("Name")
    table.add_column("Preferred Notes")
    table.add_column("Avoid Allergens")
    for pr in profiles:
        table.add_row(
        pr["id"][:8], pr.get("name", ""), ", ".join(pr.get("preferred_notes", [])), ", ".join(pr.get("avoid_allergens", []))
    )
console.print(table)

@app.command()
def recommend_cmd(
    profile_id: Optional[str] = typer.Option(None, "--profile"),
preferred_notes: str = typer.Option("", "--preferred"),
avoid_allergens: str = typer.Option("", "--avoid"),
top_k: int = typer.Option(5, "--top"),
):
    """Recommend perfumes for a profile OR ad-hoc input"""
    # Uses recommender.py to rank perfumes due to personal preference and also flags if there is any allergies in that perfume.
perfumes = list_perfumes()


# Two modes: use a saved profile (by ID) or use the ad‑hoc CLI inputs
if profile_id:
full = _resolve_profile_id(profile_id)
if not full:
return error("No profile found for that ID.")
profile = get_profile(full)
preferred = profile.get("preferred_notes", [])
avoid = profile.get("avoid_allergens", [])
else:
preferred = parse_csv_list(preferred_notes)
avoid = parse_csv_list(avoid_allergens)


# Call the recommender to rank perfumes and show the top K
ranked = recommend(perfumes, preferred, avoid, k=top_k)
if not ranked:
return error("No suitable recommendations found.")


table = Table(title="Recommendations")
table.add_column("Score")
table.add_column("Name")
table.add_column("Brand")
table.add_column("Notes")
table.add_column("Price")
for p, sc in ranked:
table.add_row(f"{sc:.2f}", p["name"], p["brand"], ", ".join(p.get("notes", [])), human_money(p.get("price", 0.0)))
console.print(table)

@app.command()
def export_csv_cmd(path: str = typer.Argument(...)):
 """Export all perfumes to CSV at PATH."""
count = export_csv(path)
info(f"Exported {count} rows to {path}")

@app.command()
def import_csv_cmd(path: str):
    """Import perfumes from CSV"""
    # This reads a CSV file and skips duplicates and adds new entries.
    ...

@app.command()
def seed_minimal():
    """Load a minimal dataset for testing"""
    # This adds 3 sample perfumes into the db for quick testing.
    ...
