# CLAUDE.md

## Project Summary
This repository is a minimal full-stack notes and action-items app used as a Week 5 playground for agentic development workflows. The backend is a FastAPI API with SQLAlchemy + SQLite, and the frontend is static HTML/CSS/JS served by FastAPI. It includes seed data, basic CRUD-style endpoints, and a focused pytest suite for backend routes and extraction logic.

## Run, Test, Format, and Lint
Run commands from the `week5/` directory unless noted otherwise.

### Environment setup
- Create/activate a Python environment.
- Install dependencies (from the parent assignments repo root if needed):
  - `pip install -e .[dev]`
- Optional: install git hooks:
  - `pre-commit install`

### Run app
- `make run`
- App URL: `http://127.0.0.1:8000`
- API docs: `http://127.0.0.1:8000/docs`

### Tests
- `make test`
- Equivalent direct command: `PYTHONPATH=. pytest -q backend/tests`

### Formatting
- `make format`
- Equivalent direct commands:
  - `black .`
  - `ruff check . --fix`

### Linting
- `make lint`
- Equivalent direct command:
  - `ruff check .`

### Seed data
- `make seed`

## Key File Locations
### Backend app entry and config
- `backend/app/main.py`: FastAPI app, startup lifecycle, static mounts, router registration.
- `backend/app/db.py`: DB engine/session setup, dependency injection, seed application.

### Models and schemas
- `backend/app/models.py`: SQLAlchemy ORM models (`Note`, `ActionItem`).
- `backend/app/schemas.py`: Pydantic request/response models.

### Routers
- `backend/app/routers/notes.py`: `/notes` list/create/get/search endpoints.
- `backend/app/routers/action_items.py`: `/action-items` list/create/complete endpoints.

### Services
- `backend/app/services/extract.py`: text extraction utility for action items.

### Tests
- `backend/tests/conftest.py`: isolated test DB fixture + FastAPI dependency override.
- `backend/tests/test_notes.py`: notes API tests.
- `backend/tests/test_action_items.py`: action items API tests.
- `backend/tests/test_extract.py`: extraction unit test.

### Frontend and data
- `frontend/index.html`, `frontend/app.js`, `frontend/styles.css`: static UI and browser logic.
- `data/seed.sql`: initial SQLite schema/data SQL.

### Tooling/config
- `Makefile`: canonical run/test/format/lint/seed targets.
- `pre-commit-config.yaml`: black, ruff, EOF/trailing-whitespace hooks.
- `docs/TASKS.md`: assignment task backlog.

## Tech Stack and Conventions
- Python + FastAPI for HTTP API.
- SQLAlchemy ORM with SQLite (`sqlite:///./data/app.db` by default via `DATABASE_PATH`).
- Pydantic models for request/response typing.
- Pytest + FastAPI TestClient for tests.
- Ruff + Black for style/lint.
- Static frontend (no Node build pipeline required in current starter).

Conventions observed in this repo:
- Use `PYTHONPATH=.` for direct Python/pytest/uvicorn commands.
- Keep changes scoped to `week5/` for assignment work.
- Prefer Makefile targets over ad-hoc commands.
- API endpoints and tests currently use trailing slashes (for example `/notes/`).
- Test isolation is done by overriding `get_db` with a temp SQLite DB fixture.

## Safe Commands to Run
These are generally safe and expected for everyday development:
- `make run`
- `make test`
- `make format`
- `make lint`
- `make seed`
- `pre-commit run --all-files`
- `pytest -q backend/tests`
- `ruff check .`
- `black .`

Read-only inspection commands are also safe:
- `rg --files`
- `rg "pattern" backend frontend`
- `ls -la`

## Commands to Avoid
Avoid these unless you intentionally want destructive effects and have confirmed with your team/instructor:
- `rm -rf data/` or deleting `data/app.db` unintentionally (wipes local DB state).
- `git reset --hard`, `git clean -fd`, or other destructive git cleanup commands.
- Running broad format/lint/test commands from outside `week5/` that affect other weeks.
- Modifying files outside `week5/` for this assignment unless explicitly required and documented.

## Workflow Rules for Developers
- Start in `week5/` and keep commits focused and small.
- Run `make test` before finalizing a change.
- Run `make format && make lint` before committing.
- If touching API behavior, update or add tests in `backend/tests/` in the same change.
- Prefer schema/model consistency: update `models.py`, `schemas.py`, routers, and tests together.
- Preserve endpoint compatibility with the current frontend unless you intentionally coordinate both sides.
- Use `docs/TASKS.md` as the source of truth for feature tasks and expected scope.
