from flask import Flask, Response

app = Flask(__name__)

HOMEPAGE = """<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8"/>
    <title>AromaVault CLI</title>
    <meta name="viewport" content="width=device-width, initial-scale=1"/>
    <style>
      body{font-family:system-ui,-apple-system,Segoe UI,Roboto,Ubuntu,Cantarell,Noto Sans,sans-serif;
           margin:2rem; line-height:1.6; max-width: 800px;}
      code,pre{background:#f6f8fa; padding:.2rem .4rem; border-radius:.25rem}
      .box{border:1px solid #e5e7eb; border-radius:.75rem; padding:1rem; background:#fff}
    </style>
  </head>
  <body>
    <h1>✅ AromaVault – Python CLI (Heroku)</h1>
    <p>This is a small landing page to keep the Heroku <strong>web dyno</strong> alive.</p>
    <div class="box">
      <p><strong>Run the CLI via one-off dynos:</strong></p>
      <pre>heroku run python run.py --help --app aromavault-eu</pre>
      <pre>heroku run python run.py hello --name Hollie --app aromavault-eu</pre>
    </div>
    <p>Health check: <a href="/health">/health</a></p>
  </body>
</html>"""

@app.get("/")
def index():
    return Response(HOMEPAGE, mimetype="text/html")

@app.get("/health")
def health():
    return {"status": "ok"}
