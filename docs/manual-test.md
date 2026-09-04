# Manual test — all four mechanisms

Run from the repo root. Hooks, skills and commands defined in `.claude/` only load for a Claude
Code session started **inside this repository**, so steps 3 and 4 need `cd ~/Repos/claude_rep`
first. Steps 1 and 2 need nothing but a shell.

## 1. The application

```bash
python3 -m unittest discover -s tests -t . -v
python3 notes.py add "manual test note"
python3 notes.py list
python3 notes.py done 1
python3 notes.py list --all
python3 notes.py add "   "        # expect: notes: note text must not be empty, exit 1
```

Expected: `Ran 7 tests ... OK`; the note appears, then shows with `x` after `done`.

## 2. Hooks, without a session

Each hook is a script that reads the harness payload on stdin. Pipe one in and check the answer.

```bash
export CLAUDE_PROJECT_DIR="$PWD"

# PreToolUse — allowed command: no output, exit 0
echo '{"tool_name":"Bash","tool_input":{"command":"python3 notes.py list"}}' \
  | .claude/hooks/guard-secrets.sh; echo "exit=$?"

# PreToolUse — blocked: recursive delete, force push, literal token
echo '{"tool_name":"Bash","tool_input":{"command":"rm -rf ~/Repos"}}' \
  | .claude/hooks/guard-secrets.sh | jq -r '.hookSpecificOutput.permissionDecision'
echo '{"tool_name":"Bash","tool_input":{"command":"git push --force origin main"}}' \
  | .claude/hooks/guard-secrets.sh | jq -r '.hookSpecificOutput.permissionDecision'
echo '{"tool_name":"Bash","tool_input":{"command":"curl -H \"Authorization: token ghp_AbCdEf0123456789xyz\" https://api.github.com"}}' \
  | .claude/hooks/guard-secrets.sh | jq -r '.hookSpecificOutput.permissionDecision'

# PostToolUse — valid file passes, non-python is skipped, broken file blocks
echo "{\"tool_name\":\"Edit\",\"tool_input\":{\"file_path\":\"$PWD/notes.py\"}}" \
  | .claude/hooks/py-syntax.sh; echo "exit=$?"
printf 'def broken(:\n    pass\n' > /tmp/broken.py
echo '{"tool_name":"Write","tool_input":{"file_path":"/tmp/broken.py"}}' \
  | .claude/hooks/py-syntax.sh | jq -r '.decision'
rm -f /tmp/broken.py

# SessionStart — prints the repo brief that gets injected into context
echo '{}' | .claude/hooks/session-brief.sh | jq -r '.hookSpecificOutput.additionalContext'
```

Expected: `deny` three times, `block` once, exit 0 on the two allowed cases, and a one-paragraph
repo brief naming the current branch and test count.

Wiring check (exit 0 and the script path printed for each event):

```bash
for ev in PreToolUse PostToolUse SessionStart; do
  jq -e --arg e "$ev" '.hooks[$e][].hooks[].command' .claude/settings.json
done
```

## 3. Hooks, end to end in a session

```bash
cd ~/Repos/claude_rep && claude
```

- **SessionStart** — at startup Claude already knows the branch, the unpushed count and that only
  stdlib is available; ask *"what do you know about this repo's state?"* and it answers without
  running git.
- **PreToolUse** — ask Claude to run `git push --force origin main`. The command must be refused
  with the rule 7 reason, not executed.
- **PostToolUse** — ask Claude to write a deliberately broken Python file
  (`echo 'def broken(:' > scratch.py` via the Write tool). The hook blocks and reports the syntax
  error back; delete `scratch.py` afterwards.

If a hook does not fire, open `/hooks` once (that reloads the config) or restart the session —
the settings watcher only watches directories that already had a settings file at startup.

## 4. Commands and skills, in a session

```
/check                       -> runs 7 tests + syntax sweep, reports pass/fail with real output
/check tests/test_notes.py   -> runs just that file
/note manual test from slash -> adds the note, prints its id and the open count
/note                        -> asks for text instead of inventing one
/rules                       -> one line per rule: pass / VIOLATED / n/a (behavioral)
```

Skills load by description, not by name — trigger them with a task, not a slash:

- **notes-cli**: *"add a `remove` subcommand to the notes CLI"* → Claude follows the documented
  order (core function with `path=STORE` → parser branch → tests → `unittest discover -s tests -t .`)
  and refuses to add a dependency.
- **release-check**: *"is this repo ready to push?"* → Claude runs the six checks and ends with
  **ready to push** / **not ready**, without pushing.

Confirm a skill actually loaded: `/context` lists it, and the answer should quote the specifics
(the `-t .` flag, the `id` / `text` / `done` contract) rather than generic advice.
