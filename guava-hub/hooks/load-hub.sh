#!/bin/sh
# Prints one part of the guava-hub start-up context: start, context or rules.
# Claude Code caps each hook's output at 10,000 characters, so each part runs
# as its own hook, and a file that won't fit is named instead of shown.
copy="$HOME/.guava-hub"
cap=9000

# show TITLE FILE: print FILE under TITLE if it fits, or say where to read it.
show() {
  if [ "$(wc -c < "$2")" -le "$cap" ]; then
    printf '%s (%s):\n\n' "$1" "$2"
    cat "$2"
  else
    printf '%s is too long to show here: read %s before substantive work.\n' "$1" "$2"
  fi
}

case "$1" in
start)
  cat "$(dirname "$0")/load-hub.md"
  echo
  if [ ! -f "$copy/sync.md" ]; then
    echo "Local copy of a Notion guava-hub: none yet at $copy."
    exit 0
  fi
  modified=$(stat -c %Y "$copy/sync.md" 2>/dev/null || stat -f %m "$copy/sync.md")
  age=$(( ($(date +%s) - modified) / 60 ))
  if [ "$age" -lt 15 ]; then state=fresh; else state="due for a refresh"; fi
  echo "Local copy of the Notion guava-hub: $copy, refreshed $age minutes ago, so it's $state."
  ;;
context)
  [ -f "$copy/context.md" ] || exit 0
  show "guava-hub context page, local copy" "$copy/context.md"
  index=$(for f in "$copy"/skills/*.md; do
    [ -f "$f" ] && awk 'NR == 1 && $0 != "---" { exit }
      /^name: / { n = substr($0, 7) }
      /^description: / { d = substr($0, 14) }
      NR > 1 && /^---$/ { print "- " n ": " d; exit }' "$f"
  done)
  [ -n "$index" ] || exit 0
  if [ $(( $(wc -c < "$copy/context.md") + ${#index} )) -le "$cap" ]; then
    printf '\nguava-hub skills, local copy (read %s/skills/<name>.md when a task needs one):\n%s\n' "$copy" "$index"
  else
    printf '\nguava-hub skills: list %s/skills/ and read a skill there when a task needs one.\n' "$copy"
  fi
  ;;
rules)
  [ -f "$copy/rules.md" ] && show "guava-hub rules page, local copy" "$copy/rules.md"
  ;;
esac
exit 0
