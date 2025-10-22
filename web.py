# web.py — minimal read-only web for AromaVault
from flask import Flask, jsonify, render_template_string, request
from storage import list_perfumes, list_profiles
from recommender import recommend
from utils import parse_csv_list, human_money

app = Flask(__name__)


@app.get("/health")
def health():
    return "OK", 200


@app.get("/")
def home():
    perfumes = list_perfumes()
    html = """
    <h1>🌸 AromaVault</h1>
    <p>Live read-only view for marking.</p>
    <p><b>Perfumes:</b> {{count}}</p>
    <ul>
      <li><a href="/api/perfumes">/api/perfumes</a></li>
      <li><a href="/api/profiles">/api/profiles</a></li>
      <li><a href="/api/recommend?preferred=jasmine,amber&avoid=coumarin&top=5">/api/recommend (sample)</a></li>
      <li><a href="/health">/health</a></li>
    </ul>
    <p>Source: <a href="https://github.com/HollieMorrison/aromavault">GitHub repo</a></p>
    """
    return render_template_string(html, count=len(perfumes))


@app.get("/api/perfumes")
def api_perfumes():
    out = []
    for p in list_perfumes():
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
