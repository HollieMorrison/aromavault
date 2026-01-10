from __future__ import annotations

import shlex

from click.testing import CliRunner
from flask import Flask, jsonify, render_template_string, request

import cli_app
import storage

app = Flask(__name__, static_folder="static", template_folder="templates")
runner = CliRunner()
app.config.setdefault("SEEDED", False)


# ---------- seed-once (safe for Flask 3) ----------
@app.before_request
def seed_once():
    if app.config["SEEDED"]:
        return
    try:
        items = storage.list_perfumes()
        if not items:
            seeder = getattr(storage, "seed_30", None) or storage.seed_minimal
            n = seeder()
            app.logger.info(f"[boot] seeded {n} perfumes")
    except Exception as e:
        app.logger.warning(f"[boot] seeding skipped: {e}")
    finally:
        app.config["SEEDED"] = True


# ---------- JSON API (kept compatible with your app) ----------
@app.get("/api/perfumes")
def api_perfumes():
    return jsonify(storage.list_perfumes())


@app.post("/api/admin/add")
def api_admin_add():
    data = request.get_json(force=True, silent=True) or {}
    name = (data.get("name") or "").strip()
    brand = (data.get("brand") or "").strip()
    price = float(data.get("price") or 0)
    notes = data.get("notes") or []
    if isinstance(notes, str):
        notes = [s.strip() for s in notes.split(",") if s.strip()]
    # delegate to storage to keep single source of truth:
    rec = storage.add_perfume(name=name, brand=brand, price=price, notes=notes)
    # rec might be id or dict depending on your storage; return something useful
    return jsonify({"ok": True, "result": rec})


# ---------- CLI bridge ----------
@app.post("/api/cli")
def api_cli():
    data = request.get_json(silent=True) or {}
    args = data.get("args") or data.get("cmd") or data.get("command") or ""
    if isinstance(args, str):
        s = args.strip()
        argv = ["--help"] if s.lower() == "help" else (shlex.split(s) if s else [])
    else:
        argv = list(args)
    res = runner.invoke(cli_app.app, argv)
    out = (res.output or "").rstrip()
    return jsonify(ok=(res.exit_code == 0), exit_code=res.exit_code, output=out)


