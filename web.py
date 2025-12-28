from __future__ import annotations

import json
from pathlib import Path

from flask import Flask, Response, jsonify, request

import storage

app = Flask(__name__, static_folder="static", static_url_path="/static")


# Seed once per dyno boot / first request (Flask 3 compatible)
@app.before_request
def seed_once():
    if not app.config.get("SEEDED"):
        if not storage.list_perfumes():
            seeder = getattr(storage, "seed_30", None) or storage.seed_minimal
            n = seeder()
            app.logger.info(f"[boot] seeded {n} perfumes")
        app.config["SEEDED"] = True


@app.get("/")
def index() -> Response:
    # super lightweight UI to prove the app works for assessors
    html = """
<!doctype html>
<html lang="en">
<meta charset="utf-8">
<title>AromaVault</title>
<style>
body{font-family:system-ui,Arial,sans-serif;margin:2rem;max-width:920px}
h1{margin:0 0 1rem}
table{border-collapse:collapse;width:100%}
th,td{border:1px solid #ddd;padding:.5rem;text-align:left}
th{background:#f6f8fa}
small{color:#666}
</style>
<h1>AromaVault</h1>
<p><small>Simple demo UI. Data comes from <code>/api/perfumes</code>.</small></p>
<table id="tbl"><thead>
<tr><th>Name</th><th>Brand</th><th>Rating</th><th>Notes</th><th>Price</th></tr>
</thead><tbody></tbody></table>
<script>
async function load(){
  const res = await fetch('/api/perfumes');
  const data = await res.json();
  const tbody = document.querySelector('#tbl tbody');
  tbody.innerHTML = '';
  for (const p of data.items || []) {
    const tr = document.createElement('tr');
    tr.innerHTML = `
      <td>${p.name ?? ''}</td>
      <td>${p.brand ?? ''}</td>
      <td>${(p.rating ?? 0).toFixed ? (p.rating ?? 0).toFixed(1) : (p.rating ?? 0)}</td>
      <td>${(p.notes || []).join(', ')}</td>
      <td>£${Number(p.price ?? 0).toFixed(2)}</td>`;
    tbody.appendChild(tr);
  }
}
load();
</script>
"""
    return Response(html, mimetype="text/html")


@app.get("/api/hello")
def api_hello():
    return jsonify(ok=True)


@app.get("/api/perfumes")
def api_list():
    items = storage.list_perfumes()
    return jsonify(count=len(items), items=items)


def _to_float(x):
    if isinstance(x, (int, float)):
        return float(x)
    if x is None:
        return 0.0
    s = str(x)
    s = s.replace("£", "").replace(",", "").strip()
    try:
        return float(s) if s else 0.0
    except Exception:
        return 0.0


def _to_int(x):
    try:
        return int(str(x).strip())
    except Exception:
        return 0


@app.post("/api/admin/add")
def api_admin_add():
    data = request.get_json(silent=True) or request.form or {}
    name = (data.get("name") or "").strip()
    brand = (data.get("brand") or "").strip()
    notes = [s.strip() for s in (data.get("notes") or "").split(",") if s.strip()]
    payload = {
        "name": name,
        "brand": brand,
        "price": _to_float(data.get("price")),
        "notes": notes,
        "allergens": data.get("allergens") or [],
        "rating": _to_float(data.get("rating")),
        "stock": _to_int(data.get("stock")),
    }
    if not name or not brand:
        return jsonify(ok=False, error="name and brand are required"), 400
    created = storage.add_perfume(payload)
    return jsonify(ok=True, item=created), 200


@app.post("/api/admin/delete")
def api_admin_delete():
    data = request.get_json(silent=True) or request.form or {}
    pid = (data.get("id") or data.get("name") or "").strip()
    if not pid:
        return jsonify(ok=False, error="id or name required"), 400
    ok = storage.delete_perfume(pid)
    return jsonify(ok=bool(ok)), 200


if __name__ == "__main__":
    # local dev run
    app.run(host="0.0.0.0", port=5000, debug=True)
