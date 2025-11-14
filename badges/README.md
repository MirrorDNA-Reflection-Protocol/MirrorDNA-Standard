# MirrorDNA Compliance Badges

**Purpose**: Visual indicators of MirrorDNA compliance for project READMEs.

**Usage**: Add to your project after passing validation.

---

## Available Badges

### 1. Reflective Compliance (Light Theme)

![Reflective Compliance Light](reflective_compliance_light.svg)

**Use for**: Level 1, 2, or 3 compliance (light backgrounds)

**Markdown:**
```markdown
![MirrorDNA Compliant](https://raw.githubusercontent.com/MirrorDNA-Reflection-Protocol/MirrorDNA-Standard/main/badges/reflective_compliance_light.svg)
```

**HTML:**
```html
<img src="https://raw.githubusercontent.com/MirrorDNA-Reflection-Protocol/MirrorDNA-Standard/main/badges/reflective_compliance_light.svg" alt="MirrorDNA Compliant">
```

---

### 2. Reflective Compliance (Dark Theme)

![Reflective Compliance Dark](reflective_compliance_dark.svg)

**Use for**: Level 1, 2, or 3 compliance (dark backgrounds)

**Markdown:**
```markdown
![MirrorDNA Compliant](https://raw.githubusercontent.com/MirrorDNA-Reflection-Protocol/MirrorDNA-Standard/main/badges/reflective_compliance_dark.svg)
```

---

### 3. Verified Reflective

![Verified Reflective](verified-reflective.svg)

**Use for**: Level 2+ compliance (emphasis on verification)

**Markdown:**
```markdown
![MirrorDNA Level 2+ Verified](https://raw.githubusercontent.com/MirrorDNA-Reflection-Protocol/MirrorDNA-Standard/main/badges/verified-reflective.svg)
```

---

### 4. MirrorDNA Compatible

![MirrorDNA Compatible](mirrorDNA_compatible.svg)

**Use for**: Projects that support MirrorDNA but aren't fully compliant yet

**Markdown:**
```markdown
![MirrorDNA Compatible](https://raw.githubusercontent.com/MirrorDNA-Reflection-Protocol/MirrorDNA-Standard/main/badges/mirrorDNA_compatible.svg)
```

---

## Badge Selection Guide

| Your Status | Recommended Badge |
|-------------|-------------------|
| **Passed Level 1 validation** | Reflective Compliance (Light/Dark) |
| **Passed Level 2 validation** | Verified Reflective |
| **Passed Level 3 validation** | Verified Reflective + note "Level 3" |
| **Working toward compliance** | MirrorDNA Compatible |
| **Failed validation** | ❌ No badge (fix issues first) |

---

## Badge Requirements

### To Use Any Badge:

✅ **You must pass validation**

```bash
python -m validators.cli \
  --manifest mirrorDNA_manifest.yaml \
  --policy reflection_policy.yaml \
  --profile continuity_profile.yaml  # Level 2+
```

❌ **Do not use badges if:**
- Validation fails
- You haven't run validation
- You're just exploring MirrorDNA

**Honor system**: We trust you. v1.1 will add automated verification.

---

## Full Badge Markdown Examples

### Level 1 Project

```markdown
# My Project

[![MirrorDNA Level 1 Compliant](https://raw.githubusercontent.com/MirrorDNA-Reflection-Protocol/MirrorDNA-Standard/main/badges/reflective_compliance_light.svg)](https://github.com/MirrorDNA-Reflection-Protocol/MirrorDNA-Standard)

This project implements MirrorDNA Level 1 compliance with:
- Cite-or-Silence (AHP) anti-hallucination
- Explicit uncertainty marking
- Basic session tracking
```

---

### Level 2 Project

```markdown
# My Project

[![MirrorDNA Level 2 Verified](https://raw.githubusercontent.com/MirrorDNA-Reflection-Protocol/MirrorDNA-Standard/main/badges/verified-reflective.svg)](https://github.com/MirrorDNA-Reflection-Protocol/MirrorDNA-Standard)

This project implements MirrorDNA Level 2 compliance with:
- All Level 1 features
- State persistence across sessions
- Session lineage tracking
- Checksum validation
```

---

### Level 3 Project

