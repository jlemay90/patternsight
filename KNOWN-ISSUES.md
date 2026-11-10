# Known issues and limits

1. **Live Gemini unverified** — no API key available in this environment. HTTP
   integration and failure handling are implemented and locally mocked; model
   availability, schema compatibility, latency, and semantic behavior must be
   checked with synthetic fixtures and an owner's configured key.
2. **Local single user only** — no auth, encryption at rest, or deployment
   hardening. Keep loopback binding. An account flag means key configured,
   not a verified Google connection.
3. **Recent context only** — up to 60 newest entries and 60,000 text characters;
   up to 30 saved corrections. Questions about older events may lack context.
4. **Not clinical monitoring** — sparse and selectively written journals cannot
   establish causes, diagnoses, or clinically reliable anomaly detection.
   Quote validation does not validate semantic conclusions.
5. **Deferred enhancements** — import/restore, editing entries, retrieval over
   older history, inferred sentiment extraction, automated semantic evaluations,
   persistent multi-turn chat, and audio recording.
6. **New user skill unavailable** — cannot certify its contents or global
   installation. Compare it with the bundled skill when it is supplied.
7. **Exports and deletion** — source export excludes personal data; journal JSON
   export includes it. Deletion invalidates stored derived records but does not
   securely erase database pages, existing exports, backups or provider records.
8. **Device coverage** — automated desktop/mobile Chromium coverage is not a
   test on a physical Android device, Safari, or every assistive technology.
9. **Claude source missing** — public jlemay90/patternsight now hosts the
   verified foundation, but Claude's referenced newer commits and evaluator
   remain unavailable until its actual source package is received. Repository
   creation/settings permissions are limited; Git push is available.
