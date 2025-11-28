#!/usr/bin/env bash
#
# Install MirrorDNA Git Hooks
#
# Usage: bash .githooks/install.sh

set -e

echo "⟡⟦INSTALLING MIRRORDNA GIT HOOKS⟧"
echo ""

# Check if in git repository
if [ ! -d ".git" ]; then
    echo "✗ Error: Not in a git repository root"
    echo "  Run this script from the repository root directory"
    exit 1
fi

# Option 1: Use core.hooksPath (recommended - affects all hooks)
echo "Installing hooks using git config core.hooksPath..."
git config core.hooksPath .githooks

# Make hooks executable
chmod +x .githooks/pre-commit
chmod +x .githooks/commit-msg
chmod +x .githooks/pre-push

echo ""
echo "✓ Git hooks installed successfully"
echo ""
echo "Installed hooks:"
echo "  - pre-commit: Runs reflective_reviewer.py on staged files"
echo "  - commit-msg: Validates commit message format"
echo "  - pre-push: Verifies vault integrity"
echo ""
echo "To bypass hooks temporarily, use:"
echo "  git commit --no-verify"
echo "  git push --no-verify"
echo ""
echo "To uninstall:"
echo "  git config --unset core.hooksPath"
echo ""

exit 0
