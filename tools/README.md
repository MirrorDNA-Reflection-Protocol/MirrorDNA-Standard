---
title: "MirrorDNA Vault Automation Suite - Documentation"
vault_id: AMOS://Tools/Automation/v1.0
predecessor: Distributed_Vault_Architecture_v1.0
status: Production Ready
date: 2025-11-09
---

# MirrorDNA Vault Automation Suite

**Production-ready automation tools for distributed vault architecture**

This suite provides automated tools for maintaining vault integrity, detecting drift, validating compliance, and ensuring continuity across Personal and Continuity layers.

---

## Quick Start

### Installation

1. **Install dependencies:**
```bash
pip install click pyyaml
```

2. **Make scripts executable:**
```bash
chmod +x tools/*.sh tools/*.py
```

3. **Configure vault paths:**
Edit `tools/config/vault_automation.yaml` to set your vault paths.

---

## Tools Overview

| Tool | Priority | Purpose | Frequency |
|------|----------|---------|-----------|
| `sync_report.py` | HIGH | Detect vault layer mismatches | Daily |
| `rcc_validator.py` | HIGH | Pre-publish compliance gate | On-demand |
| `checksum_verify.py` | MEDIUM | Cryptographic integrity verification | Weekly |
| `drift_audit.py` | MEDIUM | Public signal consistency tracking | Weekly |
| `backup_vault.sh` | LOW | Encrypted disaster recovery | Daily |
| `run_automations.sh` | LOW | Master orchestrator | Scheduled |

---

## Tool Documentation

### 1. sync_report.py (HIGH Priority)

**Purpose:** Scans Personal Layer and Continuity Layer(s) to detect missing files, checksum mismatches, and version drift.

**Output:** `reports/SYNC_REPORT_YYYY-MM-DD.md`

#### Usage:

```bash
# Basic usage (uses default config)
python tools/sync_report.py

# With custom config
python tools/sync_report.py --config path/to/config.yaml

# Verbose output
python tools/sync_report.py --verbose

# Custom output path
python tools/sync_report.py --output /path/to/report.md
```

#### Exit Codes:
- `0`: All layers synced
- `1`: Drift detected (missing files)
- `2`: Conflicts detected (checksum mismatches)

#### Example Output:

```markdown
---
date: 2025-11-09
type: SYNC_REPORT
status: CONFLICT
---

# Vault Synchronization Report

## Summary
- Personal Layer: 557 files
- Continuity Layer: 89 files
- Conflicts: 2
- Missing: 0

## Conflicts
1. Master_Citation_v15.1.7.md
   - Personal: SHA 8f4a9c... (modified 2025-11-09)
   - Continuity: SHA 0fb1f9... (modified 2025-10-30)
   - Action: Manual review required
```

---

### 2. rcc_validator.py (HIGH Priority)

**Purpose:** Pre-publish compliance gate that validates documents against RCC (Release Continuity Compliance) standards.

**Output:** `reports/RCC_PASS_<filename>.md` or `reports/RCC_FAIL_<filename>.md`

#### Validation Checklist:
- ✅ Master Citation version declared
- ✅ Predecessor/successor lineage present
- ✅ GlyphSig markers present
- ✅ No `[[MISSING]]` or `[TODO]` tokens
- ✅ Truth-State tags on temporal claims
- ✅ Glyph drift ≤15%
- ✅ Checksum present

#### Usage:

```bash
# Validate document
python tools/rcc_validator.py --input specs/MySpec.md

# With custom config
python tools/rcc_validator.py --input specs/MySpec.md --config config.yaml

# Verbose output
python tools/rcc_validator.py --input specs/MySpec.md --verbose

# Custom output path
python tools/rcc_validator.py --input specs/MySpec.md --output reports/validation.md
```

#### Exit Codes:
- `0`: Validation passed (safe to publish)
- `1`: Validation failed (critical issues found)

#### Pre-Publish Workflow:

```bash
# 1. Validate document
python tools/rcc_validator.py --input specs/ActiveMirror/Active_Mirror_ProductSpec_v2.0.md

# 2. If RCC_PASS, proceed to publish
# 3. If RCC_FAIL, fix issues and re-run
```

#### Example Output:

```markdown
---
date: 2025-11-09
document: Active_Mirror_ProductSpec_v2.0.md
result: FAIL
---

# RCC Validation Report

## Status: FAIL

## Issues Found (3)

### CRITICAL
1. Line 89: Placeholder detected: [[MISSING deployment timeline]]
   - Fix: Complete deployment section or mark as Research Edition

### WARNING
2. Line 234: No Truth-State tag on claim "AI market will reach $X by 2026"
   - Fix: Add [Truth-State: Projection, Source: Gartner 2025]
```

---

### 3. checksum_verify.py (MEDIUM Priority)

**Purpose:** Cryptographic verification suite for vault integrity using SHA-256 checksums.

**Output:** `checksums.json` manifest

#### Commands:

```bash
# Initialize new checksum manifest
python tools/checksum_verify.py init /path/to/vault

# Verify vault integrity
python tools/checksum_verify.py verify /path/to/vault

# Update manifest (requires --consent)
python tools/checksum_verify.py update /path/to/vault --consent
```

