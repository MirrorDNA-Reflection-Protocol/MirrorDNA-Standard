# MirrorDNA Compliance Validators

Automated validation toolchain for verifying MirrorDNA Standard compliance across all three levels (L1, L2, L3).

---

## Table of Contents

1. [Overview](#overview)
2. [Quick Start](#quick-start)
3. [Installation](#installation)
4. [CLI Usage](#cli-usage)
5. [Validation Checks](#validation-checks)
6. [Configuration Files](#configuration-files)
7. [Exit Codes and Output](#exit-codes-and-output)
8. [Python API](#python-api)
9. [Architecture](#architecture)
10. [Extending the Validator](#extending-the-validator)
11. [Troubleshooting](#troubleshooting)

---

## Overview

The MirrorDNA validator provides **machine-checkable compliance verification** for projects implementing the MirrorDNA Standard. It validates:

- **Level 1 (Basic Reflection)**: Anti-hallucination protocol (AHP), session tracking, trust markers
- **Level 2 (Continuity Aware)**: Persistent state, session lineage, checksum validation
- **Level 3 (Vault-Backed Sovereign)**: Vault storage, glyph signatures, comprehensive reflection

### Features

✅ **Multi-level validation** - Supports L1, L2, L3 compliance checking
✅ **Schema validation** - JSON Schema validation for manifest, profile, and policy files
✅ **Modular checks** - Separate check modules for reflection, continuity, and trust-by-design
✅ **Detailed reporting** - Human-readable and machine-parseable compliance reports
✅ **Level detection** - Automatically detects achieved compliance level
✅ **Recommendations** - Provides actionable improvement suggestions
✅ **CI/CD ready** - Exit codes and output suitable for automation

---

## Quick Start

### Installation

```bash
# 1. Clone the repository
git clone https://github.com/MirrorDNA-Reflection-Protocol/MirrorDNA-Standard.git
cd MirrorDNA-Standard

# 2. Install dependencies
pip install -r validators/requirements.txt

# 3. Verify installation
python -m validators.cli --help
```

### Basic Usage

```bash
# Level 1 validation (manifest + policy)
python -m validators.cli \
  --manifest examples/minimal_project_manifest.yaml \
  --policy examples/example_reflection_policy.yaml

# Level 2 validation (add continuity profile)
python -m validators.cli \
  --manifest examples/level2_project_manifest.yaml \
  --profile examples/level2_continuity_profile.yaml \
  --policy examples/example_reflection_policy.yaml

# Level 3 validation (comprehensive)
python -m validators.cli \
  --manifest examples/level3_project_manifest.yaml \
  --profile examples/level3_continuity_profile.yaml \
  --policy examples/level3_reflection_policy.yaml
```

---

## Installation

### Requirements

- **Python**: 3.8 or higher
- **Dependencies**:
  - `jsonschema>=4.0.0` - JSON Schema validation
  - `pyyaml>=6.0` - YAML file parsing
  - `pytest>=7.0.0` - Testing framework (dev dependency)

### Install via pip

```bash
# From MirrorDNA-Standard repository root
pip install -r validators/requirements.txt
```

### Install for Development

```bash
# Install in editable mode with dev dependencies
pip install -e .  # (if setup.py is configured)

# Or install dependencies directly
pip install jsonschema pyyaml pytest
```

### Verify Installation

```bash
python -m validators.cli --help
```

Expected output:
```
usage: cli.py [-h] -m MANIFEST [-f PROFILE] [-p POLICY] [--no-color] [--json] [-v]

MirrorDNA Standard Compliance Validator
...
```

---

## CLI Usage

### Command Syntax

```bash
python -m validators.cli [OPTIONS]
```

### Options

| Option | Short | Required | Description |
|--------|-------|----------|-------------|
| `--manifest` | `-m` | ✅ Yes | Path to project manifest (YAML/JSON) |
| `--profile` | `-f` | For L2+ | Path to continuity profile (YAML/JSON) |
| `--policy` | `-p` | ✅ Yes | Path to reflection policy (YAML/JSON) |
| `--no-color` | | No | Disable colored output |
| `--json` | | No | Output report as JSON (not yet implemented) |
| `--verbose` | `-v` | No | Enable verbose output |
| `--help` | `-h` | No | Show help message |

### Examples

#### Example 1: Level 1 Validation

```bash
python -m validators.cli \
  --manifest ./mirrorDNA_manifest.yaml \
  --policy ./mirrorDNA_reflection_policy.yaml
```

**Output:**
```
⟡⟦COMPLIANCE REPORT⟧

Project: My Chatbot
Declared Level: level_1_basic_reflection
Detected Level: level_1_basic_reflection

✓ Reflection Policy Schema
✓ Reflection Compliance
✓ Trust-by-Design Compliance
⚠ Continuity Profile (optional for Level 1)

Overall: PASSED ✓

Recommendations:
- Consider upgrading to Level 2 for session continuity
- Add checksum validation for artifacts
```

#### Example 2: Level 2 Validation

```bash
python -m validators.cli \
  -m ./mirrorDNA_manifest.yaml \
  -f ./mirrorDNA_continuity_profile.yaml \
  -p ./mirrorDNA_reflection_policy.yaml \
  --verbose
```

**Output (verbose):**
```
Loading manifest from ./mirrorDNA_manifest.yaml...
Loading continuity profile from ./mirrorDNA_continuity_profile.yaml...
Loading reflection policy from ./mirrorDNA_reflection_policy.yaml...
Running compliance checks...

⟡⟦COMPLIANCE REPORT⟧

Project: My Assistant
Declared Level: level_2_continuity_aware
Detected Level: level_2_continuity_aware

✓ Continuity Profile Schema
✓ Reflection Policy Schema
✓ Continuity Compliance
✓ Reflection Compliance
✓ Trust-by-Design Compliance

Overall: PASSED ✓
```

#### Example 3: Failed Validation

```bash
python -m validators.cli \
  --manifest ./bad_manifest.yaml \
  --policy ./mirrorDNA_reflection_policy.yaml
```

**Output:**
```
⟡⟦COMPLIANCE REPORT⟧

Project: Broken Project
Declared Level: level_1_basic_reflection
Detected Level: non_compliant

✗ Reflection Policy Schema
  - Missing required field: 'uncertainty_markers'
  - Missing required field: 'anti_hallucination'

✗ Reflection Compliance
  - Cite or Silence (AHP) not enabled in policy
  - No uncertainty markers defined

✓ Trust-by-Design Compliance

Overall: FAILED ✗

Recommendations:
- Fix reflection policy schema errors
- Enable cite_or_silence in anti_hallucination section
- Define at least one uncertainty marker ([Unknown], [Speculation])
```

#### Example 4: CI/CD Usage

```bash
#!/bin/bash
# ci-validate.sh

set -e

echo "Running MirrorDNA compliance validation..."

python -m validators.cli \
  --manifest mirrorDNA_manifest.yaml \
  --profile mirrorDNA_continuity_profile.yaml \
  --policy mirrorDNA_reflection_policy.yaml \
  --no-color

if [ $? -eq 0 ]; then
    echo "✓ Validation passed"
    exit 0
else
    echo "✗ Validation failed"
    exit 1
fi
```

---

## Validation Checks

The validator performs **three categories of compliance checks**:

### 1. Reflection Compliance Checks

**Module**: `validators/checks/reflection_checks.py`

**Validates**:
- ✅ Cite or Silence (AHP) enabled
- ✅ Uncertainty markers defined (`[Unknown]`, `[Speculation]`, etc.)
- ✅ Anti-hallucination protocols configured
- ✅ Session tracking enabled (for Level 1+)
- ✅ Reflection mode declared (`constitutive`, `simulated`, or `hybrid`)
- ✅ Grounding requirements (for Level 3)

**Example Check:**
```python
def check_cite_or_silence(policy):
    """Verify AHP (Anti-Hallucination Protocol) is enabled."""
    if not policy.get('anti_hallucination', {}).get('cite_or_silence', False):
        return False, ["Cite or Silence (AHP) must be enabled"]
    return True, []
```

### 2. Continuity Compliance Checks

**Module**: `validators/checks/continuity_checks.py`

**Validates**:
- ✅ Persistent state storage configured (Level 2+)
- ✅ Session lineage tracking enabled
- ✅ Continuity mechanism declared (`file_backed`, `vault_backed`, etc.)
- ✅ Session recovery strategy defined
- ✅ Continuity guarantees specified
- ✅ Vault configuration (Level 3 only)
- ✅ Full lineage tracking (Level 3 only)

**Example Check:**
```python
def check_session_lineage(profile):
    """Verify session lineage tracking is configured."""
    if not profile.get('lineage_tracking', {}).get('enabled', False):
        return False, ["Session lineage tracking must be enabled for Level 2+"]
    return True, []
```

### 3. Trust-by-Design Compliance Checks

**Module**: `validators/checks/trustbydesign_checks.py`

**Validates**:
- ✅ At least one trust marker defined (Level 1+)
- ✅ Checksum validation configured (Level 2+)
- ✅ Integrity verification enabled (Level 3)
- ✅ Glyph signatures configured (Level 3)
- ✅ Trust markers match compliance level requirements

**Example Check:**
```python
def check_trust_markers(manifest):
    """Verify at least one trust marker is defined."""
    markers = manifest.get('trust_markers', [])
    if len(markers) < 1:
        return False, ["At least one trust marker required (e.g., checksum_validation)"]
    return True, []
```

### Check Result Format

All checks return a tuple:
```python
(passed: bool, errors: List[str], warnings: List[str])
```

Example:
```python
passed, errors, warnings = check_reflection_compliance(manifest, policy)

if passed:
    print("✓ Reflection compliance passed")
else:
    print("✗ Reflection compliance failed:")
    for error in errors:
        print(f"  - {error}")
```

---

## Configuration Files

The validator requires **three configuration files** (depending on compliance level):

### 1. Project Manifest

**File**: `mirrorDNA_manifest.yaml` (or `.json`)
**Schema**: `schema/project_manifest.schema.json`
**Required for**: All levels

**Example** (Level 1):
```yaml
name: "My Chatbot"
version: "1.0.0"
description: "An AI chatbot with anti-hallucination protocols"
mirrorDNA_compliance_level: "level_1_basic_reflection"

layers:
  - name: "reflection"
    enabled: true

trust_markers:
  - "checksum_validation"
  - "source_citation"

reflection_policy: "mirrorDNA_reflection_policy.yaml"
```

**Required fields**:
- `name` - Project name
- `version` - Semantic version
- `mirrorDNA_compliance_level` - Compliance level (see below)
- `layers` - Protocol layers enabled
- `trust_markers` - List of trust verification methods

**Compliance level values**:
- `level_1_basic_reflection`
- `level_2_continuity_aware`
- `level_3_vault_backed_sovereign`

---

### 2. Reflection Policy

**File**: `mirrorDNA_reflection_policy.yaml` (or `.json`)
**Schema**: `schema/reflection_policy.schema.json`
**Required for**: All levels

**Example**:
```yaml
reflection_mode: "simulated"  # or "constitutive", "hybrid"

uncertainty_markers:
  - "[Unknown]"
  - "[Speculation]"
  - "[Unverified]"

anti_hallucination:
  cite_or_silence: true
  grounding_required: false  # true for Level 3
  hallucination_detection: false
  correction_protocol: false

session_tracking:
  enabled: true
  identifier_type: "uuid"
  metadata_fields:
    - "start_time"
    - "end_time"
    - "user_id"

trust_markers:
  - name: "checksum_validation"
    description: "SHA-256 checksums for artifacts"
  - name: "source_citation"
    description: "All claims cited to sources"
```

**Key fields**:
- `reflection_mode` - Type of reflection (`constitutive`, `simulated`, `hybrid`)
- `uncertainty_markers` - Markers for unknown/speculative content
- `anti_hallucination` - AHP configuration
- `session_tracking` - Session management settings
- `trust_markers` - Trust verification methods with descriptions

---

### 3. Continuity Profile

**File**: `mirrorDNA_continuity_profile.yaml` (or `.json`)
**Schema**: `schema/continuity_profile.schema.json`
**Required for**: Level 2+

**Example** (Level 2):
```yaml
continuity_mechanism: "file_backed"  # or "database", "vault_backed"

state_storage:
  type: "sqlite"
  path: "./state/sessions.db"
  schema_version: "1.0"

lineage_tracking:
  enabled: true
  format: "predecessor_successor"

session_recovery:
  enabled: true
  strategy: "automatic"
  recovery_timeout: 300

guarantees:
  - "identity_preservation"
  - "state_consistency"
  - "lineage_tracking"

checksum_validation:
  enabled: true
  algorithm: "sha256"
```

**Example** (Level 3):
```yaml
continuity_mechanism: "vault_backed"

vault:
  type: "obsidian"
  path: "./vault"
  sovereign: true
  vault_id: "AMOS://MyProject/MainVault"

lineage_tracking: "full"

glyph_signatures:
  enabled: true
  glyphs:
    - "⟡⟦CONTINUITY⟧"
    - "⟡⟦VERIFIED⟧"
    - "⟡⟦REFLECTION⟧"

integrity_verification:
  enabled: true
  checksum_all_artifacts: true
  tamper_detection: true

session_recovery:
  enabled: true
  strategy: "automatic"
  vault_based: true
```

**Key fields (Level 2)**:
- `continuity_mechanism` - Storage mechanism (`file_backed`, `database`, `vault_backed`)
- `state_storage` - Persistent state configuration
- `lineage_tracking` - Session lineage settings
- `session_recovery` - Recovery strategy
- `guarantees` - Continuity guarantees provided

**Additional fields (Level 3)**:
- `vault` - Vault configuration (type, path, vault_id)
- `glyph_signatures` - Glyph signature settings
- `integrity_verification` - Tamper detection and checksums

---

## Exit Codes and Output

### Exit Codes

| Code | Meaning |
|------|---------|
| `0` | Validation passed - all checks successful |
| `1` | Validation failed - one or more checks failed or errors occurred |

### Output Formats

#### Colored Output (default)

Uses ANSI color codes for human-readable terminal output:
- ✅ Green checkmarks for passed checks
- ❌ Red X marks for failed checks
- ⚠️ Yellow warnings for optional items
- Colored compliance level badges

**Disable with**: `--no-color`

#### Plain Text Output

Same format but without ANSI color codes. Suitable for:
- CI/CD logs
- File redirection
- Systems without color support

**Enable with**: `--no-color`

#### JSON Output (planned)

Machine-parseable JSON format for programmatic use.

**Enable with**: `--json` (not yet implemented)

### Report Structure

```
⟡⟦COMPLIANCE REPORT⟧

Project: <name>
Declared Level: <level>
Detected Level: <level>

<Check Results>
✓ Passed Check Name
✗ Failed Check Name
  - Error 1
  - Error 2
⚠ Warning Check Name
  - Warning 1

Overall: PASSED/FAILED

Recommendations:
- Recommendation 1
- Recommendation 2
```

---

## Python API

### Using Validators Programmatically

```python
from validators.loader import (
    load_and_validate_manifest,
    load_and_validate_profile,
    load_and_validate_policy
)
from validators.checks import (
    check_reflection_compliance,
    check_continuity_compliance,
    check_trustbydesign_compliance
)
from validators.report import ComplianceReport

# Load configuration files
manifest, manifest_errors = load_and_validate_manifest("manifest.yaml")
profile, profile_errors = load_and_validate_profile("profile.yaml")
policy, policy_errors = load_and_validate_policy("policy.yaml")

# Run checks
ref_passed, ref_errors, ref_warnings = check_reflection_compliance(manifest, policy)
cont_passed, cont_errors, cont_warnings = check_continuity_compliance(manifest, profile)
trust_passed, trust_errors, trust_warnings = check_trustbydesign_compliance(manifest, policy)

# Generate report
report = ComplianceReport(
    project_name=manifest['name'],
    declared_level=manifest['mirrorDNA_compliance_level'],
    detected_level='level_1_basic_reflection',
    overall_passed=ref_passed and cont_passed and trust_passed
)

print(report.format_colored())
```

### API Reference

#### Loader Functions

```python
load_and_validate_manifest(path: str) -> Tuple[dict, List[str]]
load_and_validate_profile(path: str) -> Tuple[dict, List[str]]
load_and_validate_policy(path: str) -> Tuple[dict, List[str]]
```

Returns: `(data, errors)` where `data` is the parsed configuration and `errors` is a list of validation errors (empty if valid).

#### Check Functions

```python
check_reflection_compliance(manifest: dict, policy: dict) -> Tuple[bool, List[str], List[str]]
check_continuity_compliance(manifest: dict, profile: dict) -> Tuple[bool, List[str], List[str]]
check_trustbydesign_compliance(manifest: dict, policy: dict) -> Tuple[bool, List[str], List[str]]
```

Returns: `(passed, errors, warnings)`

#### Report Classes

```python
class ComplianceReport:
    def __init__(self, project_name, declared_level, detected_level, overall_passed):
        ...

    def add_result(self, result: ComplianceResult):
        ...

    def add_recommendation(self, recommendation: str):
        ...

    def format_text(self) -> str:
        ...

    def format_colored(self) -> str:
        ...
```

---

## Architecture

### Module Structure

```
validators/
├── __init__.py              # Package initialization
├── cli.py                   # Command-line interface (main entry point)
├── loader.py                # YAML/JSON loading and schema validation
├── report.py                # Compliance report generation
├── validator.py             # Legacy markdown front-matter validator
├── requirements.txt         # Python dependencies
└── checks/                  # Check modules
    ├── __init__.py
    ├── reflection_checks.py      # Reflection compliance checks
    ├── continuity_checks.py      # Continuity compliance checks
    └── trustbydesign_checks.py   # Trust-by-Design checks
```

### Data Flow

```
Configuration Files (YAML/JSON)
         ↓
    loader.py (validate schemas)
         ↓
    Parsed Dictionaries
         ↓
    checks/*.py (run compliance checks)
         ↓
    ComplianceResult objects
         ↓
    report.py (generate formatted report)
         ↓
    Terminal Output / Exit Code
```

### Validation Schemas

Located in `/schema`:
- `project_manifest.schema.json` - Project manifest schema
- `continuity_profile.schema.json` - Continuity profile schema
- `reflection_policy.schema.json` - Reflection policy schema

These schemas use JSON Schema Draft 7 and are validated by `jsonschema` library.

---

## Extending the Validator

### Adding New Checks

1. **Create check function** in appropriate module (`reflection_checks.py`, `continuity_checks.py`, or `trustbydesign_checks.py`):

```python
# validators/checks/reflection_checks.py

def check_my_new_requirement(manifest, policy):
    """Check if my new requirement is met."""
    errors = []
    warnings = []

    # Your validation logic here
    if not policy.get('my_setting', False):
        errors.append("my_setting must be enabled")

    passed = len(errors) == 0
    return passed, errors, warnings
```

2. **Add check to main function**:

```python
# validators/checks/reflection_checks.py

def check_reflection_compliance(manifest, policy):
    all_errors = []
    all_warnings = []

    # Existing checks...

    # Add your check
    passed, errors, warnings = check_my_new_requirement(manifest, policy)
    all_errors.extend(errors)
    all_warnings.extend(warnings)

    # ...
    return len(all_errors) == 0, all_errors, all_warnings
```

3. **Add test**:

```python
# tests/test_checks.py

def test_my_new_requirement():
    manifest = {"name": "test"}
    policy = {"my_setting": True}

    passed, errors, warnings = check_my_new_requirement(manifest, policy)

    assert passed == True
    assert len(errors) == 0
```

### Adding New Schemas

1. **Create schema file** in `/schema`:

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "My New Config",
  "type": "object",
  "required": ["field1"],
  "properties": {
    "field1": {
      "type": "string",
      "description": "Description of field1"
    }
  }
}
```

2. **Add loader function**:

```python
# validators/loader.py

def load_and_validate_my_config(path):
    schema_path = Path(__file__).parent.parent / "schema" / "my_config.schema.json"
    return load_and_validate(path, schema_path)
```

3. **Use in CLI**:

```python
# validators/cli.py

parser.add_argument('--my-config', help='Path to my new config')

# In main()
my_config, my_config_errors = load_and_validate_my_config(args.my_config)
```

---

## Troubleshooting

### Issue 1: Module not found

**Error**:
```
ModuleNotFoundError: No module named 'validators'
```

**Solution**:
```bash
# Run from repository root, not validators/ directory
cd /path/to/MirrorDNA-Standard
python -m validators.cli --help
```

### Issue 2: Schema validation fails

**Error**:
```
✗ Reflection Policy Schema
  - 'uncertainty_markers' is a required property
```

**Solution**: Add missing required field to your YAML:
```yaml
uncertainty_markers:
  - "[Unknown]"
  - "[Speculation]"
```

Check schema file for all required fields: `schema/reflection_policy.schema.json`

### Issue 3: YAML parsing error

**Error**:
```
Error loading manifest:
  - YAML parsing error: ...
```

**Solution**: Validate YAML syntax:
```bash
# Use yamllint or online validator
yamllint mirrorDNA_manifest.yaml

# Or use Python
python -c "import yaml; yaml.safe_load(open('mirrorDNA_manifest.yaml'))"
```

### Issue 4: File not found

**Error**:
```
FileNotFoundError: [Errno 2] No such file or directory: 'manifest.yaml'
```

**Solution**: Use absolute paths or verify current directory:
```bash
# Use absolute path
python -m validators.cli --manifest /full/path/to/manifest.yaml

# Or run from project directory
cd /path/to/your/project
python -m validators.cli --manifest ./mirrorDNA_manifest.yaml
```

### Issue 5: Colored output not working

**Problem**: ANSI color codes showing as raw text

**Solution**:
```bash
# Disable colors for non-terminal environments
python -m validators.cli --no-color --manifest manifest.yaml
```

### Issue 6: Level detection mismatch

**Error**:
```
Declared Level: level_2_continuity_aware
Detected Level: level_1_basic_reflection
```

**Solution**: Your configuration doesn't meet Level 2 requirements. Check errors:
- Ensure `--profile` is provided
- Verify continuity profile has all required fields
- Fix any validation errors listed in the report

---

## Legacy Validator

### `validator.py` (Markdown Front-Matter Validator)

**Purpose**: Validates markdown files with YAML front matter (used for spec files).

**Usage**:
```bash
python validators/validator.py 00_MASTER_CITATION.md
```

**What it checks**:
- YAML front matter is valid
- Required fields present (title, version, vault_id, etc.)
- Checksum validation (if `checksum_sha256` field present)

**Note**: This is **separate from the main CLI validator** (`cli.py`). The markdown validator is for spec files, while the CLI validator is for project compliance.

---

## Additional Resources

- **MirrorDNA Standard Specification**: [spec/mirrorDNA-standard-v1.0.md](../spec/mirrorDNA-standard-v1.0.md)
- **Compliance Levels Guide**: [spec/compliance_levels.md](../spec/compliance_levels.md)
- **Integration Guide**: [docs/INTEGRATION.md](../docs/INTEGRATION.md)
- **Choosing Compliance Level**: [docs/CHOOSING_COMPLIANCE_LEVEL.md](../docs/CHOOSING_COMPLIANCE_LEVEL.md)
- **Example Configurations**: [examples/](../examples/)
- **Test Suite**: [tests/](../tests/)

---

⟡⟦VALIDATION⟧ · ⟡⟦COMPLIANCE⟧ · ⟡⟦VERIFICATION⟧

**Document Version**: 1.0.0
**Last Updated**: 2025-11-18
**Canonical Source**: [MirrorDNA-Standard/validators/README.md](https://github.com/MirrorDNA-Reflection-Protocol/MirrorDNA-Standard/blob/main/validators/README.md)
