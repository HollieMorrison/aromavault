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


