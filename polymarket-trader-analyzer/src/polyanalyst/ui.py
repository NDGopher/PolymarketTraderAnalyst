"""Minimal local UI for PolyAnalyst reports + update triggers."""

from __future__ import annotations

import json
import threading
from pathlib import Path

from flask import Flask, redirect, render_template_string, request, url_for

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "data"
REPORTS = DATA / "reports"
SAMPLES = ROOT / "samples"

app = Flask(__name__)
_jobs: dict[str, str] = {}

INDEX = """
<!doctype html>
<html><head><meta charset=utf-8><title>PolyAnalyst</title>
<style>
body{font-family:ui-sans-serif,system-ui;max-width:980px;margin:32px auto;padding:0 16px;background:#0b0f14;color:#e8eef7}
a{color:#7dd3fc} .card{border:1px solid #243041;border-radius:12px;padding:16px;margin:12px 0;background:#121821}
input,button{padding:10px 12px;border-radius:8px;border:1px solid #334155;background:#0f172a;color:#e8eef7}
button{cursor:pointer;background:#0369a1} table{width:100%;border-collapse:collapse} td,th{padding:8px;border-bottom:1px solid #243041;text-align:left}
.muted{color:#94a3b8}
</style></head><body>
<h1>PolyAnalyst</h1>
<p class=muted>Local research UI — browse analyses, update incrementally, add traders.</p>
<div class=card>
  <h3>Analyze / update trader</h3>
  <form method=post action="{{ url_for('analyze') }}">
    <input name=trader placeholder="username or 0x wallet" required style="width:60%">
    <label><input type=checkbox name=full> force full re-pull</label>
    <button type=submit>Run</button>
  </form>
  {% if job %}<p>Job: {{ job }}</p>{% endif %}
</div>
<div class=card>
  <h3>Analyzed traders</h3>
  <table>
    <tr><th>Trader</th><th>Files</th><th>Actions</th></tr>
    {% for t in traders %}
    <tr>
      <td><b>{{ t.name }}</b></td>
      <td class=muted>{{ t.files|join(', ') }}</td>
      <td>
        <a href="{{ url_for('trader', name=t.name) }}">open</a> ·
        <a href="{{ url_for('update', name=t.name) }}">update</a>
      </td>
    </tr>
    {% else %}
    <tr><td colspan=3 class=muted>No reports yet.</td></tr>
    {% endfor %}
  </table>
</div>
{% if comparison %}
<div class=card>
  <h3>Comparison</h3>
  <a href="{{ url_for('raw', name='_comparison', file='comparison.md') }}">Open comparison.md</a>
</div>
{% endif %}
</body></html>
"""

TRADER = """
<!doctype html>
<html><head><meta charset=utf-8><title>{{ name }}</title>
<style>
body{font-family:ui-sans-serif,system-ui;max-width:980px;margin:32px auto;padding:0 16px;background:#0b0f14;color:#e8eef7}
a{color:#7dd3fc} .card{border:1px solid #243041;border-radius:12px;padding:16px;margin:12px 0;background:#121821}
pre{white-space:pre-wrap;background:#0f172a;padding:12px;border-radius:8px;overflow:auto}
</style></head><body>
<p><a href="{{ url_for('index') }}">← all traders</a></p>
<h1>{{ name }}</h1>
<div class=card>
  <h3>Reports</h3>
  <ul>
  {% for f in files %}
    <li><a href="{{ url_for('raw', name=name, file=f) }}">{{ f }}</a></li>
  {% endfor %}
  </ul>
  <p><a href="{{ url_for('update', name=name) }}">Incremental update</a></p>
</div>
{% if preview %}
<div class=card><h3>Autopsy preview</h3><pre>{{ preview }}</pre></div>
{% endif %}
</body></html>
"""


def _list_traders():
    names = set()
    if REPORTS.exists():
        names |= {p.name for p in REPORTS.iterdir() if p.is_dir()}
    if SAMPLES.exists():
        names |= {p.name for p in SAMPLES.iterdir() if p.is_dir() and not p.name.startswith("_")}
    out = []
    for n in sorted(names):
        files = []
        for base in (REPORTS / n, SAMPLES / n):
            if base.exists():
                files.extend(x.name for x in base.glob("*") if x.is_file())
        out.append({"name": n, "files": sorted(set(files))})
    return out


def _run_job(trader: str, full: bool):
    _jobs[trader] = "running"
    try:
        from polyanalyst.autopsy_runner import run_full_autopsy
        from polyanalyst.pipeline import AnalyzerApp

        app_ = AnalyzerApp(DATA)
        run_full_autopsy(app_, trader, force_full=full, classify_maker_taker=True)
        _jobs[trader] = "done"
    except Exception as e:
        _jobs[trader] = f"error: {e}"


@app.get("/")
def index():
    comparison = (SAMPLES / "_comparison" / "comparison.md").exists() or (REPORTS / "_comparison" / "comparison.md").exists()
    return render_template_string(INDEX, traders=_list_traders(), job=request.args.get("job"), comparison=comparison)


@app.post("/analyze")
def analyze():
    trader = request.form.get("trader", "").strip()
    full = bool(request.form.get("full"))
    threading.Thread(target=_run_job, args=(trader, full), daemon=True).start()
    return redirect(url_for("index", job=f"started {trader}"))


@app.get("/trader/<name>")
def trader(name: str):
    files = []
    preview = ""
    for base in (SAMPLES / name, REPORTS / name):
        if base.exists():
            files.extend(x.name for x in base.glob("*") if x.is_file())
            autopsy = base / "autopsy.md"
            if autopsy.exists() and not preview:
                preview = autopsy.read_text()[:12000]
    return render_template_string(TRADER, name=name, files=sorted(set(files)), preview=preview)


@app.get("/update/<name>")
def update(name: str):
    threading.Thread(target=_run_job, args=(name, False), daemon=True).start()
    return redirect(url_for("index", job=f"updating {name}"))


@app.get("/raw/<name>/<file>")
def raw(name: str, file: str):
    for base in (SAMPLES / name, REPORTS / name, SAMPLES / "_comparison", REPORTS / "_comparison"):
        path = base / file if name != "_comparison" else (SAMPLES / "_comparison" / file)
        if name == "_comparison":
            path = SAMPLES / "_comparison" / file
            if not path.exists():
                path = REPORTS / "_comparison" / file
        else:
            path = base / file
        if path.exists() and path.is_file():
            text = path.read_text()
            if file.endswith(".md"):
                return f"<pre style='white-space:pre-wrap;background:#0b0f14;color:#e8eef7;padding:24px'>{text}</pre>"
            return app.response_class(text, mimetype="application/json" if file.endswith(".json") else "text/plain")
    return "Not found", 404


def main():
    app.run(host="127.0.0.1", port=8787, debug=False)


if __name__ == "__main__":
    main()
