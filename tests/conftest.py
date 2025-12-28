# conftest.py — ensure local imports and make Typer testing accept Click apps
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

# Import your modules so tests use the same singletons as the CLI
# Make Typer's testing helpers work with a pure Click Group
import click
import typer.testing as tt
from typer.main import get_command as _orig_get_command

import cli_app  # noqa: F401
import storage  # noqa: F401


def _passthrough_get_command(app):
    # If it's already a Click command/group, just return it
    if isinstance(app, click.core.BaseCommand):
        return app
    try:
        return _orig_get_command(app)
    except Exception:
        # Last-resort: return whatever we got (lets Click handle it)
        return app


# Typer's testing invokes _get_command(app) internally; point it to our passthrough.
tt._get_command = _passthrough_get_command  # type: ignore[attr-defined]

# Typer also overwrites CliRunner.invoke; restore Click's original method.
try:
    from click.testing import CliRunner as _ClickRunner

    tt.CliRunner.invoke = _ClickRunner.invoke  # type: ignore[assignment]
except Exception:
    pass

print("DEBUG conftest loaded. cli_app imported from:", getattr(cli_app, "__file__", "<unknown>"))
