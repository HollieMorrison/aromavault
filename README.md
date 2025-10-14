# AromaVault — Python CLI

AromaVault is a command-line app where you can **manage a small perfume dataset** and get **practical recommendations** based on notes, brand bias, and budget. It keeps things simple and easy to use so anyone can add, search, and export their collection without fuss.

![CLI preview](./docs/readme/cli-preview.png)  
[View AromaVault GitHub Repository](https://github.com/HollieMorrison/aromavault)

---

## Table of contents :

### [User Experience (UX)](#user-experience-ux-1)
* [User Stories](#user-stories)
### [Features](#features)
* [Existing Features](#existing-features)
* [Features Left To Implement](#features-left-to-implement-1)
### [Design](#design-1)
### [Technologies Used](#technologies-used-1)
### [Frameworks, Libraries & Programs Used](#frameworks-libraries--programs-used-1)
### [Testing](#testing-1)
* [Validation Results](#validation-results)
* [Manual Testing](#manual-testing)
* [Lighthouse Report](#lighthouse-report)
### [Deployment and local development](#deployment-and-local-development-1)
* [Heroku](#heroku)
* [Forking the GitHub Repository](#forking-the-github-repository)
* [Local Clone](#local-clone)
### [Credits](#credits-1)
### [Acknowledgements](#acknowledgements-1)

---

## User Experience (UX)

This project is aimed at perfume lovers and beginners who want a **fast, text-based tool** to store perfume details, **search/filter** by notes or brand, and get **simple recommendations** without needing a database or website.

AromaVault writes to local JSON files by default, and can **import/export CSV**, making it easy to move data in and out.

### User Stories

*First-time user goals*
  * Understand what the tool does and how to run it from the terminal.
  * Add a new perfume with basic fields (name, brand, notes, price).
  * See a list of perfumes and search by notes or brand.
  * Export data to CSV for use elsewhere.

*Returning user goals*
  * Update price or notes on an existing item.
  * Import a CSV file of items and avoid manual entry.
  * Create a simple **profile** and get **recommendations** within a budget.

- - -

## Features

### Existing Features

* **Add / Update / Delete** perfumes  
* **List** and **Search** (brand, notes, price cap)  
* **Import CSV / Export CSV** (ids supported for upsert)  
* **Profiles**: store preferences (preferred/avoid notes, brand bias, price_max)  
* **Recommend**: a tiny, deterministic scoring to return top-k matches  
* **Friendly errors** and safe file I/O (no crashes on missing files)  
* **Typer CLI** with `--help` on every command

> Notes are passed as a comma-separated list, e.g., `--notes citrus,green`.

Example screenshots:

![Help output](./docs/readme/help.png)  
![Search output](./docs/readme/search.png)  
![Export success](./docs/readme/export.png)

### Features Left To Implement

* Optional fuzzy search toggle and better ranking explanations  
* More advanced profile fields (season, longevity, occasion)  
* CSV schema validation with a helpful report

---

## Design

* **Simple, readable CLI** output using sensible defaults.  
* **Minimal data model**:
  * Perfume: `id`, `name`, `brand`, `notes` (list of strings), `price` (number).
  * Profile: `id`, `preferred_notes`, `avoid_notes`, `brand_bias`, `price_max`.

---

## Technologies Used

* [Python 3.11](https://www.python.org/)
* [Typer](https://typer.tiangolo.com/) (CLI)
* [Rich](https://rich.readthedocs.io/) (nicer console tables)
* [Pytest](https://docs.pytest.org/) (tests)

---

## Frameworks, Libraries & Programs Used

* [GitHub](https://github.com/)  
  * Version control, CI, and repo hosting.
* [GitHub Actions](https://github.com/features/actions)  
  * CI to lint, format, and run tests.
* [Visual Studio Code](https://code.visualstudio.com/)  
  * Local development.

---

## Testing

Automated tests verify a few CLI behaviors and basic storage/recommendation logic. Manual tests confirm friendly error messages and CSV flows.

Run locally:

```bash
pip install -r requirements.txt
pip install -r requirements-dev.txt
ruff check . --fix
black --check .
pytest -q
