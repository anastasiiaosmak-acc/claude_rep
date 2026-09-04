# claude_rep

Test repository for Claude Code experiments. Owner: anastasiiaosmak-acc.

## Current state

The repo holds only `README.md` and this file — no application code, package manifest,
build system, linter config, or test suite yet.

```
.
├── README.md    # one-line repo description
└── CLAUDE.md    # this file: rules Claude follows in this repo
```

## Rules

1. **Verify before you assume.** No toolchain exists here yet. Never run or suggest
   `npm`, `make`, `pytest` and friends without first confirming the matching config
   file is actually present. The same goes for files, functions and flags — check that
   a thing exists before building on it.

2. **Never commit secrets.** No tokens, API keys, `access_token` / `api_secret` values,
   `.env` files, or contents of `~/.corezoid/config.json`. Use placeholders or
   environment variables, and if a secret does land in a diff, stop and flag it instead
   of pushing.

3. **Branch for anything beyond docs.** Direct commits to `main` are fine only for
   README/CLAUDE.md-level edits; code changes go on a branch. One logical change per
   commit, and the message explains *why*, not just *what*.

4. **Keep diffs small and scoped.** Do not reformat untouched lines, rename unrelated
   things, or bundle drive-by refactors into an unrelated change. Match the style,
   naming and comment density of the surrounding code rather than importing a new one.

5. **Report results honestly.** State what was actually run and what it returned. If a
   check was skipped or a test failed, say so with the output — never report success
   for something that was not verified.

6. **Ask only when it changes the work.** Make ordinary judgment calls without asking;
   stop and ask when two readings would lead to materially different results. Do not
   expand scope past what was requested.

7. **Confirm before irreversible or outward-facing actions.** Pushing, force-pushing,
   deleting branches, publishing, or anything that leaves this machine needs explicit
   approval first — approval for one such action is not approval for the next.

8. **Keep this file current.** When code, build/test commands, or new conventions land,
   update the sections above in the same change. Delete instructions that stop being
   true — a stale rule is worse than a missing one.
