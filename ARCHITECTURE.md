# Architecture — foundation v0.1.0

- `server.py`: Python ThreadingHTTPServer bound to loopback, fixed static route
  allowlist, JSON API, input limits, same-origin checks, SQLite Store.
- `static/`: responsive framework-free single-page UI. DOM is constructed with
  textContent, including model output and entry text; no dynamic innerHTML.
- `engine.py`: server-side REST request to Gemini generateContent, structured
  response schemas and deterministic exact-entry/quote checks.
- `prompts/reflect-v1.txt`: complete versioned system instruction.
- SQLite schema version 1: entries, analyses, feedback. Each operation opens its
  own connection. UUID keys; UTC server timestamps. No external database required.
- `tests/`: API/storage/contract tests with synthetic data and mocked provider;
  optional actual-browser smoke test. `fixtures/` contains qualitative AI cases.
- `skills/app-continuity/`: portable receiving/work/handoff procedure.
- `scripts/`: continuity document checks and tracked-source export with Git bundle.

## Data flow
Journal form → validated same-origin POST → SQLite → state API → UI.
Owner enables sharing → analyze/chat → newest bounded journal context and stored
feedback → Gemini with system instruction + schema → JSON parse + shape and
exact-evidence checks → persisted analysis or session-only chat → linked evidence.
Invalid model responses do not replace existing analysis. API credentials are
sent in the Google request header, never returned to the browser.

## HTTP contract
GET `/api/state`, `/api/export`, `/api/continuity`.
POST `/api/entries` {text,mood:null|1..5,tags:[]};
`/api/delete` {id}; `/api/analyze` {consent:true};
`/api/chat` {consent:true,question};
`/api/feedback` {insight_id,rating:fits|partly|doesnt-fit,note}.
AI requests are serialized; context changes during generation invalidate output.
No arbitrary file endpoint, CORS wildcard, remote journal telemetry, or CDN assets.

## Limits
No auth, encryption, deployment hardening, migration framework, context retrieval
across the full archive, or streaming chat. Context is explicitly recent and
bounded. All state is returned for the personal archive UI; add pagination before
large-scale usage. Exact citation checks prove quote provenance, not the truth
of an interpretation. Semantic quality and provider compatibility need a live
synthetic evaluation. Corrected interpretations are supplied as context; model
compliance cannot be guaranteed by the schema alone.
