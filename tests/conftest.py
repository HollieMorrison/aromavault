# conftest.py — ensure pytest imports THIS repo's modules
import importlib.util
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

# Import storage normally so tests share the same module instance
import storage  # noqa: F401

# Force-load cli_app from the file path to avoid any weird shadowing by run.py
spec = importlib.util.spec_from_file_location("cli_app", ROOT / "cli_app.py")
cli_app = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(cli_app)
sys.modules["cli_app"] = cli_app

# Tiny debug line (you can delete later)
print(f"DEBUG conftest: cli_app loaded from {getattr(cli_app, '__file__', 'unknown')}")
