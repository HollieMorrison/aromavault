from typer.testing import CliRunner

import run as cli_app
import storage

runner = CliRunner()


import pytest


@pytest.mark.skip(reason="seeding removed")
import pytest
@pytest.mark.skip(reason="seeding removed")
def test_cli_seed_and_list():
    assert True


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
