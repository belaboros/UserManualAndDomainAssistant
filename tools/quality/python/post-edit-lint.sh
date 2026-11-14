#!/usr/bin/env bash
# Claude Code PostToolUse hook (ADR-0006, ADR-0014): lint every Python file Claude just wrote or edited.
# Exit 2 sends the findings back to Claude, which fixes them straight away.
set -uo pipefail

root="${CLAUDE_PROJECT_DIR:-$(pwd)}"
file=$(jq -r '.tool_input.file_path // .tool_input.notebook_path // empty' 2>/dev/null)
[ -z "$file" ] && exit 0
case "$file" in
  *.py|*.pyi) ;;
  *) exit 0 ;;
esac
[ -f "$file" ] || exit 0

cd "$root" || exit 0
# Use the installed ruff directly: linting one file must not depend on the lockfile being current.
ruff="$root/.venv/bin/ruff"
[ -x "$ruff" ] || { echo "post-edit-lint: $ruff not found; run 'uv sync' first" >&2; exit 2; }
if ! out=$("$ruff" check --output-format concise "$file" 2>&1); then
  printf 'ruff found problems in %s (ADR-0014). Fix them before continuing:\n%s\n' "$file" "$out" >&2
  exit 2
fi
if ! out=$("$ruff" format --check --diff "$file" 2>&1); then
  printf '%s is not formatted. Run: uv run ruff format %s\n%s\n' "$file" "$file" "$out" >&2
  exit 2
fi
exit 0
