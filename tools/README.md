# MirrorDNA Tools & Utilities

**Purpose**: Automation scripts for repository maintenance and compliance verification.

**Status**: Production-ready utilities for v1.0.0

---

## Available Tools

### 1. Checksum Verification Tools (`checksums/`)

**Purpose**: Verify integrity of specification files and artifacts.

#### Files:
- `checksum_verifier.sh` — Verify individual file checksums
- `checksum_updater.sh` — Update checksums after approved changes
- `verify_repo_checksums.sh` — Full repository integrity check
- `CHECKSUM_TOOLS_README.md` — Detailed documentation

#### Usage:

**Verify entire repository:**
```bash
./tools/checksums/verify_repo_checksums.sh
```

**Expected output (if valid):**
```
✓ All checksums verified
✓ No tampering detected
✓ Repository integrity: PASSED
```

**Update checksums (after making changes):**
```bash
./tools/checksums/checksum_updater.sh spec/mirrorDNA-standard-v1.0.md
```

**When to use:**
- Before creating a release
- After modifying spec files
- Before submitting a pull request
- When suspicious of file tampering

---

### 2. Version Sidecar Generator (`add_version_sidecars.sh`)

**Purpose**: Auto-generate `.sidecar.json` files for versioned documents.

#### What are sidecars?

**Sidecar files** contain metadata about a document:
- Version number
- Predecessor/successor links
- Checksum
- Creation/modification dates
- Lineage information

**Example:**
```
spec/mirrorDNA-standard-v1.0.md
spec/mirrorDNA-standard-v1.0.md.sidecar.json  ← Metadata
```

#### Usage:

**Generate sidecar for single file:**
```bash
./tools/add_version_sidecars.sh spec/mirrorDNA-standard-v1.0.md
```

**Generate for all specs:**
```bash
find spec/ -name "*.md" -exec ./tools/add_version_sidecars.sh {} \;
```

**Sidecar contents example:**
```json
{
  "document": "mirrorDNA-standard-v1.0.md",
  "version": "1.0.0",
  "predecessor": null,
  "successor": null,
  "checksum": "sha256:abc123...",
  "created": "2025-01-15T00:00:00Z",
  "status": "canonical"
}
```

**When to use:**
- After creating a new spec version
- Before publishing a release
- When documenting lineage

---

### 3. Blockchain Anchor Publisher (`publish_blockchain_anchor.sh`)

**Purpose**: Optionally publish checksums to blockchain for tamper-proof timestamps.

**Status**: Experimental (optional for Level 3)

#### Usage:

```bash
./tools/publish_blockchain_anchor.sh \
  --file spec/mirrorDNA-standard-v1.0.md \
  --chain ethereum \
  --network mainnet
```

**What it does:**
1. Computes file checksum (SHA-256)
2. Creates anchor transaction
3. Publishes to blockchain
4. Returns transaction ID

**When to use:**
- Level 3 vault-backed projects
- High-trust environments
- Regulatory compliance needs
- Audit trail requirements

**Note**: Requires blockchain infrastructure (not included). See script for setup.

---

## Tool Categories

### Integrity Tools

**Purpose**: Verify file integrity and detect tampering

- `checksums/checksum_verifier.sh` — Verify checksums
- `checksums/verify_repo_checksums.sh` — Full repo check

**Use cases:**
- Pre-release verification
- Security audits
- Tamper detection

---

### Metadata Tools

**Purpose**: Generate and manage document metadata

- `add_version_sidecars.sh` — Create sidecar files

**Use cases:**
- Version tracking
- Lineage documentation
- Metadata automation

---

### Publishing Tools

**Purpose**: Publish artifacts for distribution

- `publish_blockchain_anchor.sh` — Blockchain anchoring

**Use cases:**
- Level 3 compliance
- Tamper-proof timestamps
- Regulatory compliance

---

## Automation Workflows

### Pre-Release Checklist

