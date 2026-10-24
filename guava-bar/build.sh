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
cp "$dir/../guava-router/skills/guava-router/slots.json" "$dir/guava.png" "$app/Contents/Resources/"
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
GUAVA_HUB="$fixture" "$binary" picks line-cook > "$fixture/picks"
grep -Fx 'GPT-6.1 Sol (Medium) via Codex' "$fixture/picks" > /dev/null
if grep -q Antigravity "$fixture/picks"; then
    echo 'FAIL: non-Google picks contain Antigravity' >&2; exit 1
fi
echo 'PASS: non-Google picks include Sol Medium and exclude Antigravity'
ln -s "$binary" "$fixture/guava-bar"
GUAVA_HUB="$fixture" "$fixture/guava-bar" picks line-cook > "$fixture/symlink-picks"
cmp "$fixture/picks" "$fixture/symlink-picks"
echo 'PASS: CLI symlink resolves bundled slots.json'
cat > "$fixture/context.md" <<'EOF'
line-cook

- Claude Sonnet 5.5 (High) via Antigravity CLI, falling back to Gemini 3.8 Flash (High) when its usage runs out
EOF
GUAVA_HUB="$fixture" "$binary" picks line-cook > "$fixture/picks"
[ -s "$fixture/picks" ]
if grep -v 'via Antigravity CLI' "$fixture/picks"; then
    echo 'FAIL: Google picks contain another tool' >&2; exit 1
fi
echo 'PASS: Google-only slot offers only Antigravity picks'
printf 'line-cook\n\n- DeepSeek V4.1 Flash 1017 (High) via Pi\n' > "$fixture/context.md"
GUAVA_HUB="$fixture" "$binary" picks line-cook > "$fixture/picks"
[ -s "$fixture/picks" ]
if grep -v 'via Pi$' "$fixture/picks"; then
    echo 'FAIL: OpenRouter picks contain another tool' >&2; exit 1
fi
echo 'PASS: OpenRouter-only slot offers only Pi picks'
# Any agent lookup or run starts zsh; invalid input must not even reach that shell.
printf ': > "$GUAVA_HUB/agent-started"\n' > "$fixture/.zshenv"
code=0
GUAVA_HUB="$fixture" ZDOTDIR="$fixture" "$binary" set line-cook bogus > "$fixture/invalid" 2>&1 || code=$?
[ "$code" -eq 1 ]
[ ! -e "$fixture/agent-started" ]
grep -F 'guava-bar picks line-cook' "$fixture/invalid" > /dev/null
echo 'PASS: invalid set exits 1 without starting an agent or shell'
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
