# Validator Tool Documentation

The MirrorDNA validator is a Python CLI tool that checks if your project is compliant with MirrorDNA standards.

---

## Overview

The validator performs:

- **Schema validation** - Checks YAML/JSON structure
- **Semantic validation** - Verifies compliance requirements
- **Level detection** - Auto-detects actual compliance level
- **Reporting** - Provides pass/fail with recommendations

!!! tip "100% Offline"
    The validator runs entirely offline. No API calls, no telemetry, no network access required.

---

## Installation

### Prerequisites

- Python 3.8+
- pip

### Install

```bash
# Clone the repository
git clone https://github.com/MirrorDNA-Reflection-Protocol/MirrorDNA-Standard.git
cd MirrorDNA-Standard

# Install dependencies
pip install -r validators/requirements.txt
```

**Dependencies:**

- `pyyaml` - YAML parsing
- `jsonschema` - JSON Schema validation
- `click` (or `argparse`) - CLI interface

---

## CLI Usage

### Basic Command

```bash
python -m validators.cli \
  --manifest mirrorDNA_manifest.yaml \
  --policy reflection_policy.yaml
```

### Level 2+ Validation

For Level 2 (Continuity Aware) or Level 3 (Vault-Backed Sovereign), add the continuity profile:

```bash
python -m validators.cli \
  --manifest mirrorDNA_manifest.yaml \
  --policy reflection_policy.yaml \
  --profile continuity_profile.yaml
```

### Help

```bash
python -m validators.cli --help
```

**Output:**

```
Usage: python -m validators.cli [OPTIONS]

  MirrorDNA Compliance Validator

Options:
  --manifest PATH   Path to project manifest (required)
  --policy PATH     Path to reflection policy (required)
  --profile PATH    Path to continuity profile (optional, for Level 2+)
  --verbose         Enable verbose output
  --json            Output results as JSON
  --help            Show this message and exit
```

---

## Configuration Files

### Required Files

#### 1. Project Manifest

**File:** `mirrorDNA_manifest.yaml`

**Purpose:** Describes your project and declares compliance level

**Schema:** `schema/project_manifest.schema.json`

**Example:**

```yaml
name: "MyProject"
version: "1.0.0"
description: "A MirrorDNA-compliant application"
mirrorDNA_compliance_level: "level_1_basic_reflection"

layers:
  mirrorDNA_protocol: true
  trustByDesign: true

reflection_policy: "reflection_policy.yaml"

maintainers:
  - name: "Developer"
    email: "dev@example.com"

repository: "https://github.com/example/project"
license: "MIT"
```

#### 2. Reflection Policy

**File:** `reflection_policy.yaml`

**Purpose:** Defines how reflection and anti-hallucination work

**Schema:** `schema/reflection_policy.schema.json`

**Example:**

```yaml
policy_version: "1.0.0"
reflection_mode: "constitutive"

uncertainty_handling:
  cite_or_silence: true
  unknown_marker: "[Unknown]"

anti_hallucination:
  source_citation: true
  grounding_required: true

trust_markers:
  - marker: "[Unknown]"
    meaning: "Information not available"
```

### Optional Files

#### 3. Continuity Profile (Level 2+)

**File:** `continuity_profile.yaml`

**Purpose:** Defines state persistence and session tracking

**Schema:** `schema/continuity_profile.schema.json`

**Example:**

```yaml
profile_version: "1.0.0"
continuity_mechanism: "local_state"

state_persistence:
  enabled: true
  storage_type: "file_system"
  storage_location: "./data/continuity"
  checksum_validation: true

session_management:
  session_tracking: true
  session_id_format: "UUID"
  session_inheritance: true

continuity_guarantees:
  lineage_tracking: true
  anti_hallucination: true
```

---

## Validation Checks

### Level 1 Checks

**File:** `validators/checks/reflection_checks.py`

#### 1. Cite-or-Silence Protocol

**Requirement:** Must implement cite-or-silence (AHP)

**Check:**

```python
def check_cite_or_silence(policy):
    if not policy.get("uncertainty_handling", {}).get("cite_or_silence"):
        return ("FAILED", "cite_or_silence must be enabled")
    return ("PASSED", "Cite-or-silence enabled")
```

**Fix:**

```yaml
uncertainty_handling:
  cite_or_silence: true  # ← Required
```

#### 2. Unknown Marker

**Requirement:** Must define a marker for unknown information

**Check:**

```python
def check_unknown_marker(policy):
    marker = policy.get("uncertainty_handling", {}).get("unknown_marker")
    if not marker:
        return ("FAILED", "unknown_marker is required")
    return ("PASSED", f"Unknown marker: {marker}")
```

**Fix:**

```yaml
uncertainty_handling:
  unknown_marker: "[Unknown]"  # ← Required
```

#### 3. Trust Markers

**Requirement:** Must define at least one trust marker

