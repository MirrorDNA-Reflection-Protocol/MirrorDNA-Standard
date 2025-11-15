# MirrorDNA-Standard Architecture

**Purpose**: This document explains how the MirrorDNA-Standard repository is organized and how its components work together.

**Audience**: Developers contributing to this repo or building tools on top of it.

---

## Repository Role

**MirrorDNA-Standard is the PROTOCOL LAYER.**

```
┌──────────────────────────────────────────────────┐
│  ECOSYSTEM LAYERS                                 │
├──────────────────────────────────────────────────┤
│  Products (ActiveMirrorOS, third-party apps)     │ ← Implements the standard
├──────────────────────────────────────────────────┤
│  THIS REPO: MirrorDNA-Standard                   │ ← Defines the standard
│  - Specification documents                       │
│  - Validation toolchain                          │
│  - Reference implementation                      │
├──────────────────────────────────────────────────┤
│  Foundation (Obsidian, Git, llama.cpp, etc.)     │ ← Infrastructure
└──────────────────────────────────────────────────┘
```

**What this means:**
- This repo does NOT build products (use ActiveMirrorOS for that)
- This repo defines RULES that products must follow
- This repo provides TOOLS to check if products follow the rules

---

## Directory Structure

### 📋 `/spec` — Canonical Specifications

**Purpose**: The single source of truth for what MirrorDNA means.

**Key files:**
- `mirrorDNA-standard-v1.0.md` — The core standard (10KB, comprehensive)
- `principles.md` — Five immutable principles
- `compliance_levels.md` — L1, L2, L3 requirements (detailed)
- `glossary.md` — Canonical definitions (resolves ambiguity)

**Governance:**
- All specs are versioned (v1.0, v1.1, etc.)
- Each spec includes lineage tracking (predecessor/successor)
- Breaking changes require major version bump
- Principles are IMMUTABLE for v1.x

**Why separate files?**
- Modularity: Import only what you need
- Lineage: Track evolution of each component
- Clarity: Each file has a single responsibility

---

### 🔧 `/validators` — Python Validation Package

**Purpose**: Machine-checkable compliance verification.

**Architecture:**

```
validators/
├── cli.py                 ← Entry point (argparse CLI)
├── loader.py              ← Load YAML/JSON + schema validation
├── validator.py           ← Main orchestrator
├── report.py              ← Generate human-readable reports
└── checks/                ← Compliance check modules
    ├── reflection_checks.py       (Level 1+ checks)
    ├── continuity_checks.py       (Level 2+ checks)
    └── trustbydesign_checks.py    (Trust markers)
```

**Data flow:**

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
CLI outputs PASS/FAIL + suggested improvements
```

**Design decisions:**
- **Modular checks**: Each check is independent (easy to add new ones)
- **Schema-first**: Validate structure before semantics
- **Auto-detection**: Validator detects actual compliance level vs declared
- **Graceful degradation**: Partial failures still produce useful reports

---

### 📐 `/schema` — JSON Schemas

**Purpose**: Structural validation for config files.

**Files:**
- `project_manifest.schema.json` — Defines valid project metadata
- `continuity_profile.schema.json` — Defines persistence configuration
- `reflection_policy.schema.json` — Defines reflection protocols

**Why JSON Schema?**
- Industry standard (ajv, jsonschema)
- Language-agnostic (works in Python, JavaScript, etc.)
- Auto-generates documentation
- Supports complex validation rules

**Usage:**
```python
from validators.loader import load_and_validate

# Automatically validates against appropriate schema
manifest = load_and_validate("mirrorDNA_manifest.yaml", "manifest")
```

---

### 🎯 `/examples` — Working Configurations

**Purpose**: Copy-paste ready configs for all compliance levels.

**Structure:**
```
examples/
├── README.md               ← Quick start guide
├── level1/                 ← Basic Reflection
│   ├── project_manifest.yaml
│   └── reflection_policy.yaml
├── level2/                 ← Continuity Aware
│   ├── project_manifest.yaml
│   ├── reflection_policy.yaml
│   └── continuity_profile.yaml
└── level3/                 ← Vault-Backed Sovereign
    ├── project_manifest.yaml
    ├── reflection_policy.yaml
    └── continuity_profile.yaml
