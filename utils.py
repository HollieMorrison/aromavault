from typing import list
from rich.console import Console

# Reusable console instance for styled output
_console = Console()


def parse_csv_list(value: str) -> list[str]:
    """Turn a comma-separated string into a clean list; handle empty input safely."""
    if not value:
        return []
    return [x.strip() for x in value.split(",") if x.strip()]


def human_money(v: float) -> str:
    """Format a number as a currency string (GBP by default)."""
    return f"£{v:,.2f}"


def info(msg: str) -> None:
    """Print a success/info line in green."""
    _console.print(f"[bold green]✔ {msg}")


def error(msg: str) -> None:
    """Print an error line in red."""
    _console.print(f"[bold red]✖ {msg}")