**Check:**

```python
def check_trust_markers(policy):
    markers = policy.get("trust_markers", [])
    if len(markers) == 0:
        return ("FAILED", "At least one trust marker required")
    return ("PASSED", f"{len(markers)} trust markers defined")
```

**Fix:**

```yaml
trust_markers:
  - marker: "[Unknown]"
    meaning: "Information not available"
```

#### 4. Source Citation

**Requirement:** Anti-hallucination must include source citation

**Check:**

```python
def check_source_citation(policy):
    if not policy.get("anti_hallucination", {}).get("source_citation"):
        return ("FAILED", "source_citation required for anti-hallucination")
    return ("PASSED", "Source citation enabled")
```

**Fix:**

```yaml
anti_hallucination:
  source_citation: true  # ← Required
```

### Level 2 Checks

**File:** `validators/checks/continuity_checks.py`

#### 1. State Persistence

**Requirement:** Must enable state persistence

**Check:**

```python
def check_state_persistence(profile):
    if not profile.get("state_persistence", {}).get("enabled"):
        return ("FAILED", "State persistence must be enabled for Level 2")
    return ("PASSED", "State persistence enabled")
```

**Fix:**

```yaml
state_persistence:
  enabled: true  # ← Required for Level 2
```

#### 2. Session Tracking

**Requirement:** Must track sessions explicitly

**Check:**

```python
def check_session_tracking(profile):
    if not profile.get("session_management", {}).get("session_tracking"):
        return ("FAILED", "Session tracking required for Level 2")
    return ("PASSED", "Session tracking enabled")
```

**Fix:**

```yaml
session_management:
  session_tracking: true  # ← Required for Level 2
```

#### 3. Lineage Tracking

**Requirement:** Must track session lineage

**Check:**

```python
def check_lineage_tracking(profile):
    if not profile.get("continuity_guarantees", {}).get("lineage_tracking"):
        return ("FAILED", "Lineage tracking required for Level 2")
    return ("PASSED", "Lineage tracking enabled")
```

**Fix:**

```yaml
continuity_guarantees:
  lineage_tracking: true  # ← Required for Level 2
```

#### 4. Checksum Validation

**Requirement:** Must validate checksums for integrity

**Check:**

```python
def check_checksum_validation(profile):
    if not profile.get("state_persistence", {}).get("checksum_validation"):
        return ("FAILED", "Checksum validation recommended for Level 2")
    return ("PASSED", "Checksum validation enabled")
```

**Fix:**

```yaml
state_persistence:
  checksum_validation: true  # ← Recommended
```

### Level 3 Checks

**Additional requirements beyond Level 2:**

- Vault configuration
- Sovereign identity
- Glyph signatures
- Interaction safety protocols

---

## Output Interpretation

### Success Output

```
==============================================
MirrorDNA Compliance Validator v1.0
==============================================

Project: MyProject v1.0.0
Declared Level: level_1_basic_reflection

--- Schema Validation ---
✅ PASSED: Manifest schema valid
✅ PASSED: Policy schema valid

--- Compliance Checks ---
✅ PASSED: Cite-or-silence enabled
✅ PASSED: Unknown marker defined: [Unknown]
✅ PASSED: Trust markers: 3 defined
✅ PASSED: Source citation enabled

==============================================
RESULT: ✅ PASSED
Level 1 (Basic Reflection) compliance verified
==============================================

Next steps:
1. Add badge to your README:
   ![MirrorDNA Level 1](https://raw.githubusercontent.com/.../badges/reflective_compliance_light.svg)
2. Run tests: pytest tests/ -v
3. Commit configs to version control
```

### Failure Output

```
==============================================
MirrorDNA Compliance Validator v1.0
==============================================

Project: MyProject v1.0.0
Declared Level: level_1_basic_reflection

--- Schema Validation ---
✅ PASSED: Manifest schema valid
❌ FAILED: Policy schema invalid
  Error: Missing required field 'uncertainty_handling'

--- Compliance Checks ---
❌ FAILED: Cite-or-silence not enabled
  Recommendation: Add 'cite_or_silence: true' to uncertainty_handling section
✅ PASSED: Unknown marker defined: [Unknown]
❌ FAILED: No trust markers defined
  Recommendation: Add at least one trust marker to policy

==============================================
RESULT: ❌ FAILED
3 checks failed
==============================================

Fix these issues and run the validator again.
```

### JSON Output

Use `--json` flag for machine-readable output:

```bash
python -m validators.cli \
  --manifest manifest.yaml \
  --policy policy.yaml \
  --json
```

**Output:**

```json
{
  "project": "MyProject",
  "version": "1.0.0",
  "declared_level": "level_1_basic_reflection",
  "detected_level": "level_1_basic_reflection",
  "result": "PASSED",
  "checks": [
    {
      "name": "cite_or_silence",
      "status": "PASSED",
      "message": "Cite-or-silence enabled"
    },
    {
      "name": "unknown_marker",
      "status": "PASSED",
      "message": "Unknown marker defined: [Unknown]"
    }
  ],
  "schema_validation": {
    "manifest": "PASSED",
    "policy": "PASSED"
  }
}
```

