# AromaVault – Simple Perfume Manager (CLI + API + Web)

AromaVault is a small Python project that lets you **store, search and recommend perfumes**.  
It has three parts:

- a **command-line tool** (CLI) for quick admin work  
- a **JSON-based REST API** for programmatic access  
- a **tiny web page** (one file) for demo/testing

It’s purposely simple and easy to read. It uses a **JSON file** for data (no real database needed for this project).

- **Live app:** https://aromavault-eu-e54dae1bad1f.herokuapp.com  
- **Repository:** https://github.com/HollieMorrison/aromavault

---

## What the app does

- Shows a **list of perfumes**.
- Lets a user **get recommendations** based on notes they like/avoid, brand, and price.
- Lets an admin **add** a new perfume or **delete** an existing one.
- Offers the same actions by **API** and **CLI**.

This meets the Python Essentials brief: a data model, features to manage/query the data, input validation, and a working CLI/Web interface with deployment.

---

## Run locally

**Requirements:** Python 3.12+ (3.13 works), pip, terminal.

```bash
# 1) Clone and enter
git clone https://github.com/HollieMorrison/aromavault
cd aromavault

# 2) Create a virtual environment
python -m venv .venv
# Windows:
.venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate

# 3) Install requirements
pip install -r requirements.txt

# 4) Run the server locally
python run.py
# Open http://127.0.0.1:5000 in your browser
Data is kept in data.json in the project root. Seeds are included so the list is never empty.

CLI (Command Line)
The CLI is defined in cli_app.py (Typer/Click).

bash
Copy code
# Show commands
python -m cli_app --help

# Seed demo perfumes
python -m cli_app seed-minimal
# -> "Seeded 3 perfumes into data.json"

# Add a perfume (name is positional; others are options)
python -m cli_app add-perf "Rose Dusk" --brand Floral --price 55 --notes "rose,musk"
# -> "Added 'Rose Dusk' by Floral (£55.0) to data.json"
Tip: run pytest -q to check the provided tests.

API (JSON)
All endpoints live in web.py. Base URL is your local server or Heroku.

List perfumes
bash
Copy code
GET /api/perfumes
GET /api/perfumes?pretty=1
Search perfumes
sql
Copy code
GET /api/search?query=rose&price_max=80
Recommendations
bash
Copy code
GET /api/recommend
GET /api/recommend?preferred=rose,jasmine&avoid=vanilla&brand=Dior&price_max=120&k=5
Admin add
pgsql
Copy code
POST /api/admin/add
Content-Type: application/json
{
  "name": "Citrus Spark",
  "brand": "AromaVault",
  "price": 39.5,
  "notes": ["citrus", "bergamot", "musk"]
}
Admin delete
pgsql
Copy code
POST /api/admin/delete
Content-Type: application/json
{ "id": "citrus-spark" }
Quick cURL
bash
Copy code
BASE="https://aromavault-eu-e54dae1bad1f.herokuapp.com"

curl -s "$BASE/api/perfumes?pretty=1"
curl -s "$BASE/api/search?query=rose"
curl -s "$BASE/api/recommend?preferred=rose,jasmine&avoid=vanilla&k=5"

curl -s -X POST "$BASE/api/admin/add" \
  -H "Content-Type: application/json" \
  -d '{"name":"Citrus Spark","brand":"AromaVault","price":39.5,"notes":["citrus","bergamot","musk"]}'

curl -s -X POST "$BASE/api/admin/delete" \
  -H "Content-Type: application/json" \
  -d '{"id":"citrus-spark"}'
Web page (UI)
The homepage (/) is a single HTML string inside web.py. It includes:

“Say hello” demo → /api/hello

Recommendations form → /api/recommend

Admin Add/Delete → /api/admin/*

A live All perfumes list → /api/perfumes

If buttons don’t respond:

open DevTools → Console to see JS/network errors,

check Network tab to confirm APIs return 200.

Data model (JSON file)
data.json stores a list of perfume objects:

json
Copy code
{
  "id": "floral-rose-dusk",
  "name": "Rose Dusk",
  "brand": "Floral",
  "price": 55.0,
  "notes": ["rose", "musk"],
  "rating": 4.4,
  "stock": 7,
  "allergens": ["oakmoss"]
}
Rules

id must be unique (auto-generated if missing).

price must be numeric.

notes can be "rose,musk" or ["rose","musk"].

How the recommender works (simple + explainable)
Optional filters:

brand (case-insensitive match)

price_max (≤ max price)

Score:

+1 for each preferred note

−1 for each avoided note

tie-break: cheaper first, then higher rating

Return top k (default 10)

Validation & errors
Required for add: name, brand, price, notes

Types: price must be a number; notes list or comma-string

Responses:

success → {"ok": true, ...}

bad input → {"ok": false, "error": "message"} (HTTP 400)

not found on delete → HTTP 404

Tech stack
Python (Flask, Typer/Click)

Gunicorn (Heroku)

JSON file storage

Black + Ruff (code quality)

Pytest (tests)

Assessment mapping (what this project covers)
LO1 – Implement an algorithm

Recommender + filtering implemented and explained; code formatted with Black.

LO2 – Adapt/combine algorithms

Scoring + filters + tie-breakers; input handling for empty/invalid cases.

LO3 – Programming constructs

Functions, modules, lists/dicts, loops, selection; error handling.

LO4 – Explain program

This README explains purpose, how to use, and how it works.

LO5 – Find/fix errors

Manual testing steps below; (add your own found/fixed notes).

LO6 – Use libraries

Flask (web/API), Typer (CLI), Gunicorn (serve).

LO7 – Data model & logic

JSON model with CRUD, search, recommend.

LO8 – Version control

Commits show incremental development.

LO9 – Deployment

Deployed to Heroku; public URL included; no commented-out code.

Deployment (Heroku)
Heroku uses the repo’s Procfile:

makefile
Copy code
web: gunicorn web:app
Already set up for this project. Typical flow:

bash
Copy code
heroku create aromavault-eu
heroku buildpacks:set heroku/python
git push heroku main
heroku open
Note: Heroku’s filesystem is ephemeral. Seed data is provided so the app never boots empty. Admin add/delete is fine for demo but not permanent after dyno restarts.

Linting & formatting
bash
Copy code
black .
ruff check .
# optional auto-fix:
ruff check . --fix
                                        Add your latest run results here once you run them locally.

Testing (fill these placeholders after you test)
Keep this simple and honest. Replace ✅/❌ and add short notes.

Manual API tests
GET /api/perfumes → ✅/❌ (…notes…)

GET /api/search?query=rose → ✅/❌ (…)

GET /api/recommend?preferred=rose&avoid=vanilla → ✅/❌ (…)

POST /api/admin/add (valid body) → ✅/❌ (…)

POST /api/admin/delete (existing id) → ✅/❌ (…)

Manual UI tests
“Say hello” shows message → ✅/❌

“Get recommendations” lists results → ✅/❌

Admin “Add” shows new perfume → ✅/❌

Admin “Delete” removes perfume → ✅/❌

CLI tests
python -m cli_app seed-minimal → ✅/❌

python -m cli_app add-perf "Name" --brand B --price 10 --notes "x,y" → ✅/❌

Automated tests (pytest)
bash
Copy code
pytest -q
                                                   Paste your outcome here, e.g.:

Copy code
12 passed in 0.42s
Known issues / limitations
Heroku file system resets on restart; fine for this project’s scope.

Recommender is intentionally simple (easy to explain).

Single-file HTML for clarity; bigger projects would split templates/static.

Future improvements
Edit endpoint (update price/stock/notes).

Real DB (SQLite/Postgres) if persistence is needed.

User auth for admin actions.

Unit tests for validators and recommender.

Add more demo perfumes (quick ways)
Use the Admin Add form on the homepage, or

Run the CLI add-perf command, or

Manually add to data.json (keep valid JSON).

Credits

Thanks to CodeInstitute and my mentor Mitko.