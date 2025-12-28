# AromaVault — Python Essentials CLI & Web App

AromaVault is a simple, reliable perfume manager you can run from the **command line** and a tiny **Flask web API** for viewing/adding perfumes. It’s built to satisfy the **Python Essentials (PP3)** assessment criteria.

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
### [Usage (CLI & Web API)](#usage-cli--web-api)
* [CLI Commands](#cli-commands)
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
### [Credits](#credits)
### [Acknowledgements](#acknowledgements)

---

## User Experience (UX)

This project helps users quickly **browse** a curated list of perfumes (name, brand, price, notes, rating) and allows admins to **add / find / show / delete** perfumes via a **CLI**. The aim is a minimal, testable stack that meets PP3 requirements.

### User Stories

*First-time visitor goals*
- Understand the app purpose and see perfumes easily.
- View perfume **name, brand, notes, rating, price**.
- Use a simple API (or UI) to list items.

*Returning user goals*
- Search by **brand/name/notes**.
- See consistent IDs and details.

*Admin goals*
- Seed initial data (3 or 30 sample perfumes).
- Add, find, show, delete perfumes via **CLI**.
- Keep the JSON “DB” easy to reset.

---

## Features

### Existing Features
- ✅ **Seed data:** 3 (minimal) or 30 sample perfumes  
- ✅ **CLI commands:** `list`, `show`, `find`, `add-perf`, `delete`, `seed-minimal`, `seed-30`  
- ✅ **Web API** endpoints to list and add perfumes  
- ✅ **JSON “DB”** (`db.json`) that’s easy to inspect/reset  
- ✅ **Pytest** for automated tests; **Ruff + Black** for quality

![Home / List View](docs/screenshots/home.png)
![CLI Example](docs/screenshots/cli-list.png)

### Features Left To Implement
- Update endpoints for rating/stock
- Pagination & sorting on `/api/perfumes`
- Simple front-end filters and search box
- Persist stable UUIDs for seed data

---

## Design

- **Minimal** UI with focus on accessibility and clarity.  
- **JSON storage** to keep development simple.  
- **Seeding-on-first-request** (web) for quick demo on Heroku.  
- **Separation of concerns:** CLI commands vs. storage vs. web API.

> Add your own screenshots here:
> - Home page: `docs/screenshots/home.png`  
> - Perfume list: `docs/screenshots/list.png`  
> - Add flow/API demo: `docs/screenshots/add.png`  

---

## Technologies Used

- [Python 3.12+](https://www.python.org/)
- [Flask](https://flask.palletsprojects.com/) (web API)
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
```

---

## Usage (CLI & Web API)

### CLI Commands

> The CLI group name is `aromavault`. To keep it simple, we invoke via Python directly (no extra entrypoint needed).

```bash
# 3 sample perfumes
python -c "import cli_app; cli_app.app()" seed-minimal

# 30 sample perfumes (falls back to 3 if not available)
python -c "import cli_app; cli_app.app()" seed-30

# list all perfumes
python -c "import cli_app; cli_app.app()" list

# add a perfume
python -c "import cli_app; cli_app.app()" add-perf "Amber Sky" \
  --brand "Noctis" \
  --price 72 \
  --notes "amber,vanilla"

# find perfumes (case-insensitive; name, brand, notes)
python -c "import cli_app; cli_app.app()" find amber

# show one perfume (by exact id or substring of name)
python -c "import cli_app; cli_app.app()" show "Amber Sky"
# or
python -c "import cli_app; cli_app.app()" show 123e4567-e89b-12d3-a456-426614174000

# delete (by exact id or exact name)
python -c "import cli_app; cli_app.app()" delete "Amber Sky"
```

### Web API

```bash
# start locally
python web.py
# open http://localhost:5000
```

**Endpoints**
- `GET /api/perfumes` — list all perfumes  
- `POST /api/admin/add` — add a perfume (JSON)

**Example add (local)**
```bash
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
```

**Example add (Heroku)**
```bash
curl -X POST https://aromavault-eu-e54dae1bad1f.herokuapp.com/api/admin/add \
  -H "Content-Type: application/json" \
  -d '{"name":"Amber Sky","brand":"Noctis","price":72,"notes":["amber","vanilla"],"rating":4.2,"stock":2}'
```

> On the first request after deploy, the app auto-seeds if the DB is empty.

---

## Data Model

Each **Perfume** is stored as a JSON object in `db.json`:

| Field       | Type     | Notes                                    |
|-------------|----------|-------------------------------------------|
| `id`        | string   | UUID generated by CLI when adding         |
| `name`      | string   | Perfume name                              |
| `brand`     | string   | Brand name                                |
| `price`     | number   | In GBP (float)                            |
| `notes`     | string[] | Scent notes (e.g. `["rose","musk"]`)      |
| `allergens` | string[] | Currently empty by default                |
| `rating`    | number   | 0.0–5.0 (default 0.0 in CLI adds)         |
| `stock`     | number   | Integer quantity (default 0)              |

![Data Model Diagram]

flowchart TD
    U[User] --> D{Choose interface?}
    D -->|CLI| CLIstart
    D -->|Web UI / API| WEBstart

    %% ---------- CLI FLOW ----------
    subgraph CLI_Flow [CLI Flow]
      direction TB
      CLIstart[Run <code>aromavault</code> CLI<br/>(via <code>python -c "import cli_app; cli_app.app()"</code>)]
      CLIcmd{Command}

      CLIstart --> CLIcmd

      CLIseedMin[<b>seed-minimal</b><br/>→ write 3 perfumes]
      CLIseed30[<b>seed-30</b><br/>→ write 30 perfumes (if available)]
      CLIlst[<b>list</b><br/>→ print all perfumes]
      CLIadd[<b>add-perf NAME</b><br/><code>--brand --price --notes</code><br/>→ validate & add]
      CLIfind[<b>find QUERY</b><br/>→ search name/brand/notes]
      CLIshow[<b>show ID or name</b><br/>→ print details]
      CLIdel[<b>delete ID or exact name</b><br/>→ remove one]

      CLIcmd -->|seed-minimal| CLIseedMin --> DB[(<b>db.json</b>)]
      CLIcmd -->|seed-30| CLIseed30 --> DB
      CLIcmd -->|list| DB --> CLIlst
      CLIcmd -->|add-perf| CLIadd --> DB
      CLIcmd -->|find| DB --> CLIfind
      CLIcmd -->|show| DB --> CLIshow
      CLIcmd -->|delete| CLIdel --> DB
    end

    %% ---------- WEB/API FLOW ----------
    subgraph WebAPI_Flow [Web / API Flow]
      direction TB
      WEBstart[Open site or call API<br/>(Heroku or local Flask)]
      SeedCheck{On first request:<br/>Is DB empty?}
      WEBstart --> SeedCheck

      Seed30[(Run <code>seed_30</code><br/>or fallback <code>seed_minimal</code>)]
      SeedCheck -->|Yes| Seed30 --> DB
      SeedCheck -->|No| WebMenu

      WebMenu{Endpoint}
      SeedCheck --> WebMenu

      WebMenu -->|GET <code>/api/perfumes</code>| DB --> ListJSON[200 JSON list]
      WebMenu -->|POST <code>/api/admin/add</code>| Validate[Validate & normalise fields]
      Validate -->|OK| DB --> AddJSON[200 JSON of created item]
      Validate -->|Invalid| Err400[400 error JSON]
    end

    %% ---------- SHARED STORAGE ----------
    DB[(<b>db.json</b><br/>array of Perfume objects)]

    %% ---------- STYLES ----------
    style DB fill:#eef,stroke:#468,stroke-width:1px
    style CLIstart fill:#efe,stroke:#484
    style WEBstart fill:#efe,stroke:#484

---

## Testing

The project uses **pytest** for automated tests and **Ruff + Black** for code quality.

### Validation Results

```bash
# lint & format
ruff check --select I --fix .
black .

# compile check (syntax gate)
python -m py_compile cli_app.py storage.py web.py
```

### Manual Testing

- CLI commands exercised on Windows/macOS/Linux shells.
- Web API tested locally and on Heroku with `curl` / Postman.
- Verified empty/invalid inputs are handled with helpful messages.
- Family/friends/peers asked to try list/find/add/delete flows.

> Add screenshots of manual testing:
> - CLI list: `docs/screenshots/cli-list.png`  
> - CLI add: `docs/screenshots/cli-add.png`  
> - Web add flow: `docs/screenshots/add.png`

### Automated Tests (pytest)

```bash
# run everything
pytest -q

# run just CLI tests verbosely
pytest -k "test_cli_seed_and_list or test_cli_add_and_find" -vv -s
```

*(Testing Summary Table)*

| Test name                | Purpose                        | Result |
|--------------------------|--------------------------------|--------|
| `test_cli_seed_and_list` | Seeds & lists perfumes         | ✅      |
| `test_cli_add_and_find`  | Adds and finds by keywords     | ✅      |

---

## Deployment and local development

### Heroku

**Prereqs:** Heroku CLI logged in, an app created, and a `Procfile` containing:

```
web: gunicorn web:app
```

**Deploy**
```bash
git add -A
git commit -m "Deploy"
git push heroku main
```

**Logs**
```bash
heroku logs --tail
```

### Forking the GitHub Repository

By forking the repository, you can make a copy to your own GitHub account:

1. Log in to GitHub and open the repo:  
   https://github.com/HollieMorrison/aromavault
2. Click **Fork** (top-right).
3. You now have your own copy to modify safely.

### Local Clone

1. Log in to GitHub and open the repo:  
   https://github.com/HollieMorrison/aromavault
2. Click **Code** → choose HTTPS/SSH/GitHub CLI and copy the link.
3. Open your terminal and navigate to a folder.
4. Run:
   ```bash
   git clone <your-copied-url>
   cd aromavault
   ```
5. (Optional) Create and activate a virtual environment, then:
   ```bash
   pip install -r requirements.txt
   ```

---

## Credits

- Built using **Python & Flask**.
- README structure inspired by Code Institute README templates and prior projects.
- Thanks to assessors and mentors for guidance.

---

## Acknowledgements

- My mentor and the Slack community for ongoing support, feedback, and encouragement.
- Friends and family for helping test and validate features.

---
