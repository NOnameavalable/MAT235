#!/bin/sh
set -eu

SCRIPT_DIR=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
cd "$SCRIPT_DIR/.."

for source in Study-Notes Answers-and-Practice; do
  pandoc --standalone --pdf-engine=xelatex \
    --metadata-file=scripts/pdf-metadata.yaml \
    --lua-filter=scripts/pdf-layout.lua \
    "$source.md" -o "$source.pdf"
done
