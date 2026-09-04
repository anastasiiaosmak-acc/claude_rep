#!/usr/bin/env bash
# PostToolUse:Write|Edit — parse a .py file that was just written and block on a syntax error.
# Uses ast.parse rather than py_compile so no __pycache__ artifacts are produced.
set -uo pipefail

payload=$(cat)
file=$(printf '%s' "$payload" | jq -r '.tool_input.file_path // .tool_response.filePath // ""')

case "$file" in
  *.py) ;;
  *) exit 0 ;;
esac
[ -f "$file" ] || exit 0

if err=$(python3 -c 'import ast,sys; ast.parse(open(sys.argv[1],encoding="utf-8").read(), sys.argv[1])' "$file" 2>&1); then
  exit 0
fi

jq -nc --arg e "$err" --arg f "$file" \
  '{decision:"block",
    reason:("Syntax error in " + $f + " — fix it before moving on:\n" + $e),
    systemMessage:("Blocked: " + $f + " does not parse (CLAUDE.md rule 5).")}'
exit 0
