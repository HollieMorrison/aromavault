from __future__ import annotations
from flask import Flask, jsonify, request, render_template
import os, storage

app = Flask(__name__, static_folder="static", template_folder="templates")
\n\n@app.before_request
def seed_once():
    if not app.config.get("SEEDED"):
        if not storage.list_perfumes():
            seeder = getattr(storage, "seed_30", None) or storage.seed_minimal
            n = seeder()
            app.logger.info(f"[boot] seeded {n} perfumes")
        app.config["SEEDED"] = True

# Seed once on the first *actual* request (Flask 3+ removed before_first_request)
app.config.setdefault("SEEDED", False)


@app.get("/")
def home():
    return render_template("index.html")

@app.get("/api/perfumes")
def api_list():
    return jsonify(storage.list_perfumes())

@app.get("/api/perfumes/<pid>")
def api_get(pid: str):
    it = storage.get_perfume(pid)
    if not it:
        return jsonify({"error": "not found"}), 404
    return jsonify(it)

@app.post("/api/admin/add")
def api_add():
    data = request.get_json(silent=True) or request.form or {}
    name = (data.get("name") or "").strip()
    brand = (data.get("brand") or "").strip()
    try:
        price = float(data.get("price", 0) or 0)
    except Exception:
        price = 0.0
    notes = [s.strip() for s in (data.get("notes") or "").split(",") if s.strip()]

    if not name or not brand:
        return jsonify({"error": "name and brand are required"}), 400

    created = storage.add_perfume({
        "name": name, "brand": brand, "price": price,
        "notes": notes, "allergens": [], "rating": 0.0, "stock": 0
    })
    return jsonify({"ok": True, "item": created})

@app.post("/api/admin/update")
def api_update():
    data = request.get_json(silent=True) or request.form or {}
    pid = (data.get("id") or "").strip()
    if not pid:
        return jsonify({"error": "id is required"}), 400

    patch = {}
    if "name"   in data: patch["name"]   = (data.get("name") or "").strip()
    if "brand"  in data: patch["brand"]  = (data.get("brand") or "").strip()
    if "notes"  in data:
        raw = data.get("notes")
        patch["notes"] = [s.strip() for s in raw.split(",")] if isinstance(raw, str) else (raw or [])
    if "price"  in data:
        try: patch["price"] = float(data.get("price"))
        except Exception: pass
    if "rating" in data:
        try: patch["rating"] = float(data.get("rating"))
        except Exception: pass
    if "stock"  in data:
        try: patch["stock"] = int(data.get("stock"))
        except Exception: pass

    ok = storage.update_perfume(pid, patch)
    if not ok:
        return jsonify({"error": "not found"}), 404
    return jsonify({"ok": True})

@app.post("/api/admin/delete")
def api_delete():
    data = request.get_json(silent=True) or request.form or {}
    pid = (data.get("id") or "").strip()
    if not pid:
        return jsonify({"error": "id is required"}), 400
    ok = storage.delete_perfume(pid)
    if not ok:
        return jsonify({"error": "not found"}), 404
    return jsonify({"ok": True})

if __name__ == "__main__":
    app.run(debug=True, port=int(os.environ.get("PORT", 5000)))
