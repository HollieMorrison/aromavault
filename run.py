from cli_app import app  # re-export Click group as "app"

if __name__ == "__main__":
    # Allow local manual runs: python run.py --help
    app()
