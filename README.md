# AromaVault

AromaVault is a command-line application built in Python that allows users to manage a perfume catalogue and receive personalised fragrance recommendations.  
It’s designed to help fragrance enthusiasts and retailers keep track of their collections, store personal scent preferences, and discover new perfumes tailored to their taste — all through a simple terminal interface.

![AromaVault CLI Screenshot](./assets/readme/aromavault-cli-preview.png)  
[View AromaVault live deployment here](https://replit.com/@yourusername/aromavault)

---

## Table of Contents :

### [User Experience (UX)](#user-experience-ux-1)
* [User Stories](#user-stories)
### [Features](#features)
* [Existing Features](#existing-features)
### [Features Left To Implement](#features-left-to-implement-1)
### [Design](#design-1)
### [Technologies Used](#technologies-used-1)
### [Frameworks, Libraries & Programs Used](#frameworks-libraries--programs-used-1)
### [Testing](#testing-1)
* [Validation Results](#validation-results)
* [Manual Testing](#manual-testing)
### [Deployment and Local Development](#deployment-and-local-development-1)
* [Replit Deployment](#replit-deployment)
* [Forking the GitHub Repository](#forking-the-github-repository)
* [Local Clone](#local-clone)
### [Credits](#credits-1)
### [Acknowledgements](#acknowledgements-1)

---

## User Experience (UX)

AromaVault provides an intuitive and efficient way for users to interact with a structured dataset through the terminal.  
The focus is on simplicity, speed, and clarity — using text-based menus instead of a visual interface to keep things lightweight and accessible.

This application was designed for users who want to easily manage fragrance data, view quick statistics, and generate perfume recommendations without needing a web browser.

### User Stories

* **First-time user goals**
  * Understand the main purpose of the app and what it does.
  * Be able to run the program and see clear help instructions.
  * Add perfumes easily and list them in an organised table.
  * Try the perfume recommendation system quickly and see results.

* **Returning user goals**
  * Manage saved perfumes and profiles efficiently.
  * Export data to CSV and re-import later.
  * Use saved profiles for quicker recommendations.

---

## Features

### Existing Features

* **Perfume Management**
  * Add, list, update, and delete perfumes from a stored JSON database.
  * Filter perfumes by brand or note and sort by name, price, or rating.

* **Fuzzy Search**
  * Use RapidFuzz to find perfumes even if names are partially typed or misspelled.

* **User Profiles**
  * Create user profiles with preferred fragrance notes and allergens to avoid.

* **Personalised Recommendations**
  * Suggest perfumes using a similarity algorithm that compares scent notes while avoiding allergens.

* **Data Persistence**
  * Data is saved automatically in a JSON file.
  * CSV import/export options for backup or sharing.

* **Rich Output**
  * Results are displayed in clean, coloured tables using the Rich library.

* **Error Handling**
  * Invalid inputs and missing data are handled gracefully with clear messages.

* **Seed Data**
  * Load a small sample dataset instantly using:
    ```bash
    python app.py seed-minimal
    ```

![CLI Example](./assets/readme/aromavault-list-example.png)

---

### Features Left To Implement

* Add a fragrance “family” classifier (e.g., floral, woody, citrus).
* Create an option to calculate average user ratings.
* Enable export and import of user profiles.
* Add a “backup to cloud” feature for easier deployment recovery.

---

## Design

Although AromaVault is a text-based project, its layout follows a structured, user-friendly design:
* Simple and consistent colour themes (green for success, red for errors).
* Clearly labelled columns and data tables.
* Logical flow between commands — every command can be discovered through the help menu.
* Minimal text clutter for readability.

---

## Technologies Used

* [Python 3.11](https://www.python.org/) - Main programming language.
* [JSON](https://www.json.org/json-en.html) - For data storage.
* [CSV](https://en.wikipedia.org/wiki/Comma-separated_values) - For file imports and exports.

---

## Frameworks, Libraries & Programs Used

* [Typer](https://typer.tiangolo.com/) - Command-line interface framework.
* [Rich](https://rich.readthedocs.io/en/stable/) - For coloured text and styled tables.
* [RapidFuzz](https://maxbachmann.github.io/RapidFuzz/) - Fuzzy matching and search.
* [Black](https://black.readthedocs.io/en/stable/) - Code formatter.
* [Ruff](https://docs.astral.sh/ruff/) - Code linter and static analysis tool.
* [GitHub](https://github.com/) - Repository hosting and version control.
* [Replit](https://replit.com/) - Cloud deployment platform.
* [Visual Studio Code](https://code.visualstudio.com/) - Code editor.

---

## Testing

### Validation Results

* All Python files were checked using `black` and `ruff` with no major issues.
* The application runs successfully from the terminal with all expected functionality.
* JSON database and CSV import/export verified to ensure correct data persistence.

### Manual Testing

* Tested every command in the CLI to ensure correct output and error handling.
* Confirmed that incorrect IDs and invalid data types trigger appropriate error messages.
* Verified that the seed data loads correctly.
* Exported and re-imported CSV files successfully.
* Checked fuzzy search accuracy with partial and misspelled names.
* Confirmed graceful exit with Ctrl+C during runtime.

---

## Deployment and Local Development

### Replit Deployment

AromaVault was deployed using [Replit](https://replit.com/).

**Steps:**
1. Log in to your Replit account.
2. Create a new Repl using “Import from GitHub”.
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
