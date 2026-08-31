#!/usr/bin/env bash
set -euo pipefail

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$PROJECT_ROOT"

OUTPUT="po/io.github.yioannides.Throwdown.pot"
PACKAGE_NAME="io.github.yioannides.Throwdown"
POTFILES="po/POTFILES.in"
LINGUAS="po/LINGUAS"

OTHER_FILES=$(mktemp)
BLP_FILES=$(mktemp)
trap 'rm -f "$OTHER_FILES" "$BLP_FILES"' EXIT

grep -vE '^[[:space:]]*(#|$)' "$POTFILES" | grep -v '\.blp$' > "$OTHER_FILES"
grep -vE '^[[:space:]]*(#|$)' "$POTFILES" | grep '\.blp$' > "$BLP_FILES"

xgettext \
    --files-from="$OTHER_FILES" \
    --output="$OUTPUT" \
    --package-name="$PACKAGE_NAME" \
    --from-code=UTF-8 \
    --add-comments \
    --keyword=_ \
    --keyword=C_:1c,2

xgettext \
    --files-from="$BLP_FILES" \
    --output="$OUTPUT" \
    --package-name="$PACKAGE_NAME" \
    --from-code=UTF-8 \
    --add-comments \
    --keyword=_ \
    --keyword=C_:1c,2 \
    --language=C \
    --join-existing

sed -i 's/charset=CHARSET/charset=UTF-8/g' "$OUTPUT"

grep -vE '^[[:space:]]*(#|$)' "$LINGUAS" |
while read -r line; do
    for lang in $line; do
    		if [ ! -f po/${lang}.po ]; then
            echo -ne "Requesting locale code for: \e[1m${lang}\e[0m > "
            read -r REQ < /dev/tty
            msginit -i "$OUTPUT" -o "po/${lang}.po" -l "${REQ}.utf8"
    		else
		    msgmerge \
		        --previous \
		        --backup=none \
		        --update \
		        "po/${lang}.po" \
		        "$OUTPUT"
		fi
    done
done