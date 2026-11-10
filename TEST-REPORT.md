# Verification — foundation v0.1.0

## GitHub preparation documentation update
Application source remains unchanged. Continuity document checks and whitespace
validation are rerun for the GitHub-first handoff update; no new provider or UI
verification is claimed. Owner subsequently created the public repository, which
was verified empty before Git push. Historical branches and baseline tags were
pushed. Repository settings remain integration-limited. Final Git ref equality
and fresh-clone checks are verified by the publishing agent after pushing this
documentation. Claude's referenced commits remain unverified.

Tested source: b1fdcaaab5b37541632f633abc1300f0c8ce452a. A subsequent docs-only
commit records results; source code is unchanged. Final export metadata records
the handoff-complete HEAD and stable tag.

## Completed
- `python -m unittest discover -s tests -v`: 11 tests passed. API/storage checks
  run against temporary SQLite databases and loopback HTTP servers. Tests cover
  persistence, export, mood/tag/input validation, cross-origin/rebinding rejection,
  sharing consent, missing-key behavior, correction context, deletion invalidation,
  bounded context, preservation of old analysis on failure, and stale-result
  rejection. Contract checks reject invented IDs, quotes and empty citations,
  enforce the three-insight maximum, and allow insufficient evidence.
- Provider HTTP request and structured response parsing tested with a synthetic
  mock only. No Google call made and no semantic model evaluation claimed.
- `node --check static/app.js`: passed (syntax only).

## Browser and packaging
- `CHROMIUM_EXECUTABLE=/usr/bin/chromium python tests/browser_smoke.py`: passed
  using a disposable database. Desktop 1440×1050 and mobile 390×844; journal
  creation, reload persistence, mood chart, consent rejection, explicit missing-key
  error, continuity text box, JSON download and deletion. No page JavaScript
  errors or horizontal overflow. Screenshots inspected for both viewports.
- `CHROMIUM_EXECUTABLE=/usr/bin/chromium python tests/browser_ai_smoke.py`:
  passed. Real browser → local API → SQLite; only Gemini provider mocked.
  Analysis cards, exact citation navigation, correction save, feedback supplied to
  chat, evidence-linked answer, and reload persistence all passed.
- `python scripts/check_handoff.py`: passed; required permanent docs and private
  tracked-path exclusion checked. `git diff --check`: passed.
- `python scripts/export_handoff.py`: passed. Exported 26 tracked source files,
  manifest with SHA-256 checksums, and complete Git history bundle. Fresh archive
  extraction verified all checksums and absence of .env/data. `git bundle verify`
  passed; cloning restored exact revision and original history. All 11 tests,
  JS syntax and continuity checks passed again from the restored project.
  Documentation-only finalization is included in the final regenerated archive.

## Environment notes
Default command sandbox prohibited loopback sockets. API tests were rerun with
approved execution outside that sandbox. Playwright's bundled Chromium was not
installed; browser verification uses system `/usr/bin/chromium` via
`CHROMIUM_EXECUTABLE`. An attempted optional browser download could not reach the
proxy from the sandbox; no download is required with system Chromium.

## Not verified
Live Google authentication/quota/model availability/schema compatibility,
semantic output quality, physical Android device behavior, Safari, screen readers,
hosted deployment, large archives, import/restore, multi-turn conversation, or
the contents of the user's separately created skill.
