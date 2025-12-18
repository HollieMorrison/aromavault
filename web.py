from __future__ import annotations
from flask import Flask, request, jsonify, Response
import json
import typing as t

# Reuse your existing domain logic
import storage
import recommender

app = Flask(__name__)

HOMEPAGE = """<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8"/>
  <meta name="viewport" content="width=device-width, initial-scale=1"/>
  <title>AromaVault</title>
  <style>
    :root { color-scheme: light dark; }
    body { font-family: system-ui, -apple-system, Segoe UI, Roboto, Ubuntu, Cantarell, Noto Sans, sans-serif; margin: 2rem; line-height: 1.5; }
    main { max-width: 800px; margin: 0 auto; }
    h1 { margin-bottom: .25rem; }
    form, .card { border: 1px solid #ccc; padding: 1rem; border-radius: .75rem; margin: 1rem 0; }
    label { display: block; margin: .25rem 0; }
    input, button { font: inherit; padding: .5rem .75rem; }
    code { background: rgba(127,127,127,.15); padding: .1rem .3rem; border-radius: .3rem; }
    .muted { opacity: .7; }
    .grid { display: grid; gap: .75rem; grid-template-columns: repeat(auto-fit, minmax(240px, 1fr)); }
    .pill { display:inline-block; padding:.15rem .5rem; border-radius:999px; border:1px solid #888; font-size:.85rem; margin-right:.35rem;}
    .footer { margin-top: 2rem; font-size: .9rem; opacity: .8; }
  </style>
</head>
<body>
<main>
  <h1>AromaVault</h1>
  <p class="muted">Simple dataset manager for perfumes. This page lets anyone use the app on Heroku.</p>

  <div class="card">
    <h2>Quick Links</h2>
    <p>
      <a href="/api/perfumes">/api/perfumes</a> — list all<br>
      <a href="/api/health">/api/health</a> — health check
    </p>
  </div>

  <div class="card">
    <h2>Search</h2>
    <form action="/api/search" method="get">
      <div class="grid">
        <label>Query <input name="query" placeholder="e.g. vanilla"></label>
        <label>Brand <input name="brand" placeholder="e.g. Dior"></label>
        <label>Notes (any, comma separated) <input name="notes_any" placeholder="vanilla,jasmine"></label>
        <label>Max Price <input name="price_max" placeholder="80"></label>
      </div>
      <button type="submit">Search</button>
    </form>
  </div>

  <div class="card">
    <h2>Recommend</h2>
    <form action="/api/recommend" method="get">
      <div class="grid">
        <label>Preferred notes <input name="preferred_notes" placeholder="vanilla,jasmine"></label>
        <label>Avoid notes <input name="avoid_notes" placeholder="oud,patchouli"></label>
        <label>Brand bias <input name="brand_bias" placeholder="Dior"></label>
        <label>Max Price <input name="price_max" placeholder="70"></label>
        <label>K (results) <input name="k" placeholder="5"></label>
      </div>
      <button type="submit">Recommend</button>
    </form>
  </div>

  <div class="footer">
    <p>Programmatic usage: <code>GET /api/search</code>, <code>GET /api/recommend</code>. See README for examples.</p>
  </div>
</main>
</body>
</html>
"""

def _csv_to_list(s: str | None) -> list[str] | None:
    if not s:
        return None
    return [part.strip() for part in s.split(",") if part.strip()]

@app.get("/")
def homepage() -> Response:
    return Response(HOMEPAGE, mimetype="text/html")

@app.get("/api/health")
def health():
    return {"ok": True, "service": "AromaVault", "version": 1}

@app.get("/api/perfumes")
def list_perfumes():
    # Use your storage helpers directly
    items = storage.list_perfumes()
    return jsonify(items)

@app.get("/api/search")
def search():
    query = request.args.get("query") or None
    brand = request.args.get("brand") or None
    notes_any = _csv_to_list(request.args.get("notes_any"))
    price_max = request.args.get("price_max")
    price_max_f = float(price_max) if price_max else None

    results = storage.search(
        query=query,
        brand=brand,
        notes_any=notes_any,
        price_max=price_max_f,
        path=None,
    )
    return jsonify(results)

@app.get("/api/recommend")
def recommend():
    catalog = storage.list_perfumes()
    preferred_notes = _csv_to_list(request.args.get("preferred_notes"))
    avoid_notes = _csv_to_list(request.args.get("avoid_notes"))
    brand_bias = request.args.get("brand_bias") or None
    price_max = request.args.get("price_max")
    k = request.args.get("k")

    price_max_f = float(price_max) if price_max else None
    k_i = int(k) if k else 5

    results = recommender.recommend(
        catalog=catalog,
        preferred_notes=preferred_notes,
        avoid_notes=avoid_notes,
        brand_bias=brand_bias,
        price_max=price_max_f,
        k=k_i,
    )
    return jsonify(results)
