import typer

app = typer.Typer(no_args_is_help=True, add_completion=False)
"""
Shim file for tests that expect `import app`.
Re-exports the Typer app object from run.py.
"""


# --- Minimal root command so the CLI has something to run on Heroku ---
@app.callback()
def main():
    """AromaVault command-line interface."""
    # Having a callback makes 'app' a valid command group even with no subcommands.
    pass


# --- Tiny subcommand for smoke test ---
@app.command()
def hello(name: str = "world"):
    """Say hello (deployment smoke test)."""
    import typer

    typer.echo(f"Hello, {name}!")
