---
name: update-claude-md
description: "Update CLAUDE.md to reflect the current repository accurately. Use for refreshing run/test/lint commands, file map, conventions, and safe/unsafe command guidance after project changes."
argument-hint: "Describe what changed in the repo and which CLAUDE.md sections should be updated."
---

# Update CLAUDE.md

## Purpose

Maintain CLAUDE.md as a trustworthy, current guide for contributors and coding agents in this workspace.

## When to Use

- Build, test, lint, or format commands changed.
- File structure or key paths changed.
- Stack, conventions, or workflow rules changed.
- Safe or risky command guidance needs correction.

## Inputs to Collect

- Current repository tree and important files.
- Current developer commands from Makefile and docs.
- Any user-provided scope for what should or should not change.

## Workflow

1. Confirm scope and constraints.
- Determine whether the update is full-document or section-specific.
- Preserve existing style and voice unless the user asks for rewrites.

2. Gather source-of-truth facts.
- Read Makefile targets and equivalent direct commands.
- Read docs that define workflow expectations.
- Verify key paths in backend, frontend, tests, and data folders.

3. Plan section updates before editing.
- Map repository facts to CLAUDE.md sections:
  - Project Summary
  - Run/Test/Format/Lint
  - Key File Locations
  - Tech Stack and Conventions
  - Safe Commands to Run
  - Commands to Avoid
  - Workflow Rules

4. Apply minimal edits.
- Update only inaccurate or stale lines.
- Keep command examples copy-pasteable.
- Keep lists concise and internally consistent.

5. Validate consistency.
- Ensure every referenced command exists and is appropriate for this repo.
- Ensure referenced file paths exist.
- Ensure no section contradicts another section.

6. Report changes.
- Summarize what was updated and why.
- Call out assumptions if some facts could not be verified.

## Decision Points

- If requested changes conflict with repository facts:
  - Prefer verified facts from files.
  - Note the conflict and ask the user whether to document desired future state instead.

- If commands work from a specific directory only:
  - State that directory explicitly.
  - Include equivalent commands when useful.

- If content is uncertain or missing:
  - Keep existing text unchanged for that part.
  - Flag it as a follow-up question.

## Quality Checks

- Accuracy: commands, paths, and tool names are valid.
- Completeness: all affected sections were updated.
- Safety: risky commands are clearly labeled and constrained.
- Readability: concise bullets, no redundant or conflicting guidance.

## Output

A revised CLAUDE.md aligned with the current repository, plus a short change summary and any open questions.