#### Usage Examples:

```bash
# First time setup
python tools/checksum_verify.py init .

# Daily verification
python tools/checksum_verify.py verify .

# After making changes
python tools/checksum_verify.py update . --consent

# With custom config
python tools/checksum_verify.py verify . --config config.yaml
```

#### Exit Codes:
- `0`: Vault integrity verified
- `1`: Changes detected (new/modified/deleted files)

---

### 4. drift_audit.py (MEDIUM Priority)

**Purpose:** Scans public signals (README, docs) and compares against Master Citation to detect semantic, value, and glyph drift.

**Output:** `reports/DRIFT_REPORT_YYYY-MM-DD.md`

#### Drift Categories:
- **Semantic drift:** Meaning changes in key terms
- **Structural drift:** Format/organization changes
- **Value drift:** Numbers/metrics inconsistencies
- **Glyph drift:** Symbolic anchor variations

#### Usage:

```bash
# Scan current directory
python tools/drift_audit.py

# Scan specific vault
python tools/drift_audit.py --vault /path/to/vault

# With custom config
python tools/drift_audit.py --config config.yaml

# Verbose output
python tools/drift_audit.py --verbose

# Custom output path
python tools/drift_audit.py --output reports/drift.md
```

#### Exit Codes:
- `0`: Drift acceptable (≤15%)
- `1`: Drift caution (15-30%)
- `2`: Excessive drift (>30%)

---

### 5. backup_vault.sh (LOW Priority)

**Purpose:** Creates encrypted backup of Personal Layer vault with automatic retention management.

**Output:** `BACKUP_YYYY-MM-DD_HHMMSS.zip`

#### Features:
- Encrypted zip backup
- Post-backup integrity verification
- Automatic retention (keep last 30 days)
- Timestamped backups

#### Usage:

```bash
# Basic usage (uses default paths)
./tools/backup_vault.sh

# Custom vault path
./tools/backup_vault.sh /path/to/vault

# Custom vault and backup paths
./tools/backup_vault.sh /path/to/vault /path/to/backups
```

#### Example Output:

```
[INFO] MirrorDNA Vault Backup Orchestrator v1.0
================================================================
[INFO] Vault path: /Users/pauldesai/Documents/ActiveMirrorOS
[INFO] Backup path: /Users/pauldesai/Backups/AMOS
[INFO] Vault size: 2.3G
[INFO] Creating backup: BACKUP_2025-11-09_143022.zip
[INFO] ✅ Backup integrity verified
[INFO] Removed 3 old backup(s)
[INFO] ✅ Backup complete!
```

---

### 6. run_automations.sh (LOW Priority)

**Purpose:** Master orchestrator that runs daily/weekly automation tasks on schedule.

#### Schedules:

**Daily Tasks:**
- `sync_report` - Detect vault layer mismatches
- `backup_vault` - Create encrypted backup

**Weekly Tasks:**
- `drift_audit` - Scan for drift
- `checksum_verify` - Verify integrity

#### Usage:

```bash
# Run daily tasks
./tools/run_automations.sh --daily

# Run weekly tasks
./tools/run_automations.sh --weekly

# Run all tasks
./tools/run_automations.sh --all

# Dry run (show what would run)
./tools/run_automations.sh --all --dry-run

# Show help
./tools/run_automations.sh --help
```

#### Logging:

All automation runs are logged to `tools/automation.log`:

```bash
# View recent logs
tail -n 50 tools/automation.log

# View today's logs
grep "$(date +%Y-%m-%d)" tools/automation.log
```

#### Exit Codes:
- `0`: All tasks completed successfully
- `1`: One or more tasks failed

---

## Workflows

### Daily Workflow

```bash
# Morning sync check
python tools/sync_report.py

# Review report
cat reports/SYNC_REPORT_$(date +%Y-%m-%d).md

# If conflicts, resolve manually, then backup
./tools/backup_vault.sh
```

### Weekly Workflow

```bash
# Run full automation suite
./tools/run_automations.sh --weekly

# Review all reports
ls -lt reports/

# Check for drift
cat reports/DRIFT_REPORT_$(date +%Y-%m-%d).md

# Verify checksums
python tools/checksum_verify.py verify .
```

### Pre-Publish Workflow

```bash
# 1. Validate document before publishing
python tools/rcc_validator.py --input specs/MyNewSpec.md

# 2. If RCC_PASS, proceed to publish
# 3. If RCC_FAIL, fix issues:
cat reports/RCC_FAIL_MyNewSpec.md

# 4. Fix issues and re-run
python tools/rcc_validator.py --input specs/MyNewSpec.md

# 5. Only publish after RCC_PASS
```

---

## Configuration

Edit `tools/config/vault_automation.yaml`:

