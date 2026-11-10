# PatternSight

An intelligent reflective journal that helps its owner notice recurring
situations, inspect the evidence, and test what helps. Initial request: quick
text/pasted voice-to-text entries with timestamps and mood tags; historical
pattern/anomaly analysis; emotional trajectory; up to three actionable insights;
and chat grounded in past entries. Responsive single-page app with Gemini.

The second essential goal is continuity across Gemini, ChatGPT, Claude and other
coding agents without repeated explanations, arbitrary rewrites, or lost versions.
This project is the first concrete implementation of that reusable protocol.

## Contracts
- Mood ratings are self-reported. Inferred tone is separate and uncertain.
- Insights are hypotheses with supporting entry IDs and exact quotes, possible
  alternative explanations, a question and a small experiment.
- Return zero to three insights; insufficient evidence is a valid outcome.
- Track helpful patterns as well as stressors. Do not diagnose or infer withdrawal
  from missing entries. Correlation does not establish a cause.
- User corrections persist and are included in subsequent AI context.
- Journals stay in local SQLite until the owner explicitly requests AI analysis
  or chat, which sends the displayed bounded context to Google.
- API keys remain on the server. No fake AI results when a key is absent.
- Each agent leaves source, test evidence, decisions, known issues and handoff.

## Foundation scope
Python standard-library backend, SQLite, HTML/CSS/JavaScript frontend. Local
single-user prototype. Entry creation/deletion, mood history, export, insights,
feedback, grounded questions and continuity panel. No accounts, hosted deployment,
clinical inference, audio recording, or autonomous background monitoring.
