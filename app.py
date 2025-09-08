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
def add_perf(...):
    """Add a new perfume to the catalogue."""
    # Creates a new perfume and saves it to the JSON database using storage helpers.
    ...

@app.command()
def list_perfumes_cmd(...):
    """List of perfumes with optional filters and sorting method"""
# Filtering perfumes by brands or notes.
...

@app.command()
def update(...):
    """Update a perfume field by ID."""
    # Allows the user to update any single field and includes input validation for numbers
    ...

@app.command()
def remove(pid: str):
    """Delete a perfume by ID."""
    # This will remove a perfume from the database.
    ...
