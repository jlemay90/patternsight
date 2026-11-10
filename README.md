# PatternSight

A local reflective journal with evidence-linked Gemini analysis, self-reported
mood history, a reflection partner, and a portable multi-agent continuity protocol.

## Run now

Requires Python 3.12 or newer. No runtime packages or frontend build needed.

```sh
python server.py
```

Open http://127.0.0.1:8000. Journal entries persist in
`data/patternsight.sqlite3`. Leave the server running; Ctrl+C stops it.
For another port: `python server.py --port 8001`.

## Connect Gemini

Copy `.env.example` to `.env`, enter your key in that local file, choose a
currently supported model from Google AI Studio, then restart. Do not put a key
in chat, browser code, or Git. The default `gemini-2.5-flash` is configurable;
availability in your account must be verified with a real request.

```sh
cp .env.example .env
```

The journal works without a key. In Hidden layers, review the selected-context
description and check Google sharing, then request analysis. Each request sends
the newest bounded context (60 entries / 60,000 text characters) and up to 30
saved corrections. No automatic background AI requests. Model errors are visible;
no demo or fabricated analysis replaces a failed call. The system prompt is
`prompts/reflect-v1.txt`; schemas and exact-quote validation live in `engine.py`.

## Use

Write or paste a reflection, optionally select mood and comma-separated tags,
then Save reflection. Mood bars show your ratings rather than inferred tone.
Analyze, follow quote links back to entries, and save Fits / Partly fits /
Doesn't fit with an optional correction. Ask an independent reflection question
in the chat. Chat itself is session-only and is not sent as conversation history.
Export my journal downloads a private JSON backup. Import/restore is not yet built.

Deleting an entry clears stored analyses and corrections that could quote it.
Database pages, SQLite backups, downloaded exports, and Google-held data are not
securely erased by this action. The app is a local single-user prototype without
authentication or encryption at rest. Do not expose its port to the public web.

## Verification

```sh
python -m unittest discover -s tests -v
node --check static/app.js
python scripts/check_handoff.py
```

Optional browser check: install Playwright in your own virtual environment,
install Chromium, start the app on port 8000 with a disposable `--db` path,
and run `python tests/browser_smoke.py`. Never run that smoke test against your
personal journal. See TEST-REPORT.md for actual checks in this build.
`python tests/browser_ai_smoke.py` starts its own disposable app and mocks only
the Google provider to exercise the complete local insight/correction/chat flow.
With system Chromium, set `CHROMIUM_EXECUTABLE=/usr/bin/chromium` for either test.

## Continue with another agent

Read AGENTS.md and AGENT-HANDOFF.md. Copy NEXT-AGENT-PROMPT.txt (also in the
Project continuity panel) and attach the complete source export. A reusable
skill is bundled at `skills/app-continuity/SKILL.md`; it is not globally installed.
The separately created user skill was not visible in this session and has not
been reviewed. Export source and Git history with:

```sh
python scripts/export_handoff.py
```

This creates ignored `artifacts/patternsight-handoff.zip` with tracked source,
revision metadata, checksums, and a Git bundle. It excludes journal data and
secrets. Journal export is a separate, private operation. To restore Git history,
extract the zip, then `git clone patternsight.bundle restored-project`.

Reference policy: `original` is the initial documentation baseline (not an
earlier app); `stable/foundation-v0.1.0` identifies the verified foundation once
tagged. No previous working app existed. CURRENT is actual HEAD plus dirty state.
The foundation stays on `agent/01-foundation`; no experimental merge into main.
