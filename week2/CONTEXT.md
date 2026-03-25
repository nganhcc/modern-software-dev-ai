# Week 2 Project Context

## Project Overview

**Action Item Extractor** is a FastAPI-based web application that automatically extracts actionable tasks from unstructured meeting notes and text. The application provides two extraction methods: rule-based heuristics and AI-powered inference using local LLM models (Ollama).

### Core Purpose
Enable users to convert lengthy notes into structured, deduplicated lists of action items with optional persistence to a local SQLite database.

## Architecture

### Technology Stack
- **Framework**: FastAPI 0.111+
- **Database**: SQLite3 with context-managed transactions
- **Validation**: Pydantic v2
- **AI/ML**: Ollama (local LLM inference) with structured outputs
- **Testing**: pytest with mock patching
- **Development**: Poetry, Python 3.10+

### Directory Structure
```
week2/
├── app/
│   ├── main.py              # App factory, lifecycle events, exception handlers
│   ├── db.py                # Database layer with transaction management
│   ├── schemas.py           # Pydantic models for all API contracts
│   ├── exceptions.py        # Custom exception hierarchy
│   ├── models.py            # (legacy - unused)
│   ├── routers/
│   │   ├── __init__.py
│   │   ├── action_items.py  # Action item extraction and management routes
│   │   └── notes.py         # Note creation and retrieval routes
│   └── services/
│       └── extract.py       # Extraction logic (rules + LLM)
├── tests/
│   ├── __init__.py
│   ├── conftest.py          # (prepared for pytest configuration)
│   └── test_extract.py      # Unit tests with mocked Ollama calls
├── data/
│   └── app.db               # SQLite database (auto-created)
├── frontend/
│   ├── index.html           # Single-page UI with extraction toggle
│   └── styles.css           # (inline styles in HTML)
├── pyproject.toml           # Poetry configuration and dependencies
├── REFACTORING.md           # Backend refactoring documentation
├── PROCESS.md               # (This document - work process summary)
└── CONTEXT.md               # (This document - project context)
```

## API Contract

### Endpoints

#### Action Items
- **POST /action-items/extract** - Rule-based extraction
  - Request: `ExtractActionItemsRequest` (text: str, save_note: bool)
  - Response: `ExtractActionItemsResponse` (note_id, items)
  
- **POST /action-items/extract-llm** - LLM-powered extraction with fallback
  - Request: `ExtractActionItemsLLMRequest` (text: str, save_note: bool)
  - Response: `ExtractActionItemsLLMResponse` (note_id, extraction_method, fallback_reason, items)
  
- **GET /action-items** - List all action items (optionally filtered by note_id)
  - Response: `list[ActionItemResponse]`
  
- **POST /action-items/{id}/done** - Mark action item as done/undone
  - Request: `MarkActionItemDoneRequest` (done: bool)
  - Response: `MarkActionItemDoneResponse` (id, done)

#### Notes
- **POST /notes** - Create a new note
  - Request: `CreateNoteRequest` (content: str)
  - Response: `NoteResponse` (id, content, created_at)
  
- **GET /notes/{note_id}** - Retrieve a specific note
  - Response: `NoteResponse`

