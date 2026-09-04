---
name: notes-cli
description: Conventions for extending notes.py — the storage contract, how to add a subcommand, and the stdlib-only constraint. Use when adding, changing, or debugging a notes CLI subcommand, when touching notes.json handling, or when a change to notes.py needs matching tests.
---

# Extending the notes CLI

`notes.py` is the whole application. It has no dependencies and must keep having none:
this machine has Python 3.9 and **no pytest, no ruff, no black** (CLAUDE.md rule 1 — verify before
assuming a tool exists). Tests run on `unittest` from the standard library.

## Storage contract

`notes.json` sits next to `notes.py` and holds a JSON list of records:

```json
[{"id": 1, "text": "wire the hooks", "done": false}]
```

Rules that other code depends on:

- `id` is `max(existing) + 1`, never reused, never renumbered
- `text` is stripped and never empty — `add()` raises `ValueError` on blank input
- `done` is a bool, not a timestamp or a status string
- every function takes an explicit `path=STORE` argument so tests can point it at a temp file.
  Never read the module-level `STORE` inside a function body.
- `notes.json` is gitignored: it is runtime data, not fixture data

## Adding a subcommand

Work in this order — the last step is not optional:

1. **Core function** in `notes.py`, taking `path=STORE` last, raising `ValueError` for bad input
   and `KeyError` for a missing id. Do not print inside it; return the affected record.
2. **Parser** in `main()`: a `sub.add_parser(...)` block plus one `elif args.cmd == ...` branch
   that does the printing. Keep output one line per record, machine-greppable.
3. **Tests** in `tests/test_notes.py` — at minimum a happy path and one failure mode, each using
   `self.path` from `setUp`, never the real store.
4. **Run them**: `python3 -m unittest discover -s tests -t .` — the `-t .` matters, it is what puts
   the repo root on `sys.path` so `import notes` resolves.

## Things that look reasonable and are not

- Adding `requirements.txt` or reaching for `pytest`, `click`, `rich` — the no-dependency
  constraint is the point of this project, not an accident
- Rewriting the store as SQLite or one-file-per-note — the flat JSON list is the contract
- Printing inside core functions — it makes them untestable and breaks the `--all` filter
- Mutating `notes.json` from a test — use the temp path

## Where the guard rails are

A `PostToolUse` hook parses every `.py` file right after it is written and blocks on a syntax
error (`.claude/hooks/py-syntax.sh`), so a broken edit surfaces immediately rather than at the
next test run. `/check` runs tests plus a full syntax sweep.
