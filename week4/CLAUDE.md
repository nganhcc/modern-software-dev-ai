# Week 4 Developer Guide (CLAUDE.md)

## What This Project Does
This is a minimal full-stack developer command center used for week4 automation work. It provides a FastAPI backend with SQLite persistence for notes and action items, plus a static frontend served directly by FastAPI. The codebase is intentionally small so developers and coding agents can practice safe, test-driven feature work and automation workflows.

## Quick Commands (from `week4/`)

### Run the app
```bash
make run
```

### Run tests
```bash
make test
```

### Format code
```bash
make format
```

### Lint code
```bash
make lint
```

### Seed local DB if needed
```bash
make seed
```

### Optional: install and run pre-commit
```bash
pre-commit install
pre-commit run --all-files
```

## Key File Map

### Backend entrypoints and app wiring
- `backend/app/main.py`: FastAPI app creation, startup hooks, static mounting, router registration.
- `backend/app/db.py`: SQLAlchemy engine/session setup, DB dependency injection, seed application logic.

### Routers (API endpoints)
- `backend/app/routers/notes.py`: Notes list/create/get/search endpoints under `/notes`.
- `backend/app/routers/action_items.py`: Action item list/create/complete endpoints under `/action-items`.

### Data models and schemas
- `backend/app/models.py`: SQLAlchemy ORM models (`Note`, `ActionItem`).
- `backend/app/schemas.py`: Pydantic request/response schemas.

### Services
- `backend/app/services/extract.py`: text-to-action-item extraction helper.

### Tests
- `backend/tests/conftest.py`: isolated SQLite test client fixture and DB override.
- `backend/tests/test_notes.py`: notes API behavior.
- `backend/tests/test_action_items.py`: action-item API behavior.
- `backend/tests/test_extract.py`: extraction service behavior.

### Frontend and static assets
- `frontend/index.html`: single-page UI shell.
- `frontend/app.js`: browser logic calling backend endpoints.
- `frontend/styles.css`: lightweight styles.

### Config and tasking
- `Makefile`: canonical run/test/format/lint/seed commands.
- `pre-commit-config.yaml`: formatting/lint hooks.
- `data/seed.sql`: initial schema/data seed.
- `docs/TASKS.md`: suggested extension tasks.

## Tech Stack and Conventions
- Backend: FastAPI, SQLAlchemy ORM, Pydantic.
- Database: SQLite file DB at `./data/app.db` by default (`DATABASE_PATH` override supported).
- Frontend: plain HTML/CSS/vanilla JS (no Node toolchain).
- Testing: `pytest` with `fastapi.testclient` and isolated temporary SQLite DB.
- Code quality: Black + Ruff (also enforced via pre-commit hooks).

Conventions to follow:
- Keep endpoint behavior and response models consistent with existing routers/schemas.
- Use dependency-injected DB sessions via `get_db` rather than creating ad-hoc sessions in routers.
- Update tests with every backend behavior change before/alongside implementation.
- Prefer small, incremental changes over broad refactors.

## Safe Commands to Run
Use these as default commands during development:
- `make run`
- `make test`
- `make format`
- `make lint`
- `make seed`
- `pre-commit install`
- `pre-commit run --all-files`
- `pytest -q backend/tests`

## Commands to Avoid
Avoid destructive or noisy operations unless explicitly requested:
- `git reset --hard`
- `git checkout -- .`
- `rm -rf data/` (or deleting `data/app.db` without intent)
- Running bulk format/refactor tools outside `week4/` scope
- Editing `__pycache__/` artifacts manually

## Workflow Rules for Developers and Agents
1. Work from the `week4/` directory when using `make` targets.
2. For feature changes: write/update tests first, then implement, then run `make test`.
3. Before finalizing changes: run `make format`, `make lint`, and `make test`.
4. Keep API, schemas, and frontend usage aligned; if endpoints change, update `frontend/app.js` and relevant tests.
5. Prefer non-destructive git operations; do not revert unrelated local changes.
6. Keep docs in sync for behavior changes (`docs/TASKS.md` and assignment write-up as needed).

## Practical Notes
- The app auto-creates tables and attempts seeding on startup.
- API docs are available at `/docs` when running the app.
- Static frontend is served at `/` and assets are mounted at `/static`.
