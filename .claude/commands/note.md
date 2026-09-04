---
description: Add a note to the notes CLI store and show the open list
argument-hint: "<the note text>"
allowed-tools: Bash(python3 notes.py:*)
---

Add `$ARGUMENTS` as a note, then show what is open.

1. If `$ARGUMENTS` is empty, stop and ask for the text — `notes.py add` rejects blank input by design, so do not invent a placeholder.
2. `python3 notes.py add "$ARGUMENTS"`
3. `python3 notes.py list`

Report the new note's id and the current open count. Keep it to one or two lines — this is a shortcut, not a report.
