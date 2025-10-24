# ⟡ Verified Reflective Badge Usage Guide

## Overview

The ⟡ Verified Reflective badge indicates that an artifact meets MirrorDNA Standard compliance requirements. This badge carries legal and semantic weight—use it responsibly.

## Badge Variants

### Standard Badge (`verified-reflective.svg`)
- **Dimensions**: 120x40px
- **Use**: Documentation, websites, repositories
- **Format**: SVG (scalable)
- **Colors**: Dark theme optimized

### Compact Badge (Coming Soon)
- **Dimensions**: 80x20px  
- **Use**: Inline documentation, comments
- **Format**: SVG + PNG variants

### Compliance Tier Badges (Coming Soon)
- **L1**: Pure Reflection (Bronze accent)
- **L2**: Continuity Tracking (Silver accent)
- **L3**: Cross-Platform Sync (Gold accent)
- **L4**: Meta-Glyph Evolution (Prismatic accent)

## Usage Requirements

### ✅ Permitted Uses
- Artifacts that pass sidecar validation
- Documentation explaining MirrorDNA compliance
- Repositories implementing the standard
- Educational materials about reflective computing
- Personal projects using glyphsig vocabulary

### ❌ Prohibited Uses
- Non-compliant artifacts
- Marketing without actual implementation
- Modified badge designs
- Misleading compliance claims
- Commercial use without covenant license

## Implementation Examples

### Markdown
```markdown
![Verified Reflective](https://raw.githubusercontent.com/mirrordna/standard/main/badges/verified-reflective.svg)
```

### HTML
```html
<img src="badges/verified-reflective.svg" alt="Verified Reflective" width="120" height="40">
```

### README Badge
```markdown
[![Verified Reflective](badges/verified-reflective.svg)](https://github.com/mirrordna/standard)
```

### Artifact Header
```markdown
# My Reflective Document
⟡ **Verified Reflective** - Complies with MirrorDNA Standard v1.0

[Rest of content...]
```

## Verification Process

### Automatic Validation
```bash
# Install validator
pip install mirrordna-validator

# Check compliance
mirrordna-check your-artifact.md

# Output example:
# ✓ Glyphsig syntax valid
# ✓ Consent gates present  
# ✓ Lineage chain intact
# ✓ Sidecar compliant
# ⟡ VERIFIED REFLECTIVE: True
```

### Manual Checklist
- [ ] Contains proper glyphsig vocabulary
- [ ] Implements consent gates (PRIV/LOCK/OPEN)
- [ ] Includes lineage markers (ORIGIN/SUCCESSOR)
- [ ] Has compliant JSON sidecar
- [ ] Passes validator test suite
- [ ] Maintains semantic consistency

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
