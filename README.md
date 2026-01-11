# AromaVault — Python Essentials CLI & Web App

AromaVault is a simple, reliable perfume manager you can run from the **command line**, a tiny **Flask web API**, and a **web terminal** that feels like a CLI in your browser. It’s built to satisfy the **Python Essentials (PP3)** assessment criteria.

![Am I Responsive / App Mockup](docs/readme/ami-responsive.png)

[View the live app here](https://aromavault-eu-e54dae1bad1f.herokuapp.com/)  
[View the GitHub repository here](https://github.com/HollieMorrison/aromavault)

---

## Table of contents :

### [User Experience (UX)](#user-experience-ux)
* [User Stories](#user-stories)
### [Features](#features)
* [Existing Features](#existing-features)
* [Features Left To Implement](#features-left-to-implement)
### [Design](#design)
### [Technologies Used](#technologies-used)
### [Frameworks, Libraries & Programs Used](#frameworks-libraries--programs-used)
### [Getting Started (Local)](#getting-started-local)
### [Usage (CLI, Web Terminal & Web API)](#usage-cli-web-terminal--web-api)
* [CLI Commands](#cli-commands)
* [Web Terminal (browser CLI)](#web-terminal-browser-cli)
* [Web API](#web-api)
### [Data Model](#data-model)
### [Testing](#testing)
* [Validation Results](#validation-results)
* [Manual Testing](#manual-testing)
* [Automated Tests (pytest)](#automated-tests-pytest)
### [Deployment and local development](#deployment-and-local-development)
* [Heroku](#heroku)
* [Forking the GitHub Repository](#forking-the-github-repository)
* [Local Clone](#local-clone)
### [PP3 Criteria Mapping](#pp3-criteria-mapping)
### [Credits](#credits)
### [Acknowledgements](#acknowledgements)

---

## User Experience (UX)

This project helps users quickly **browse** a curated list of perfumes (name, brand, price, notes, rating) and lets admins **add / find / show / update / delete** perfumes via a **CLI**. The aim is a minimal, testable stack that meets PP3 requirements.

### User Stories

*First-time visitor goals*
- Understand the app purpose and see perfumes easily.
- View perfume **name, brand, notes, rating, price**.
- Use a simple UI (web terminal) to run commands.

*Returning user goals*
- Search by **brand/name/notes**.
- See consistent IDs and details.

*Admin goals*
- Seed initial data (3 or 30 sample perfumes).
- Add, find, show, update, delete perfumes via **CLI**.
- Keep the JSON “DB” easy to reset.

---

## Features

### Existing Features
- ✅ **Seed data:** 3 (minimal) or 30 sample perfumes  
- ✅ **CLI commands:** `list`, `list-perfumes-cmd`, `show`, `find`, `add-perf`, `update-perf`, `delete`, `seed-minimal`, `seed-30`  
- ✅ **Web Terminal**: type CLI commands directly in the browser on the live app  
- ✅ **Web API** endpoints to list and add perfumes  
- ✅ **JSON “DB”** (`db.json`) that’s easy to inspect/reset  
- ✅ **Pytest** for automated tests; **Ruff + Black** for quality

![Web Terminal](docs/screenshots/web-terminal.png)  
![CLI Example](docs/screenshots/cli-list.png)

### Features Left To Implement
- More update options (e.g. edit notes/brand via flags)
- Pagination & sorting on `/api/perfumes`
- Optional front-end table with filters/stars
- Import/Export CSV
- Stricter validation (price ≥ 0, rating 0–5, etc.)

---

## Design

- **Minimal** UI with focus on clarity.  
- **JSON storage** to keep development simple.  
- **Auto-seed on first request** (web) if the DB is empty.  
- **Separation of concerns:** CLI (`cli_app.py`) vs. storage (`storage.py`) vs. web (`web.py`).

> Add your own screenshots here:
> - Web terminal: `docs/screenshots/web-terminal.png`  
> - Perfume list (API/UI): `docs/screenshots/list.png`  
> - Add flow/API demo: `docs/screenshots/add.png`  

---

## Technologies Used

- [Python 3.12+](https://www.python.org/)
- [Flask](https://flask.palletsprojects.com/) (web + web terminal)
- [Click](https://click.palletsprojects.com/) (CLI)
- [Pytest](https://docs.pytest.org/) (tests)
- [Ruff](https://docs.astral.sh/ruff/) + [Black](https://black.readthedocs.io/) (lint/format)
- [Gunicorn](https://gunicorn.org/) + [Heroku](https://www.heroku.com/) (deployment)

---

## Frameworks, Libraries & Programs Used

- **GitHub** – version control and repository hosting  
- **Heroku** – cloud deployment  
- **VS Code** – code editor  
- **cURL / HTTPie / Postman** – API testing (optional)

---

## Getting Started (Local)

```bash
# clone
git clone https://github.com/HollieMorrison/aromavault.git
cd aromavault

# create & activate venv
python -m venv .venv

# Windows:
. .venv/Scripts/activate
# macOS/Linux:
# source .venv/bin/activate

# install deps
pip install -r requirements.txt

Usage (CLI, Web Terminal & Web API)
CLI Commands

The CLI group name is aromavault. To keep it simple, we invoke via Python directly (no extra entrypoint needed).

# 3 sample perfumes
python -c "import cli_app; cli_app.app()" seed-minimal

# 30 sample perfumes (falls back to 3 if not available)
python -c "import cli_app; cli_app.app()" seed-30

# list all perfumes
python -c "import cli_app; cli_app.app()" list

# list with count header "Perfumes (N)"
python -c "import cli_app; cli_app.app()" list-perfumes-cmd

# add a perfume
python -c "import cli_app; cli_app.app()" add-perf "Amber Sky" \
  --brand "Noctis" \
  --price 72 \
  --notes "amber,vanilla"

# find perfumes (case-insensitive; name, brand, notes)
python -c "import cli_app; cli_app.app()" find amber

# show one perfume (by exact id or substring of name)
python -c "import cli_app; cli_app.app()" show "Amber Sky"
# or by id:
python -c "import cli_app; cli_app.app()" show 123e4567-e89b-12d3-a456-426614174000

# update (by exact name or exact id)
python -c "import cli_app; cli_app.app()" update-perf "Amber Sky" --rating 4.6 --stock 3

# delete (by exact id or exact name)
python -c "import cli_app; cli_app.app()" delete "Amber Sky"

Web Terminal (browser CLI)

Open the live app and type commands (e.g. help, list, find rose, add-perf ...):
https://aromavault-eu-e54dae1bad1f.herokuapp.com/

Short help appears on the page (how to add, update, delete).
Use ↑/↓ to cycle command history, Ctrl+L to clear.

Web API
# start locally
python web.py
# open http://localhost:5000


Endpoints

GET /api/perfumes — list all perfumes

POST /api/admin/add — add a perfume (JSON)

Example add (local)

curl -X POST http://localhost:5000/api/admin/add \
  -H "Content-Type: application/json" \
  -d '{
        "name":"Amber Sky",
        "brand":"Noctis",
        "price":72,
        "notes":["amber","vanilla"],
        "rating":4.2,
        "stock":2
      }'


Example add (Heroku)

curl -X POST https://aromavault-eu-e54dae1bad1f.herokuapp.com/api/admin/add \
  -H "Content-Type: application/json" \
  -d '{"name":"Amber Sky","brand":"Noctis","price":72,"notes":["amber","vanilla"],"rating":4.2,"stock":2}'


On the first request after deploy, the app auto-seeds if the DB is empty.

Data Model

Each Perfume is stored as a JSON object in db.json:

Field	Type	Notes
id	string	UUID generated by CLI when adding
name	string	Perfume name
brand	string	Brand name
price	number	In GBP (float)
notes	string[]	Scent notes (e.g. ["rose","musk"])
allergens	string[]	Optional (empty by default)
rating	number	0.0–5.0 (default 0.0)
stock	number	Integer quantity (default 0)

Add your own diagram image: docs/diagrams/data-model.png

Testing

The project uses pytest for automated tests and Ruff + Black for code quality.

Validation Results
# lint & format
ruff check --select I --fix .
black .

# compile check (syntax gate)
python -m py_compile cli_app.py storage.py web.py

Manual Testing

Seed & List

Run seed-minimal then list → should show 3 items.

Add & Show

add-perf "Test Scent" --brand "Demo" --price 10 --notes "citrus"

show "Test Scent" → shows item with id.

Find

find citrus → includes “Test Scent”.

Update

update-perf "Test Scent" --rating 4.2 --stock 5

show "Test Scent" → rating/stock updated.

Delete

delete "Test Scent"

find Test → no results.

Header list

list-perfumes-cmd → first line Perfumes (N).

Add manual testing screenshots:

CLI list: docs/screenshots/cli-list.png

CLI add: docs/screenshots/cli-add.png

CLI update: docs/screenshots/cli-update.png

CLI delete: docs/screenshots/cli-delete.png

Automated Tests (pytest)
# run everything
pytest -q

# run just the CLI tests verbosely
pytest -k "test_cli_seed_and_list or test_cli_add_and_find" -vv -s


(Testing Summary Table)

Test name	Purpose	Result
test_cli_seed_and_list	Seeds & lists perfumes	✅
test_cli_add_and_find	Adds and finds by keywords	✅
Deployment and local development
Heroku

Prereqs: Heroku CLI logged in, an app created, and a Procfile containing:

web: gunicorn web:app


Deploy

git add -A
git commit -m "Deploy"
git push heroku main


Logs

heroku logs --tail

Forking the GitHub Repository

By forking the repository, you can make a copy to your own GitHub account:

Log in to GitHub and open the repo:
https://github.com/HollieMorrison/aromavault

Click Fork (top-right).

You now have your own copy to modify safely.

Local Clone

Log in to GitHub and open the repo:
https://github.com/HollieMorrison/aromavault

Click Code → choose HTTPS/SSH/GitHub CLI and copy the link.

Open your terminal and navigate to a folder.

Run:

git clone <your-copied-url>
cd aromavault


(Optional) Create and activate a virtual environment, then:

pip install -r requirements.txt

PP3 Criteria Mapping

LO1: Clean Python; linted with Ruff/Black; intended features work (seed/list/find/add/show/update/delete).

LO2: Handles empty/invalid input (simple checks); clear separation (CLI, storage, web).

LO3: Uses functions, selection, loops, modules, and list/dict structures; basic exception handling.

LO4: README explains purpose, usage, and value in simple language.

LO5: Tests provided (pytest) and a manual test plan.

LO6: Uses external libraries (Flask, Click, Gunicorn, Pytest, Ruff, Black).

LO7: Real domain data model with CRUD operations via CLI & API.

LO8: Git/GitHub used for version control and deployment history.

LO9: Deployed to Heroku; no commented-out code in final deploy.

Credits

Built using Python, Click, and Flask.

README structure inspired by Code Institute style guides.

Thanks to assessors and mentors for guidance.