```markdown
# My Project

[![MirrorDNA Level 3 Verified](https://raw.githubusercontent.com/MirrorDNA-Reflection-Protocol/MirrorDNA-Standard/main/badges/verified-reflective.svg)](https://github.com/MirrorDNA-Reflection-Protocol/MirrorDNA-Standard)

**MirrorDNA Level 3: Vault-Backed Sovereign**

This project implements full MirrorDNA compliance with:
- All Level 1 & 2 features
- Vault-backed storage (Obsidian)
- Sovereign identity (user owns vault_id)
- Glyph signatures
- Comprehensive interaction safety
```

---

## Badge Linking

### Link to MirrorDNA-Standard Repo

```markdown
[![MirrorDNA Compliant](badge-url)](https://github.com/MirrorDNA-Reflection-Protocol/MirrorDNA-Standard)
```

**Why**: Helps users discover MirrorDNA Standard

---

### Link to Your Compliance Docs

```markdown
[![MirrorDNA Compliant](badge-url)](docs/MIRRORDNA_COMPLIANCE.md)
```

**Why**: Shows transparency about your implementation

---

### Link to Validator Report

```markdown
[![MirrorDNA Compliant](badge-url)](reports/validation-report.txt)
```

**Why**: Proves you passed validation

---

## Badge Customization (Coming in v1.1)

**Future features:**
- Auto-generated badges with level numbers
- Badges with last-validated date
- Badges with validator version
- Custom colors/styles

**Current**: Use provided SVGs as-is

---

## Embedding in Documentation

### README.md

```markdown
## Compliance

This project is MirrorDNA Level 2 compliant.

[![Verified](badge-url)](validation-link)

See [COMPLIANCE.md](COMPLIANCE.md) for details.
```

---

### CONTRIBUTING.md

```markdown
## MirrorDNA Compliance

All contributions must maintain MirrorDNA compliance.

Before submitting:
1. Run validator
2. Ensure all checks pass
3. Update badge if level changes
```

---

### Documentation Site

```html
<div class="compliance-badge">
  <img src="badge-url" alt="MirrorDNA Compliant">
  <p>This project follows MirrorDNA Standard v1.0</p>
</div>
```

---

## Badge Verification (Manual)

**How to verify a project's compliance:**

1. **Clone the project**
   ```bash
   git clone project-url
   cd project
   ```

2. **Find MirrorDNA configs**
   ```bash
   ls mirrorDNA*.yaml
   ls *_policy.yaml
   ls *_profile.yaml
   ```

3. **Run validator yourself**
   ```bash
   python -m validators.cli \
     --manifest mirrorDNA_manifest.yaml \
     --policy reflection_policy.yaml
   ```

4. **Check results**
   - PASSED = Badge is legitimate
   - FAILED = Badge usage is incorrect

---

## Reporting Badge Misuse

**If you find a project using a MirrorDNA badge without passing validation:**

1. **Verify** the misuse (run validator yourself)
2. **Contact** the project maintainers (polite, helpful)
3. **Report** to MirrorDNA-Standard repo (GitHub issue)

**We prefer education over enforcement.**

---

## Badge Files

All badges are SVG format:

| File | Size | Use |
|------|------|-----|
| `reflective_compliance_light.svg` | ~1 KB | Level 1+ (light bg) |
| `reflective_compliance_dark.svg` | ~1 KB | Level 1+ (dark bg) |
| `verified-reflective.svg` | ~2 KB | Level 2+ (verified) |
| `mirrorDNA_compatible.svg` | ~1 KB | Compatible (not fully compliant) |

**Format**: Scalable Vector Graphics (works at any size)

---

## Future: Automated Badge Service (v1.1)

**Coming soon:**

```bash
# Generate badge from validation
mirrordna badge --from-validation validation-report.json

# Auto-update badge on CI/CD
mirrordna badge --auto-update --output README.md
```

**Current workaround**: Copy markdown manually after validation.

---

## Questions?

- 🔧 **Validation help**: [`../docs/INTEGRATION.md`](../docs/INTEGRATION.md)
- ❓ **General FAQ**: [`../docs/FAQ.md`](../docs/FAQ.md)
- 📋 **Compliance levels**: [`../docs/CHOOSING_COMPLIANCE_LEVEL.md`](../docs/CHOOSING_COMPLIANCE_LEVEL.md)

---

⟡⟦BADGES⟧

*Use badges responsibly. Only display them after passing validation.*
