# Agent instructions

## Repository scope

This repository publishes public AI Baseline examples and packaged integration
artifacts. Keep changes inside this repository unless the user explicitly
authorizes another repository. Preserve unrelated work and never read or commit
credentials, local environment files, private data, or generated notebook output.

Packaged Claude assets are built from source owned by `../InfoWeaver`. Do not
hand-edit or rebuild them unless the task explicitly includes that artifact
update and its source change.

## Git workflow

Use a task-specific branch from the latest `origin/main` and open a pull request
into `main`. Never push or merge directly into `main`. Record the manual
validation appropriate to the changed public artifact, require one approving
review, resolve review conversations, and use squash merge.

An LLM agent may use the administrator PR-only exception to bypass the
approving-review requirement and squash-merge a pull request limited to a bug
fix and its directly related documentation. Complete all applicable validation,
resolve every review conversation, and record
"LLM bug-fix self-merge: <reason>" in the PR first. A bug fix restores documented
or previously working behavior. LLM agents must leave new features, behavior
expansions, mixed changes, and unclear classifications open for a human to merge.
The exception never permits a direct `main` push or bypassing failed validation.
