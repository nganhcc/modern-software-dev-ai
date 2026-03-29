---
description: Implement a feature using a TestAgent -> CodeAgent TDD loop with verification and summary.
argument-hint: "Feature request (example: DELETE /notes/{id} removes a note)"
allowed-tools: Read,Edit,Write,MultiEdit,Glob,Grep,Bash,Task
---

# /ttd-feature

Implement a feature using a strict TDD workflow with specialized subagents.

## Input
- `$ARGUMENTS`: feature behavior to implement.

If `$ARGUMENTS` is empty, stop and ask for a concrete feature statement.

## Safety Rules
1. Prefer minimal, scoped changes.
2. Never run destructive commands (`git reset --hard`, `git checkout -- .`, mass delete).
3. Do not revert unrelated local changes.
4. If environment/setup is broken, stop and report exact unblock steps.

## Workflow
1. Plan and locate scope.
   - Read `CLAUDE.md`.
   - Read only relevant files under `backend/app` and `backend/tests`.
   - Identify likely test target file before coding.

2. Spawn TestAgent to write failing tests.
   - Launch `test-agent` with this prompt:

   ```text
   Task: Write or update pytest coverage for this feature: $ARGUMENTS

   Constraints:
   - Follow .claude/agents/test-agent.md.
   - Prefer adding tests in existing files under backend/tests.
   - Ensure at least one test fails against current code.
   - Report exact failing test names and failure messages.
   ```

3. Review test quality before implementation.
   - Confirm tests assert behavior (not internals).
   - Confirm failures are relevant to `$ARGUMENTS`.
   - If tests are incorrect, fix tests first and re-run focused tests.

4. Spawn CodeAgent to make tests pass.
   - Launch `code-agent` with this prompt:

   ```text
   Task: Implement the feature so these failing tests pass: $ARGUMENTS

   Constraints:
   - Follow .claude/agents/code-agent.md.
   - Keep changes minimal and in-scope.
   - Run focused tests first, then make test.
   - If API behavior changes, update dependent files (schemas/frontend/tests) as needed.
   ```

5. Verify end-to-end.
   - Run focused tests for changed files.
   - Run `make test`.
   - If code changed, run `make format` and `make lint`.

6. Iterate at most 2 fix rounds.
   - If tests still fail, run one more TestAgent/CodeAgent cycle.
   - If still failing after second round, stop and report blockers clearly.

7. Return a final report.

## Final Output Format
1. `Feature implemented`
2. `Test files changed`
3. `Application files changed`
4. `Validation results`
5. `Edge cases / gaps`
6. `Next step` (only if blocked or partial)