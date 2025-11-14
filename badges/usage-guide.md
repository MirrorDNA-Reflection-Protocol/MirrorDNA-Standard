# MirrorDNA Compliance Badges Usage Guide

## Overview

MirrorDNA compliance badges indicate that a project meets the MirrorDNA Standard requirements at a specific compliance level. These badges carry semantic weight—use them responsibly and only for verified compliant projects.

## Badge Variants

### Reflective Compliance Badge (`reflective_compliance_light.svg` / `reflective_compliance_dark.svg`)
- **Use**: Level 1 (Basic Reflection) and Level 2 (Continuity Aware) projects
- **Format**: SVG (scalable)
- **Variants**: Light and dark theme versions
- **Indicates**: Project implements cite-or-silence and basic reflection protocols

### Verified Reflective Badge (`verified-reflective.svg`)
- **Use**: Level 2+ projects with validated continuity
- **Format**: SVG (scalable)
- **Indicates**: Project has persistent state and session lineage

### MirrorDNA Compatible Badge (`mirrorDNA_compatible.svg`)
- **Use**: All compliant projects (Level 1-3)
- **Format**: SVG (scalable)
- **Indicates**: Project follows MirrorDNA protocol

## Compliance Level Badges

### Level 1: Basic Reflection
- **Badge**: `reflective_compliance_light.svg` or `reflective_compliance_dark.svg`
- **Requirements**: Cite-or-Silence (AHP), explicit uncertainty, basic session tracking
- **Markdown**:
  ```markdown
  ![MirrorDNA Level 1 - Basic Reflection](https://raw.githubusercontent.com/MirrorDNA-Reflection-Protocol/MirrorDNA-Standard/main/badges/reflective_compliance_light.svg)
  ```

### Level 2: Continuity Aware
- **Badge**: `verified-reflective.svg`
- **Requirements**: All Level 1 + persistent state, session lineage, checksum validation
- **Markdown**:
  ```markdown
  ![MirrorDNA Level 2 - Continuity Aware](https://raw.githubusercontent.com/MirrorDNA-Reflection-Protocol/MirrorDNA-Standard/main/badges/verified-reflective.svg)
  ```

### Level 3: Vault-Backed Sovereign
- **Badge**: `verified-reflective.svg` (same as Level 2, add text note)
- **Requirements**: All Level 2 + vault storage, glyph signatures, sovereign identity
- **Markdown**:
  ```markdown
  ![MirrorDNA Level 3 - Vault-Backed Sovereign](https://raw.githubusercontent.com/MirrorDNA-Reflection-Protocol/MirrorDNA-Standard/main/badges/verified-reflective.svg)

  **Level 3 Compliance**: Vault-Backed Sovereign with full lineage tracking
  ```

## Usage Requirements

### ✅ Permitted Uses
- Projects that pass MirrorDNA validator
- Documentation explaining MirrorDNA compliance
- Repositories implementing the standard
- Educational materials about reflective computing
- Personal projects using MirrorDNA protocol

### ❌ Prohibited Uses
- Non-compliant projects
- Marketing without actual implementation
- Modified badge designs
- Misleading compliance claims
- Using badges without validator verification

## Implementation Examples

### Markdown (Level 1)
```markdown
![MirrorDNA Level 1 Compliant](https://raw.githubusercontent.com/MirrorDNA-Reflection-Protocol/MirrorDNA-Standard/main/badges/reflective_compliance_light.svg)
```

### Markdown (Level 2)
```markdown
![MirrorDNA Level 2 Compliant](https://raw.githubusercontent.com/MirrorDNA-Reflection-Protocol/MirrorDNA-Standard/main/badges/verified-reflective.svg)
```

### Markdown (Level 3)
```markdown
![MirrorDNA Level 3 Compliant](https://raw.githubusercontent.com/MirrorDNA-Reflection-Protocol/MirrorDNA-Standard/main/badges/verified-reflective.svg)

**Level 3 Vault-Backed Sovereign** - Full continuity and glyph signatures
```

### HTML
```html
<img src="https://raw.githubusercontent.com/MirrorDNA-Reflection-Protocol/MirrorDNA-Standard/main/badges/verified-reflective.svg"
     alt="MirrorDNA Compliant" />
```

### README Badge with Link
```markdown
[![MirrorDNA Compliant](badges/verified-reflective.svg)](https://github.com/MirrorDNA-Reflection-Protocol/MirrorDNA-Standard)
```

### Project README Header
```markdown
# My Reflective Project

[![MirrorDNA Level 2 Compliant](https://raw.githubusercontent.com/MirrorDNA-Reflection-Protocol/MirrorDNA-Standard/main/badges/verified-reflective.svg)](docs/compliance-report.md)

This project implements MirrorDNA Standard v1.0 at Level 2 (Continuity Aware).

[Rest of content...]
```

