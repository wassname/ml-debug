#!/bin/sh
# Link every skill in this repository into an agent's skills directory.
#   ./install.sh ~/.claude/skills        (or ~/.agents/skills, ~/.pi/agent/skills, ...)
# The repository root is the skill `ml-debug`; each first-level directory with a SKILL.md is one
# more skill, linked under the `name:` in its front matter. Nothing is copied, so `git pull`
# updates every skill. An existing path that is not a link to this repository stops the script.
set -eu
target=${1:?usage: ./install.sh <skills directory>}
repo=$(cd "$(dirname "$0")" && pwd -P)
mkdir -p "$target"
link() {  # link <source dir> <skill name>
    dest="$target/$2"
    if [ "$(cd "$target" && cd "$2" 2>/dev/null && pwd -P)" = "$1" ]; then echo "ok       $2"; return; fi
    if [ -e "$dest" ] || [ -L "$dest" ]; then echo "STOP: $dest exists and is not this repository's $2" >&2; exit 1; fi
    ln -s "$1" "$dest"; echo "linked   $2 -> $1"
}
link "$repo" ml-debug
for f in "$repo"/*/SKILL.md; do
    name=$(sed -n 's/^name: *//p' "$f" | head -1 | tr -d '"')
    [ -n "$name" ] || { echo "STOP: no name in $f" >&2; exit 1; }
    link "$(dirname "$f")" "$name"
done
