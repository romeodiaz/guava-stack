#!/bin/sh
set -eu

case "${1-}" in
    ''|--no-install) ;;
    *) echo "Usage: $0 [--no-install]" >&2; exit 2 ;;
esac
[ "$#" -le 1 ] || { echo "Usage: $0 [--no-install]" >&2; exit 2; }
dir=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
build="$dir/build"
app="$build/GuavaBar.app"
mkdir -p "$build" "$app/Contents/MacOS" "$app/Contents/Resources"
xcrun swiftc -O -parse-as-library -target "$(uname -m)-apple-macosx14.0" "$dir/GuavaBar.swift" -o "$build/guava-bar"
cp "$build/guava-bar" "$app/Contents/MacOS/guava-bar"
router="$dir/../guava-router/skills/guava-router"
cp "$router/slots.json" "$router/router-check.py" "$dir/guava.png" "$app/Contents/Resources/"
# The app icon, for Login Items and Finder: the guava logo at each size iconutil wants.
iconset="$build/AppIcon.iconset"
mkdir -p "$iconset"
for size in 16 32 128 256 512; do
    sips -z $size $size "$dir/../assets/logo.png" --out "$iconset/icon_${size}x${size}.png" > /dev/null
    sips -z $((size * 2)) $((size * 2)) "$dir/../assets/logo.png" --out "$iconset/icon_${size}x${size}@2x.png" > /dev/null
done
iconutil -c icns "$iconset" -o "$app/Contents/Resources/AppIcon.icns"
version=1.0.0
if [ -f "$dir/.claude-plugin/plugin.json" ]; then
    version=$(plutil -extract version raw -o - "$dir/.claude-plugin/plugin.json")
fi
cat > "$app/Contents/Info.plist" <<EOF
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0"><dict>
<key>CFBundleIdentifier</key><string>dev.workwithguava.guava-bar</string>
<key>CFBundleName</key><string>guava-bar</string>
<key>CFBundleExecutable</key><string>guava-bar</string>
<key>CFBundlePackageType</key><string>APPL</string>
<key>CFBundleIconFile</key><string>AppIcon</string>
<key>CFBundleShortVersionString</key><string>$version</string>
<key>LSUIElement</key><true/>
<key>LSMinimumSystemVersion</key><string>14.0</string>
</dict></plist>
EOF
codesign --force --sign - "$app"

fixture=$(mktemp -d)
trap 'rm -rf "$fixture"' 0
trap 'exit 1' 1 2 15
binary="$app/Contents/MacOS/guava-bar"
cat > "$fixture/context.md" <<'EOF'
## guava-stack settings

head-chef

- Claude Opus 5.5 (High) via Claude Code
  - Orchestration, research, planning.

line-cook

- GPT-6.1 Sol (High) via Codex
  - Bulk execution, coding.
EOF
touch "$fixture/sync.md"
GUAVA_HUB="$fixture" "$binary" show > "$fixture/show"
grep -Fx 'head-chef: Claude Opus 5.5 (High) via Claude Code' "$fixture/show" > /dev/null
grep -Fx 'line-cook: GPT-6.1 Sol (High) via Codex' "$fixture/show" > /dev/null
echo 'PASS: show parses both slots across blank lines'

# Picks follow the AI tools installed on this Mac, so each test sets its own through a stand-in zsh
# profile: "none" has no AI tools on PATH, "all" has stand-ins for the four that only leave a mark if run.
for set in none all; do
    mkdir -p "$fixture/$set/bin"
    printf 'export PATH="%s:/usr/bin:/bin"\n' "$fixture/$set/bin" > "$fixture/$set/.zprofile"
done
for tool in claude codex agy pi; do
    printf '#!/bin/sh\n: > "$GUAVA_HUB/agent-started"\n' > "$fixture/all/bin/$tool"
    chmod +x "$fixture/all/bin/$tool"
