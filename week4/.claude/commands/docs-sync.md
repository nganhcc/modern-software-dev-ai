---
description: Sync API docs with current FastAPI routes and report route deltas.
argument-hint: "[optional focus like notes|action-items|all]"
allowed-tools: Read,Edit,Write,MultiEdit,Glob,Grep,Bash
---

# /docs-sync

Synchronize `docs/API.md` with the real API surface from `backend/app/main.py` and summarize exactly what changed.

## Inputs
- `$ARGUMENTS` (optional): route focus filter, for example `notes`, `action-items`, or `all`.

## Safety Rules
1. Only edit documentation files unless the user explicitly asks for code fixes.
2. Do not run destructive commands (`rm -rf`, `git reset --hard`, `git checkout -- .`).
3. If app import or OpenAPI generation fails, stop and report the blocking error with next steps.

## Steps
1. Ensure you are in `week4/`.
2. Always read CLAUDE.md and week4/docs/API.md if it exists.
3. Read route source only when needed:
    - if files changed since last run,
    - or if OpenAPI generation output differs,
    - or if user passed a focused argument (like notes/action-items).
4. Prefer targeted reads:
    - main.py
    - notes.py
    - action_items.py
    - TASKS.md
5. Generate the current OpenAPI document directly from the app (without requiring a running server):

	```bash
	PYTHONPATH=. python - <<'PY'
	import json
	from backend.app.main import app
	spec = app.openapi()
	print(json.dumps(spec))
	PY
	```

6. Build a route inventory from OpenAPI:
	- method
	- path
	- summary/operationId (if present)
	- tags
	- request body schema (if present)
	- response status codes
7. If `$ARGUMENTS` is provided and not `all`, focus comparisons on matching routes first, but still preserve a complete API doc unless the user asks for partial output.
8. Create or update `docs/API.md` with:
	- Title and short project API overview
	- Base URL and docs URLs (`/`, `/docs`, `/openapi.json`)
	- Endpoint table grouped by tag/resource
	- Per-endpoint request/response notes
	- Error behavior notes (e.g., 404 responses)
9. Compute and report drift vs previous docs:
	- Added routes
	- Removed routes
	- Changed methods/paths/response codes
10. Return a concise summary including:
	- files modified
	- route delta list
	- TODOs for anything ambiguous or undocumented in code

## Output Format
Use this structure in your final response:

1. `Updated files`
2. `Route deltas`
3. `Docs sync summary`
4. `TODOs / follow-ups`

## Quality Bar
- Keep docs factual and derived from current code/OpenAPI.
- Avoid inventing endpoints or payload fields not present in OpenAPI or source.
- Keep endpoint descriptions concise and implementation-aligned.
