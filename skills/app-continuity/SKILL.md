---
name: app-continuity
description: Continue an existing application across coding agents (Gemini, Claude, ChatGPT/Codex) using a canonical GitHub repository as the single source of truth and a copyable next-agent prompt box—eliminating manual ZIP archive sharing.
---

# App Continuity (v2 — GitHub-First, Zero-ZIP Handoff)

Continue an existing application across coding agents using https://github.com/jlemay90/patternsight as the canonical source of truth and a copyable next-agent prompt box.

## Receive
1. Clone or fetch `https://github.com/jlemay90/patternsight.git` (`git fetch origin --prune --tags`) and switch to the latest active branch listed in `NEXT-AGENT-PROMPT.txt` and `AGENT-HANDOFF.md`.
2. Read `REPOSITORY.md`, `AGENTS.md`, `NEXT-AGENT-PROMPT.txt`, `README.md`, `PROJECT-OVERVIEW.md`, `ARCHITECTURE.md`, `DECISIONS.md`, `KNOWN-ISSUES.md`, `TEST-REPORT.md`, and `AGENT-HANDOFF.md`.
3. Report upfront before edits: preserved goal/contracts, actual remote and local `HEAD` SHA, branch, tags (`original`, `stable/foundation-v0.1.0`), dirty state, and any discrepancy with handoff claims.
4. Run baseline checks (`python -m unittest discover -s tests -v`, `node --check static/app.js`, `python scripts/eval_reflection.py --mock`, `python scripts/check_handoff.py`).

## Work
1. Create a dedicated work branch (`agent/<number>-<topic>`) for substantial work. Never merge into `main` without owner approval; preserve `original` and `stable/*` tags.
2. Keep secrets (`.env`), local databases (`data/*.sqlite3`), and personal journal exports out of source control and commits. Never ask for an API key in chat.
3. Separate `MODE: LIVE` provider evaluations from `MODE: MOCK` or `MODE: BLOCKED` runs; claim live verification only when live requests succeeded.

## Verify and Hand Off
1. Run all tests and evaluation checks covering changed behavior.
2. Update permanent docs in place (`REPOSITORY.md`, `ARCHITECTURE.md`, `CHANGELOG.md`, `DECISIONS.md`, `KNOWN-ISSUES.md`, `TEST-REPORT.md`, `AGENT-HANDOFF.md`, `NEXT-AGENT-PROMPT.txt`).
3. Commit and save all changes directly to the work branch on `https://github.com/jlemay90/patternsight` (via `git push` or authenticated GitHub browser session), verify the remote commit SHA, and provide the updated `NEXT-AGENT-PROMPT.txt` in a copyable text box for the next agent.
