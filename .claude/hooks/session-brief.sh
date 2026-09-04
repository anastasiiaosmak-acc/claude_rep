#!/usr/bin/env bash
# SessionStart — inject the repo's real state so nothing has to be assumed (CLAUDE.md rule 1).
set -uo pipefail

cat >/dev/null 2>&1 || true   # drain the payload we do not need

root=${CLAUDE_PROJECT_DIR:-$(cd "$(dirname "$0")/../.." && pwd)}
branch=$(git -C "$root" rev-parse --abbrev-ref HEAD 2>/dev/null || echo "unknown")
dirty=$(git -C "$root" status --porcelain 2>/dev/null | wc -l | tr -d ' ')
ahead=$(git -C "$root" rev-list --count '@{u}..HEAD' 2>/dev/null || echo "0")
tests=$(grep -ch '    def test_' "$root"/tests/test_*.py 2>/dev/null | paste -sd+ - | bc 2>/dev/null || echo "?")

text=$(printf 'claude_rep state: branch %s, %s uncommitted file(s), %s commit(s) unpushed, %s unit tests.\nNo package manifest or linter here: python3 + stdlib only. Checks run via `python3 -m unittest discover -s tests -t .`.' \
  "$branch" "$dirty" "$ahead" "$tests")

jq -nc --arg t "$text" \
  '{hookSpecificOutput:{hookEventName:"SessionStart",additionalContext:$t}}'
exit 0
