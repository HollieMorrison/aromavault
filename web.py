from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any

from flask import Flask, Response, jsonify, request

# Use the same DB file as the CLI
import storage  # must expose DEFAULT_DB (a Path or str)

app = Flask(__name__)


# ---------- Helpers ----------
def _db_path() -> Path:
    return Path(storage.DEFAULT_DB)


def _load() -> list[dict[str, Any]]:
    p = _db_path()
    if not p.exists():
        return []
    try:
        return json.loads(p.read_text(encoding="utf-8"))
    except Exception:
        return []


def _save(items: list[dict[str, Any]]) -> None:
    p = _db_path()
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(items, ensure_ascii=False, indent=2), encoding="utf-8")


def _norm_name(s: str) -> str:
    return " ".join(s.strip().split()).lower()


# ---------- Public API (kept for compatibility) ----------
@app.get("/api/perfumes")
def api_list_perfumes():
    return jsonify(_load())


@app.get("/api/hello")
def api_hello():
    name = (request.args.get("name") or "there").strip()
    return jsonify({"message": f"Hello, {name}!"})


@app.get("/api/recommend")
def api_recommend():
    """
    Query params:
      preferred: comma-separated notes to include (e.g. rose,jasmine)
      avoid:     comma-separated notes to avoid (e.g. vanilla,oud)
      brand:     brand bias (optional; if present, prefer those first)
      price_max: float (optional)
      k:         how many results to return (default 5)
    """
    items = _load()

    preferred = [
        x.strip().lower() for x in (request.args.get("preferred") or "").split(",") if x.strip()
    ]
    avoid = [x.strip().lower() for x in (request.args.get("avoid") or "").split(",") if x.strip()]
    brand_bias = (request.args.get("brand") or "").strip().lower()
    price_max = request.args.get("price_max")
    k = int(request.args.get("k") or 5)

    def score(p: dict[str, Any]) -> float:
        s = 0.0
        notes = [n.lower() for n in p.get("notes", [])]
        # +2 per preferred note present
        for n in preferred:
            if n in notes:
                s += 2.0
        # -3 per avoided note present
        for n in avoid:
            if n in notes:
                s -= 3.0
        # small boost if brand matches bias
        if brand_bias and p.get("brand", "").lower() == brand_bias:
            s += 1.0
        return s

    filtered: list[dict[str, Any]] = items
    if price_max:
        try:
            pm = float(price_max)
            filtered = [p for p in filtered if float(p.get("price", 0)) <= pm]
        except ValueError:
            pass

    ranked = sorted(filtered, key=score, reverse=True)[:k]
    return jsonify(ranked)


# ---------- Admin API (new) ----------
@app.post("/api/admin/add")
def api_admin_add():
    data = request.get_json(silent=True) or request.form
    name = (data.get("name") or "").strip()
    brand = (data.get("brand") or "").strip()
    price = (data.get("price") or "").strip()
    notes_raw = (data.get("notes") or "").strip()

    if not name or not brand or not price:
        return jsonify({"ok": False, "error": "name, brand and price are required"}), 400

    try:
        price_f = float(price)
    except ValueError:
        return jsonify({"ok": False, "error": "price must be a number"}), 400

    notes = [n.strip() for n in notes_raw.split(",") if n.strip()]

    items = _load()
    # if exists, replace; else append
    idx = next(
        (i for i, p in enumerate(items) if _norm_name(p.get("name", "")) == _norm_name(name)), None
    )
    new_item = {
        "id": p_id(name, brand),
        "name": name,
        "brand": brand,
        "price": price_f,
        "notes": notes,
        "allergens": p_allergens(notes),
        "stock": str(p_stock(items, name)),  # keep type aligned with your seed format
        "rating": p_rating(items, name),
    }
    if idx is not None:
        items[idx] = new_item
        action = "updated"
    else:
        items.append(new_item)
        action = "added"

    _save(items)
    return jsonify({"ok": True, "action": action, "item": new_item})


@app.post("/api/admin/delete")
def api_admin_delete():
    data = request.get_json(silent=True) or request.form
    name = (data.get("name") or "").strip()
    if not name:
        return jsonify({"ok": False, "error": "name is required"}), 400

    items = _load()
    before = len(items)
    items = [p for p in items if _norm_name(p.get("name", "")) != _norm_name(name)]
    removed = before - len(items)
    _save(items)
    return jsonify({"ok": True, "removed": removed})


# Helpers for admin defaults (simple stubs)
def p_id(name: str, brand: str) -> str:
    # simple deterministic id
    base = f"{brand}:{name}".encode()
    import hashlib

    return hashlib.sha1(base).hexdigest()[:24]


