---
description: Audit the working tree against the eight rules in CLAUDE.md and report violations
allowed-tools: Bash(git:*), Bash(grep:*), Read, Glob
---

Check the current working tree against the numbered rules in @CLAUDE.md and report which ones are violated right now.

Gather evidence first:
- `git status --porcelain` and `git diff` — what is actually changed
- `git log --oneline -5` — commit message shape (rule 3)
- `git branch --show-current` — are code changes sitting on `main` (rule 3)
- `git diff | grep -niE 'ghp_|github_pat_|xox[baprs]-|PRIVATE KEY|api_secret|access_token'` — secrets in the diff (rule 2)
- whether `CLAUDE.md` still describes the real layout and commands (rule 8)

Then output one line per rule: `N. pass` or `N. VIOLATED — <what and where>`.

Rules 1, 5, and 6 are about how work is done rather than about file contents — mark them `n/a (behavioral)` unless something in the diff or history contradicts them.

Report only. Do not fix anything unless I ask.