```

**Design principle**: WORKING examples only. Each config must pass validation.

---

### 🏅 `/badges` — Compliance Badges

**Purpose**: Visual markers of compliance for project READMEs.

**Files:**
- `verified-reflective.svg` — Primary badge (Level 2+)
- `reflective_compliance_light.svg` — Light theme variant
- `reflective_compliance_dark.svg` — Dark theme variant
- `mirrorDNA_compatible.svg` — Compatibility badge

**Usage:**
```markdown
![MirrorDNA Level 1](https://raw.githubusercontent.com/.../badges/reflective_compliance_light.svg)
```

**Badge criteria:**
- L1: Basic badge
- L2/L3: "Verified Reflective" badge
- Must pass validation to use badge

---

### ✅ `/tests` — Pytest Suite

**Purpose**: Ensure validators work correctly.

**Coverage:**
- Schema validation (malformed YAML/JSON)
- Compliance checks (L1, L2, L3 requirements)
- CLI interface (argument parsing, output format)
- Edge cases (missing files, invalid configs)

**Run tests:**
```bash
pytest tests/ -v
```

---

### 🛠️ `/tools` — Utility Scripts

**Purpose**: Automation for repo maintenance.

**Key tools:**
- `checksums/` — Verify integrity of specs and artifacts
- `add_version_sidecars.sh` — Auto-generate version metadata
- `publish_blockchain_anchor.sh` — Optional blockchain anchoring

**Why checksums?**
- Trust-by-Design™: Verify file integrity
- Detect tampering or corruption
- Enable artifact lineage tracking

---

### 💼 `/portable` — Reference Implementation

**Purpose**: Show how Level 3 compliance works in practice.

**Status**: Experimental / reference architecture.

**Components:**
- `launcher/` — Electron desktop app (cross-platform)
- `vault-template/` — Pre-configured Obsidian vault
- `glyphs/` — Visual identity system (SVG files)

**Why include this?**
- Demonstrates feasibility of vault-backed sovereignty
- Provides starting point for product implementations
- Tests the specification in practice

**Note**: This is NOT a production product. Use ActiveMirrorOS for that.

---

## Component Interaction Diagram

```
┌─────────────────────────┐
│  User / Developer       │
└──────────┬──────────────┘
           │
           │ (1) Reads
           ▼
┌─────────────────────────┐
│  /spec (Specifications) │
└──────────┬──────────────┘
           │
           │ (2) Creates configs based on spec
           ▼
┌─────────────────────────┐
│  Project Config Files   │
│  - manifest.yaml        │
│  - policy.yaml          │
│  - profile.yaml         │
└──────────┬──────────────┘
           │
           │ (3) Validates
           ▼
┌─────────────────────────┐
│  /validators (CLI)      │
│  Uses /schema           │
└──────────┬──────────────┘
           │
           │ (4) Returns
           ▼
┌─────────────────────────┐
│  PASS / FAIL Report     │
│  + Suggested Improvements│
└──────────┬──────────────┘
           │
           │ (5) If PASS
           ▼
┌─────────────────────────┐
│  Add /badges to README  │
└─────────────────────────┘
```

---

## Design Principles

### 1. **Separation of Concerns**
- **Spec**: What compliance means (immutable)
- **Validator**: How to check compliance (upgradeable)
- **Examples**: How to implement (copy-paste ready)

### 2. **Open & Vendor-Neutral**
- Anyone can implement the spec
- No proprietary dependencies
- MIT licensed

### 3. **Machine-Checkable**
- JSON schemas for structure
- Python checks for semantics
- Exit codes for CI/CD

### 4. **Backward Compatible**
- v1.x will never break v1.0 compliance
- Additive changes only (new optional fields)
- Major version for breaking changes

### 5. **Trust-by-Design™**
- Checksums for all specs
- Lineage tracking for evolution
- Glyph signatures for semantic marking

---

## Extension Points

### Adding a New Compliance Check

1. Create `validators/checks/my_check.py`
2. Implement check function:
   ```python
   def check_my_feature(config):
       """Check if feature X is implemented."""
       if not config.get("feature_x"):
           return ("FAILED", "Feature X is required")
       return ("PASSED", "Feature X detected")
   ```
3. Register in `validators/validator.py`
4. Add test in `tests/test_checks.py`
5. Update spec if needed

### Adding a New Schema

1. Create `schema/my_config.schema.json`
2. Define JSON Schema structure
3. Update `validators/loader.py` to handle new schema
4. Add example in `examples/`
5. Document in spec

### Adding a New Compliance Level

1. Update `spec/compliance_levels.md`
2. Add checks in `validators/checks/`
3. Update schemas if needed
4. Create example configs
5. Update badges
6. Bump minor version (v1.1.0)

---

## Versioning Strategy

**Semantic Versioning** (major.minor.patch):

- **Major (2.0.0)**: Breaking changes (e.g., new principles, removed levels)
- **Minor (1.1.0)**: New features (e.g., Level 4, new checks)
- **Patch (1.0.1)**: Bug fixes (e.g., validator errors, schema typos)

**v1.x Commitment**: Principles are immutable. Existing levels won't change requirements.

---

## Testing Strategy

### Unit Tests (`tests/test_checks.py`)
- Test individual compliance checks
- Mock config files
- Cover edge cases

### Integration Tests (`tests/test_cli.py`)
- Test full CLI workflow
- Use example configs
- Verify output format

### Regression Tests
- Run validators on example configs
- Ensure all examples pass
- Detect spec drift

---

## Security Considerations

### Supply Chain
- Pin dependencies in `requirements.txt`
- Checksum verification for downloaded files
- No external API calls (offline-first)

### Trust Anchors
- Glyph signatures (`⟡⟦VERIFIED⟧`)
- SHA-256 checksums for specs
- Git commit signatures (optional)

### Interaction Safety
- Validator never modifies user files
- Read-only operations only
- No network access required

---

## Future Architecture

### v1.1: Enhanced Tooling
- JSON/YAML output formats
- Web-based validator
- GitHub Action

### v2.0: Network Protocols
- Agent-to-agent communication
- Distributed vault sync
- Multi-agent compliance

### v3.0: Standards Body
- W3C-style governance
- Conformance testing program
- Certified implementations registry

---

⟡⟦ARCHITECTURE⟧

*This architecture is designed for clarity, extensibility, and trust.*
