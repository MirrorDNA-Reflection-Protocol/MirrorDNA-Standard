# MirrorDNA Tools

Automation scripts and utilities for maintaining MirrorDNA Standard compliance, integrity verification, and release management.

---

## Table of Contents

1. [Overview](#overview)
2. [Checksum Tools](#checksum-tools)
3. [Version Management](#version-management)
4. [Blockchain Anchoring](#blockchain-anchoring)
5. [Quick Reference](#quick-reference)
6. [Installation](#installation)
7. [CI/CD Integration](#cicd-integration)

---

## Overview

This directory contains shell scripts for:
- **Integrity verification**: SHA-256 checksum validation for anti-hallucination protocol (AHP)
- **Version management**: Automatic version sidecar file generation
- **Blockchain anchoring**: Optional immutable timestamping on public blockchains
- **Release automation**: Preparing and validating releases

All tools follow MirrorDNA principles: **Trust by Design**, **Continuity**, and **Anti-Hallucination Protocol**.

---

## Checksum Tools

### Purpose

Maintain and verify SHA-256 checksums in MirrorDNA markdown files to ensure **integrity** and support the **Anti-Hallucination Protocol (AHP)**. Checksums provide tamper detection and verifiable citations.

### Tools Location

```
tools/checksums/
├── checksum_verifier.sh      # Verify existing checksums
├── checksum_updater.sh        # Update checksums after edits
├── verify_repo_checksums.sh  # Batch verify all files
└── CHECKSUM_TOOLS_README.md  # Detailed checksum documentation
```

### 1. `checksum_verifier.sh`

**Verifies** that a file's declared `checksum_sha256:` matches its actual content.

#### Usage

```bash
cd /home/user/MirrorDNA-Standard
./tools/checksums/checksum_verifier.sh 00_MASTER_CITATION.md
```

#### Output

```
✓ Checksum valid
  File: 00_MASTER_CITATION.md
  Checksum: 788ccffe78de2633332c3b1629a002f283c5337d5df327ede84c6997750a143a
```

#### Exit Codes

- `0` = checksum valid
- `1` = checksum invalid or missing

#### When to Use

- Before committing changes
- After pulling updates
- During CI/CD validation
- When verifying artifact integrity

---

### 2. `checksum_updater.sh`

**Updates** the `checksum_sha256:` field with the correct hash after file modifications.

#### Usage

```bash
# After editing a file
./tools/checksums/checksum_updater.sh spec/mirrorDNA-standard-v1.0.md
```

#### What It Does

1. Removes the existing `checksum_sha256:` line from the file
2. Calculates SHA-256 of the remaining content
3. Updates the file with the new checksum
4. Creates a `.bak` backup (removed on success)

#### When to Use

- After editing any spec file with a checksum field
- Before committing changes to Git
- When verification fails and you need to recalculate
- As part of your document update workflow

#### Example Workflow

```bash
# 1. Edit the file
vim spec/principles.md

# 2. Update checksum automatically
./tools/checksums/checksum_updater.sh spec/principles.md

# 3. Verify it worked
./tools/checksums/checksum_verifier.sh spec/principles.md

# 4. Commit
git add spec/principles.md
git commit -m "Update principles.md content and checksum"
```

---

### 3. `verify_repo_checksums.sh`

**Batch verifies** all checksummed files in the repository.

#### Usage

```bash
# From repo root
./tools/checksums/verify_repo_checksums.sh

# Or specify path
./tools/checksums/verify_repo_checksums.sh /path/to/MirrorDNA-Standard
```

#### Output

```
⟡⟦INTEGRITY CHECK⟧ — Verifying MirrorDNA checksums...

✓ 00_MASTER_CITATION.md
✓ spec/mirrorDNA-standard-v1.0.md
✓ spec/Reflection_Chain_Manifest_v1.0.md
✓ spec/principles.md

─────────────────────────────────────────
Total files: 4
Valid:       4
Invalid:     0
─────────────────────────────────────────

⟡⟦INTEGRITY VERIFIED⟧ — All checksums valid
```

#### When to Use

- Before pushing to GitHub
- As part of pre-commit hooks
- In CI/CD pipelines
- Before creating releases
- When auditing repository integrity

---

### How Checksums Work

The checksum is calculated **excluding the checksum line itself** to prevent circular dependency.

#### Example File

```markdown
---
title: "Example Spec"
version: 1.0.0
vault_id: AMOS://Example/v1.0
checksum_sha256: abc123def456...
---

# Example Specification

Content here...
```

#### Calculation Process

1. Remove the line: `checksum_sha256: abc123def456...`
2. Calculate SHA-256 of remaining text
3. That hash becomes the checksum value
4. Insert checksum back into the file

This ensures:
- Checksum is verifiable without knowing the checksum itself
- Content tampering is detectable
- AHP compliance (cited sources with integrity verification)

---

### Detailed Documentation

For comprehensive checksum tool documentation, see:
- **[tools/checksums/CHECKSUM_TOOLS_README.md](checksums/CHECKSUM_TOOLS_README.md)**

Covers:
- Detailed usage examples
- CI/CD integration patterns
- Troubleshooting guide
- Windows/macOS/Linux compatibility

---

## Version Management

### `add_version_sidecars.sh`

Automatically adds version metadata to JSON sidecar files.

#### Purpose

Ensures all JSON metadata files (sidecars) include a `version` field for lineage tracking and compatibility checking.

#### Usage

```bash
# Add version 1.0.0 to all sidecar files
./tools/add_version_sidecars.sh 1.0.0

# Default version (1.0.0) if not specified
./tools/add_version_sidecars.sh
```

#### What It Does

1. Scans repository for JSON sidecar files (`*sidecar.json`, `kernel/**/*.json`)
2. Checks if each file has a `version` field
3. Adds version metadata if missing
4. Uses `jq` if available, falls back to `awk` otherwise

#### Output

```
Added version to: CHANGELOG_v1.sidecar.json
Added version to: kernel/GlyphKernel_Ecosystem.sidecar.json
Done. Files edited: 2
```

#### When to Use

- Before releasing a new version
- After creating new sidecar files
- When standardizing version metadata across the repository

#### Sidecar File Example

**Before:**
```json
{
  "description": "CHANGELOG metadata"
}
```

**After:**
```json
{
  "version": "1.0.0",
  "description": "CHANGELOG metadata"
}
```

---

## Blockchain Anchoring

### `publish_blockchain_anchor.sh`

Compute SHA-256 hashes for canonical artifacts and prepare blockchain anchor metadata.

#### Purpose

Provides **optional immutable timestamping** by logging checksums that can be notarized on public blockchains (Ethereum, Polygon, etc.). This supports:
- Immutable proof of existence at a specific time
- Tamper-evident version history
- Public auditability
- Advanced trust markers

**Note**: This is an **optional** Level 3+ feature. Not required for basic MirrorDNA compliance.

#### Usage

```bash
# Basic: Compute hash and log metadata
./tools/publish_blockchain_anchor.sh spec/Reflection_Chain_Manifest_v1.0.md

# Specify blockchain and transaction ID
./tools/publish_blockchain_anchor.sh \
  --chain polygon \
  --txid 0xabc123... \
  00_MASTER_CITATION.md

# Multiple files
./tools/publish_blockchain_anchor.sh \
  spec/mirrorDNA-standard-v1.0.md \
  spec/principles.md \
  spec/compliance_levels.md
```

#### Options

```
-c, --chain <name>     Blockchain name (default: ethereum)
-o, --output <path>    Output file for anchor log
                       (default: tools/checksums/blockchain_anchors.log)
-t, --txid <hash>      Transaction hash to record
                       (optional, can add later)
-h, --help             Show help message
```

#### What It Does

1. Calculates SHA-256 for each specified file
2. Generates anchor metadata (timestamp, checksum, filename)
3. Appends to blockchain anchor log
4. Outputs human-readable entry for blockchain transaction memo

#### Output

```
⟡⟦BLOCKCHAIN ANCHOR⟧

File: spec/Reflection_Chain_Manifest_v1.0.md
Checksum: 788ccffe78de2633332c3b1629a002f283c5337d5df327ede84c6997750a143a
Timestamp: 2025-11-18T12:34:56Z
Chain: polygon
TxID: 0xabc123... (pending if not provided)

Anchor logged to: tools/checksums/blockchain_anchors.log
```

#### When to Use

- Publishing official releases (v1.0, v1.1, etc.)
- Creating immutable proof of specification version
- Establishing public audit trail
- Level 3 compliance with blockchain anchoring enhancement

#### Example Workflow

1. **Finalize release files**:
   ```bash
   ./tools/checksums/checksum_updater.sh 00_MASTER_CITATION.md
   ```

2. **Prepare blockchain anchor**:
   ```bash
   ./tools/publish_blockchain_anchor.sh 00_MASTER_CITATION.md
   ```

3. **Copy checksum to blockchain transaction memo**:
   - Use Ethereum/Polygon wallet
   - Send 0 ETH/MATIC to yourself
   - Paste checksum in transaction memo field

4. **Record transaction ID**:
   ```bash
   ./tools/publish_blockchain_anchor.sh \
     --txid 0xYourTransactionHash \
     00_MASTER_CITATION.md
   ```

5. **Commit anchor log**:
   ```bash
   git add tools/checksums/blockchain_anchors.log
   git commit -m "Blockchain anchor for v1.0.0 release"
   ```

---

## Quick Reference

### Common Workflows

#### Workflow 1: Edit and Update Spec File

```bash
# 1. Edit file
vim spec/mirrorDNA-standard-v1.0.md

# 2. Update checksum
./tools/checksums/checksum_updater.sh spec/mirrorDNA-standard-v1.0.md

# 3. Verify
./tools/checksums/checksum_verifier.sh spec/mirrorDNA-standard-v1.0.md

# 4. Commit
git add spec/mirrorDNA-standard-v1.0.md
git commit -m "Update MirrorDNA standard content"
```

#### Workflow 2: Pre-Push Verification

```bash
# Verify all checksums before pushing
./tools/checksums/verify_repo_checksums.sh

# If any failures, fix them
./tools/checksums/checksum_updater.sh <failed_file.md>

# Re-verify
./tools/checksums/verify_repo_checksums.sh

# Push
git push
```

#### Workflow 3: Prepare New Release

```bash
# 1. Update version sidecars
./tools/add_version_sidecars.sh 1.1.0

# 2. Verify all checksums
./tools/checksums/verify_repo_checksums.sh

# 3. Update any invalid checksums
./tools/checksums/checksum_updater.sh <file.md>

# 4. (Optional) Blockchain anchor
./tools/publish_blockchain_anchor.sh \
  00_MASTER_CITATION.md \
  spec/mirrorDNA-standard-v1.0.md

# 5. Tag release
git tag -a v1.1.0 -m "Release v1.1.0"
git push --tags
```

---

## Installation

### Prerequisites

**Required:**
- Bash (4.0+)
- `shasum` or `sha256sum` (usually pre-installed on Linux/macOS)

**Optional:**
- `jq` (for better JSON handling in version sidecar tool)
- Git (for version control integration)

### Setup

```bash
# 1. Clone MirrorDNA-Standard repository
git clone https://github.com/MirrorDNA-Reflection-Protocol/MirrorDNA-Standard.git
cd MirrorDNA-Standard

# 2. Make scripts executable
chmod +x tools/*.sh
chmod +x tools/checksums/*.sh

# 3. Verify installation
./tools/checksums/verify_repo_checksums.sh
```

### Platform-Specific Notes

**macOS:**
```bash
# Install coreutils if shasum not available
brew install coreutils

# Install jq for version management
brew install jq
```

**Linux (Debian/Ubuntu):**
```bash
# Usually pre-installed, but if needed:
sudo apt-get install coreutils

# Install jq
sudo apt-get install jq
```

**Windows:**
- Use **Git Bash** (comes with Git for Windows)
- Or use **WSL** (Windows Subsystem for Linux)
- PowerShell versions of these tools coming soon

---

## CI/CD Integration

### GitHub Actions Example

Add checksum verification to your CI pipeline:

```yaml
# .github/workflows/integrity-check.yml
name: MirrorDNA Integrity Check

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

jobs:
  verify-checksums:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout repository
        uses: actions/checkout@v3

      - name: Verify all checksums
        run: ./tools/checksums/verify_repo_checksums.sh

      - name: Check version sidecars
        run: |
          if [ -f tools/add_version_sidecars.sh ]; then
            ./tools/add_version_sidecars.sh 1.0.0 --dry-run
          fi
```

### Pre-Commit Hook

Automatically verify checksums before commits:

```bash
# .git/hooks/pre-commit
#!/bin/bash

echo "Running MirrorDNA checksum verification..."
./tools/checksums/verify_repo_checksums.sh

if [ $? -ne 0 ]; then
    echo ""
    echo "❌ Checksum verification failed!"
    echo "Run: ./tools/checksums/checksum_updater.sh <file.md>"
    echo "Then commit again."
    exit 1
fi

echo "✓ All checksums valid"
```

Make it executable:
```bash
chmod +x .git/hooks/pre-commit
```

### Pre-Push Hook

```bash
# .git/hooks/pre-push
#!/bin/bash

echo "Running pre-push MirrorDNA verification..."

# Verify checksums
./tools/checksums/verify_repo_checksums.sh || exit 1

# Run validator (if available)
if [ -f validators/cli.py ]; then
    python -m validators.cli --manifest mirrorDNA_manifest.yaml --policy mirrorDNA_reflection_policy.yaml || exit 1
fi

echo "✓ All pre-push checks passed"
```

---

## Troubleshooting

### Issue 1: `shasum: command not found`

**Solution:**
- **macOS**: `brew install coreutils`
- **Linux**: `sudo apt-get install coreutils`
- **Windows**: Use Git Bash or WSL

### Issue 2: Checksum fails after editing

**Cause**: File content changed but checksum not updated

**Solution**:
```bash
./tools/checksums/checksum_updater.sh <file.md>
```

### Issue 3: Script permission denied

**Cause**: Scripts not executable

**Solution**:
```bash
chmod +x tools/*.sh
chmod +x tools/checksums/*.sh
```

### Issue 4: `jq: command not found` (version sidecar tool)

**Cause**: `jq` not installed (optional dependency)

**Solution**:
- **macOS**: `brew install jq`
- **Linux**: `sudo apt-get install jq`
- **Alternative**: Script will fall back to `awk` (less reliable but functional)

### Issue 5: `.bak` files left behind

**Cause**: Checksum updater failed mid-operation

**Solution**:
```bash
# Remove backup files
rm *.bak

# Re-run updater
./tools/checksums/checksum_updater.sh <file.md>
```

---

## Best Practices

### 1. Always Update Checksums After Edits

```bash
# Bad workflow
vim spec/principles.md
git commit -am "Updated principles"  # ❌ Checksum invalid!

# Good workflow
vim spec/principles.md
./tools/checksums/checksum_updater.sh spec/principles.md
git commit -am "Updated principles"  # ✅ Checksum valid
```

### 2. Verify Before Pushing

```bash
# Always run before git push
./tools/checksums/verify_repo_checksums.sh
```

### 3. Automate with Hooks

Set up pre-commit and pre-push hooks (see [CI/CD Integration](#cicd-integration)) to catch issues early.

### 4. Use Blockchain Anchoring for Official Releases

For production releases (v1.0, v1.1, etc.), consider blockchain anchoring:

```bash
./tools/publish_blockchain_anchor.sh \
  --chain ethereum \
  00_MASTER_CITATION.md \
  spec/mirrorDNA-standard-v1.0.md
```

### 5. Keep Tools Updated

```bash
# Pull latest tools from MirrorDNA-Standard
cd MirrorDNA-Standard
git pull origin main
```

---

## Additional Resources

- **Checksum Tools Detailed Docs**: [checksums/CHECKSUM_TOOLS_README.md](checksums/CHECKSUM_TOOLS_README.md)
- **MirrorDNA Standard Spec**: [spec/mirrorDNA-standard-v1.0.md](../spec/mirrorDNA-standard-v1.0.md)
- **Validator Documentation**: [validators/README.md](../validators/README.md)
- **Integration Guide**: [docs/INTEGRATION.md](../docs/INTEGRATION.md)

---

## Tool Summary

| Tool | Purpose | When to Use |
|------|---------|-------------|
| `checksum_verifier.sh` | Verify checksums | Before commits, in CI/CD |
| `checksum_updater.sh` | Update checksums | After editing files |
| `verify_repo_checksums.sh` | Batch verify all | Before releases, pre-push |
| `add_version_sidecars.sh` | Add version metadata | New releases, standardization |
| `publish_blockchain_anchor.sh` | Blockchain timestamping | Official releases (optional) |

---

⟡⟦TOOLS⟧ · ⟡⟦INTEGRITY⟧ · ⟡⟦AUTOMATION⟧

**Document Version**: 1.0.0
**Last Updated**: 2025-11-18
**Canonical Source**: [MirrorDNA-Standard/tools/README.md](https://github.com/MirrorDNA-Reflection-Protocol/MirrorDNA-Standard/blob/main/tools/README.md)