```bash
# 1. Verify all checksums
./tools/checksums/verify_repo_checksums.sh

# 2. Generate sidecars for new specs
./tools/add_version_sidecars.sh spec/new-spec-v1.0.md

# 3. Run validator on examples
python -m validators.cli --manifest examples/level1/project_manifest.yaml --policy examples/level1/reflection_policy.yaml

# 4. (Optional) Publish blockchain anchor
./tools/publish_blockchain_anchor.sh --file spec/mirrorDNA-standard-v1.0.md

# 5. Tag release
git tag v1.0.0
git push --tags
```

---

### Post-Edit Workflow

```bash
# 1. Update checksum
./tools/checksums/checksum_updater.sh spec/modified-file.md

# 2. Update sidecar
./tools/add_version_sidecars.sh spec/modified-file.md

# 3. Commit changes
git add spec/modified-file.md spec/modified-file.md.sidecar.json
git commit -m "Update spec: description of changes"
```

---

### CI/CD Integration

**GitHub Actions example:**

```yaml
name: Verify Integrity

on: [push, pull_request]

jobs:
  checksum-verification:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Verify checksums
        run: ./tools/checksums/verify_repo_checksums.sh
```

---

## Tool Requirements

### Checksum Tools

**Dependencies:**
- `bash` (4.0+)
- `sha256sum` (GNU coreutils)
- `find`, `grep`, `awk`

**Installation (Ubuntu/Debian):**
```bash
sudo apt-get install coreutils
```

---

### Version Sidecars

**Dependencies:**
- `bash` (4.0+)
- `jq` (JSON processor)
- `sha256sum`

**Installation:**
```bash
sudo apt-get install jq coreutils
```

---

### Blockchain Anchor

**Dependencies:**
- `node` (v14+)
- `web3.js` or `ethers.js`
- Ethereum node access (Infura, Alchemy, etc.)

**Installation:**
```bash
npm install -g web3
# Configure RPC endpoint in script
```

---

## Troubleshooting

### "Checksum verification failed"

**Cause**: File was modified after checksum was recorded.

**Fix:**
1. **If modification was intentional**: Update checksum
   ```bash
   ./tools/checksums/checksum_updater.sh file.md
   ```

2. **If modification was accidental**: Restore from git
   ```bash
   git checkout HEAD -- file.md
   ```

3. **If unsure**: Check git diff
   ```bash
   git diff file.md
   ```

---

### "Sidecar generation failed"

**Cause**: Missing `jq` or invalid JSON.

**Fix:**
```bash
# Install jq
sudo apt-get install jq

# Verify JSON syntax
jq . file.sidecar.json
```

---

### "Blockchain publish failed"

**Cause**: Network issues or insufficient funds.

**Fix:**
1. Check network connectivity
2. Verify blockchain node is accessible
3. Ensure wallet has sufficient balance
4. Check script configuration

---

## Contributing New Tools

**Want to add a tool?**

1. **Create script** in appropriate directory
   ```bash
   tools/my-tool.sh
   ```

2. **Add documentation** to this README

3. **Test thoroughly**
   ```bash
   shellcheck tools/my-tool.sh  # Lint check
   ```

4. **Submit PR** with:
   - Tool script
   - Documentation
   - Usage examples
   - Test cases

---

## Future Tools (v1.1+)

**Planned:**
- `mirrordna-release.sh` — Automated release builder
- `badge-generator.sh` — Auto-generate compliance badges
- `report-formatter.sh` — Convert validator output to markdown
- `spec-differ.sh` — Show differences between spec versions

**Want to contribute?** Open a GitHub issue or PR.

---

## Tool Standards

All tools in this directory follow these standards:

✅ **POSIX-compliant shell** (portable across systems)
✅ **Error handling** (exit codes, error messages)
✅ **Help text** (`--help` flag)
✅ **Safe defaults** (don't modify without confirmation)
✅ **Idempotent** (safe to run multiple times)

---

## Questions?

- 📋 **Spec questions**: [`../spec/README.md`](../spec/README.md)
- ❓ **FAQ**: [`../docs/FAQ.md`](../docs/FAQ.md)
- 🐛 **Tool issues**: GitHub Issues

---

⟡⟦TOOLS⟧

*These tools support Trust-by-Design™ through automated verification.*
