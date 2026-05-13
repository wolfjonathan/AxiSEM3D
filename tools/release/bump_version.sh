#!/usr/bin/env bash
set -euo pipefail

shopt -s nullglob

if [[ $# -ne 1 || -z $1 ]]; then
  echo "Usage: ${0##*/} <version>" >&2
  exit 1
fi

readonly NEW_VERSION="$1"
ROOT="$(cd $(dirname "${BASH_SOURCE[0]}")/../../ && pwd)"
readonly ROOT
echo "ROOT = $ROOT"
printf '%s\n' "$NEW_VERSION" > "$ROOT/VERSION"

updated=0
for screen in "$ROOT/tests/"*/screen-output; do
  tmp="$(mktemp)"
  awk -v ver="$NEW_VERSION" '
    NR == 10 { sub(/v [^[:space:]]+/, "v " ver) }
    { print }
  ' "$screen" > "$tmp"
  mv "$tmp" "$screen"
  ((++updated))
done

if ((updated == 0)); then
  echo "warning: no tests/*/screen-output files found" >&2
fi
