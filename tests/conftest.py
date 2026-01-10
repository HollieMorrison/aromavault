# Ensure pytest imports THIS repo's modules (repo root first on sys.path)
import sys, pathlib
ROOT = pathlib.Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

# Import local modules so tests see the same singletons as the CLI
import storage  # noqa: F401
import cli_app  # noqa: F401

# Optional: make Typer's test helper accept Click apps (harmless if unused)
try:
    import click
    import typer
    from typer.main import get_command as _orig_get_command

    def _get_command(app):
        # If it's a Click command/group, just return it unchanged
        if isinstance(app, click.BaseCommand):
            return app
        return _orig_get_command(app)

    # Patch Typer's internal testing getter (no-op if not used)
    typer.testing._get_command = _get_command  # type: ignore[attr-defined]
except Exception:
    pass
