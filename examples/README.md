# MirrorDNA Configuration Examples

**Purpose**: Copy-paste ready configuration files for all three compliance levels.

**Status**: Production-tested (all examples pass validation)

---

## Quick Start

**Pick your level:**

| Level | Anti-Hallucination | Continuity | Sovereignty | Time to Setup |
|-------|-------------------|------------|-------------|---------------|
| **Level 1** | ✅ | ❌ | ❌ | 10 minutes |
| **Level 2** | ✅ | ✅ | ❌ | 30 minutes |
| **Level 3** | ✅ | ✅ | ✅ | 1-2 hours |

---

## Level 1: Basic Reflection

**What you get**: Anti-hallucination (cite-or-silence) + explicit uncertainty marking

### Files

- [`level1/project_manifest.yaml`](level1/project_manifest.yaml) — Project metadata
- [`level1/reflection_policy.yaml`](level1/reflection_policy.yaml) — Reflection protocol config

### Quick Start

```bash
# 1. Copy files to your project
cp examples/level1/*.yaml .
mv project_manifest.yaml mirrorDNA_manifest.yaml

# 2. Edit for your project
nano mirrorDNA_manifest.yaml
# Update: name, version, description

# 3. Validate
python -m validators.cli \
  --manifest mirrorDNA_manifest.yaml \
  --policy reflection_policy.yaml
```

### Key Features

✅ **Cite-or-Silence (AHP)**
```yaml
uncertainty_handling:
  cite_or_silence: true
  unknown_marker: "[Unknown]"
```

✅ **Trust Markers**
```yaml
trust_markers:
  - type: "cite_or_silence"
    description: "AHP implemented"
```

✅ **Basic Session Tracking**
```yaml
session_tracking:
  enabled: true
  session_id_format: "timestamp"
```

---

## Level 2: Continuity Aware

**What you get**: Level 1 + state persistence + session lineage + checksums

### Files

- [`level2/project_manifest.yaml`](level2/project_manifest.yaml) — Manifest with continuity
- [`level2/reflection_policy.yaml`](level2/reflection_policy.yaml) — Same as Level 1
- [`level2/continuity_profile.yaml`](level2/continuity_profile.yaml) — Persistence config

### Quick Start

```bash
# 1. Copy files
cp examples/level2/*.yaml .
mv project_manifest.yaml mirrorDNA_manifest.yaml

# 2. Edit configs
nano mirrorDNA_manifest.yaml
nano continuity_profile.yaml
# Update: storage_location, checkpoint settings

# 3. Validate
python -m validators.cli \
  --manifest mirrorDNA_manifest.yaml \
  --policy reflection_policy.yaml \
  --profile continuity_profile.yaml
```

### Key Features (Beyond Level 1)

✅ **State Persistence**
```yaml
state_persistence:
  enabled: true
  storage_type: "filesystem"
  storage_location: "./vault/state"
```

✅ **Session Lineage**
```yaml
session_lineage:
  track_predecessors: true
  track_successors: true
  lineage_format: "json"
```

✅ **Checksum Validation**
```yaml
integrity_verification:
  enabled: true
  checksum_algorithm: "sha256"
  verify_on_load: true
```

✅ **Session Recovery**
```yaml
session_recovery:
  enabled: true
  recovery_mechanism: "checkpoint"
  checkpoint_interval_minutes: 15
```

---

## Level 3: Vault-Backed Sovereign

**What you get**: Level 1 + Level 2 + vault storage + sovereignty + glyphs

### Files

- [`level3/project_manifest.yaml`](level3/project_manifest.yaml) — Full vault config
- [`level3/reflection_policy.yaml`](level3/reflection_policy.yaml) — With glyphs + safety
- [`level3/continuity_profile.yaml`](level3/continuity_profile.yaml) — Vault-backed storage

### Quick Start

```bash
# 1. Copy files
cp examples/level3/*.yaml .
mv project_manifest.yaml mirrorDNA_manifest.yaml

# 2. Edit ALL three files
nano mirrorDNA_manifest.yaml
# Update: vault_id, vault_path

nano continuity_profile.yaml
# Update: vault settings

nano reflection_policy.yaml
# Update: glyph signature format

# 3. Validate
python -m validators.cli \
  --manifest mirrorDNA_manifest.yaml \
  --policy reflection_policy.yaml \
  --profile continuity_profile.yaml
```

### Key Features (Beyond Level 2)

✅ **Vault Configuration**
```yaml
vault_configuration:
  vault_type: "obsidian"
  vault_id: "ProjectName://Vault/v1.0"
  vault_path: "./vault"
```

✅ **Glyph Signatures**
```yaml
glyph_signatures:
  enabled: true
  primary_glyph: "⟡"
  signature_format: "⟡⟦PROJECTNAME⟧"
```

✅ **Interaction Safety**
```yaml
interaction_safety:
  enabled: true
  session_limit_minutes: 90
  escalation_protocol: true
```

✅ **Vault-Backed Storage**
```yaml
state_persistence:
  storage_type: "vault"
  vault_integration: true
```

---

## Common Customizations

### Change Storage Type (Level 2+)

