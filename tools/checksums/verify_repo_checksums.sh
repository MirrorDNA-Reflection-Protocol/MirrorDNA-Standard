#!/bin/bash
# verify_repo_checksums.sh
# Verifies all checksums in the MirrorDNA-Standard repository
# Usage: ./verify_repo_checksums.sh [repo_root_path]

REPO_ROOT="${1:-.}"

echo "⟡⟦INTEGRITY CHECK⟧ — Verifying MirrorDNA checksums..."
echo ""

# Find all markdown files with checksums in front matter (within first 50 lines)
FILES=$(find "$REPO_ROOT" -name "*.md" -type f -exec sh -c 'head -50 "$1" | grep -q "^checksum_sha256:" && echo "$1"' _ {} \;)

if [ -z "$FILES" ]; then
    echo "No files with checksums found in $REPO_ROOT"
    exit 0
fi

TOTAL=0
VALID=0
INVALID=0

for FILE in $FILES; do
    TOTAL=$((TOTAL + 1))

    # Extract declared checksum from front matter (first 50 lines only)
    DECLARED=$(head -50 "$FILE" | grep "^checksum_sha256:" | head -1 | awk '{print $2}')

    # Calculate actual checksum (excluding checksum line)
    TEMP=$(mktemp)
    grep -v "^checksum_sha256:" "$FILE" > "$TEMP"
    ACTUAL=$(shasum -a 256 "$TEMP" | awk '{print $1}')
    rm "$TEMP"

    # Compare
    if [ "$DECLARED" = "$ACTUAL" ]; then
        echo "✓ $FILE"
        VALID=$((VALID + 1))
    else
        echo "✗ $FILE"
        echo "  Declared: $DECLARED"
        echo "  Actual:   $ACTUAL"
        INVALID=$((INVALID + 1))
    fi
done

echo ""
echo "─────────────────────────────────────────"
echo "Total files: $TOTAL"
echo "Valid:       $VALID"
echo "Invalid:     $INVALID"
echo "─────────────────────────────────────────"

if [ $INVALID -gt 0 ]; then
    echo ""
    echo "⚠ Fix invalid checksums with:"
    echo "  ./checksum_updater.sh <file.md>"
    exit 1
else
    echo ""
    echo "⟡⟦INTEGRITY VERIFIED⟧ — All checksums valid"
    exit 0
fi
