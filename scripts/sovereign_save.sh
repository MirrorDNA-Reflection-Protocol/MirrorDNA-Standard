#!/bin/bash
# sovereign_save.sh
# Sovereign Save Protocol for Active MirrorOS

echo "⟡ Initiating Sovereign Checkpoint..."

# 1. Stage all changes
git add .

# 2. Commit with Timestamp
TIMESTAMP=$(date "+%Y-%m-%d %H:%M:%S")
git commit -m "⟡ Sovereign Save: $TIMESTAMP"

# 3. Confirm
echo "⟡ Checkpoint Created. Syncthing will replicate to Hub."
