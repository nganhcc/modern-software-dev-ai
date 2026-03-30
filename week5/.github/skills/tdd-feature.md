---
name: tdd-feature
description: "Run a strict test-driven-development loop for one feature: write failing tests first, confirm failures, implement minimal code, confirm passing tests, then update durable docs."
argument-hint: "Describe one feature, target area, and acceptance criteria."
user-invocable: true
---

# TDD Feature

## Purpose
Run a strict TDD loop for one feature at a time.
Never implement production code until tests are written and confirmed failing.

## Inputs Required
- Feature description in one sentence.
- Target area (backend route, service, frontend behavior, or end-to-end path).
- Acceptance criteria (what must be true when done).

## References
- Test role: ../../agents/test-agent.agent.md
- Code role: ../../agents/code-agent.agent.md
- Documentation sync: ../update-claude-md.md

## Workflow

### Step 1 - Write failing tests (Test Specialist role)
Read .github/agents/test-agent.agent.md.
Write tests that represent the requested feature behavior.

Requirements:
- Tests must run immediately with a concrete command.
- At least one new assertion must fail for the feature gap.
- Do not write production code in this step.

Output:
- Test command to run (single exact command).
- List of test files created or modified.
- Brief coverage summary per test.

### Step 2 - Confirm tests fail
Tell the user exactly:
Tests written. Please run: [exact test command]
Paste the output here before I write any code.

Hard gate:
- STOP and wait for user output.
- Do not continue to Step 3 until output is provided.

### Step 3 - Analyze failure output
From the pasted output, list:
- Exactly which new feature tests failed.
- Failure reasons in plain language.

Decision branch:
- If no test failed, return to Step 1 and strengthen tests.
- If failures are unrelated infra/setup failures, isolate and request a narrower command.

### Step 4 - Implement minimal code to pass tests (Code Agent role)
Read .github/agents/code-agent.agent.md.
Implement only what is required to satisfy failing tests.

Constraints:
- No speculative features.
- No unrelated refactors.
- Keep changes minimal and traceable to failing assertions.

Output:
- List of production files created or modified.
- Mapping from each change to the failing test it addresses.

### Step 5 - Confirm tests pass
Tell the user exactly:
Code written. Please run: [exact test command] again.
Paste results to confirm all tests pass.

Hard gate:
- Do not claim success without pasted passing output.

### Step 6 - Update CLAUDE.md when needed
If implementation introduced a durable project rule, pattern, or command change:
- Read and apply .github/skills/update-claude-md.md.
- Document only stable, reusable guidance.

## Non-Negotiable Rules
- Never write production code before Step 2 evidence is received.
- Never assume pass/fail status; require explicit output.
- Keep scope to one feature.
- If scope expands, pause and re-plan with a new feature statement.

## Completion Checklist
- New tests exist and were observed failing first.
- Minimal production code was added to satisfy those tests.
- User confirmed passing test output.
- CLAUDE.md was updated when long-lived guidance changed.

## Usage Example
Use tdd-feature skill for: user can archive a note and exclude archived notes from the default list endpoint.
