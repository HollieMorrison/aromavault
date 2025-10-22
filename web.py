# web.py — Minimal read-only web UI for the AromaVault CLI data

from flask import Flask, jsonify, request, render_template_string
from storage import list_perfumes, list_profiles
from recommender import recommend
from utils import parse_csv_list, human_money

app = Flask(__name__)

INDEX_HTML = """
<!doctype html>
<html>
  <head>
    <meta charset="utf-8" />
    <title>AromaVault</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
      body { font-family: system-ui, -apple-system, Segoe UI, Roboto, Arial, sans-serif; margin: 2rem; }
      .card { max-width: 840px; padding: 1.25rem 1.5rem; border: 1px solid #ddd; border-radius: 12px; }
      code, pre { background: #f6f8fa; padding: .2rem .4rem; border-radius: 6px; }
      table { border-collapse: collapse; width: 100%; }
      th, td { border-bottom: 1px solid #eee; padding: .5rem; text-align: left; }
      small { color: #666; }
      a { color: #0b5fff; }
    </style>
  </head>
  <body>
    <div class="card">
      <h1>🌸 AromaVault</h1>
      <p>This is the lightweight web view for the AromaVault CLI project.</p>
      <p><b>Perfumes in store:</b> {{ count }}</p>

      <h2>Quick links</h2>
      <ul>
        <li><a href="/api/perfumes">/api/perfumes</a> — JSON of all perfumes</li>
        <li><a href="/api/profiles">/api/profiles</a> — JSON of saved profiles</li>
        <li><a href="/api/recommend?preferred=jasmine,amber&avoid=coumarin&top=5">/api/recommend</a> — sample recommendations</li>
      </ul>

      <h2>About</h2>
      <p>Source code: <a href="https://github.com/HollieMorrison/aromavault">GitHub: HollieMorrison/aromavault</a></p>
      <p><small>Note: full functionality (add/update/export etc.) runs via the CLI commands documented in the repo. This web view is for marking and quick read-only checks.</small></p>
    </div>
  </body>
</html>
"""


@app.get("/")
def home():
    return render_template_string(INDEX_HTML, count=len(list_perfumes()))


@app.get("/api/perfumes")
def api_perfumes():
    # Pretty-print money for convenience
    perfumes = list_perfumes()
    out = []
    for p in perfumes:
        q = dict(p)
        q["price_human"] = human_money(p.get("price", 0.0))
        out.append(q)
    return jsonify(out)


@app.get("/api/profiles")
def api_profiles():
    return jsonify(list_profiles())


@app.get("/api/recommend")
def api_recommend():
    preferred = parse_csv_list(request.args.get("preferred", ""))
    avoid = parse_csv_list(request.args.get("avoid", ""))
    top = int(request.args.get("top", 5))
    ranked = recommend(list_perfumes(), preferred, avoid, k=top)
    return jsonify([{"score": float(sc), **p} for (p, sc) in ranked])
