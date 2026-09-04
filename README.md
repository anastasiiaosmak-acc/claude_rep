# claude_rep

Pet project demonstrating the four Claude Code customization mechanisms on a real (if tiny) app.

| Mechanism | Where | What it does |
|---|---|---|
| Rules | `CLAUDE.md` | 8 numbered rules loaded into every session in this repo |
| Skills | `.claude/skills/` | `notes-cli` (how to extend the CLI), `release-check` (pre-push checklist) |
| Commands | `.claude/commands/` | `/check`, `/note`, `/rules` |
| Hooks | `.claude/settings.json` + `.claude/hooks/` | PreToolUse secret/destructive guard, PostToolUse Python syntax gate, SessionStart repo brief |

The application is `notes.py` — a stdlib-only notes CLI with `add`, `list` and `done`.

```bash
python3 -m unittest discover -s tests -t .   # 7 tests
python3 notes.py add "hello" && python3 notes.py list
```

Manual test for every mechanism: [`docs/manual-test.md`](docs/manual-test.md).
