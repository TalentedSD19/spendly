# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project

**Spendly** — a Flask-based expense tracker web app. Currently a learning scaffold with the foundation in place and feature implementations being built out progressively.

## Commands

```bash
# Setup
python -m venv venv
source venv/Scripts/activate   # Windows/bash
pip install -r requirements.txt

# Run dev server (port 5001, debug mode)
python app.py

# Tests
pytest
pytest --verbose
pytest tests/test_foo.py       # single file
```

## Architecture

**Backend:** Flask 3.x, SQLite via `database/db.py`, Jinja2 templates.

**Entry point:** `app.py` — Flask app instantiation and all route definitions live here.

**Database layer:** `database/db.py` — SQLite helpers. Connect/query functions go here; `database/__init__.py` makes it a package.

**Template hierarchy:** `templates/base.html` is the parent layout (navbar, footer). All other templates extend it via `{% block content %}`.

**Static assets:** Single CSS file at `static/css/style.css` (uses CSS custom properties; accent colors `--accent: #1a472a` green, `--accent-2: #c17f24` orange; Google Fonts DM Serif Display + DM Sans). JS stub at `static/js/main.js`.

## Implemented Routes

| Route | Method | Template |
|-------|--------|----------|
| `/` | GET | landing.html |
| `/register` | GET | register.html |
| `/login` | GET | login.html |
| `/terms` | GET | terms.html |
| `/privacy` | GET | privacy.html |

## Planned Routes (stubs in app.py)

- `GET /logout`
- `GET /profile`
- `POST /expenses/add`
- `GET|POST /expenses/<id>/edit`
- `GET /expenses/<id>/delete`

## Dependencies

- Flask 3.1.3, Werkzeug 3.1.6
- itsdangerous 2.2.0 (token/session handling)
- pytest 8.3.5, pytest-flask 1.3.0
