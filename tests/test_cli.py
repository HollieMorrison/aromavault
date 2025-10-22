from typer.testing import CliRunner

import app as cli_app
import storage

runner = CliRunner()


def test_cli_seed_and_list(tmp_path, monkeypatch):
    monkeypatch.setattr(storage, "DEFAULT_DB", tmp_path / "db.json")

    # seed 3 sample perfumes
    r = runner.invoke(cli_app.app, ["seed-minimal"])
    assert r.exit_code == 0
    # list should show "Perfumes (3)"
    r = runner.invoke(cli_app.app, ["list-perfumes-cmd"])
    assert r.exit_code == 0
    assert "Perfumes (3)" in r.stdout


def test_cli_add_and_find(tmp_path, monkeypatch):
    monkeypatch.setattr(storage, "DEFAULT_DB", tmp_path / "db.json")

    # add one (NAME is positional; others are options)
    r = runner.invoke(
        cli_app.app,
        [
            "add-perf",
            "Rose Dusk",
            "--brand",
            "Floral",
            "--price",
            "55",
            "--notes",
            "rose,musk",
        ],
    )
    assert r.exit_code == 0

    # fuzzy find
    r = runner.invoke(cli_app.app, ["find", "rose"])
    assert r.exit_code == 0
    assert "Rose Dusk" in r.stdout
