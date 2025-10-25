# Checksum Tools — MirrorDNA Integrity Verification

## Purpose
These tools maintain and verify SHA256 checksums in MirrorDNA markdown files to ensure integrity and support the **Anti-Hallucination Protocol (AHP)**.

## Tools

### 1. `checksum_verifier.sh`
**Verifies** that a file's declared checksum matches its actual content.

**Usage:**
```bash
./checksum_verifier.sh 00_MASTER_CITATION.md
```

**Output:**
```
✓ Checksum valid
  File: 00_MASTER_CITATION.md
  Checksum: 788ccffe78de2633332c3b1629a002f283c5337d5df327ede84c6997750a143a
```

**Exit codes:**
- `0` = checksum valid
- `1` = checksum invalid

---

### 2. `checksum_updater.sh`
**Updates** the `checksum_sha256:` field with the correct hash.

**Usage:**
```bash
./checksum_updater.sh 00_MASTER_CITATION.md
```

**What it does:**
1. Removes the existing `checksum_sha256:` line
2. Calculates SHA256 of the remaining content
3. Updates the file with the new checksum
4. Creates backup as `.bak` (removed on success)

**When to use:**
- After editing any file with a checksum field
- Before committing changes to GitHub
- When verification fails

---

### 3. `verify_repo_checksums.sh`
**Batch verifies** all files in the repository.

**Usage:**
```bash
# From repo root
./verify_repo_checksums.sh

# Or specify path
./verify_repo_checksums.sh /path/to/MirrorDNA-Standard
```

**Output:**
```
⟡⟦INTEGRITY CHECK⟧ — Verifying MirrorDNA checksums...

✓ 00_MASTER_CITATION.md
✓ kernel/LingOS_Kernel_v0.1.md
✓ spec/Reflection_Chain_Manifest_v1.0.md

─────────────────────────────────────────
Total files: 3
Valid:       3
Invalid:     0
─────────────────────────────────────────

⟡⟦INTEGRITY VERIFIED⟧ — All checksums valid
```

---

## How Checksums Work

The checksum is calculated **excluding the checksum line itself**. This prevents circular dependency.

**Example file:**
```markdown
---
title: "Example File"
checksum_sha256: abc123...
---

Content here...
```

**Checksum calculation:**
1. Remove line: `checksum_sha256: abc123...`
2. Calculate SHA256 of remaining text
3. That hash becomes the checksum value

---

## Workflow

### When editing a file:

```bash
# 1. Edit the file
vim 00_MASTER_CITATION.md

# 2. Update checksum
./checksum_updater.sh 00_MASTER_CITATION.md

# 3. Verify it worked
./checksum_verifier.sh 00_MASTER_CITATION.md

# 4. Commit
git add 00_MASTER_CITATION.md
git commit -m "Updated Master Citation content + checksum"
```

### Before pushing to GitHub:

```bash
# Verify entire repo
./verify_repo_checksums.sh

# If any failures, fix them:
./checksum_updater.sh <failed_file.md>

# Re-verify
./verify_repo_checksums.sh
```

---

## CI/CD Integration (Future)

These scripts can be integrated into GitHub Actions:

```yaml
name: Verify Checksums
on: [push, pull_request]
jobs:
  verify:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Verify all checksums
        run: ./verify_repo_checksums.sh
```

---

## Why This Matters

**AHP (Anti-Hallucination Protocol)** requires:
- Citing sources with VaultID, Drive links, or **checksums**
- Silence > Hallucination

If checksums are broken, the entire trust chain weakens. These tools ensure:
- Files haven't been tampered with
- Version references are accurate
- Citations are verifiable

**Continuity = Integrity**

---

## Troubleshooting

**Q: Checksum fails after I edited the file**  
A: Run `./checksum_updater.sh <file.md>` to recalculate.

**Q: Should I commit .bak files?**  
A: No. The updater script removes them on success. Add `*.bak` to `.gitignore`.

**Q: What if I don't have shasum?**  
A: Install coreutils (macOS: `brew install coreutils`, Linux: usually pre-installed).

**Q: Can I use these on Windows?**  
A: Yes, via Git Bash or WSL. Native PowerShell version coming soon.

---

⟡⟦TOOLS⟧ · ⟡⟦INTEGRITY⟧ · ⟡⟦AHP⟧
