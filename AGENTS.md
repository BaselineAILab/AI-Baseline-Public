# Agent instructions

## Repository scope

This repository publishes public AI Baseline examples and packaged integration
artifacts. Keep changes inside this repository unless the user explicitly
authorizes another repository. Preserve unrelated work and never read or commit
credentials, local environment files, private data, or generated notebook output.

Packaged Claude assets are built from source owned by `../InfoWeaver`. Do not
hand-edit or rebuild them unless the task explicitly includes that artifact
update and its source change.

## Temporary implementation plans

Implementation plans are temporary working documents for unfinished changes, not permanent
documentation or a second backlog. Create one only when the change warrants it. Code, tests,
runbooks, and contributor guides must not depend on a plan.

Before completing work that used a plan:

1. Reconcile the plan with the implementation. Move lasting decisions, contracts, procedures,
   rollback guidance, and known limitations into the existing canonical documentation. Do not
   copy execution logs or superseded proposals into the guides.
2. Put remaining work in the issue tracker and distinguish completed validation from pending
   acceptance. Preserve useful evidence and an immutable Git link to the final committed plan
   in the owning issue or pull request before deleting it; commit any needed uncommitted history
   first.
3. Delete the completed plan and related temporary reviews or handoffs, preferably in the final
   implementation PR, or in a focused cleanup PR if implementation has already merged. Replace
   incoming links with canonical documentation or an explicitly historical commit link.

Keep a plan only while its work remains unfinished. Do not retain completed plans in place or
move them to an in-repository archive. Git and the linked issue or PR preserve execution history.

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