# ---------- Terminal-style homepage ----------
INDEX_HTML = r"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8" />
<title>AromaVault — Web Terminal</title>
<meta name="viewport" content="width=device-width, initial-scale=1" />
<style>
:root{--bg:#0d1117;--panel:#0b0f14;--fg:#e6edf3;--muted:#9da7af;--green:#7bd389;--red:#ff8585;--blue:#86b7ff;--border:#1f2630}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--fg);font-family:ui-monospace,SFMono-Regular,Menlo,Consolas,monospace}
header{padding:18px 16px;border-bottom:1px solid var(--border)}
header h1{margin:0 0 6px;font-size:18px}
header p{margin:0;color:var(--muted);font-size:13px}
main{max-width:1000px;margin:0 auto;padding:14px}
.term{background:#0a0e13;border:1px solid var(--border);border-radius:10px;padding:12px;min-height:62vh;display:flex;flex-direction:column}
.out{white-space:pre-wrap;word-break:break-word;flex:1 1 auto;overflow:auto;padding:4px}
.promptline{display:flex;align-items:center;gap:8px;margin-top:8px;border-top:1px solid var(--border);padding-top:8px}
.prompt{color:var(--green)}
input#cmd{flex:1;background:#0f141a;color:var(--fg);border:1px solid var(--border);border-radius:8px;padding:10px;outline:none}
.hint{color:var(--muted);font-size:12px;margin-top:6px}
.btns{display:flex;gap:8px;margin:10px 0 0}
button{background:#10161d;color:var(--fg);border:1px solid var(--border);border-radius:8px;padding:8px 10px;cursor:pointer}
button.primary{color:var(--green);border-color:#243026;background:#0f1512}
.ok{color:var(--green)}
.err{color:var(--red)}
.blue{color:var(--blue)}
.kbd{background:#0c1218;border:1px solid var(--border);padding:2px 6px;border-radius:4px}

/* --- CLI cheat-sheet styles --- */
.cheatsheet{margin:14px 0 8px;padding:12px 14px;border:1px solid #2e2e2e;border-radius:10px;background:#0f1115}
.cheatsheet details>summary{cursor:pointer;font-weight:700;color:#9ae6b4;margin-bottom:8px}
.cheatsheet code,.cheatsheet pre{font-family:ui-monospace, SFMono-Regular, Menlo, Consolas, "Liberation Mono", monospace;
  font-size:13px;white-space:pre-wrap}
.cheatsheet .grid{display:grid;gap:8px}
.cheatsheet .grid .card{padding:8px 10px;border:1px solid #262626;border-radius:8px;background:#0b0d12}
.cheatsheet .label{font-size:12px;color:#a0aec0;margin-bottom:6px;text-transform:uppercase;letter-spacing:.08em}

</style>
</head>
<body>
<header>
  <h1>AromaVault — Web Terminal</h1>
  <p>Try <span class="kbd">help</span>, <span class="kbd">list</span>, <span class="kbd">find rose</span>,
     <span class="kbd">add-perf "Amber Sky" --brand "Noctis" --price 72 --notes "amber,vanilla"</span>,
     <span class="kbd">delete "Amber Sky"</span>, <span class="kbd">seed-minimal</span>, <span class="kbd">seed-30</span>.
     ↑/↓ for history, <span class="kbd">Ctrl+L</span> to clear.

<div class="cheatsheet">
  <details open>
    <summary>How to use the AromaVault CLI (add • find • update • delete)</summary>
    <div class="grid">
      <div class="card">
        <div class="label">Add a perfume</div>
        <pre><code>add-perf "Amber Sky" --brand "Noctis" --price 72 --notes "amber,vanilla"</code></pre>
        <small>Quotes are required when values contain spaces.</small>
      </div>
      <div class="card">
        <div class="label">Find perfumes</div>
        <pre><code>find amber
find "rose musk"</code></pre>
        <small>Searches name, brand, and notes (case-insensitive).</small>
      </div>
      <div class="card">
        <div class="label">Show one</div>
        <pre><code>show "Amber Sky"</code></pre>
        <small>Accepts an exact ID or a name substring.</small>
      </div>
      <div class="card">
        <div class="label">Update rating / stock</div>
        <pre><code>update-perf "Amber Sky" --rating 4.6 --stock 3</code></pre>
        <small>Target by exact name or exact ID.</small>
      </div>
      <div class="card">
        <div class="label">Delete by name or ID</div>
        <pre><code>delete "Amber Sky"</code></pre>
      </div>
      <div class="card">
        <div class="label">Seed sample data</div>
        <pre><code>seed-minimal
seed-30</code></pre>
        <small><i>seed-30</i> falls back to 3 if the large seed isn’t available.</small>
      </div>
    </div>
  </details>
</div>
</p>
</header>
<main>
  <div class="term">
    <div id="out" class="out"></div>
    <div class="promptline">
      <span class="prompt">aromavault&gt;</span>
      <input id="cmd" type="text" placeholder='Type "help" to see commands…' autocomplete="off" />
    </div>
    <div class="btns">
      <button class="primary" id="btn-help">help</button>
      <button id="btn-list">list</button>
      <button id="btn-seed3">seed-minimal</button>
      <button id="btn-seed30">seed-30</button>
      <button id="btn-clear">clear</button>
    </div>
    <div class="hint">This web terminal invokes the same Click CLI as your local app (server-side).</div>
  </div>
</main>
<script>
(function(){
  const out = document.getElementById('out');
  const cmd = document.getElementById('cmd');
  const log = (html)=>{ out.insertAdjacentHTML('beforeend', html); out.scrollTop = out.scrollHeight; };
  const esc = (s)=>s.replace(/[&<>]/g, c=>({ '&':'&amp;','<':'&lt;','>':'&gt;' }[c]));
  log('<span class="blue">AromaVault CLI</span> — type <span class="kbd">help</span> to list commands.\\n');

  let history = []; let hIndex = -1;

  async function run(input){
    if(!input.trim()) return;
    history.push(input); hIndex = history.length;
    log('<span class="prompt">aromavault&gt;</span> '+esc(input)+'\\n');
    const payload = { args: input.trim()==='help' ? '--help' : input };
    try{
      const res = await fetch('/api/cli', { method:'POST', headers:{'Content-Type':'application/json'}, body: JSON.stringify(payload) });
      const data = await res.json();
      const ok = !!(data && data.ok);
      const text = (data && data.output) ? data.output : '(no output)';
      log('<div class="'+(ok?'ok':'err')+'">'+esc(text)+'</div>\\n');
    }catch(e){ log('<div class="err">Request failed.</div>\\n'); }
  }

  cmd.addEventListener('keydown', (e)=>{
    if (e.key === 'Enter'){ run(cmd.value); cmd.value=''; }
    else if(e.key === 'ArrowUp'){ e.preventDefault(); if(hIndex>0){ hIndex--; cmd.value=history[hIndex]||''; cmd.setSelectionRange(cmd.value.length, cmd.value.length);} }
    else if(e.key === 'ArrowDown'){ e.preventDefault(); if(hIndex<history.length){ hIndex++; cmd.value=history[hIndex]||''; cmd.setSelectionRange(cmd.value.length, cmd.value.length);} }
    else if(e.key.toLowerCase() === 'l' && e.ctrlKey){ e.preventDefault(); out.innerHTML=''; }
  });

  document.getElementById('btn-help').onclick = ()=> run('help');
  document.getElementById('btn-list').onclick = ()=> run('list');
  document.getElementById('btn-seed3').onclick = ()=> run('seed-minimal');
  document.getElementById('btn-seed30').onclick = ()=> run('seed-30');
  document.getElementById('btn-clear').onclick = ()=> { out.innerHTML=''; cmd.focus(); };
  cmd.focus();
})();
</script>
</body>
</html>
"""


@app.get("/")
def index():
    return render_template_string(INDEX_HTML)


if __name__ == "__main__":
    app.run(debug=True)
