#!/bin/sh
# Bismillah
#
# update-web.sh - ozdenui v0.1 (OzdenUI: basic.js for Python)
# Copies basic.js (the min files, scroll-bar, the fonts, the license) and every component of comp/ (the .js files and
# their asset folders) from the repository into the package. Run it again after basic/ or comp/ changes.
# Usage: ./update-web.sh                                  (inside the js-components repository)
#        ./update-web.sh --commit HEAD                    the files as they are in a commit of the repository
#        BASIC_REPO=path/to/js-components ./update-web.sh  (from a clone of ozdenui-python)
# WHY --commit: other sessions work in the same folder; a file of basic/ or comp/ they changed and did not commit went
#     into the package with the folder.
#
# Started Date: November 2026
# Webpage: https://bug7a.github.io/ozdenui-python/
#
# Copyright 2020-2026 Bugra Ozden <bugra.ozden@gmail.com> (https://bug7a.github.io/)
# Licensed under the Apache License, Version 2.0
# SPDX-License-Identifier: Apache-2.0

set -e
cd "$(dirname "$0")"

REPO="${BASIC_REPO:-../../..}"
if [ "${1:-}" = "--commit" ]; then
    COMMIT="${2:?the commit: ./update-web.sh --commit HEAD}"
    # WHY: git archive of a mistyped commit fails, but tar takes the empty input without a word
    if ! git -C "$REPO" rev-parse --verify --quiet "$COMMIT^{commit}" >/dev/null; then
        echo "Not a commit of $REPO: $COMMIT (nothing was changed)" >&2
        exit 1
    fi
    SNAPSHOT="$(mktemp -d)"
    trap 'rm -rf "$SNAPSHOT"' EXIT
    git -C "$REPO" archive "$COMMIT" basic comp | tar -x -C "$SNAPSHOT"
    echo "From the commit $(git -C "$REPO" rev-parse --short "$COMMIT")"
    REPO="$SNAPSHOT"
fi
BASIC_TARGET="ozdenui/web/basic"
COMP_TARGET="ozdenui/web/comp"

# WHY before the old copy goes: an empty source (a wrong BASIC_REPO, a failed archive) left the package without
#     basic.js and the components, as the copy below failed after the delete
if [ ! -f "$REPO/basic/basic.min.js" ] || [ ! -d "$REPO/comp" ]; then
    echo "No basic/basic.min.js and comp/ in $REPO (nothing was changed)" >&2
    exit 1
fi
rm -rf "$BASIC_TARGET" "$COMP_TARGET"
mkdir -p "$BASIC_TARGET/font" "$COMP_TARGET"
cp "$REPO/basic/basic.min.js" "$REPO/basic/basic.min.css" "$REPO/basic/scroll-bar.min.js" "$REPO/basic/LICENSE" "$BASIC_TARGET/"
cp -R "$REPO/basic/font/open-sans" "$BASIC_TARGET/font/"
cp "$REPO"/comp/*.js "$COMP_TARGET/"
for folder in "$REPO"/comp/*/; do
    cp -R "${folder%/}" "$COMP_TARGET/"  # WHY no slash: "cp -R x/ y" copies the contents of x, not x
done
find "$COMP_TARGET" \( -name "*.webloc" -o -name ".DS_Store" \) -delete  # not files of a component
# WHY: the components name their icons from 02-comp-examples/ ("../comp/x/icon.png"); the page of the package stands
#      next to comp/, so those icons were not found (SmartTable had no arrows).
sed -i.bak 's#\.\./comp/#comp/#g' "$COMP_TARGET"/*.js
rm "$COMP_TARGET"/*.js.bak
# WHY: a file of the repository may be readable only by its owner (search-input.js was 600)
find ozdenui/web -type f -exec chmod 644 {} +
find ozdenui/web -type d -exec chmod 755 {} +

VERSION=$(grep -m1 -o 'basic.js (v[0-9.]*)' "$BASIC_TARGET/basic.min.js")
COUNT=$(ls "$COMP_TARGET"/*.js | wc -l | tr -d ' ')
echo "Copied $VERSION and $COUNT components into ozdenui/web"

# WHY: the stubs hold the params of the components; a new param of the kit is offered by an editor only after this
if [ -x .venv/bin/python ]; then
    .venv/bin/python make_stubs.py
else
    echo "Run make_stubs.py with the Python of the package: the stubs hold the params of the kit"
fi
