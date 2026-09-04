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

grep -vE '^[[:space:]]*(#|$)' "$POTFILES" |
    grep -v '\.blp$' > "$OTHER_FILES"

grep -vE '^[[:space:]]*(#|$)' "$POTFILES" |
    grep '\.blp$' > "$BLP_FILES"

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
    --from-code=UTF-8 \
    --add-comments \
    --keyword=_ \
    --keyword=C_:1c,2 \
    --language=C \
    --join-existing \
    --output="$OUTPUT"

sed -i 's/charset=CHARSET/charset=UTF-8/g' "$OUTPUT"

choose_locale()
{
    local lang=$1
    local -a locales
    local choice

    mapfile -t locales < <(
        locale -a |
        grep -iE "^${lang}([_.@-].*)?([.]utf-?8|[.]utf8)$"
    )

    case ${#locales[@]} in
        0)
            echo "No UTF-8 locale found for '$lang'." >&2
            return 1
            ;;
        1)
            printf '%s\n' "${locales[0]}"
            ;;
        *)
            echo "Multiple locales found for '$lang':" >&2
            select choice in "${locales[@]}"; do
                [[ -n $choice ]] && {
                    printf '%s\n' "$choice"
                    break
                }
                echo "Invalid choice." >&2
            done
            ;;
    esac
}

create()
{
    local lang=$1
    local locale_code=$2
    
    msginit \
        -i "$OUTPUT" \
        -o "po/$lang.po" \
        -l "$locale_code"
    mkdir -p "po/locale/$lang/LC_MESSAGES"
    msgfmt \
        "po/$lang.po" \
        -o "po/locale/$lang/LC_MESSAGES/$PACKAGE_NAME.mo"
}

update()
{
    local lang=$1
    
    msgmerge \
        --previous \
        --backup=none \
        --update \
        "po/$lang.po" \
        "$OUTPUT"
    mkdir -p "po/locale/$lang/LC_MESSAGES"
    msgfmt \
        "po/$lang.po" \
        -o "po/locale/$lang/LC_MESSAGES/$PACKAGE_NAME.mo"
}

process()
{
    local lang=$1

    if [[ -f "po/$lang.po" ]]; then
        update "$lang"
    else
        create "$lang" "$(choose_locale "$lang")"
    fi
}

add()
{
    local lang=$1
    local locale_code
    local tmp

    locale_code=$(choose_locale "$lang") || return 1

    printf '%s\n' "$lang" >> "$LINGUAS"
    {
        grep '^#' "$LINGUAS"
        grep -vE '^[[:space:]]*(#|$)' "$LINGUAS" | sort
    } > "$LINGUAS.tmp"
    mv "$LINGUAS.tmp" "$LINGUAS"
    create "$lang" "$locale_code"
}

if [[ $# -gt 1 ]]; then
    echo "Usage: $0 [language]" >&2
    exit 1
fi

if [[ -n ${1:-} ]]; then
    if grep -qwF "$1" "$LINGUAS"; then
        process "$1"
    else
        add "$1"
    fi
else
    while read -ra languages; do
        for lang in "${languages[@]}"; do
            process "$lang"
        done
    done < <(grep -vE '^[[:space:]]*(#|$)' "$LINGUAS")
fi