done
picks() { GUAVA_HUB="$1" ZDOTDIR="$fixture/$2" "$binary" picks "$3"; }
# Expected names come from slots.json, so a new model pick doesn't break the build.
name() { plutil -extract "$1" raw -o - "$router/slots.json"; }
sol=$(name claude-and-chatgpt.line-cook.name)
sonnet=$(name claude.line-cook.name)
flash=$(name google.line-cook.fallback.name)
deepseek=$(name openrouter.line-cook.name)
only() {
    if grep -v "$2" "$1"; then echo "FAIL: $3" >&2; exit 1; fi
}

picks "$fixture" none line-cook > "$fixture/picks"
grep -Fx "$sol (Medium) via Codex" "$fixture/picks" > /dev/null
grep -Fx "$sonnet (Max) via Claude Code" "$fixture/picks" > /dev/null
only "$fixture/picks" 'via \(Claude Code\|Codex\)$' 'Claude and ChatGPT slots offer another tool with none installed'
echo 'PASS: Claude and ChatGPT slots offer both tools, and only those, with no other tool installed'
mkdir "$fixture/claude"
printf 'head-chef\n\n- %s (High) via Claude Code\n\nline-cook\n\n- %s (Medium) via Claude Code (own pick)\n' "$(name claude.head-chef.name)" "$sonnet" > "$fixture/claude/context.md"
picks "$fixture/claude" none line-cook > "$fixture/claude-picks"
grep -Fx "$sonnet (High) via Claude Code" "$fixture/claude-picks" > /dev/null
only "$fixture/claude-picks" 'via Claude Code$' 'Claude-only slots offer another tool'
echo 'PASS: Claude-only slots, one an own pick, offer only Claude Code picks'
ln -s "$binary" "$fixture/guava-bar"
GUAVA_HUB="$fixture" ZDOTDIR="$fixture/none" "$fixture/guava-bar" picks line-cook > "$fixture/symlink-picks"
cmp "$fixture/picks" "$fixture/symlink-picks"
echo 'PASS: CLI symlink resolves bundled slots.json'
mkdir "$fixture/google"
printf 'line-cook\n\n- %s (High) via Antigravity CLI, falling back to %s (High) when its usage runs out\n' "$(name google.line-cook.name)" "$flash" > "$fixture/google/context.md"
picks "$fixture/google" none line-cook > "$fixture/google-picks"
grep -Fx "$flash (Low) via Antigravity CLI" "$fixture/google-picks" > /dev/null
only "$fixture/google-picks" '(\(Low\|Medium\|High\)) via Antigravity CLI' 'Google picks offer another tool, or an effort Antigravity lacks'
echo 'PASS: a Google AI slot offers Antigravity picks at Low, Medium and High, Gemini on its own included'
mkdir "$fixture/openrouter"
printf 'line-cook\n\n- %s (High) via Pi\n' "$deepseek" > "$fixture/openrouter/context.md"
picks "$fixture/openrouter" none line-cook > "$fixture/openrouter-picks"
grep -Fx "$deepseek (Max) via Pi" "$fixture/openrouter-picks" > /dev/null
only "$fixture/openrouter-picks" 'via Pi$' 'OpenRouter picks offer another tool'
echo 'PASS: an OpenRouter slot offers only Pi picks, at every effort'
picks "$fixture" all line-cook > "$fixture/all-picks"
grep -Fx "$flash (High) via Antigravity CLI" "$fixture/all-picks" > /dev/null
grep -Fx "$deepseek (High) via Pi" "$fixture/all-picks" > /dev/null
GUAVA_HUB="$fixture" ZDOTDIR="$fixture/all" "$binary" pairs > "$fixture/pairs"
[ "$(wc -l < "$fixture/pairs")" -eq 6 ]
grep -F "line-cook \"$flash (High) via Antigravity CLI\"" "$fixture/pairs" > /dev/null
grep -F "line-cook \"$deepseek (High) via Pi\"" "$fixture/pairs" > /dev/null
echo 'PASS: with all four tools installed, every plan pair is offered, Gemini and OpenRouter included'
[ ! -e "$fixture/agent-started" ]
code=0
GUAVA_HUB="$fixture" ZDOTDIR="$fixture/all" "$binary" set line-cook bogus > "$fixture/invalid" 2>&1 || code=$?
[ "$code" -eq 1 ]
[ ! -e "$fixture/agent-started" ]
grep -F 'guava-bar picks' "$fixture/invalid" > /dev/null
echo 'PASS: looking up tools runs none of them, and an invalid set exits 1 without starting an agent'

