# AromaVault — Simple Perfume Recommender & Catalog (CLI + API)

AromaVault helps you explore a small perfume catalog, search by notes/brand/price, and get simple recommendations.  
It exposes a **friendly web page** and **readable API endpoints** on Heroku, and includes a **Typer-based CLI** for one-off admin tasks.

![Am I responsive](./assets/readme/am-i-responsive-image.png)  
[**View the live AromaVault project here**](https://aromavault-eu-e54dae1bad1f.herokuapp.com/)

---

## Table of contents :

### [User Experience (UX)](#user-experience-ux-1)
* [User Stories](#user-stories)

### [Features](#features)
* [Existing Features](#existing-features)

### [Features Left To Implement](#features-left-to-implement-1)

### [Design](#design-1)

### [Technologies Used](#technologies-used-1)

### [Frameworks, Libraries & Programs Used](#frameworks-libraries-programs-used-1)

### [Testing](#testing-1)
* [Validation Results](#validation-results)
* [Manual Testing](#manual-testing)
* [Lighthouse Report](#lighthouse-report)

### [Deployment and local development](#deployment-and-local-development-1)
* [Heroku](#heroku)
* [Forking the GitHub Repository](#forking-the-github-repository)
* [Local Clone](#local-clone)
* [Running the CLI (one-off)](#running-the-cli-one-off)

### [Bug Fix Log (3 issues + resolutions)](#bug-fix-log-3-issues--resolutions-1)

### [Credits](#credits-1)

### [Acknowledgements](#acknowledgements-1)

---

## User Experience (UX)

AromaVault is for users who want a **simple way to browse perfumes** by notes (e.g., rose, vanilla), filter by price, and get **quick recommendations**.

There is a clear homepage on Heroku with links to both **HTML** and **JSON** views.

### User Stories

*First-time visitor goals*
- Understand the main purpose of the app (browse/search perfumes and get recommendations).
- Navigate quickly from the homepage to a readable list of perfumes.
- Use a simple search (`/api/search?query=rose&price_max=80`) to find options.
- Get basic recommendations (`/api/recommend?preferred=rose,vanilla`).

---

## Features

### Existing Features

- **Homepage** with quick links:
  - `/perfumes` — readable HTML table of the catalog  
  - `/api/perfumes?pretty=1` — the same data in formatted JSON  
  - `/api/search?query=...&brand=...&price_max=...` — filter results  
  - `/api/recommend?preferred=note1,note2&avoid=...&price_max=...` — simple scoring based on notes/price  
  - `/api/health` — health check (returns JSON `{status:"ok"}`)

- **Readable JSON**: add `?pretty=1` to any API endpoint for nicely formatted output.

- **Typer CLI (one-off on Heroku)**:
  - `hello` smoke test (`heroku run python run.py hello --name Hollie --app <app>`).
  - Structure is in place to add more admin commands (import/export, seeding, etc).

- **Data storage**: JSON dataset with a small sample perfume catalog.

![Homepage](./assets/readme/homepage.png)  
![Perfumes HTML](./assets/readme/perfumes-table.png)  
![Pretty JSON](./assets/readme/pretty-json.png)

---

## Features Left To Implement

- CLI commands to import/export CSV and seed/reset catalog.
- Pagination for `/perfumes` when the dataset grows.
- Save favourite notes per user.
- Simple admin authentication for write routes.

---

## Design

- Simple, clean HTML with system fonts for accessibility and speed.
- Minimal, predictable API with clear query parameters.
- CLI commands grouped under a single Typer app with built-in help.

---

## Technologies Used

- Python 3.12  
- Flask (web server & routes)  
- Typer (command-line interface)  
- Gunicorn (production WSGI server on Heroku)  
- JSON files for data

---

## Frameworks, Libraries & Programs Used

- GitHub — version control & hosting  
- Heroku — deployment  
- Visual Studio Code — development  
- Black & Ruff — formatting and linting  
- Pytest — unit testing

---

## Testing

We validated code style and ran tests locally, and manually exercised the endpoints on Heroku.

- `ruff check .` — no significant issues after the final pass  
- `black .` — consistent formatting  
- `pytest -q` — unit tests pass locally

### Validation Results

<details>
<summary>Ruff & Black</summary>

- Ruff fixed minor nits; Black formatted the codebase consistently.
</details>

<details>
<summary>Pytest</summary>

- All tests passed locally in the last run.
</details>

### Manual Testing

- Visited `/` homepage, `/perfumes` HTML table.  
- Confirmed JSON endpoints with and without `?pretty=1`.  
- Searched by brand/notes, verified price filters.  
- Checked `/api/health` returns `{ "status": "ok" }`.  
- Ran CLI on dyno: `hello` prints a greeting.

### Lighthouse Report

*(Add screenshots once captured.)*

---

## Deployment and local development

### Heroku

1. **Procfile**
2. **Python version**
3. **Deploy**
```bash
git push heroku main
heroku logs --tail --app <your-app-name>

## Live App

Live app:
https://aromavault-eu-e54dae1bad1f.herokuapp.com/

Forking the GitHub Repository

Open the repository and click Fork.

Work on your copy without affecting the original.

Local Clone
git clone <repo-url>
cd aromavault
python -m venv .venv
# Windows:
.venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate

pip install -r requirements.txt
# Development server:
flask --app web run     # or: python web.py (dev only)
# Visit:
# http://127.0.0.1:5000/

Running the CLI (one-off)

On Heroku:

heroku run python run.py --help --app <your-app>
heroku run python run.py hello --name Hollie --app <your-app>


Locally:

python run.py --help
python run.py hello --name Hollie

Bug Fix Log (3 issues + resolutions)
1) Heroku started Node/Total.js instead of Python

Symptom: Logs showed node index.js then node: command not found → app crashed.

Cause: A leftover Node scaffold and an old Procfile made Heroku detect/run Node.

Fix: Removed the Node entrypoint and switched to Python:

Procfile → web: gunicorn web:app

Kept Python buildpack only.

Result: Gunicorn boots, the web dyno stays up, and / serves the homepage.



2) Circular import between app.py and run.py

Symptom: Terminal page showed import/circular errors when loading the CLI.

Cause: app.py imported run.py and run.py imported app.py.

Fix: Ensured app.py defines the Typer app and run.py only imports it:


# app.py
import typer
app = typer.Typer(help="AromaVault command-line interface.")

# run.py
from app import app
if __name__ == "__main__":
    app(prog_name="run.py")


Result: CLI imports cleanly with no circular reference.

3) Typer had no commands → “Missing command.”

Symptom: Deployed terminal printed usage text with no commands; --help was not useful.

Cause: A Typer app existed but no commands were registered.

Fix: Added a minimal command to prove the CLI wiring:

@app.command()
def hello(name: str = "world"):
    """Say hello (deployment smoke test)."""
    print(f"Hello, {name}!")


Result: heroku run python run.py hello --name Hollie --app <app> prints a greeting; --help shows available commands.

Credits
Code

README structure adapted from a previous project template and tailored for a CLI + API app.

Typer & Flask docs for quick-start patterns.

Content

Sample perfume entries created for demonstration/testing.

Media

Placeholder screenshots in ./assets/readme/ (replace with real app captures).

Acknowledgements

Thanks to mentors/reviewers for deployment and structure feedback.

Slack community for tips on Heroku Procfiles and Typer.