from flask import Flask, Response, jsonify, request
from markupsafe import escape

try:
    from recommender import recommend
    from storage import list_perfumes

    _import_error = None
except Exception as e:
    recommend = None
    list_perfumes = None
    _import_error = e

app = Flask(__name__)

HOMEPAGE = """<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8"/>
  <title>AromaVault</title>
  <meta name="viewport" content="width=device-width, initial-scale=1"/>
  <style>
    body{font-family:system-ui,-apple-system,Segoe UI,Roboto,Ubuntu,Cantarell,Noto Sans,sans-serif;line-height:1.55;margin:0;background:#0b0e14;color:#e6e6e6}
    header{padding:24px 18px;background:#121722;border-bottom:1px solid #23283b}
    main{max-width:960px;margin:0 auto;padding:24px 18px}
    h1{margin:0 0 4px;font-size:26px}
    h2{margin:18px 0 10px;font-size:20px}
    .muted{color:#9aa4b2}
    .card{background:#121722;border:1px solid #23283b;border-radius:12px;padding:16px;margin:14px 0}
    label{display:block;margin:8px 0 4px}
    input,button{width:100%;padding:10px;border-radius:10px;border:1px solid #23283b;background:#0f1320;color:#e6e6e6}
    button{cursor:pointer}
    .row{display:grid;gap:12px;grid-template-columns:repeat(2,minmax(0,1fr))}
    pre{background:#0f1320;border:1px solid #23283b;border-radius:10px;padding:12px;overflow:auto}
    code{font-family:ui-monospace,Menlo,Consolas,monospace}
    a{color:#93c5fd;text-decoration:none}
    .ok{color:#a7f3d0}
    .error{color:#fecaca}
    @media (max-width:800px){.row{grid-template-columns:1fr}}
  </style>
</head>
<body>
  <header>
    <h1>AromaVault</h1>
    <div class="muted">Public demo — Browser UI + JSON API</div>
  </header>
  <main>
    {BANNER}
    <div class="card">
      <h2>How to Use</h2>
      <ol>
        <li>Click <strong>Hello</strong> to test the API.</li>
        <li>Use <strong>Recommend Perfumes</strong> to get suggestions.</li>
        <li>CLI (one-off): <code>heroku run python run.py hello --app &lt;your-app&gt;</code></li>
      </ol>
    </div>

    <div class="card">
      <h2>Hello</h2>
      <div class="row">
        <div>
          <label for="hello_name">Your name</label>
          <input id="hello_name" value="Hollie"/>
        </div>
        <div style="align-self:end">
          <button id="hello_btn">Say hello</button>
        </div>
      </div>
      <div id="hello_out" class="ok" style="margin-top:10px"></div>
      <details style="margin-top:8px">
        <summary>Show JSON</summary>
        <pre><code id="hello_json">{ }</code></pre>
      </details>
    </div>

    <div class="card">
      <h2>Recommend Perfumes</h2>
      <div class="row">
        <div>
          <label for="pref">Preferred notes (comma-separated)</label>
          <input id="pref" placeholder="rose,jasmine,citrus"/>
        </div>
        <div>
          <label for="avoid">Avoid notes (comma-separated)</label>
          <input id="avoid" placeholder="vanilla,oud"/>
        </div>
      </div>
      <div class="row">
        <div>
          <label for="brand">Brand bias (optional)</label>
          <input id="brand" placeholder="Dior"/>
        </div>
        <div>
          <label for="price">Max price (optional)</label>
          <input id="price" type="number" step="0.01" placeholder="100.00"/>
        </div>
      </div>
      <div class="row">
        <div>
          <label for="k">Number of results</label>
          <input id="k" type="number" min="1" max="20" value="5"/>
        </div>
        <div style="align-self:end">
          <button id="rec_btn">Get recommendations</button>
        </div>
      </div>
      <div id="rec_out" style="margin-top:10px"></div>
      <details style="margin-top:8px">
        <summary>Show JSON</summary>
        <pre><code id="rec_json">{ }</code></pre>
      </details>
    </div>

    <div class="card">
      <h2>API Endpoints</h2>
      <ul>
        <li><code>GET /api/hello?name=Hollie</code></li>
        <li><code>GET /api/recommend?preferred=rose,jasmine&avoid=vanilla&brand=Dior&price_max=120&k=5</code></li>
      </ul>
    </div>
  </main>

  <script>
    const H = (id) => document.getElementById(id);

    H('hello_btn').onclick = async () => {
      const name = encodeURIComponent(H('hello_name').value || '');
      const res = await fetch('/api/hello?name=' + name);
      const data = await res.json();
      H('hello_out').textContent = data.message || JSON.stringify(data);
      H('hello_json').textContent = JSON.stringify(data, null, 2);
    };

    H('rec_btn').onclick = async () => {
      const params = new URLSearchParams();
      if (H('pref').value) params.set('preferred', H('pref').value);
      if (H('avoid').value) params.set('avoid', H('avoid').value);
      if (H('brand').value) params.set('brand', H('brand').value);
      if (H('price').value) params.set('price_max', H('price').value);
      if (H('k').value) params.set('k', H('k').value);

      const res = await fetch('/api/recommend?' + params.toString());
      const data = await res.json();

      const list = Array.isArray(data.results) ? data.results : [];
      const items = list.map((p, i) => {
        const nm = (p && (p.name || (p['name']))) || 'Unnamed';
        const br = (p && (p.brand || p['brand'])) || '';
        const pr = (p && (p.price || p['price'])) || '';
        const btxt = br ? ' • ' + br : '';
        const ptxt = (pr !== '' && pr !== null && pr !== undefined) ? ' • £' + pr : '';
        return '<li>#'+(i+1)+' <strong>'+nm+'</strong>'+btxt+ptxt+'</li>';
      }).join('') || '<li>No results.</li>';

      H('rec_out').innerHTML = '<ol>'+items+'</ol>';
      H('rec_json').textContent = JSON.stringify(data, null, 2);
    };
  </script>
</body>
</html>
"""


