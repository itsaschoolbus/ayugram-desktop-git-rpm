#!/usr/bin/env bash
set -euo pipefail

SCRIPT_PWD="$(pwd)"

REPO="https://github.com/AyuGram/AyuGramDesktop.git"

TOPDIR="AyuGramDesktop-full"
TARBALL="${TOPDIR}.tar.gz"

TMPDIR="$(mktemp -d)"
trap 'rm -rf "$TMPDIR"' EXIT

echo "Cloning AyuGramDesktop with submodules..."
git clone --recursive "$REPO" "$TMPDIR/$TOPDIR"

cd "$TMPDIR/$TOPDIR"

echo "Generating bundled() Provides into provides.txt..."

PROVIDES_FILE="${SCRIPT_PWD}/provides.txt"
: > "$PROVIDES_FILE"

git submodule foreach --recursive --quiet '
commit=$(git rev-parse --short=7 HEAD)
url=$(git config --get remote.origin.url)
name="${url##*/}"
name="${name%.git}"

if tag=$(git describe --tags --exact-match 2>/dev/null); then
    ver=${tag#v}
elif tag=$(git describe --tags --abbrev=0 2>/dev/null); then
    ver="${tag#v}~git${commit}"
else
    ver="0~git${commit}"
fi

echo "# $url"
echo "Provides: bundled(${name}) = ${ver}"
' >> "$PROVIDES_FILE"

echo "Generating version..."
if GIT_VERSION=$(git describe --tags --long 2>/dev/null); then
    VERSION=$(echo "$GIT_VERSION" | sed -E 's/^v//; s/-([0-9]+)-g([0-9a-f]+)$/.git.\1.\2/')
fi

echo "Removing all .git directories..."
find . -name .git -prune -exec rm -rf {} +

cd "$TMPDIR"

echo "Creating tarball ${TARBALL}..."
tar --sort=name \
    --mtime="@${SOURCE_DATE_EPOCH:-$(date +%s)}" \
    --owner=0 --group=0 --numeric-owner \
    -czf "$TARBALL" "$TOPDIR"

mv "$TARBALL" "$SCRIPT_PWD/"

SPEC_FILE="${SCRIPT_PWD}/ayugram-desktop-git.spec"
if [ -f "$SPEC_FILE" ]; then
    sed -i "s/^Version:.*/Version: ${VERSION}/" "$SPEC_FILE"
    sed -i "s/^Source0:.*/Source0: ${TARBALL}/" "$SPEC_FILE"
fi

echo "Done:"
echo "$(readlink -f "$SCRIPT_PWD/$TARBALL")"
