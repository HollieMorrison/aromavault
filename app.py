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
    """Add a new perfume to the catalogue"""
    # Creates a new perfume and saves it to the JSON database using storage helpers.
    ...

@app.command()
def list_perfumes_cmd(...):
    """List of perfumes with optional filters and sorting method"""
# Filtering perfumes by brands or notes.
...

@app.command()
def update(...):
    """Update a perfume field by ID"""
    # Allows the user to update any single field and includes input validation for numbers
    ...

@app.command()
def remove(pid: str):
    """Delete a perfume by ID"""
    # This will remove a perfume from the database.
    ...

@app.command()
def add_profile_cmd(...):
    """Create a user profile"""
    # Shows profiles that are stored and relevant allergy information.
    ...

@app.command()
def list_profiles_cmd():
    """List user Profiles"""
    # Displays all saved profiles in a rich table.
    ...

@app.command()
def recommend_cmd(...):
    """Recommend perfumes for a profile OR ad-hoc input"""
    # Uses recommender.py to rank perfumes due to personal preference and also flags if there is any allergies in that perfume.
    ...

@app.command()
def export_csv_cmd(path: str):
    """Export all perfumes to CSV"""
    # Writes perfumes from JSON to CSV so its available to view in excel
    ...

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
