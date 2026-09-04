---
name: release-check
description: Pre-push checklist for claude_rep — tests, secret scan, CLAUDE.md freshness, commit and branch shape. Use before pushing, before opening a PR, when asked whether the repo is ready to ship, or after finishing a batch of changes.
---

# Pre-push check for claude_rep

Run every step. Report each as pass or fail with the evidence, then state one verdict:
**ready to push** or **not ready** plus what blocks it. Never push as part of this skill —
CLAUDE.md rule 7 puts that decision with the human.

## 1. Tests pass

```bash
python3 -m unittest discover -s tests -t . -v
```

`-t .` is required (it puts the repo root on `sys.path`). Report the count. A failure is a hard
block; paste the real output rather than describing it (rule 5).

## 2. Every tracked Python file parses

```bash
git ls-files '*.py' | xargs -n1 python3 -c 'import ast,sys; ast.parse(open(sys.argv[1]).read(), sys.argv[1])'
```

Silence means pass.

## 3. No secrets in what is about to leave the machine

```bash
git diff origin/main..HEAD | grep -niE 'ghp_|github_pat_|xox[baprs]-|BEGIN [A-Z ]*PRIVATE KEY|api_secret|access_token|\.corezoid/config'
```

Any hit is a hard block (rule 2). Also confirm `notes.json` and `__pycache__/` are not staged —
both are gitignored runtime artifacts.

## 4. Diff scope is honest

```bash
git diff --stat origin/main..HEAD
```

Flag reformatting of untouched lines, unrelated renames, and drive-by refactors bundled into an
unrelated change (rule 4). Flag anything that grew far past what the task asked for.

## 5. CLAUDE.md still true

Read `CLAUDE.md` against the tree. It must not claim there is no code or no toolchain once code
exists, its Layout tree must match reality, and new commands or conventions introduced by this
change must appear there (rule 8). A stale rule is a block, not a nit.

## 6. Commits and branch

```bash
git log --oneline origin/main..HEAD
git branch --show-current
```

Each commit is one logical change with a message that says why (rule 3). Code changes on `main`
are a violation; docs-only changes there are fine.

## Verdict

List the failed steps in severity order. If everything passes, say so plainly and hand the push
decision back to the human with the exact command they would run.