---

## CI/CD Integration

!!! info "Coming in v1.1"
    Structured exit codes and GitHub Action are planned for v1.1.

### GitHub Actions (Manual)

```yaml
# .github/workflows/mirrordna-validation.yml
name: MirrorDNA Validation

on: [push, pull_request]

jobs:
  validate:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v3

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.10'

      - name: Install dependencies
        run: |
          git clone https://github.com/MirrorDNA-Reflection-Protocol/MirrorDNA-Standard.git
          cd MirrorDNA-Standard
          pip install -r validators/requirements.txt

      - name: Run MirrorDNA validator
        run: |
          cd MirrorDNA-Standard
          python -m validators.cli \
            --manifest ../mirrorDNA_manifest.yaml \
            --policy ../reflection_policy.yaml
```

### Exit Codes (Current)

- `0` - Validation passed
- `1` - Validation failed

### Exit Codes (Planned for v1.1)

- `0` - Validation passed
- `1` - Schema validation failed
- `2` - Compliance checks failed
- `3` - File not found
- `4` - Invalid arguments

---

## Troubleshooting

### Common Errors

#### Error: "Schema validation failed"

**Cause:** YAML/JSON structure doesn't match schema

**Solution:**

1. Check YAML syntax: `yamllint manifest.yaml`
2. Compare to examples: `diff manifest.yaml examples/minimal_project_manifest.yaml`
3. Check field names for typos

#### Error: "Cite-or-silence check failed"

**Cause:** `cite_or_silence` not enabled in policy

**Solution:**

```yaml
uncertainty_handling:
  cite_or_silence: true  # ← Add this
```

#### Error: "Level mismatch detected"

**Cause:** Declared level doesn't match actual implementation

**Example:**

```
Declared: level_2_continuity_aware
Detected: level_1_basic_reflection (missing continuity profile)
```

**Solution:**

Add the missing `continuity_profile.yaml`:

```bash
cp examples/example_continuity_profile.yaml ./continuity_profile.yaml
```

Then update manifest:

```yaml
continuity_profile: "continuity_profile.yaml"
```

#### Error: "File not found"

**Cause:** Referenced file doesn't exist

**Solution:**

Check paths in manifest:

```yaml
reflection_policy: "reflection_policy.yaml"  # ← File must exist
```

---

## Advanced Usage

### Custom Validators

You can extend the validator with custom checks:

```python
# my_custom_checks.py
def check_my_feature(manifest, policy):
    """Custom compliance check"""
    if "my_feature" not in manifest:
        return ("FAILED", "my_feature is required")
    return ("PASSED", "my_feature detected")

# Register the check
from validators.validator import register_check
register_check("my_feature", check_my_feature, level=1)
```

### Programmatic Usage

```python
from validators.loader import load_and_validate
from validators.validator import run_validation

# Load configs
manifest = load_and_validate("manifest.yaml", "manifest")
policy = load_and_validate("policy.yaml", "policy")

# Run validation
results = run_validation(manifest, policy)

# Check results
if results["result"] == "PASSED":
    print("✅ Validation passed!")
else:
    print("❌ Validation failed:")
    for check in results["checks"]:
        if check["status"] == "FAILED":
            print(f"  - {check['name']}: {check['message']}")
```

---

## Validator Architecture

### Data Flow

```
User runs CLI
  ↓
cli.py parses arguments
  ↓
loader.py loads YAML/JSON files
  ↓
loader.py validates against JSON schemas
  ↓
validator.py runs compliance checks
  ↓
checks/*.py execute specific validations
  ↓
report.py aggregates results
  ↓
CLI outputs PASS/FAIL + recommendations
```

### File Structure

```
validators/
├── cli.py                 # Entry point (argparse CLI)
├── loader.py              # Load YAML/JSON + schema validation
├── validator.py           # Main orchestrator
├── report.py              # Generate human-readable reports
└── checks/                # Compliance check modules
    ├── reflection_checks.py       (Level 1+ checks)
    ├── continuity_checks.py       (Level 2+ checks)
    └── trustbydesign_checks.py    (Trust markers)
```

---

## Resources

- [Examples](examples.md) - Working configurations to validate
- [Integration Guide](integration.md) - How to implement compliance
- [Compliance Levels](compliance-levels.md) - Requirements for each level
- [FAQ](faq.md) - Common questions

---

## Future Enhancements (v1.1+)

- [ ] JSON/YAML output formats
- [ ] Structured exit codes
- [ ] GitHub Action
- [ ] Web-based validator
- [ ] Auto-fix suggestions
- [ ] Badge verification service
