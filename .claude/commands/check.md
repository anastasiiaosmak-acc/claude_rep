---
description: Run the unit tests and the syntax check for this repo, then report pass/fail with real output
argument-hint: "[optional: a single test file, e.g. tests/test_notes.py]"
allowed-tools: Bash(python3:*), Read
---

Run this repo's checks and report what actually happened.

1. Tests — if `$ARGUMENTS` names a file, run only that file, otherwise the whole suite:
   - all: `python3 -m unittest discover -s tests -t . -v`
   - one: `python3 -m unittest <dotted.path.of.$ARGUMENTS> -v`
2. Syntax — parse every tracked Python file:
   `git ls-files '*.py' | xargs -n1 python3 -c 'import ast,sys; ast.parse(open(sys.argv[1]).read(), sys.argv[1])'`

Then report, per CLAUDE.md rule 5:
- how many tests ran and how many passed
- if anything failed, paste the failing output verbatim — do not summarize it away
- if a step could not run at all, say so instead of implying it passed

Do not fix anything unless I ask. This command reports.
