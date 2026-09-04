# claude_rep

Pet project for exercising the four Claude Code customization mechanisms: rules (this file),
skills, slash commands, and hooks. The application under them is a tiny notes CLI.

## Current state

Python 3.9, **standard library only** — this machine has no pytest, no ruff, no black, and there
is no package manifest. Tests run on `unittest`.

```
.
├── notes.py                     # the whole application: add / list / done
├── notes.json                   # runtime store, gitignored
├── tests/test_notes.py          # 7 unittest cases
├── docs/manual-test.md          # step-by-step manual test for all four mechanisms
├── CLAUDE.md                    # this file — the rules
└── .claude/
    ├── settings.json            # hook wiring + project permissions
    ├── skills/                  # notes-cli, release-check
    ├── commands/                # /check, /note, /rules
    └── hooks/                   # guard-secrets, py-syntax, session-brief
```

## Commands

```bash
python3 -m unittest discover -s tests -t .     # test suite (-t . puts the root on sys.path)
python3 notes.py add "text"                    # add a note
python3 notes.py list [--all]                  # list open notes, or all of them
python3 notes.py done <id>                     # mark a note done
```

In a Claude Code session: `/check` runs tests plus a syntax sweep, `/note <text>` adds a note,
`/rules` audits the working tree against the rules below.

## Rules

1. **Verify before you assume.** Never run or suggest `pytest`, `npm`, `make`, `ruff` and friends
   here — they are not installed and there is no config for them. The same goes for files,
   functions and flags: check that a thing exists before building on it.

2. **Never commit secrets.** No tokens, API keys, `access_token` / `api_secret` values, `.env`
   files, or contents of `~/.corezoid/config.json`. Use placeholders or environment variables, and
   if a secret does land in a diff, stop and flag it instead of pushing. A `PreToolUse` hook also
   refuses shell commands that carry a literal credential.

3. **Branch for anything beyond docs.** Direct commits to `main` are fine only for
   README/CLAUDE.md-level edits; code changes go on a branch. One logical change per commit, and
   the message explains *why*, not just *what*.

4. **Keep diffs small and scoped.** Do not reformat untouched lines, rename unrelated things, or
   bundle drive-by refactors into an unrelated change. Match the style, naming and comment density
   of the surrounding code rather than importing a new one.

5. **Report results honestly.** State what was actually run and what it returned. If a check was
   skipped or a test failed, say so with the output — never report success for something that was
   not verified.

6. **Ask only when it changes the work.** Make ordinary judgment calls without asking; stop and ask
   when two readings would lead to materially different results. Do not expand scope past what was
   requested.

7. **Confirm before irreversible or outward-facing actions.** Pushing, force-pushing, deleting
   branches, publishing, or anything that leaves this machine needs explicit approval first —
   approval for one such action is not approval for the next. A `PreToolUse` hook blocks the
   sharpest of these outright.

8. **Keep this file current.** When code, build/test commands, or new conventions land, update the
   sections above in the same change. Delete instructions that stop being true — a stale rule is
   worse than a missing one.

## Skills

- **notes-cli** — the storage contract for `notes.json` and the order in which a new subcommand
  gets added (core function → parser branch → tests → run them). Loads when work touches `notes.py`.
- **release-check** — the pre-push checklist: tests, syntax sweep, secret scan, diff scope,
  CLAUDE.md freshness, commit and branch shape. Ends with a verdict and hands the push to a human.

## Hooks

| Event | Matcher | Script | Behavior |
|---|---|---|---|
| PreToolUse | `Bash` | `guard-secrets.sh` | denies `rm -rf` outside the repo, force-push / `reset --hard origin`, and commands containing a literal credential (rules 2, 7) |
| PostToolUse | `Write\|Edit` | `py-syntax.sh` | parses any `.py` just written via `ast.parse` and blocks on a syntax error; ignores every other extension |
| SessionStart | — | `session-brief.sh` | injects branch, uncommitted count, unpushed count, test count, and the fact that only stdlib is available (rule 1) |

Each hook reads the harness payload on stdin and answers with decision JSON. To test one without a
session, pipe a payload into it directly — `docs/manual-test.md` has the exact commands. Hooks in
`.claude/settings.json` only load for sessions started **inside this repo**; a session rooted
elsewhere will not fire them.
