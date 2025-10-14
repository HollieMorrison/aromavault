from typer.testing import CliRunner
import app

runner = CliRunner()


def test_cli_help():
    result = runner.invoke(app.app, ["--help"])
    assert result.exit_code == 0
    assert "Usage" in result.stdout


def test_invalid_menu_input():

    result = runner.invoke(app.app, ["recommend", "--note", ""])
    assert result.exit_code != 0 or "invalid" in result.stdout.lower()
