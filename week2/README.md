# NOTE
Qúa trình tôi làm việc vơi AI để hoanf thiện dụư án này đưuocj viết ở fie writeup.md

# Week 2: Action Item Extractor

A FastAPI + SQLite application that turns free-form notes into structured action items.

The project supports two extraction modes:
- Rule-based extraction using heuristics and pattern matching
- LLM-based extraction using Ollama with automatic fallback to rules if LLM extraction fails

It also includes a lightweight frontend for manual testing and note/action-item management.

## Features

- Extract action items from raw text via API
- Optional note persistence when extracting
- LLM extraction with fallback metadata (`extraction_method`, `fallback_reason`)
- Store and list notes and action items in SQLite
- Mark action items as done/undone
- Minimal browser UI served by FastAPI

## Tech Stack

- Python 3.10+
- FastAPI
- Pydantic v2
- SQLite3
- Ollama (`llama3.1:8b` by default)
- pytest
- Poetry

## Project Structure

```text
week2/
  app/
    main.py
    db.py
    exceptions.py
    schemas.py
    routers/
      action_items.py
      notes.py
    services/
      extract.py
  frontend/
    index.html
  tests/
    test_extract.py
  data/
    app.db
```

## Setup

### 1) Install dependencies

From the repository root:

```bash
poetry install
```

### 2) (Optional) Configure LLM model

The default model is `llama3.1:8b`. Override with:

```bash
export OLLAMA_MODEL=llama3.1:8b
```

### 3) Ensure Ollama is running (for LLM endpoint)

```bash
ollama run llama3.1:8b
```

If Ollama/model is unavailable, the LLM endpoint still responds using rule-based fallback.

## Run the Application

You can run from either location below.

From repository root:

```bash
poetry run uvicorn week2.app.main:app --reload
```

Or from `week2/`:

```bash
cd week2
poetry run python -m uvicorn app.main:app --reload
```

Then open:
- App UI: http://127.0.0.1:8000/
- OpenAPI docs: http://127.0.0.1:8000/docs
- Health check: http://127.0.0.1:8000/health

## API Endpoints

### Utility

- `GET /`
  - Serves the frontend (`week2/frontend/index.html`)
- `GET /health`
  - Returns app health status

### Notes

- `POST /notes`
  - Create a note
  - Request:
    ```json
    { "content": "Team sync notes..." }
    ```

- `GET /notes/{note_id}`
  - Retrieve a single note by ID

- `GET /notes`
  - List all notes (newest first)

### Action Items

- `POST /action-items/extract`
  - Rule-based extraction
  - Request:
    ```json
    { "text": "- [ ] Set up DB", "save_note": true }
    ```
  - Response includes optional `note_id` and extracted items

- `POST /action-items/extract-llm`
  - LLM extraction with automatic fallback to rules
  - Request:
    ```json
    { "text": "Action: write tests", "save_note": true }
    ```
  - Response includes:
    - `extraction_method`: `"llm"` or `"rules"`
    - `fallback_reason`: reason when fallback occurred
    - extracted items

- `GET /action-items`
  - List all action items
  - Optional query param: `note_id`

- `POST /action-items/{action_item_id}/done`
  - Mark an action item done/undone
  - Request:
    ```json
    { "done": true }
    ```

## Frontend Usage

At `/`, the UI provides:
- Text area for notes input
- `Save as note` toggle
- `Use LLM extraction` toggle
- `Extract` button for action-item extraction
- `List Notes` button to fetch and render all saved notes

## Run Tests

From repository root:

```bash
poetry run pytest week2/tests/test_extract.py -v
```

Or from `week2/`:

```bash
cd week2
poetry run pytest tests/test_extract.py -v
```

Current suite validates:
- Rule-based extraction behavior
- LLM extraction success path
- LLM fallback behavior on malformed/failed responses
- Route-level metadata from LLM endpoint

## Notes on Data Storage

- SQLite database file: `week2/data/app.db`
- Tables are initialized on application startup
- Deleting `app.db` resets local data
