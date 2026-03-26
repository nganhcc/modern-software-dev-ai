---
name: assignment-workflow
description: 'Execute a complete weekly assignment lifecycle: intake → scaffold → implement → test → document → review → deploy. Use when starting a new assignment or stuck on a phase.'
argument-hint: 'Describe which phase you need help with, or ask for the full workflow'
---

# Assignment Workflow

A structured methodology for tackling weekly assignments efficiently in the modern-software-dev course. Covers all phases from reading requirements to deployment.

## When to Use

- Starting a new week's assignment
- Unsure what step to do next
- Need quality criteria to know when a phase is "done"
- Want to reuse a proven process across multiple assignments

## Phases at a Glance

| Phase | Goal | Estimated Time | Output |
|-------|------|---|--------|
| **Intake** | Parse requirements, identify deliverables | 10-15 min | Checklist, acceptance criteria |
| **Scaffold** | Set up folder structure, environment, git | 10-20 min | Running app + clean repo |
| **Implement** | Build features with AI assistance | 60-120 min | Working code, meaningful tests |
| **Validate** | Test, debug, ensure quality | 20-30 min | Passing tests, error handling verified |
| **Document** | Write README and assignment writeup | 15-25 min | Complete docs for reproduction |
| **Review** | Code quality, refactoring, pre-commit | 10-20 min | Clean code, formatted, lint-free |
| **Deploy** | Run locally, verify end-to-end | 10-15 min | Working demo, ready to submit |

---

## Phase 1: Assignment Intake (10-15 min)

**Goal**: Extract requirements, scope, and acceptance criteria before coding.

### Steps

1. **Read the assignment fully** (`weekX/assignment.md`)
   - Skim for learning goals
   - Identify the big picture and deliverables
   
2. **Extract key requirements**
   - List functional requirements (what must the code do?)
   - List non-functional requirements (reliability, docs, deployment mode)
   - Note any optional/bonus requirements
   
3. **Identify deliverables**
   - Code location (e.g., `week3/server/`)
   - README scope (setup, tools, example invocations)
   - Tests (if required)
   - Writeup file (`writeup.md`)
   
