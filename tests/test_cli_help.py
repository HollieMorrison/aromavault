import subprocess, sys

def test_cli_help_exits_zero():
    cp = subprocess.run([sys.executable, "run.py", "--help"], capture_output=True, text=True)
    assert cp.returncode == 0
    assert "Usage:" in cp.stdout