```yaml
# Filesystem (default)
storage_type: "filesystem"
storage_location: "./vault/state"

# Database
storage_type: "database"
connection_string: "postgresql://localhost/mydb"

# Cloud (with caveats - see Level 3 for sovereignty)
storage_type: "cloud"
provider: "s3"
bucket: "my-mirrordna-vault"
```

---

### Change Vault Type (Level 3 only)

```yaml
# Obsidian (recommended)
vault_type: "obsidian"
vault_path: "./vault"

# Custom vault
vault_type: "custom"
vault_implementation: "MyVaultClass"
```

---

### Adjust Session Safety (Level 3)

```yaml
interaction_safety:
  enabled: true
  session_limit_minutes: 60    # Shorter sessions
  escalation_protocol: true
  warning_at_minutes: 45       # Warn before limit
```

---

## Validation Workflow

### Step 1: Choose Level

```
Stateless? → Level 1
Need memory? → Level 2
Need sovereignty? → Level 3
```

### Step 2: Copy Files

```bash
cp examples/levelN/*.yaml .
```

### Step 3: Customize

```bash
# Edit files for your project
nano mirrorDNA_manifest.yaml
nano reflection_policy.yaml
nano continuity_profile.yaml  # Level 2+ only
```

### Step 4: Validate

```bash
python -m validators.cli --manifest mirrorDNA_manifest.yaml --policy reflection_policy.yaml
# Add --profile continuity_profile.yaml for Level 2+
```

### Step 5: Fix Errors

Read validator output and adjust configs.

### Step 6: Badge It

Add compliance badge to your README:

```markdown
![MirrorDNA Level N](https://raw.githubusercontent.com/MirrorDNA-Reflection-Protocol/MirrorDNA-Standard/main/badges/reflective_compliance_light.svg)
```

---

## Testing Your Config

### Level 1 Tests

```bash
# Should pass
python -m validators.cli \
  --manifest examples/level1/project_manifest.yaml \
  --policy examples/level1/reflection_policy.yaml

# Should fail (missing policy)
python -m validators.cli \
  --manifest examples/level1/project_manifest.yaml
```

### Level 2 Tests

```bash
# Should pass
python -m validators.cli \
  --manifest examples/level2/project_manifest.yaml \
  --policy examples/level2/reflection_policy.yaml \
  --profile examples/level2/continuity_profile.yaml

# Should fail (Level 2 declared but no profile)
python -m validators.cli \
  --manifest examples/level2/project_manifest.yaml \
  --policy examples/level2/reflection_policy.yaml
```

### Level 3 Tests

```bash
# Should pass
python -m validators.cli \
  --manifest examples/level3/project_manifest.yaml \
  --policy examples/level3/reflection_policy.yaml \
  --profile examples/level3/continuity_profile.yaml

# Should auto-detect Level 3
# (validator sees vault_configuration in manifest)
```

---

## Troubleshooting

### "Schema validation failed"

**Fix**: Check YAML syntax

```bash
python -c "import yaml; yaml.safe_load(open('mirrorDNA_manifest.yaml'))"
```

---

### "cite_or_silence must be true"

**Fix**: In `reflection_policy.yaml`:

```yaml
uncertainty_handling:
  cite_or_silence: true  # Must be true, not false
```

---

### "Level mismatch detected"

**Fix**: Either:
1. Downgrade declared level in manifest, OR
2. Add missing features for higher level

---

### "No trust markers found"

**Fix**: In `mirrorDNA_manifest.yaml`:

```yaml
trust_markers:
  - type: "cite_or_silence"
    description: "AHP protocol implemented"
```

---

## File Structure

```
examples/
├── README.md                          ← You are here
│
├── level1/                            ← Basic Reflection
│   ├── project_manifest.yaml          (Level 1 manifest)
│   └── reflection_policy.yaml         (Basic policy)
│
├── level2/                            ← Continuity Aware
│   ├── project_manifest.yaml          (Level 2 manifest)
│   ├── reflection_policy.yaml         (Same as Level 1)
│   └── continuity_profile.yaml        (Persistence config)
│
└── level3/                            ← Vault-Backed Sovereign
    ├── project_manifest.yaml          (Level 3 manifest)
    ├── reflection_policy.yaml         (With glyphs + safety)
    └── continuity_profile.yaml        (Vault-backed)
```

---

## Next Steps

After validation passes:

1. **Add badge** to your README (see [`../badges/README.md`](../badges/README.md))
2. **Document compliance** in your project docs
3. **Re-validate** on each release
4. **Track changes** in CHANGELOG

---

## Need Help?

- 📋 **Spec details**: [`../spec/mirrorDNA-standard-v1.0.md`](../spec/mirrorDNA-standard-v1.0.md)
- 🔌 **Integration guide**: [`../docs/INTEGRATION.md`](../docs/INTEGRATION.md)
- 🎯 **Choose level**: [`../docs/CHOOSING_COMPLIANCE_LEVEL.md`](../docs/CHOOSING_COMPLIANCE_LEVEL.md)
- ❓ **FAQ**: [`../docs/FAQ.md`](../docs/FAQ.md)

---

⟡⟦EXAMPLES⟧

*All examples are tested and pass validation. Use them as templates.*
