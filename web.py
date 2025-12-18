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
    body { font-family: system-ui,-apple-system,Segoe UI,Roboto,Ubuntu,Cantarell,Noto Sans,sans-serif; margin: 2rem; line-height: 1.5; }
    main { max-width: 980px; margin: 0 auto; }
    h1 { margin-bottom: .25rem; }
    .card, form { border: 1px solid #ccc; padding: 1rem; border-radius: .75rem; margin: 1rem 0; }
    label { display:block; margin:.25rem 0; }
    input, button { font: inherit; padding:.5rem .75rem; }
    code { background: rgba(127,127,127,.15); padding:.1rem .3rem; border-radius:.3rem; }
    .muted { opacity:.7; }
    .grid { display:grid; gap:.75rem; grid-template-columns: repeat(auto-fit,minmax(240px,1fr)); }
    .footer { margin-top:2rem; font-size:.9rem; opacity:.8; }
    a.button { display:inline-block; padding:.5rem .8rem; border:1px solid #888; border-radius:.5rem; text-decoration:none; margin-right:.5rem;}
  </style>
</head>
<body>
<main>
  <h1>AromaVault</h1>
  <p class="muted">Simple dataset manager for perfumes. Use the quick links or the forms below.</p>

  <div class="card">
    <h2>Quick Links</h2>
    <p>
      <a class="button" href="/perfumes">View perfumes (HTML)</a>
      <a class="button" href="/api/perfumes?pretty=1">Perfumes (pretty JSON)</a>
      <a class="button" href="/api/perfumes">Perfumes (raw JSON)</a>
      <a class="button" href="/api/health">Health</a>
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
      <button type="submit">Search (JSON)</button>
      <p class="muted">Tip: add <code>?pretty=1</code> to the URL for readable JSON.</p>
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
      <button type="submit">Recommend (JSON)</button>
      <p class="muted">Tip: add <code>?pretty=1</code> to the URL for readable JSON.</p>
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

# ---------- HTML LIST VIEW ----------
@app.get("/perfumes")
def perfumes_html():
    items = storage.list_perfumes()
    def pill(text): return f'<span class="pill">{text}</span>'
    css = """
    <style>
      :root { color-scheme: light dark; }
      body { font-family: system-ui,-apple-system,Segoe UI,Roboto,Ubuntu,Cantarell,Noto Sans,sans-serif; margin:2rem; }
      main { max-width: 1100px; margin:0 auto; }
      h1 { margin-bottom: .25rem; }
      .grid { display:grid; grid-template-columns: repeat(auto-fit,minmax(260px,1fr)); gap:1rem; }
      .card { border:1px solid #ccc; border-radius:.75rem; padding:1rem; }
      .title { font-weight:600; margin-bottom:.25rem; }
      .muted { opacity:.75; font-size:.9rem; }
      .row { margin:.25rem 0; }
      .pill { display:inline-block; padding:.15rem .5rem; border-radius:999px; border:1px solid #888; font-size:.85rem; margin:.15rem .25rem .15rem 0; }
      .bad { border-color:#c44; }
      .top { display:flex; justify-content:space-between; align-items:center; }
    </style>
    """
    cards = []
    for p in items:
        notes = "".join(pill(n) for n in p.get("notes", []))
        allergens = "".join(f'<span class="pill bad">{a}</span>' for a in p.get("allergens", []))
        cards.append(f"""
          <div class="card">
            <div class="top">
              <div class="title">{p.get('name','(no name)')}</div>
              <div class="muted">{p.get('brand','')}</div>
            </div>
            <div class="row">Price: £{p.get('price','')}</div>
            <div class="row">Rating: {p.get('rating','')}</div>
            <div class="row">Stock: {p.get('stock','')}</div>
            <div class="row">Notes: {notes or '<span class="muted">(none)</span>'}</div>
            <div class="row">Allergens: {allergens or '<span class="muted">(none)</span>'}</div>
            <div class="row muted">ID: {p.get('id','')}</div>
          </div>
        """)

    html = f"""<!doctype html>
<html><head><meta charset="utf-8"/><title>AromaVault – Perfumes</title>{css}</head>
<body><main>
  <h1>Perfumes</h1>
  <p class="muted"><a href="/">← Back</a> • Also available as JSON: <a href="/api/perfumes?pretty=1">/api/perfumes?pretty=1</a></p>
  <div class="grid">
    {''.join(cards)}
  </div>
</main></body></html>"""
    return Response(html, mimetype="text/html")

# ---------- JSON API (pretty support) ----------
@app.get("/api/perfumes")
def list_perfumes():
    items = storage.list_perfumes()
    if request.args.get("pretty"):
        return Response(json.dumps(items, indent=2, ensure_ascii=False), mimetype="application/json")
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
    if request.args.get("pretty"):
        return Response(json.dumps(results, indent=2, ensure_ascii=False), mimetype="application/json")
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
    if request.args.get("pretty"):
        return Response(json.dumps(results, indent=2, ensure_ascii=False), mimetype="application/json")
    return jsonify(results)
