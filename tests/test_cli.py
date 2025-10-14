from typer.testing import CliRunner
import importlib

# Import your Typer app object from app.py
app = getattr(importlib.import_module("app"), "app")

runner = CliRunner()

def test_cli_help_displays_usage():
    r = runner.invoke(app, ["--help"])
    assert r.exit_code == 0
    assert "Usage" in r.stdout
