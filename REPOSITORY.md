# Shared repository and synchronization

Intended public repository: https://github.com/jlemay90/patternsight
Status: **NOT CREATED OR PUBLISHED by this session**.
GitHub rejected `gh repo create jlemay90/patternsight --public` with
`Resource not accessible by integration (createRepository)` on 2026-11-10.
The connected CLI authenticates as jlemay90, but lacks repository-creation
permission. The owner must create the empty public repository first. Do not
interpret the intended URL as a verified existing repository.

Create it as public with no README, license or .gitignore initialization:
https://github.com/new?name=patternsight&visibility=public

## Initial publication after creation

Inspect the remote before pushing; never overwrite a repository that already
contains independent work. This checkout has not configured origin, pushed any
commits, or synchronized with GitHub yet. Publish the tested foundation history,
the current documentation branch, and original/stable tags. Keep main unchanged
unless the owner authorizes promotion of the foundation. Set the repository's
default branch to the branch containing the app rather than the docs-only main.
Verify remote commit IDs after every push and record them in AGENT-HANDOFF.md.

## Every incoming agent

1. Clone the canonical repository or inspect `git remote -v` in an existing copy.
2. Run `git fetch origin --prune --tags`, inspect default/current remote branches,
   and read their AGENTS.md and AGENT-HANDOFF.md. A fetch failure is a blocker to
   claiming current remote state; a ZIP alone may be stale.
3. Record repository URL, source branch, exact commit, baseline test results and
   local dirty state. Start a new work branch from the intended latest source.
4. Preserve work on other branches. No force pushes, silent resets, or experimental
   merge into stable main without owner approval.

## Every outgoing agent

Commit code and updated permanent docs, push the work branch, verify that the
remote branch points to the same exact commit, and give the owner a repository
URL, branch URL, commit URL, checks and next task. If authorized, open a PR for
review. Public visibility enables reading; pushing still requires account access.
Do not claim synchronization when a push or verification failed. Keep the ZIP
and Git bundle as offline fallback. Exclude .env, journals, databases and private
exports from both source control and history.

## Claude continuity gap

User supplied a Claude handoff claiming branch `agent/02-live-eval-prep`, docs
HEAD `b346504`, tested source `e0a0315`, `scripts/eval_reflection.py`, and eight
synthetic fixtures. No source archive or bundle for those changes has been
received; neither commit nor that evaluator exists in this checkout. Claude did
not use GitHub according to the owner. These are unverified handoff claims,
not source that can be recreated from the message. Preserve and import Claude's
actual source/Git bundle when supplied, then compare ancestry and changes before
continuing its live evaluation. Do not label the agent-01 foundation as agent 02.
