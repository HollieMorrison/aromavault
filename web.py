from flask import Flask, Response, request, jsonify
from markupsafe import escape

# Import your existing logic so the web can call the same core as the CLI
try:
    from recommender import recommend
    from storage import list_perfumes
except Exception as e:
    # Fallbacks so the app still boots with a helpful error on UI
    recommend = None
    list_perfumes = None
    _import_error = e
else:
    _import_error = None

app = Flask(__name__)

HOMEPAGE = """<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8"/>
  <title>AromaVault – Try it in your browser</title>
  <meta name="viewport" content="width=device-width, initial-scale=1"/>
  <style>
    :root{
      --bg:#0b0e14;--panel:#121722;--line:#23283b;--txt:#e6e6e6;--muted:#9aa4b2;--link:#93c5fd;--accent:#a7f3d0;
    }
    *{box-sizing:border-box}
    body{font-family:system-ui,-apple-system,"Segoe UI",Roboto,Ubuntu,Cantarell,"Noto Sans",sans-serif;line-height:1.55;margin:0;background:var(--bg);color:var(--txt)}
    header{padding:28px 20px;background:var(--panel);border-bottom:1px solid var(--line)}
    main{max-width:1000px;margin:0 auto;padding:28px 20px}
    h1{margin:0 0 6px 0;font-size:28px}
    h2{margin:22px 0 10px;font-size:22px}
    .muted{color:var(--muted)}
    .card{background:var(--panel);border:1px solid var(--line);border-radius:14px;padding:18px 16px;margin:16px 0}
    label{display:block;margin:8px 0 4px}
    input,select,button,textarea{width:100%;padding:10px;border-radius:10px;border:1px solid var(--line);background:#0f1320;color:var(--txt)}
    button{cursor:pointer}
    .row{display:grid;gap:12px;grid-template-columns:repeat(2,minmax(0,1fr))}
    pre{background:#0f1320;border:1px solid var(--line);border-radius:10px;padding:12px;overflow:auto}
    code{font-family:ui-monospace,SFMono-Regular,Menlo,Monaco,Consolas,"Liberation Mono","Courier New",monospace}
    a{color:var(--link);text-decoration:none}
    .ok{color:var(--accent)}
    .error{color:#fecaca}
    .pill{display:inline-block;padding:2px 8px;border-radius:999px;background:#1b2030;border:1px solid #2b3147;color:#cfe1ff;font-size:12px}
    footer{margin-top:36px;color:var(--muted);font-size:14px}
    .grid{display:grid;gap:10px}
    @media (max-width:800px){.row{grid-template-columns:1fr}}
  </style>
</head>
<body>
  <header>
    <h1>AromaVault</h1>
    <div class="muted">Public demo • Browser UI + JSON API • Backed by the same Python logic as the CLI</div>
  </header>
  <main>
    <div class="card">
      <h2>Quick Start</h2>
      <p>Use the forms below (no login needed). The page calls public JSON endpoints hosted on Heroku.</p>
      <ul>
        <li><strong>Hello test:</strong> send your name, get a greeting.</li>
        <li><strong>Recommend perfumes:</strong> choose notes/filters, get top matches.</li>
      </ul>
      <span class="pill">Tip</span> Click <em>Show JSON</em> to see the raw API response.
    </div>

    <div class="card">
      <h2>Hello (smoke test)</h2>
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
      <div class="grid">
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
    </div>

    <div class="card">
      <h2>API Endpoints</h2>
      <ul>
        <li><code>GET /api/hello?name=Hollie</code></li>
        <li><code>GET /api/recommend?preferred=rose,jasmine&avoid=vanilla&brand=Dior&price_max=120&k=5</code></li>
      </ul>
      <p class="muted">These return JSON and are safe to share with anyone.</p>
    </div>

    <footer>© AromaVault • Public web/API demo • Backed by Python</footer>
  </main>

  <script>
    const H = (id) => document.getElementById(id);

    // Hello
    H('hello_btn').onclick = async () => {
      const name = encodeURIComponent(H('hello_name').value || '');
      const res = await fetch('/api/hello?name=' + name);
      const data = await res.json();
      H('hello_out').textContent = data.message || JSON.stringify(data);
      H('hello_json').textContent = JSON.stringify(data, null, 2);
    };

    // Recommend
    H('rec_btn').onclick = async () => {
      const params = new URLSearchParams();
      if (H('pref').value) params.set('preferred', H('pref').value);
      if (H('avoid').value) params.set('avoid', H('avoid').value);
      if (H('brand').value) params.set('brand', H('brand').value);
      if (H('price').value) params.set('price_max', H('price').value);
      if (H('k').value) params.set('k', H('k').value);

      const res = await fetch('/api/recommend?' + params.toString());
      const data = await res.json();

      // Render simple HTML result
      const items = (data.results || []).map((p, i) => {
        const price = (p.price is NaN || p.price===undefined) ? '' : ` • £${p.price}`;
        const brand = p.brand ? ` • ${p.brand}` : '';
        return `<li>#${i+1} <strong>${p.get('name', 'Unnamed')}</strong>${brand}${price}</li>`;
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
    # If imports failed, show a helpful banner (but still serve the page)
    if _import_error:
        banner = f"<p class='error'>Backend import error: {escape(str(_import_error))}</p>"
        html = HOMEPAGE.replace("<main>", "<main>" + banner)
        return Response(html, mimetype="text/html")
    return Response(HOMEPAGE, mimetype="text/html")

# -------- Public JSON API (no auth) --------

@app.get("/api/hello")
def api_hello():
    name = request.args.get("name", "there")
    return jsonify({"message": f"Hello, {name} ���"})

@app.get("/api/recommend")
def api_recommend():
    if _import_error:
        return jsonify({"error": f"Backend not ready: {_import_error}"}), 500

    # Collect params
    preferred = request.args.get("preferred") or ""
    avoid = request.args.get("avoid") or ""
    brand = request.args.get("brand") or None
    price_max = request.args.get("price_max")
    k = request.args.get("k", "5")

    # Parse
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

# Health check
@app.get("/healthz")
def healthz():
    return jsonify({"ok": True, "imports_ok": _import_error is None})
