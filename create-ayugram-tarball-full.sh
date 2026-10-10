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

echo "Cloning tlottie..."
TLOTTIE_STAGE="$(awk '/^stage\(.tlottie./,/^"""/' Telegram/build/prepare/prepare.py)"
TLOTTIE_REPO="$(printf '%s\n' "$TLOTTIE_STAGE" | sed -n 's/.*git clone \(.*tlottie[^ ]*\).*/\1/p' | head -n1)"
TLOTTIE_COMMIT="$(printf '%s\n' "$TLOTTIE_STAGE" | sed -n 's/.*git checkout //p' | head -n1)"
TLOTTIE_PATCH="$(printf '%s\n' "$TLOTTIE_STAGE" | sed -n 's/.*git apply .*patches\///p' | head -n1)"

git clone "${TLOTTIE_REPO:-https://github.com/dkaraush/tlottie.git}" "$TMPDIR/$TOPDIR/tlottie-src"
if [ -n "$TLOTTIE_COMMIT" ]; then
    git -C "$TMPDIR/$TOPDIR/tlottie-src" checkout "$TLOTTIE_COMMIT"
fi

if [ -n "$TLOTTIE_PATCH" ]; then
    PATCHES_STAGE="$(awk '/^stage\(.patches./,/^"""/' Telegram/build/prepare/prepare.py)"
    PATCHES_COMMIT="$(printf '%s\n' "$PATCHES_STAGE" | sed -n 's/.*git checkout //p' | head -n1)"
    git clone https://github.com/desktop-app/patches.git "$TMPDIR/patches"
    if [ -n "$PATCHES_COMMIT" ]; then
        git -C "$TMPDIR/patches" checkout "$PATCHES_COMMIT"
    fi
    git -C "$TMPDIR/$TOPDIR/tlottie-src" apply "$TMPDIR/patches/$TLOTTIE_PATCH"
fi
echo "tlottie commit: ${TLOTTIE_COMMIT:-default branch}, patch: ${TLOTTIE_PATCH:-none}"

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