@app.get("/")
def index():
    banner = ""
    if _import_error:
        banner = f"<div class='card'><div class='error'>Backend import error: {escape(str(_import_error))}</div></div>"
    html = HOMEPAGE.replace("{BANNER}", banner)
    return Response(html, mimetype="text/html")


@app.get("/api/hello")
def api_hello():
    name = request.args.get("name", "there")
    return jsonify({"message": f"Hello, {name}"})


@app.get("/api/recommend")
def api_recommend():
    if _import_error:
        return jsonify({"error": f"Backend not ready: {_import_error}"}), 500

    preferred = request.args.get("preferred") or ""
    avoid = request.args.get("avoid") or ""
    brand = request.args.get("brand") or None
    price_max = request.args.get("price_max")
    k = request.args.get("k", "5")

    def _split(s):
        return [x.strip() for x in s.split(",") if x.strip()] if s else None

    try:
        preferred_notes = _split(preferred)
        avoid_notes = _split(avoid)
        price_val = float(price_max) if price_max else None
        k_val = max(1, min(20, int(k)))
    except Exception as e:
        return jsonify({"error": f"Invalid parameters: {e}"}), 400

    try:
        catalog = list_perfumes()
        results = recommend(
            catalog=catalog,
            preferred_notes=preferred_notes,
            avoid_notes=avoid_notes,
            brand_bias=brand,
            price_max=price_val,
            k=k_val,
        )
    except Exception as e:
        return jsonify({"error": f"Recommendation failed: {e}"}), 500

    return jsonify({"count": len(results), "results": results})


@app.get("/healthz")
def healthz():
    return jsonify({"ok": True, "imports_ok": _import_error is None})


@app.get("/api/all")
def api_all():
    import json
    from pathlib import Path

    import storage

    p = Path(storage.DEFAULT_DB)
    items = json.loads(p.read_text("utf-8")) if p.exists() and p.read_text().strip() else []
    return {"items": items, "count": len(items)}
