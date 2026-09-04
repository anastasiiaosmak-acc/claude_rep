#!/usr/bin/env bash
# PreToolUse:Bash — enforce CLAUDE.md rules 2 and 7 before a shell command runs.
# Reads the hook payload on stdin, prints a deny decision as JSON, exits 0 either way.
set -uo pipefail

payload=$(cat)
cmd=$(printf '%s' "$payload" | jq -r '.tool_input.command // ""')

deny() {
  jq -nc --arg r "$1" \
    '{hookSpecificOutput:{hookEventName:"PreToolUse",permissionDecision:"deny",permissionDecisionReason:$r}}'
  exit 0
}

case "$cmd" in
  *"rm -rf /"*|*"rm -rf ~"*|*"rm -rf .."*)
    deny "CLAUDE.md rule 7: refusing a recursive delete that reaches outside the repo." ;;
  *"git push --force"*|*"git push -f"*|*"git reset --hard origin"*)
    deny "CLAUDE.md rule 7: history-rewriting git command needs explicit human approval." ;;
esac

# Rule 2: a literal credential in a shell command lands in history and logs.
if printf '%s' "$cmd" | grep -qiE 'ghp_[A-Za-z0-9]{10,}|github_pat_[A-Za-z0-9_]{10,}|xox[baprs]-[A-Za-z0-9-]{10,}|BEGIN [A-Z ]*PRIVATE KEY|(api_secret|access_token|api_key)[[:space:]]*=[[:space:]]*[A-Za-z0-9]'; then
  deny "CLAUDE.md rule 2: this command carries a literal credential — pass it via an env var or a file outside the repo."
fi

exit 0