4. **Check evaluation rubric**
   - Map rubric categories to your plan
   - Identify point distribution (what's worth most?)
   - Note any extra credit opportunities
   
5. **Create a task checklist**
   - Break requirements into discrete, testable items
   - Use this as your acceptance criteria

### Quality Criteria

- [ ] You can explain the assignment in 2-3 sentences
- [ ] You've identified all deliverables and their location
- [ ] Rubric categories align with your implementation plan
- [ ] You have a prioritized task list

### Common Pitfalls

- **Skipping references**: Don't skip the "helpful references" section—they often point to real solutions
- **Misunderstanding scope**: Ask yourself: "Is this a small feature or a full system?"
- **Ignoring rubric**: The rubric is your specification—code to it

---

## Phase 2: Scaffold (10-20 min)

**Goal**: Create folder structure, environment, and verify the app runs.

### Steps

1. **Create folder structure** (from assignment spec)
   ```
   weekX/
   ├── README.md           # Setup guide, tool reference
   ├── writeup.md          # Your documentation (filled in later)
   ├── requirements.txt    # or poetry, depending on week
   └── [app folders]       # backend/, server/, frontend/ etc.
   ```
   
2. **Set up environment**
   - Create/activate Python venv or conda environment
   - Install base dependencies (FastAPI, pytest, requests, etc.)
   - Create `.env` file for API keys (add to `.gitignore`)
   
3. **Initialize git (if not already)**
   ```
   cd weekX/
   git init
   git add .
   git commit -m "Initial scaffold"
   ```
   
4. **Create a minimal "working" app**
   - Minimal FastAPI `main.py` that starts
   - Or minimal MCP server that runs
   - Test: Run locally and verify no import errors
   
5. **Document setup in README.md** (draft version)
   - Prerequisites (Python version, OS)
   - Installation steps
   - How to run locally
   - Environment variables needed

### Quality Criteria

- [ ] App runs without import errors
- [ ] Git repo initialized with clean history
- [ ] Environment is isolated (venv/conda)
- [ ] README covers setup and how to run

### Decision Point

**Does the assignment provide a starter?**
- **Yes**: Copy starter, verify it runs, then proceed to Implement
- **No**: Build minimal structure from scratch, test that it starts

---

## Phase 3: Implement (60-120 min)

**Goal**: Build features with structured AI assistance and checkpoints.

### Steps

1. **Break features into small tasks** (2-5 per feature)
   - Ask Claude Code / Cursor to help scaffold each part
   - Example: "Implement the GET /notes endpoint with SQLAlchemy"
   
2. **For each feature**:
   - Write a one-sentence acceptance test (what must work?)
   - Ask AI to implement
   - Review the generated code (understand it)
   - Test the feature in isolation (call the endpoint, verify output)
   - Commit with a clear message
   
3. **Add error handling proactively**
   - Input validation (type hints, pydantic models)
   - Rate limits (if API-dependent)
   - Graceful failures (try-except, meaningful error messages)
   
4. **Keep a log in `writeup.md`**
   - Record major features implemented
   - Document AI prompts that worked well
   - Note any changes you made to AI-generated code
   
5. **Checkpoint every 15-20 min**
   - Run the app end-to-end
   - Verify no runtime errors
   - Commit progress to git

### Quality Criteria

- [ ] Each feature has a passing acceptance test
- [ ] Error handling covers API failures, bad input, timeouts
- [ ] Code is readable (clear variable names, comments on tricky bits)
- [ ] App runs without errors after each checkpoint
- [ ] Git history is clean (logical commits, clear messages)

### Common Pitfalls

- **Over-relying on AI**: Review every line, understand the flow
- **Skipping tests**: Write tests *as* you implement, not after
- **Ignoring type hints**: Use Pydantic models, type hints everywhere
- **Massive commits**: Commit every feature, not all at the end

---

## Phase 4: Validate (20-30 min)

**Goal**: Test thoroughly, verify reliability, catch bugs.

### Steps

1. **Run all tests**
   ```
   pytest tests/ -v
   ```
   - All tests pass (fixing any failures now)
   - Review test coverage (aim for 80%+)
   
2. **Test edge cases manually**
   - Empty responses from API
   - API rate limits hit
   - Network timeout
   - Invalid input to UI
   - Use curl/Postman if backend
   
3. **Verify logging** (especially important for async/servers)
   - Check logs for errors, warnings
   - Ensure no stdout printed (breaks STDIO servers)
   - Log to file or stderr only
   
4. **Load test** (if applicable)
   - Can the endpoint handle 10 requests? 100?
   - Does rate limiting work?
   
5. **Integration test**
   - Run the complete flow as a user would
   - Frontend → Backend → API → Response
   - Verify the happy path works end-to-end

### Quality Criteria

- [ ] All unit tests pass
- [ ] Edge cases handled (empty, timeout, invalid input)
- [ ] Logs are clean (no errors unless intentional)
- [ ] Manual integration test succeeds
- [ ] App doesn't crash on bad input

### Decision Point

**Found a bug?**
- **Critical** (app crashes): Fix immediately, add a test
- **Minor** (edge case): Log it in `writeup.md`, fix if time permits
- **Design flaw**: Discuss in writeup; don't ship broken code

---

## Phase 5: Document (15-25 min)

**Goal**: Write clear, reproducible docs in README and writeup.

### Deliverables

**README.md** (for someone running your code)
- Prerequisites (Python 3.10+, OS, etc.)
- Step-by-step setup (install, environment variables, run)
- Tool reference (which endpoints/functions, what they do)
- Example invocations (with sample input/output)
- Troubleshooting (common errors + fixes)

**writeup.md** (for the instructor + you)
- Summary of what you implemented
- Prompts/workflows that worked well
- Changes you made to AI-generated code and why
- Challenges faced + solutions
- Rubric self-assessment (where you think you score points)
- Extra credit attempted (if any)

### Structure Template

```markdown
# README
## Prerequisites
## Installation
## Usage
## API Reference / Tool Reference
### [Tool/Endpoint Name]
- Parameters
- Response
- Example
## Troubleshooting

# writeup.md
## Summary
## Implementation
### [Feature Name]
- Approach
- Prompts used
- Issues encountered
## Testing
## Challenges & Lessons
## Rubric Self-Assessment
```

### Quality Criteria

- [ ] README is step-by-step (someone else could follow it)
- [ ] Examples include real input/output
- [ ] Writeup references specific prompts and decisions
- [ ] Both files are spell-checked and properly formatted
- [ ] No dead links or missing sections

---

## Phase 6: Review (10-20 min)

**Goal**: Clean up code, ensure it follows best practices.

### Steps

1. **Run linter / formatter**
   - Black (Python formatting)
   - Ruff (linting)
   - Pre-commit hooks (if configured)
   ```
   black .
   ruff check . --fix
   ```
   
2. **Code review checklist**
   - [ ] Type hints on all functions
   - [ ] Docstrings on public functions
   - [ ] No unused imports
   - [ ] No hardcoded secrets (API keys, tokens)
   - [ ] No console.log / print(debug statements)
   
3. **Refactor if needed**
   - Extract repeated code into helpers
   - Simplify complex conditionals
   - Use meaningful variable names
   - Ask Claude Code: "Can this be cleaner?" (and review suggestions)
   
4. **Check for common issues**
   - Trailing whitespace
   - Inconsistent line endings
   - Missing newlines at end of file
   
5. **Final git commit**
   ```
   git add .
   git commit -m "Review: formatting, type hints, cleanup"
   ```

### Quality Criteria

- [ ] Code passes linter with no warnings
- [ ] All functions have type hints and docstrings
- [ ] No hardcoded secrets or debug statements
- [ ] Folder structure is clean and organized
- [ ] Git history tells a story (not 100 commits with "fix" messages)

---

## Phase 7: Deploy / Verify (10-15 min)

**Goal**: Run the final app end-to-end and ensure it's submission-ready.

### Steps

1. **Fresh environment test** (optional but recommended)
   - Create a new venv
   - Follow your README step-by-step
   - Verify the app runs without errors
   ```
   python -m venv test_env
   source test_env/bin/activate
   pip install -r requirements.txt
   python -m [app]
   ```
   
2. **Run the complete workflow**
   - Start the app/server
   - Execute the example from your README
   - Verify output matches expected
   
3. **Check deployment specifics**
   - **Local STDIO server**: Can Claude Desktop find and run it?
   - **Remote HTTP**: Is it accessible? Returns correct status codes?
   - **FastAPI**: Does `/docs` swagger work?
   
4. **Create a summary checklist**
   - Verify all rubric items are met
   - Verify all deliverables are present
   - Verify README + writeup are complete
   
5. **Final commit and tag**
   ```
   git commit --allow-empty -m "Deploy: ready for submission"
   git tag submission-final
   ```

### Quality Criteria

- [ ] App starts and runs without errors
- [ ] README workflow reproduces the expected output
- [ ] All deliverables present in correct locations
- [ ] Writeup includes all required sections
- [ ] No untracked files (git status is clean)

---

## Decision Trees

### "I'm stuck on a feature"

1. **Is it a code error?** → Provide error + context to Claude Code with `/fix` or `/debug`
2. **Is it a design question?** → Ask Claude Code `/explain` on the relevant section
3. **Is it architectural?** → Jump to Architecture consultation (see Phase 3 note)

### "How do I know I'm done?"

Check against the rubric + your task list:
- Functional requirement met? (code + test)
- Non-functional requirement met? (docs + error handling)
- Extra credit attempted? (bonus features working)

### "Should I refactor now or later?"

- **During Implement**: Only if it unblocks a feature or clarifies logic
- **During Review**: Always—this is the time to clean up

---

## Tips & Tricks

- **Parallel work**: While tests run, update documentation
- **Timeboxing**: If a feature takes >30 min, break it smaller or ask for help
- **Git as checkpoint**: Commit after each feature—not all at the end
- **Test-driven**: Write the test first, then the code
- **Writeup as you go**: Don't leave it for the end; document decisions in real-time

---

## References

- Course materials: [modern-software-dev](https://github.com/your-course)
- [Claude Code best practices](https://www.anthropic.com/engineering/claude-code-best-practices)
- [SubAgents overview](https://docs.anthropic.com/en/docs/claude-code/sub-agents)
- Testing: `pytest` docs, `unittest` if needed
- Pre-commit: [pre-commit.com](https://pre-commit.com)
