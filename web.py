from __future__ import annotations

import shlex
from typing import Tuple

from click.testing import CliRunner
from flask import Flask, jsonify, render_template_string, request

import cli_app
import storage

app = Flask(__name__)


# ---------------------- helpers ----------------------
def run_cli(cmdline: str) -> Tuple[str, int]:
    """Execute your Click CLI (cli_app.app) with a shell-like string."""
    argv = shlex.split(cmdline or "")
    if not argv:
        return "No command provided.\n", 2
    res = CliRunner().invoke(cli_app.app, argv)
    return res.output, int(res.exit_code)


# ---------------------- routes -----------------------
@app.get("/")
def index():
    # Minimal in-page "terminal" UI
    html = r"""
<!doctype html>
<meta charset="utf-8" />
<title>AromaVault — Web Terminal</title>
<style>
  :root { color-scheme: dark; }
  body { font-family: ui-monospace, SFMono-Regular, Menlo, Consolas, monospace; margin: 0; background:#0b0f14; color:#d7e3ff; }
  header { padding: 18px 24px; font-weight: 700; font-size: 22px; background:#0f1620; border-bottom:1px solid #1b2533;}
  main { padding: 16px 20px; max-width: 1100px; margin: 0 auto;}
  .chips { display:flex; flex-wrap:wrap; gap:8px; margin-bottom:12px;}
  .chip { background:#142030; color:#bfe1ff; border:1px solid #223247; padding:6px 10px; border-radius:8px; cursor:pointer; }
  .chip:hover { background:#1a2a3d; }
  #out { background:#0f1620; border:1px solid #1b2533; border-radius:10px; padding:18px; min-height:320px; white-space:pre-wrap; }
  .prompt { display:flex; gap:8px; margin-top:10px; }
  #cmd { flex:1; background:#0f1620; color:#e8f2ff; border:1px solid #1b2533; border-radius:8px; padding:10px; }
  #run { background:#1f6feb; border:none; color:white; padding:10px 14px; border-radius:8px; cursor:pointer; }
  #run:hover { background:#2c7dfc; }
  .helpbox { margin-top:14px; padding:12px; background:#0f1620; border:1px solid #24344a; border-radius:10px; color:#b5c9e6; }
  code { color:#d4e7ff; }
</style>
<header>AromaVault — Web Terminal</header>
<main>
  <div class="chips">
    <div class="chip" onclick="ins('--help')">help</div>
    <div class="chip" onclick="ins('list')">list</div>
    <div class="chip" onclick="ins('find rose')">find rose</div>
    <div class="chip" onclick="ins('add-perf \"Amber Sky\" --brand \"Noctis\" --price 72 --notes \"amber,vanilla\"')">add-perf…</div>
    <div class="chip" onclick="ins('update-perf \"Amber Sky\" --price 80 --stock 5')">update-perf…</div>
    <div class="chip" onclick="ins('show \"Amber Sky\"')">show "Amber Sky"</div>
    <div class="chip" onclick="ins('delete \"Amber Sky\"')">delete "Amber Sky"</div>
    <div class="chip" onclick="clearOut()">clear</div>
  </div>

  <div id="out">AromaVault CLI — type <code>help</code> to list commands.\n</div>

  <div class="prompt">
    <input id="cmd" placeholder='Type "help" to see commands…' />
    <button id="run" onclick="runCmd()">Run</button>
  </div>

  <div class="helpbox">
    <strong>How to use</strong><br><br>
    <u>Add a perfume</u><br>
    <code>add-perf "Amber Sky" --brand "Noctis" --price 72 --notes "amber,vanilla"</code><br><br>

    <u>Update a perfume</u> (by exact <b>name</b> or by <b>id</b>)<br>
    <code>update-perf "Amber Sky" --price 80 --stock 5</code><br>
    <code>update-perf &lt;id&gt; --rating 4.7</code><br><br>

    <u>Find perfumes</u><br>
    <code>find amber</code> &nbsp; (searches name / brand / notes, case-insensitive)<br><br>

    <u>Show one perfume</u><br>
    <code>show "Amber Sky"</code> &nbsp; or &nbsp; <code>show &lt;id&gt;</code><br><br>

    <u>Delete</u><br>
    <code>delete "Amber Sky"</code> &nbsp; or &nbsp; <code>delete &lt;id&gt;</code><br>
  </div>
</main>

<script>
  const out = document.getElementById('out');
  const cmd = document.getElementById('cmd');

  function esc(s){return s.replaceAll('&','&amp;').replaceAll('<','&lt;').replaceAll('>','&gt;');}
  function printLine(s){ out.innerHTML += s; out.scrollTop = out.scrollHeight; }
  function ins(s){ cmd.value = s; cmd.focus(); }
  function clearOut(){ out.innerHTML = ''; }

  async function runCmd(){
    const input = cmd.value.trim();
    if(!input){ return; }
    printLine("\\naromavault> " + esc(input) + "\\n");
    cmd.value = '';
    try{
      const r = await fetch('/api/cli', { method:'POST', headers:{'Content-Type':'application/json'}, body: JSON.stringify({cmd: input}) });
      const j = await r.json();
      printLine(esc(j.output || '') + "\\n");
    }catch(e){
      printLine("Error: " + esc(String(e)) + "\\n");
    }
  }

  cmd.addEventListener('keydown', (ev)=>{ if(ev.key==='Enter'){ runCmd(); } });
</script>
"""
    return render_template_string(html)


@app.post("/api/cli")
def api_cli():
    data = request.get_json(silent=True) or {}
    cmd = (data.get("cmd") or "").strip()
    output, code = run_cli(cmd)
    return jsonify({"ok": code == 0, "exit_code": code, "output": output})


@app.get("/api/perfumes")
def api_perfumes():
    return jsonify(storage.list_perfumes())


@app.post("/api/admin/add")
def api_admin_add():
    data = request.get_json(silent=True) or {}
    notes = data.get("notes")
    if isinstance(notes, str):
        data["notes"] = [n.strip() for n in notes.split(",") if n.strip()]
    return jsonify(storage.add_perfume(data))


@app.post("/api/admin/update")
def api_admin_update():
    """
    JSON:
    {
      "id": "...",          # or "name": "Exact Name"
      "name": "New Name",
      "brand": "New Brand",
      "price": 99.0,
      "notes": "rose,musk"  # or ["rose","musk"]
      "rating": 4.6,
      "stock": 5
    }
    """
    data = request.get_json(silent=True) or {}
    ident = data.get("id") or data.get("name")
    if not ident:
        return jsonify({"ok": False, "error": "id or name is required"}), 400

    allowed = {"name", "brand", "price", "notes", "rating", "stock", "allergens"}
    changes = {k: v for k, v in data.items() if k in allowed}

    # normalise notes
    if "notes" in changes and isinstance(changes["notes"], str):
        changes["notes"] = [n.strip() for n in changes["notes"].split(",") if n.strip()]

    res = storage.update_perfume(ident, changes)
    if isinstance(res, tuple):
        ok, updated = res
    else:
        ok, updated = bool(res), None

    if not ok:
        return jsonify({"ok": False, "error": "not found"}), 404

    return jsonify({"ok": True, "perfume": updated or {}})


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