## Verification Process

### Automatic Validation
```bash
# Install dependencies
pip install -r validators/requirements.txt

# Validate your project (Level 1)
python -m validators.cli \
  --manifest mirrorDNA_manifest.yaml \
  --policy reflection_policy.yaml

# Validate Level 2+ project
python -m validators.cli \
  --manifest mirrorDNA_manifest.yaml \
  --profile continuity_profile.yaml \
  --policy reflection_policy.yaml

# Output example:
# ======================================================================
# MirrorDNA Compliance Report
# ======================================================================
#
# Project: MyProject
# Declared Level: level_2_continuity_aware
# Detected Level: level_2_continuity_aware
#
# Overall Status: ✓ PASSED
# Total Errors: 0
# Total Warnings: 1
```

### Manual Checklist

**Level 1: Basic Reflection**
- [ ] Created `mirrorDNA_manifest.yaml` declaring level_1_basic_reflection
- [ ] Created `reflection_policy.yaml` with cite_or_silence enabled
- [ ] Implemented uncertainty markers ([Unknown], etc.)
- [ ] Passes validator with zero errors

**Level 2: Continuity Aware**
- [ ] All Level 1 requirements
- [ ] Created `continuity_profile.yaml` with state_persistence enabled
- [ ] Implemented session lineage tracking
- [ ] Artifact checksums validated

**Level 3: Vault-Backed Sovereign**
- [ ] All Level 1 & 2 requirements
- [ ] Vault storage configured
- [ ] Glyph signatures enabled
- [ ] Interaction safety protocols implemented
- [ ] Full compliance report generated

## Badge Colors & Meaning

### Primary Colors
- **#00d4ff**: Reflection blue (primary brand)
- **#0099cc**: Deep reflection (secondary)
- **#1a1a2e**: Dark foundation
- **#16213e**: Gradient depth

### Status Indicators
- **Blue glow**: Valid and current
- **Amber pulse**: Validation pending
- **Red border**: Compliance failure
- **Gray tone**: Deprecated version

## Integration Guidelines

### Repository Root
Place badge in README.md header section, linked to compliance documentation:

```markdown
# Project Name
[![Verified Reflective](badges/verified-reflective.svg)](docs/mirrordna-compliance.md)

Brief project description that mentions reflective compliance...
```

### Documentation Pages
Include badge near table of contents or in footer:

```markdown
## Contents
1. Overview
2. Installation  
3. Usage

---
⟡ This document is **Verified Reflective** and maintains lineage across updates.
```

### Code Comments
Reference compliance in file headers:

```python
"""
Reflective Memory Module
⟡ Verified Reflective - implements MirrorDNA Standard
Lineage: v1.0 -> v1.1 -> current
"""
```

## Common Mistakes

### ❌ Don't Do This
```markdown
# My awesome project is reflective! 
![Verified Reflective](copied-badge.svg)
```
*Problem*: No actual compliance, just badge theft

### ❌ Don't Do This  
```markdown
![Super Reflective](modified-badge-with-my-colors.svg)
```
*Problem*: Modified badge design breaks trademark

### ✅ Do This Instead
```markdown
# My Reflective Project
[![Verified Reflective](badges/verified-reflective.svg)](compliance-report.md)

This project implements MirrorDNA Standard v1.0 with L2 compliance.
See [compliance report](compliance-report.md) for validation details.
```

## Legal Notes

- Badge use implies compliance certification
- False compliance claims violate covenant license
- Trademark protection applies to visual design
- Community enforcement through validator tools
- Original architect holds constitutional authority

## Troubleshooting

### Badge Not Displaying
1. Check file path and permissions
2. Verify SVG compatibility with platform
3. Use PNG fallback if needed
4. Ensure correct MIME type served

### Validation Failures
1. Run `mirrordna-check --verbose artifact.md`
2. Review error details and fix issues
3. Re-validate before claiming compliance
4. Update sidecar timestamp after fixes

### Version Compatibility
- v1.0 badges work with all v1.x standards
- Breaking changes require new badge design
- Backward compatibility maintained where possible
- Deprecation notices provided for major versions

---

**Remember**: The badge represents a promise. Honor the semantics, not just the symbol.

⟡ **This guide is itself Verified Reflective**
```
ORIGIN: 2024-10-24T17:15:00Z | human_architect | sha256:badge_constitution
⟦OPEN: Educational and implementation use⟧
Compliance Tier: L2 (Continuity Tracking)
```