# A switch with stand-in tools: the copy changes at once, and a model that fails its test is switched back.
fake="$fixture/fake"
mkdir -p "$fake/bin" "$fake/hub"
printf '#!/bin/sh\necho "${REPLY:-done: mock}"\n' > "$fake/bin/claude"
cp "$fake/bin/claude" "$fake/bin/codex"
cat > "$fake/bin/python3" <<'EOF'
#!/bin/sh
echo "{\"slots\": [{\"ok\": $OK, \"verdict\": \"mock\"}]}"
EOF
chmod +x "$fake/bin/claude" "$fake/bin/codex" "$fake/bin/python3"
printf 'export PATH="%s:/usr/bin:/bin"\n' "$fake/bin" > "$fake/.zprofile"
# Never let this test reach the real tools, which would edit the owner's Notion.
if [ "$(ZDOTDIR="$fake" zsh -lc 'command -v claude python3' | tr '\n' ' ')" != "$fake/bin/claude $fake/bin/python3 " ]; then
    echo 'FAIL: stand-in tools are not first on PATH, so the switch test did not run' >&2; exit 1
fi
opus=$(name claude-and-chatgpt.head-chef.name)
printf 'head-chef\n\n- %s (High) via Claude Code\n  - jobs\n\nline-cook\n\n- %s (High) via Codex\n  - jobs\n' "$opus" "$sol" > "$fake/hub/context.md"
switch() { GUAVA_HUB="$fake/hub" ZDOTDIR="$fake" "$binary" set "$@" > "$fake/out" 2>&1; }
has() { grep -Fx -- "- $1" "$fake/hub/context.md" > /dev/null; }
OK=true switch line-cook "$sol (Medium) via Codex"
has "$sol (Medium) via Codex"
grep -Fx -- '  - jobs' "$fake/hub/context.md" > /dev/null
code=0
OK=false switch line-cook "$sol (Low) via Codex" || code=$?
[ "$code" -eq 1 ]
grep -F 'Switched back' "$fake/out" > /dev/null
has "$sol (Medium) via Codex"
OK=true switch head-chef "$opus (Max) via Claude Code" line-cook "$sonnet (High) via Claude Code"
has "$opus (Max) via Claude Code"
has "$sonnet (High) via Claude Code"
code=0
OK=false switch head-chef "$opus (Low) via Claude Code" line-cook "$sol (High) via Codex" || code=$?
[ "$code" -eq 1 ]
grep -F 'Switched back' "$fake/out" > /dev/null
has "$opus (Max) via Claude Code"
has "$sonnet (High) via Claude Code"
echo 'PASS: switching one slot or both edits only the model lines, and a failed test switches them all back'
code=0
REPLY='done: nothing. failed: not supported' OK=true switch line-cook "$sol (High) via Codex" || code=$?
[ "$code" -eq 1 ]
grep -F "Notion wasn't updated" "$fake/out" > /dev/null
has "$sol (High) via Codex"
echo "PASS: a reply that says done but also failed keeps the Mac switched and reports Notion wasn't updated"
echo 'Build and self-test passed.'

if [ "${1-}" != --no-install ]; then
    pkill -f 'GuavaBar.app/Contents/MacOS/guava-bar' || true
    mkdir -p "$HOME/Applications" "$HOME/.local/bin"
    rm -rf "$HOME/Applications/GuavaBar.app"
    cp -R "$app" "$HOME/Applications/GuavaBar.app"
    ln -sf "$HOME/Applications/GuavaBar.app/Contents/MacOS/guava-bar" "$HOME/.local/bin/guava-bar"
    open "$HOME/Applications/GuavaBar.app"
    echo "Installed $HOME/Applications/GuavaBar.app"
    echo "CLI: $HOME/.local/bin/guava-bar"
fi
