# AromaVault — Python Essentials CLI & Web App

AromaVault is a simple, reliable perfume manager you can run from the **command line** and a tiny **Flask web API** for viewing/adding perfumes. Project 3.

![Am I Responsive / App Mockup](docs/readme/ami-responsive.png)

[View the live app here](https://aromavault-eu-e54dae1bad1f.herokuapp.com/)  
[View the GitHub repository here](https://github.com/HollieMorrison/aromavault)

---

## Table of contents :

### [User Experience (UX)](#user-experience-ux-1)
* [User Stories](#user-stories)
### [Features](#features-1)
* [Existing Features](#existing-features)
* [Features Left To Implement](#features-left-to-implement-1)
### [Design](#design-1)
### [Technologies Used](#technologies-used-1)
### [Frameworks, Libraries & Programs Used](#frameworks-libraries--programs-used-1)
### [Usage (CLI & Web API)](#usage-cli--web-api-1)
* [CLI Commands](#cli-commands)
* [Web API](#web-api)
### [Data Model](#data-model-1)
### [Testing](#testing-1)
* [Validation Results](#validation-results)
* [Manual Testing](#manual-testing)
* [Automated Tests (pytest)](#automated-tests-pytest)
### [Deployment and local development](#deployment-and-local-development-1)
* [Heroku](#heroku)
* [Forking the GitHub Repository](#forking-the-github-repository)
* [Local Clone](#local-clone)
### [Credits](#credits-1)
### [Acknowledgements](#acknowledgements-1)

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

Add your own screenshots here:
- Home page: `docs/screenshots/home.png`  
- Perfume list: `docs/screenshots/list.png`  
- Add flow/API demo: `docs/screenshots/add.png`  

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
- **cURL / HTTPie / Postman** – API testing

---

## Usage (CLI & Web API)

### CLI Commands

> The CLI group name is `aromavault`.

**Seed data**
```bash
# 3 sample perfumes
python -c "import cli_app; cli_app.app()" seed-minimal

# 30 sample perfumes (falls back to 3 if not available)
python -c "import cli_app; cli_app.app()" seed-30