def p_allergens(notes: list[str]) -> list[str]:
    # trivial example: if oakmoss present, mark as allergen
    lowers = [n.lower() for n in notes]
    return ["oakmoss"] if "oakmoss" in lowers else []


def p_stock(items: list[dict[str, Any]], name: str) -> int:
    # default 5; if replacing, preserve stock if present
    for p in items:
        if _norm_name(p.get("name", "")) == _norm_name(name):
            try:
                return int(p.get("stock", 5))
            except Exception:
                return 5
    return 5


def p_rating(items: list[dict[str, Any]], name: str) -> str:
    # keep empty string if not previously set
    for p in items:
        if _norm_name(p.get("name", "")) == _norm_name(name):
            return str(p.get("rating", ""))
    return ""


# ---------- Health ----------
@app.get("/healthz")
def healthz():
    return jsonify({"ok": True})


# ---------- Homepage ----------
@app.get("/")
def index():
    # single-file dark UI with Admin panel
    html = """
<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1"/>
<title>AromaVault</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600&display=swap" rel="stylesheet">
<style>
:root { --bg:#0b0e12; --panel:#141a22; --muted:#9fb1c1; --text:#eaf2f8; --accent:#7bd389; --danger:#ff7a7a; }
* { box-sizing: border-box; font-family: Inter, system-ui, -apple-system, Segoe UI, Roboto, Helvetica, Arial, sans-serif; }
body { margin:0; background:var(--bg); color:var(--text); }
.wrapper { max-width:1100px; margin:48px auto; padding:0 20px; }
.card { background:var(--panel); border:1px solid #1f2730; border-radius:14px; padding:22px; margin:18px 0; }
h1 { font-size:28px; margin:0 0 8px; }
h2 { font-size:20px; margin:0 0 12px; }
label { display:block; font-size:13px; color:var(--muted); margin:8px 0 6px; }
input, select { width:100%; background:#0f141a; color:var(--text); border:1px solid #273241; border-radius:10px; padding:10px 12px; }
button { background:var(--accent); color:#0a0f0c; font-weight:600; border:0; padding:10px 14px; border-radius:10px; cursor:pointer; }
button.secondary { background:#243140; color:var(--text); }
button.danger { background:var(--danger); color:#250b0b; }
.row { display:grid; grid-template-columns:1fr 1fr; gap:14px; }
small.muted { color:var(--muted); }
code.inline { background:#0f141a; padding:2px 6px; border-radius:6px; border:1px solid #273241; }
ul.clean { padding-left:16px; margin:8px 0; }
.table { width:100%; border-collapse:collapse; font-size:14px; }
.table th, .table td { border-bottom:1px solid #273241; padding:8px 6px; text-align:left; }
pre.json { background:#0f141a; padding:12px; border-radius:10px; border:1px solid #273241; max-height:260px; overflow:auto; }
@media (max-width: 800px) { .row { grid-template-columns:1fr; } }
</style>
</head>
<body>
<div class="wrapper">

  <div class="card">
    <h1>AromaVault</h1>
    <p><strong>How to Use</strong></p>
    <ul class="clean">
      <li>1) Click <em>Hello</em> to test the API.</li>
      <li>2) Use <em>Recommend Perfumes</em> to get suggestions.</li>
      <li>3) See the full catalogue at <code class="inline">/api/perfumes</code>.</li>
      <li>4) Admin (below): add/delete perfumes and view the list.</li>
    </ul>
  </div>

  <!-- Hello -->
  <div class="card">
    <h2>Hello</h2>
    <div class="row">
      <div>
        <label>Your name</label>
        <input id="helloName" value="Hollie" />
      </div>
      <div style="align-self:end;">
        <button onclick="sayHello()">Say hello</button>
      </div>
    </div>
    <details style="margin-top:12px;">
      <summary>Show JSON</summary>
      <pre id="helloOut" class="json">{}</pre>
    </details>
  </div>

  <!-- Recommend -->
  <div class="card">
    <h2>Recommend Perfumes</h2>
    <div class="row">
      <div>
        <label>Preferred notes (comma-separated)</label>
        <input id="pref" placeholder="rose,jasmine,citrus" />
      </div>
      <div>
        <label>Avoid notes (comma-separated)</label>
        <input id="avoid" placeholder="vanilla,oud" />
      </div>
    </div>
    <div class="row">
      <div>
        <label>Brand bias (optional)</label>
        <input id="brand" placeholder="Dior" />
      </div>
      <div>
        <label>Max price (optional)</label>
        <input id="priceMax" placeholder="100.00" />
      </div>
    </div>
    <div class="row">
      <div>
        <label>Number of results</label>
        <input id="k" value="10" />
      </div>
      <div style="align-self:end;">
        <button onclick="getRecs()">Get recommendations</button>
      </div>
    </div>
    <details style="margin-top:12px;">
      <summary>Show JSON</summary>
      <pre id="recsOut" class="json">[]</pre>
    </details>
  </div>

  <!-- Admin -->
  <div class="card">
    <h2>Admin – Manage Perfumes</h2>
    <div class="row">
      <div>
        <label>Name</label>
        <input id="pName" placeholder="Amber Bloom" />
      </div>
      <div>
        <label>Brand</label>
        <input id="pBrand" placeholder="AromaVault" />
      </div>
    </div>
    <div class="row">
      <div>
        <label>Price</label>
        <input id="pPrice" placeholder="59" />
      </div>
      <div>
        <label>Notes (comma-separated)</label>
        <input id="pNotes" placeholder="amber,vanilla,musk" />
      </div>
    </div>
    <div style="margin-top:12px; display:flex; gap:10px;">
      <button onclick="addPerf()">Add / Update</button>
      <button class="danger" onclick="delPerf()">Delete by name</button>
      <button class="secondary" onclick="loadAll()">Refresh list</button>
    </div>

    <div style="margin-top:16px;">
      <h3 style="margin:0 0 8px;">Catalogue</h3>
      <table class="table" id="perfTable">
        <thead>
          <tr><th>Name</th><th>Brand</th><th>Price</th><th>Notes</th></tr>
        </thead>
        <tbody></tbody>
      </table>
      <details style="margin-top:10px;">
        <summary>Show JSON</summary>
        <pre id="listOut" class="json">[]</pre>
      </details>
    </div>
  </div>

</div>

<script>
async function sayHello() {
  const name = document.getElementById('helloName').value.trim() || 'there';
  const r = await fetch(`/api/hello?name=${encodeURIComponent(name)}`);
  const j = await r.json();
  document.getElementById('helloOut').textContent = JSON.stringify(j, null, 2);
}

async function getRecs() {
  const qs = new URLSearchParams();
  const pref = document.getElementById('pref').value.trim();
  const avoid = document.getElementById('avoid').value.trim();
  const brand = document.getElementById('brand').value.trim();
  const priceMax = document.getElementById('priceMax').value.trim();
  const k = document.getElementById('k').value.trim() || '5';
  if (pref) qs.set('preferred', pref);
  if (avoid) qs.set('avoid', avoid);
  if (brand) qs.set('brand', brand);
  if (priceMax) qs.set('price_max', priceMax);
  qs.set('k', k);
  const r = await fetch(`/api/recommend?${qs.toString()}`);
  const j = await r.json();
  document.getElementById('recsOut').textContent = JSON.stringify(j, null, 2);
}

async function loadAll() {
  const r = await fetch('/api/perfumes');
  const items = await r.json();
  document.getElementById('listOut').textContent = JSON.stringify(items, null, 2);
  const tbody = document.querySelector('#perfTable tbody');
  tbody.innerHTML = '';
  items.forEach(p => {
    const tr = document.createElement('tr');
    tr.innerHTML = `<td>${p.name||''}</td><td>${p.brand||''}</td><td>£${p.price}</td><td>${(p.notes||[]).join(', ')}</td>`;
    tbody.appendChild(tr);
  });
}

async function addPerf() {
  const name = document.getElementById('pName').value.trim();
  const brand = document.getElementById('pBrand').value.trim();
  const price = document.getElementById('pPrice').value.trim();
  const notes = document.getElementById('pNotes').value.trim();
  const r = await fetch('/api/admin/add', {
    method:'POST',
    headers:{'Content-Type':'application/json'},
    body: JSON.stringify({name, brand, price, notes})
  });
  const j = await r.json();
  alert(j.ok ? `Saved: ${j.item.name} (${j.action})` : `Error: ${j.error||'unknown'}`);
  await loadAll();
}

async function delPerf() {
  const name = document.getElementById('pName').value.trim();
  if (!name) return alert('Enter a name to delete.');
  const r = await fetch('/api/admin/delete', {
    method:'POST',
    headers:{'Content-Type':'application/json'},
    body: JSON.stringify({name})
  });
  const j = await r.json();
  alert(j.ok ? `Removed: ${j.removed}` : `Error: ${j.error||'unknown'}`);
  await loadAll();
}

loadAll();
</script>

</body>
</html>
    """
    return Response(html, mimetype="text/html")


# Heroku entry point
app = app

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
