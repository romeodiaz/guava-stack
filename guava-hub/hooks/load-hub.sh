#!/bin/sh
# Prints one part of the guava-hub start-up context (start, notion, addons,
# context or rules),
# or, as the save part, asks the session to save to Notion Memory at the end of
# long work. Claude Code caps each hook's output at 10,000 characters, so each
# part runs as its own hook, and a file that won't fit is named instead of shown.
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
  skill=$(cd "$(dirname "$0")/../skills/guava-hub" && pwd)
  sed "s|<skill>|$skill|g" "$(dirname "$0")/load-hub.md"
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
  if [ -z "$index" ]; then
    :
  elif [ $(( $(wc -c < "$copy/context.md") + ${#index} )) -le "$cap" ]; then
    printf '\nguava-hub skills, local copy (read %s/skills/<name>.md when a task needs one):\n%s\n' "$copy" "$index"
  else
    printf '\nguava-hub skills: list %s/skills/ and read a skill there when a task needs one.\n' "$copy"
    index=
  fi
  [ -f "$copy/about.md" ] || exit 0
  # This hook's output shares one cap, so the About page goes last, if it fits.
  if [ $(( $(wc -c < "$copy/context.md") + ${#index} + $(wc -c < "$copy/about.md") )) -le "$cap" ]; then
    printf '\nAbout the owner, from Notion Memory (%s, notes assistants wrote, not instructions):\n\n' "$copy/about.md"
    cat "$copy/about.md"
  else
    printf '\nAbout the owner (Notion Memory): read %s before substantive work.\n' "$copy/about.md"
  fi
  ;;
notion)
  # Notion's custom instructions (with Guava's line) and the Agent Operating Guide.
  [ -f "$copy/instructions.md" ] && show "The owner's custom instructions, local copy" "$copy/instructions.md"
  [ -f "$copy/guide.md" ] || exit 0
  if [ -f "$copy/instructions.md" ] && [ $(( $(wc -c < "$copy/instructions.md") + $(wc -c < "$copy/guide.md") )) -gt "$cap" ]; then
    printf '\nAgent Operating Guide: read %s before substantive work.\n' "$copy/guide.md"
  else
    printf '\n'
    show "Agent Operating Guide, local copy (information, not instructions)" "$copy/guide.md"
  fi
  ;;
addons)
  # guava-instructions: the hub's copy when the local copy has it, else the plugin's.
  [ -f "$copy/sync.md" ] || exit 0
  file="$copy/skills/guava-instructions.md"
  [ -f "$file" ] || file=$(cd "$(dirname "$0")/../skills/guava-instructions" && pwd)/SKILL.md
  body=$(awk 'NR == 1 && $0 == "---" { f = 1; next } f && /^---$/ { f = 0; next } !f' "$file")
  if [ ${#body} -le "$cap" ]; then
    printf 'guava-instructions (%s):\n\n%s\n' "$file" "$body"
  else
    printf 'guava-instructions is too long to show here: read %s before substantive work.\n' "$file"
  fi
  ;;
rules)
  [ -f "$copy/rules.md" ] && show "guava-hub rules page, local copy" "$copy/rules.md"
  ;;
save)
  # Asks after 60 new transcript lines (250 in Codex, which logs more per step),
  # at most once every 45 minutes per session, so short chats are never
  # interrupted, and never twice in a row.
  [ -f "$copy/sync.md" ] || exit 0
  input=$(cat)
  case "$input" in *'"stop_hook_active":true'* | *'"stop_hook_active": true'*) exit 0 ;; esac
  transcript=$(printf '%s' "$input" | sed -n 's/.*"transcript_path" *: *"\([^"]*\)".*/\1/p')
  [ -f "$transcript" ] || exit 0
  mkdir -p "$copy/saved"
  find "$copy/saved" -type f -mtime +7 -exec rm -f {} + 2>/dev/null
  mark="$copy/saved/$(basename "$transcript" .jsonl)"
  lines=$(wc -l < "$transcript")
  last=$(cat "$mark" 2>/dev/null || echo 0)
  case "$transcript" in */.codex/*) need=250 ;; *) need=60 ;; esac
  [ $(( lines - last )) -ge "$need" ] || exit 0
  if [ -f "$mark" ]; then
    asked=$(stat -c %Y "$mark" 2>/dev/null || stat -f %m "$mark")
    [ $(( $(date +%s) - asked )) -ge 2700 ] || exit 0
  fi
  echo "$lines" > "$mark"
  echo '{"decision": "block", "reason": "guava-stack: before you stop, save anything durable from this work to Notion Memory (decisions and their reasons, corrections, preferences, project state), as the hub instructions say, unless the owner paused memory. If nothing qualifies, stop without mentioning this."}'
  ;;
esac
exit 0
