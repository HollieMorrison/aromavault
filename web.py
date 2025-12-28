from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any

from flask import Flask, Response, jsonify, request

# Use the same DB file as the CLI
import storage  # must expose DEFAULT_DB (a Path or str)

app = Flask(__name__)


def _ensure_seed_on_boot():
    try:
        import storage

        if not storage.list_perfumes():
            storage.seed_minimal()
            print("[boot] seeded minimal data")
    except Exception as e:
        print("[boot] seed skipped:", e)


_ensure_seed_on_boot()


# --- ensure we have data when the dyno (ephemeral FS) restarts ---------------
def ensure_seed_on_boot():
    try:
        import storage

        if not storage.list_perfumes():
            storage.seed_minimal()
    except Exception as e:
        print("Boot seed skipped:", e)


ensure_seed_on_boot()


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

    price_raw = data.get("price", 0)
    try:
        price = float(price_raw)
    except Exception:
        try:
            price = float(str(price_raw).replace("£", "").replace(",", "").strip() or 0)
        except Exception:
            price = 0.0

    notes_raw = data.get("notes") or []
    if isinstance(notes_raw, str):
        notes_list = [s.strip() for s in notes_raw.split(",") if s.strip()]
    elif isinstance(notes_raw, list):
        notes_list = [str(s).strip() for s in notes_raw if str(s).strip()]
    else:
        notes_list = []

    stock_raw = data.get("stock", 0)
    try:
        stock = int(stock_raw)
    except Exception:
        try:
            stock = int(str(stock_raw).replace(",", "").strip() or 0)
        except Exception:
            stock = 0

    rating_raw = data.get("rating", 0)
    try:
        rating = float(rating_raw)
    except Exception:
        rating = 0.0

    item = {
        "name": name,
        "brand": brand,
        "price": price,
        "notes": notes_list,
        "allergens": [],
        "stock": stock,
        "rating": rating,
    }

    # Prefer add_or_update_perfume if available; else fall back to add_perfume
    if hasattr(storage, "add_or_update_perfume"):
        ok, err = storage.add_or_update_perfume(item)
        if not ok:
            return jsonify({"ok": False, "error": err, "item": None}), 400
        try:
            created = next(
                (
                    it
                    for it in storage.list_perfumes()
                    if it.get("name") == name and it.get("brand") == brand
                ),
                item,
            )
        except Exception:
            created = item
    else:
        created = storage.add_perfume(item)

    return jsonify({"ok": True, "error": None, "item": created})
