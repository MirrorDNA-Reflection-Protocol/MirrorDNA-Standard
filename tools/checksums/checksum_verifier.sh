#!/bin/bash
# checksum_verifier.sh
# Verifies checksum_sha256 fields in MirrorDNA markdown files
# Usage: ./checksum_verifier.sh <file.md>
# Returns: 0 if valid, 1 if invalid

set -e

if [ $# -eq 0 ]; then
    echo "Usage: $0 <markdown_file>"
    echo "Example: $0 00_MASTER_CITATION.md"
    exit 1
fi

FILE="$1"

if [ ! -f "$FILE" ]; then
    echo "Error: File '$FILE' not found"
    exit 1
fi

# Check if file has a checksum line
if ! grep -q "^checksum_sha256:" "$FILE"; then
    echo "⚠ Warning: File does not contain 'checksum_sha256:' field"
    exit 0
fi

# Extract declared checksum
DECLARED_CHECKSUM=$(grep "^checksum_sha256:" "$FILE" | awk '{print $2}')

# Create temp file without checksum line
TEMP_FILE=$(mktemp)
grep -v "^checksum_sha256:" "$FILE" > "$TEMP_FILE"

# Calculate actual checksum
ACTUAL_CHECKSUM=$(shasum -a 256 "$TEMP_FILE" | awk '{print $1}')

# Clean up
rm "$TEMP_FILE"

# Compare
if [ "$DECLARED_CHECKSUM" = "$ACTUAL_CHECKSUM" ]; then
    echo "✓ Checksum valid"
    echo "  File: $FILE"
    echo "  Checksum: $ACTUAL_CHECKSUM"
    exit 0
else
    echo "✗ Checksum MISMATCH"
    echo "  File: $FILE"
    echo "  Declared: $DECLARED_CHECKSUM"
    echo "  Actual:   $ACTUAL_CHECKSUM"
    echo ""
    echo "  Run './checksum_updater.sh $FILE' to fix"
    exit 1
fi
