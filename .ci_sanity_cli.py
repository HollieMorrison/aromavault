from click.testing import CliRunner
import cli_app

runner = CliRunner()

print("=== CLI TYPE:", type(cli_app.app))
h = runner.invoke(cli_app.app, ["--help"])
print("=== --help exit:", h.exit_code)
print("=== --help output START ===")
print(h.output)
print("=== --help output END ===")

r1 = runner.invoke(cli_app.app, ["seed-minimal"])
print("=== seed-minimal exit:", r1.exit_code, "output:", r1.output.strip())

r2 = runner.invoke(cli_app.app, ["add-perf","Rose Dusk","--brand","Floral","--price","55","--notes","rose,musk"])
print("=== add-perf exit:", r2.exit_code, "output:", r2.output.strip())
