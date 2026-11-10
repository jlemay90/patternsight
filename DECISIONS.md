# Decisions

## 2026-11-10 — Initial public repository publication
- Owner created jlemay90/patternsight and supplied its clone URL. Confirmed public
  access and an empty remote before publishing branches and baseline tags.
- Git push works; changing repository default-branch settings returned HTTP 403.
  Publish the tested foundation as the initial public main baseline via a
  fast-forward, preserving original history and tags. This fulfills the owner's
  repository/publication request without merging new experimental application code.
- Keep agent session branches and GitHub-first handoff instructions. Claude's
  newer work remains a documented source-recovery gap, not a claimed import.

## 2026-11-10 — GitHub continuity preparation
- Owner requested a separate public patternsight repository. GitHub CLI access
  was authenticated as jlemay90, but creation failed with an integration permission
  error. No repository creation, remote setup, or push is claimed.
- Make GitHub fetch/push plus exact remote revision verification part of every
  agent handoff. Archive/bundle is the offline fallback, not the preferred shared
  source after publication. No application code changed.
- Preserve Claude's supplied revision claims without inventing its unavailable
  source. REPOSITORY.md records the missing package and recovery requirements.

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
