from flask import Flask, Response

app = Flask(__name__)

HOMEPAGE = """<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8"/>
  <title>AromaVault – CLI App (How to Use)</title>
  <meta name="viewport" content="width=device-width, initial-scale=1"/>
  <style>
    :root{
      --bg:#0b0e14;--panel:#121722;--line:#23283b;--txt:#e6e6e6;--muted:#9aa4b2;--link:#93c5fd;
    }
    *{box-sizing:border-box}
    body{font-family:system-ui,-apple-system,"Segoe UI",Roboto,Ubuntu,Cantarell,"Noto Sans",sans-serif;line-height:1.55;margin:0;background:var(--bg);color:var(--txt)}
    header{padding:32px 20px;background:var(--panel);border-bottom:1px solid var(--line)}
    main{max-width:920px;margin:0 auto;padding:28px 20px}
    h1{margin:0 0 6px 0;font-size:28px}
    h2{margin:22px 0 10px;font-size:22px}
    .muted{color:var(--muted)}
    .card{background:var(--panel);border:1px solid var(--line);border-radius:14px;padding:18px 16px;margin:16px 0}
    pre{background:#0f1320;border:1px solid var(--line);border-radius:10px;padding:12px;overflow:auto}
    code{font-family:ui-monospace,SFMono-Regular,Menlo,Monaco,Consolas,"Liberation Mono","Courier New",monospace}
    a{color:var(--link);text-decoration:none}
    ul{margin:8px 0 0 20px}
    .pill{display:inline-block;padding:2px 8px;border-radius:999px;background:#1b2030;border:1px solid #2b3147;color:#cfe1ff;font-size:12px}
    footer{margin-top:36px;color:var(--muted);font-size:14px}
  </style>
</head>
<body>
  <header>
    <h1>AromaVault</h1>
    <div class="muted">Command-line application • Deployed on Heroku</div>
  </header>
  <main>
    <div class="card">
      <h2>What is this?</h2>
      <p>AromaVault is a <strong>command-line (CLI) app</strong>. This page is a simple landing page.
         To use the app, run the commands below via the Heroku CLI (one-off dynos) or run it locally.</p>
      <span class="pill">Quick tip</span> Copy the commands and paste them into your terminal.
    </div>

    <div class="card">
      <h2>Run on Heroku (no install)</h2>
      <ol>
        <li>Open a terminal and make sure you’re logged in to the Heroku CLI.</li>
        <li>Show CLI help (checks connectivity):</li>
      </ol>
      <pre><code>heroku run python run.py --help --app aromavault-eu</code></pre>
      <ol start="3">
        <li>Run a quick smoke test:</li>
      </ol>
      <pre><code>heroku run python run.py hello --name "Hollie" --app aromavault-eu</code></pre>
      <p class="muted">More commands (e.g. <code>recommend</code>, <code>search</code>, <code>list</code>) will be added to the CLI.</p>
    </div>

    <div class="card">
      <h2>Run locally (developer mode)</h2>
      <pre><code>git clone https://github.com/HollieMorrison/aromavault.git
cd aromavault
python -m venv .venv
source .venv/Scripts/activate     # Windows Git Bash
# or: source .venv/bin/activate   # macOS/Linux
pip install -r requirements.txt
python run.py --help
python run.py hello --name "Hollie"</code></pre>
    </div>

    <div class="card">
      <h2>Troubleshooting</h2>
      <ul>
        <li><strong>No commands listed?</strong> Ensure <code>app.py</code> defines a Typer <code>app</code> and <code>run.py</code> calls it.</li>
        <li><strong>Heroku build fails on requirements?</strong> Make sure <code>requirements.txt</code> has no merge markers or typos.</li>
        <li><strong>“App crashed” on the web page?</strong> That’s normal for CLI apps if started incorrectly. Use <code>heroku run python run.py ...</code>.</li>
      </ul>
    </div>

    <footer>© AromaVault • CLI app • Heroku</footer>
  </main>
</body>
</html>
"""

@app.get("/")
def index():
    return Response(HOMEPAGE, mimetype="text/html")