#### Utility
- **GET /** - Serves interactive web UI
- **GET /health** - Health check endpoint
- **GET /static/** - Static file serving (frontend assets)

### Error Handling
All errors follow a consistent format with proper HTTP status codes:
- **400 Bad Request**: `ValidationError` - missing or invalid input
- **404 Not Found**: `ResourceNotFoundError` - resource doesn't exist
- **500 Internal Server Error**: `DatabaseError` or unexpected exceptions

## Extraction Methods

### 1. Rule-Based Extraction (`extract_action_items`)
Pattern matching against:
- Bullet points: `- item`, `* item`, `• item`
- Numbered lists: `1. item`
- Keyword prefixes: `todo:`, `action:`, `next:`
- Checkbox markers: `[ ]`, `[todo]`
- Fallback: Imperative sentence detection (add, create, implement, fix, etc.)

**Characteristics**:
- Fast, deterministic
- No external dependencies
- Works offline
- Limited scope detection

### 2. LLM-Based Extraction (`extract_action_items_llm_with_meta`)
Uses local Ollama model (llama3.1:8b by default) with:
- Structured output schema (JSON format enforcement)
- Zero temperature (deterministic)
- System prompt for actionable task focus
- Automatic fallback to rule-based if LLM unavailable

**Characteristics**:
- More intelligent scope understanding
- Context-aware filtering
- Requires Ollama running locally
- Returns metadata (`extraction_method`, `fallback_reason`)

## Data Model

### Note
```sql
CREATE TABLE notes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    content TEXT NOT NULL,
    created_at TEXT DEFAULT (datetime('now'))
)
```

### Action Item
```sql
CREATE TABLE action_items (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    note_id INTEGER,
    text TEXT NOT NULL,
    done INTEGER DEFAULT 0,
    created_at TEXT DEFAULT (datetime('now')),
    FOREIGN KEY (note_id) REFERENCES notes(id)
)
```

## Key Features

### 1. Dual Extraction Methods
- Rule-based for reliability
- LLM for intelligence
- Seamless fallback between them

### 2. Flexible Persistence
- Optional note saving (`save_note` parameter)
- Automatic action item insertion
- Returned IDs for reference

### 3. Deduplication
- Case-insensitive duplicate detection
- Order-preserving dedup (keeps first occurrence)
- Uniform normalization across both extraction methods

### 4. Robust Error Handling
- Custom exception hierarchy
- Structured logging throughout
- Graceful degradation

### 5. Interactive UI
- Single-page app (no build step required)
- Toggle between extraction methods
- Real-time method/fallback visibility
- Checkbox interface for marking items done

## Configuration

### Environment Variables
- `OLLAMA_MODEL` - LLM model to use (default: `llama3.1:8b`)

### Database Configuration
- `DB_PATH`: `week2/data/app.db`
- `DB_TIMEOUT`: 5.0 seconds
- `DB_CHECK_SAME_THREAD`: False (allows async operations)

### Application Configuration
Via `week2/app/main.py`:
- Startup event: Database initialization
- Shutdown event: Graceful cleanup
- Exception handlers: Custom error serialization
- CORS: Not enabled (add if frontend moved to separate domain)

## Testing Strategy

### Unit Tests (`week2/tests/test_extract.py`)
- **5 passing tests** covering:
  - Rule-based extraction with various formats
  - LLM extraction with mocked Ollama
  - Fallback behavior on LLM failure
  - Route-level metadata propagation
  - Error handling and deduplication

### Mocking Strategy
- Tests mock `ollama.chat()` to avoid runtime dependency
- Monkeypatch database insert for isolation
- All tests run locally without network

### Test Coverage
- Extraction logic: 100% covered
- Router handlers: Happy path + fallback covered
- Edge cases: Empty input, malformed response, runtime errors

## Deployment Notes

### Local Development
```bash
cd week2
poetry install
poetry run python -m uvicorn app.main:app --reload
# UI available at http://localhost:8000
```

### Production Considerations
1. **Ollama Setup**: Ensure Ollama is running with `llama3.1:8b` model
2. **Database**: SQLite suitable for small/medium workloads; consider PostgreSQL for scale
3. **Connection Pooling**: Currently single-conn per operation; add pooling for concurrent load
4. **Logging**: Currently stdout; add file-based or centralized logging
5. **CORS**: Enable if frontend moves to different domain/port
6. **Rate Limiting**: Add per-user extraction quotas if exposed publicly

## Performance Characteristics

| Metric | Value | Notes |
|--------|-------|-------|
| Rule-based extraction | < 10ms | Regex patterns over small text |
| LLM extraction | 1-5s | Depends on Ollama performance |
| Fallback latency | < 50ms | Automatic if LLM unavailable |
| Database insert (single) | < 5ms | SQLite local operation |
| Deduplication | < 1ms | Case-insensitive hash comparison |
| API response time | 10-5100ms | Dominated by extraction method |

## Known Limitations & Future Work

### Current Limitations
1. No authentication/authorization
2. SQLite not suitable for multi-user concurrent writes
3. No backup/restore mechanisms
4. Ollama dependency required for LLM method
5. No API rate limiting

### Planned Enhancements
1. Request/response logging middleware
2. Database connection pooling
3. Integration tests with real database
4. Repository pattern for further data abstraction
5. API versioning support (`/v1/`, `/v2/`)
6. Pagination for list endpoints
7. Batch extraction mode

## Success Criteria

The application successfully meets these criteria:
- ✓ Extracts action items from text using multiple methods
- ✓ Provides transparent fallback behavior
- ✓ Persists data reliably to local database
- ✓ Exposes type-safe REST API via Pydantic schemas
- ✓ Handles errors gracefully with proper HTTP codes
- ✓ Supports both programmatic (API) and interactive (UI) usage
- ✓ All tests passing with mocked external dependencies
- ✓ Clean architecture with separation of concerns