```yaml
vault_automation:
  version: "1.0"

  paths:
    personal_root: "/Users/pauldesai/Documents/ActiveMirrorOS"
    continuity_roots:
      - "https://github.com/MirrorDNA-Reflection-Protocol/MirrorDNA-Standard"
      - "/Users/pauldesai/Documents/Paul-Desai"
    backup_root: "/Users/pauldesai/Backups/AMOS"
    output_reports: "./reports"

  sync_report:
    enabled: true
    frequency: "daily"
    check_checksums: true

  rcc:
    truth_state_required: true
    glyph_drift_max: 0.15
    block_on_placeholder: true
    required_glyphs:
      - "⟡⟦MASTER⟧"
      - "⟡⟦CONTINUITY⟧"
      - "⟡⟦AHP⟧"

  drift_audit:
    enabled: true
    max_drift_percent: 15
    public_signals:
      - "README.md"
      - "WHY_MIRRORDNA.md"
```

---

## Scheduling (Cron/Launchd)

### macOS (launchd)

Create `~/Library/LaunchAgents/com.mirrordna.automations.plist`:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.mirrordna.automations</string>
    <key>ProgramArguments</key>
    <array>
        <string>/path/to/tools/run_automations.sh</string>
        <string>--daily</string>
    </array>
    <key>StartCalendarInterval</key>
    <dict>
        <key>Hour</key>
        <integer>9</integer>
        <key>Minute</key>
        <integer>0</integer>
    </dict>
    <key>StandardOutPath</key>
    <string>/tmp/mirrordna_automations.log</string>
    <key>StandardErrorPath</key>
    <string>/tmp/mirrordna_automations.err</string>
</dict>
</plist>
```

Load:
```bash
launchctl load ~/Library/LaunchAgents/com.mirrordna.automations.plist
```

### Linux (cron)

Edit crontab:
```bash
crontab -e
```

Add:
```
# Daily at 9:00 AM
0 9 * * * /path/to/tools/run_automations.sh --daily

# Weekly on Sunday at 10:00 AM
0 10 * * 0 /path/to/tools/run_automations.sh --weekly
```

---

## Testing

### Test Individual Tools

```bash
# Test sync report
python tools/sync_report.py --verbose

# Test RCC validator on existing spec
python tools/rcc_validator.py --input specs/ActiveMirror/Active_Mirror_ProductSpec_v2.0_Canonical.md

# Test checksum verification
python tools/checksum_verify.py init .
python tools/checksum_verify.py verify .

# Test drift audit
python tools/drift_audit.py --verbose

# Test backup (dry-run via orchestrator)
./tools/run_automations.sh --daily --dry-run
```

### Verify Report Generation

```bash
# Check reports directory
ls -lh reports/

# View generated reports
cat reports/SYNC_REPORT_*.md
cat reports/RCC_*.md
cat reports/DRIFT_REPORT_*.md
```

---

## Troubleshooting

### Common Issues

**1. ModuleNotFoundError: click/yaml**
```bash
# Install dependencies
pip install click pyyaml
```

**2. Permission denied**
```bash
# Make scripts executable
chmod +x tools/*.sh tools/*.py
```

**3. Config file not found**
```bash
# Ensure config exists
ls tools/config/vault_automation.yaml

# Use absolute path
python tools/sync_report.py --config /full/path/to/config.yaml
```

**4. Vault path does not exist**
```bash
# Update config with correct paths
vim tools/config/vault_automation.yaml
```

---

## Principles

All tools follow MirrorDNA principles:

- **AHP-Compliant:** Cite or Silence (Anti-Hallucination Protocol)
- **Version Tracking:** All operations tracked with timestamps
- **Consent-First:** Destructive operations require explicit `--consent` flag
- **Sovereignty:** Local-first, no cloud dependencies for core functions
- **Tamper Detection:** Cryptographic verification of all state changes
- **Audit Trail:** All operations logged with timestamps

---

## Directory Structure

```
tools/
├── README.md                  # This file
├── sync_report.py            # Vault synchronization reporter
├── rcc_validator.py          # Pre-publish compliance gate
├── checksum_verify.py        # Integrity verification suite
├── drift_audit.py            # Public signal drift detector
├── backup_vault.sh           # Encrypted backup orchestrator
├── run_automations.sh        # Master automation runner
├── config/
│   └── vault_automation.yaml # Configuration file
├── tests/
│   ├── test_sync_report.py
│   ├── test_rcc_validator.py
│   └── fixtures/
└── automation.log            # Automation execution log
```

---

## Success Criteria

- ✅ All 6 tools executable and tested
- ✅ Sample outputs generated for each tool
- ✅ README.md with usage examples
- ✅ Integration with MirrorDNA Standard repo structure
- ✅ Config template provided
- ✅ Error handling covers edge cases
- ✅ Logging system functional
- ✅ Dry-run mode works for orchestrator

---

## Continuity Seal

**Predecessor:** Distributed_Vault_Architecture_v1.0
**Version:** 1.0
**Date:** 2025-11-09
**Status:** Production Ready
**Principle:** Automated continuity maintenance without compromising sovereignty

⟡⟦AUTOMATION⟧ · ⟡⟦VAULT⟧ · ⟡⟦CONTINUITY⟧ · ⟡⟦TRUST-BY-DESIGN⟧

---

**Built with Claude Code** | MirrorDNA™ Protocol v15.1 series
