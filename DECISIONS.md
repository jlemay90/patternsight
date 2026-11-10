# Decisions

## 2026-11-10 — agent 01
- Chose HTML/CSS/JavaScript and Python stdlib + SQLite for immediate local use
  without package installation. User allowed HTML or Python alternatives. React
  remains an option if future needs justify migration; do not rewrite by preference.
- Gemini called only server-side. Configurable model ID rather than hardwiring the
  outdated Gemini 1.5 request. Default model availability is unverified.
- Native mood ratings are the first trajectory. Deferred inferred sentiment
  velocity because it can imply precision unsupported by journal text.
- Zero to three hypotheses, exact quote links, alternative explanations, optional
  experiments, and saved correction context. No clinical anomaly labels.
- No seeded private-looking demo journal. Blank states are honest; synthetic
  fixtures stay outside the personal database.
- User's newly authored skill is not exposed by cloud/executor catalogs or the
  workspace. Included a clearly identified portable implementation based on the
  shared protocol; have not claimed installation or equivalence.
- Git original baseline is docs-only. Foundation built on a separate branch;
  no previous stable application exists. User controls experimental merges.
- Code handoffs deliberately exclude journals and .env; personal backups are
  separate. Include Git bundle so commits and tags survive agent transfers.
- Deferred accounts, cloud deploy, audio capture, import, full-history retrieval,
  sentiment extraction pipeline and statistical anomaly scoring.
