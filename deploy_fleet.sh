#!/bin/bash
# Active MirrorOS Fleet Deployer
# Purpose: Inject Sovereign Protocols into all repositories

SOURCE_DIR=$(pwd)
TARGET_ROOT=~/Documents/GitHub

echo "⟡ Starting Fleet Deployment..."

# Loop through all directories in GitHub folder
for repo in "$TARGET_ROOT"/*; do
    if [ -d "$repo" ]; then
        repo_name=$(basename "$repo")
        echo ">> Upgrading: $repo_name"

        # 1. Create scripts folder
        mkdir -p "$repo/scripts"

        # 2. Copy the Save Script
        cp "$SOURCE_DIR/scripts/sovereign_save.sh" "$repo/scripts/"
        chmod +x "$repo/scripts/sovereign_save.sh"

        # 3. Copy the Agent Rules
        cp "$SOURCE_DIR/.cursorrules" "$repo/"

        # 4. Set Local Identity (Just in case)
        cd "$repo"
        git config user.name "Paul Desai"
        git config user.email "paul.mirroros@hotmail.com"
        
        echo "   [✓] Sovereign Kit Installed"
    fi
done

echo "⟡ Fleet Upgrade Complete. All systems Sovereign."
