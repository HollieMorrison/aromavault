import typer
app = typer.Typer(no_args_is_help=True, add_completion=False)
"""
Shim file for tests that expect `import app`.
Re-exports the Typer app object from run.py.
"""