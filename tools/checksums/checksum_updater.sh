#!/bin/bash
# checksum_updater.sh
# Automatically updates checksum_sha256 fields in MirrorDNA markdown files
# Usage: ./checksum_updater.sh <file.md>

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
    echo "Error: File does not contain 'checksum_sha256:' field"
    exit 1
fi

# Create temp file without checksum line
TEMP_FILE=$(mktemp)
grep -v "^checksum_sha256:" "$FILE" > "$TEMP_FILE"

# Calculate new checksum
NEW_CHECKSUM=$(shasum -a 256 "$TEMP_FILE" | awk '{print $1}')

# Update the file with new checksum
sed -i.bak "s/^checksum_sha256:.*/checksum_sha256: $NEW_CHECKSUM/" "$FILE"

# Verify the update worked
if grep -q "checksum_sha256: $NEW_CHECKSUM" "$FILE"; then
    echo "✓ Checksum updated successfully"
    echo "  File: $FILE"
    echo "  New checksum: $NEW_CHECKSUM"
    rm "$FILE.bak"
    rm "$TEMP_FILE"
else
    echo "✗ Checksum update failed"
    mv "$FILE.bak" "$FILE"
    rm "$TEMP_FILE"
    exit 1
fi
