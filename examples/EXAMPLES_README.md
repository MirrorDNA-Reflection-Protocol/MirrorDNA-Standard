# MirrorDNA Standard Examples

This directory contains example configuration files demonstrating MirrorDNA compliance at different levels.

## Example Files

### Level 1: Basic Reflection

**Files:**
- `minimal_project_manifest.yaml` - Minimal manifest for Level 1 compliance
- `example_reflection_policy.yaml` - Basic reflection policy

**Usage:**
```bash
python -m validators.cli \
  --manifest examples/minimal_project_manifest.yaml \
  --policy examples/example_reflection_policy.yaml
```

**What Level 1 Provides:**
- Cite-or-Silence (AHP) anti-hallucination protocol
- Explicit uncertainty marking
- Basic session tracking
- At least one trust marker

### Level 2: Continuity Aware

**Files:**
- `level2_project_manifest.yaml` - Manifest for Level 2 compliance
- `example_continuity_profile.yaml` - Continuity configuration with persistent state
- `example_reflection_policy.yaml` - Reflection policy (same as Level 1)

**Usage:**
```bash
python -m validators.cli \
  --manifest examples/level2_project_manifest.yaml \
  --profile examples/example_continuity_profile.yaml \
  --policy examples/example_reflection_policy.yaml
```

**What Level 2 Adds:**
- Persistent state storage
- Session lineage tracking (predecessor/successor)
- Artifact checksum validation
- Session recovery capabilities

### Level 3: Vault-Backed Sovereign

**Files:**
- `level3_project_manifest.yaml` - Manifest for Level 3 compliance
- `level3_continuity_profile.yaml` - Vault-backed continuity configuration
- `level3_reflection_policy.yaml` - Comprehensive reflection policy with glyphs and safety

**Usage:**
```bash
python -m validators.cli \
  --manifest examples/level3_project_manifest.yaml \
  --profile examples/level3_continuity_profile.yaml \
  --policy examples/level3_reflection_policy.yaml
```

**What Level 3 Adds:**
- Vault-backed storage (Obsidian or custom)
- Sovereign identity (user owns vault)
- Glyph signatures for semantic marking
- Comprehensive interaction safety protocols
- Full lineage tracking and compliance reporting

## Quick Start

1. **Install dependencies:**
   ```bash
   pip install -r validators/requirements.txt
   ```

2. **Run validator on an example:**
   ```bash
   # Level 1 example
   python -m validators.cli \
     --manifest examples/minimal_project_manifest.yaml \
     --policy examples/example_reflection_policy.yaml
   ```

3. **Interpret results:**
   - ✓ PASSED: Configuration meets declared compliance level
   - ✗ FAILED: Errors found, see details in output
   - Warnings: Non-critical issues or recommendations

## Creating Your Own Configuration

### For Level 1 (Basic Reflection)

Create two files:

1. `mirrorDNA_manifest.yaml`:
   ```yaml
   name: "YourProject"
   version: "1.0.0"
   mirrorDNA_compliance_level: "level_1_basic_reflection"
   layers:
     mirrorDNA_protocol: true
   reflection_policy: "reflection_policy.yaml"
   ```

2. `reflection_policy.yaml`:
   ```yaml
   policy_version: "1.0.0"
   reflection_mode: "constitutive"
   uncertainty_handling:
     cite_or_silence: true
     unknown_marker: "[Unknown]"
   ```

Then validate:
```bash
python -m validators.cli --manifest mirrorDNA_manifest.yaml --policy reflection_policy.yaml
```

### For Level 2 (Continuity Aware)

Add a third file:

3. `continuity_profile.yaml`:
   ```yaml
   profile_version: "1.0.0"
   continuity_mechanism: "local_state"
   state_persistence:
     enabled: true
     storage_type: "file_system"
     storage_location: "./data"
   ```

Update manifest to declare `level_2_continuity_aware` and reference the profile.

### For Level 3 (Vault-Backed Sovereign)

Update continuity profile to use vault:
```yaml
continuity_mechanism: "vault_backed"
vault_configuration:
  vault_type: "obsidian"
  vault_id: "AMOS://YourProject/Vault/v1.0"
  vault_path: "./vault"
```

Add glyph signatures to reflection policy:
```yaml
glyph_signatures:
  enabled: true
  registered_glyphs:
    - glyph: "⟡⟦CONTINUITY⟧"
      meaning: "Continuity marker"
      category: "continuity"
```

## Schema References

All examples validate against schemas in `/schema`:
- `project_manifest.schema.json`
- `continuity_profile.schema.json`
- `reflection_policy.schema.json`

See schema files for complete field documentation.

## Legacy Examples

This directory may also contain legacy example files from earlier versions:
- `minimal-artifact.md` - Legacy artifact example
- `complete-artifact.md.json` - Legacy sidecar example
- `template_sidecar.json` - Legacy template

These are kept for backward compatibility but new projects should use the YAML examples above.

## Support

For questions or issues:
- See `/spec/mirrorDNA-standard-v1.0.md` for full specification
- See `/spec/compliance_levels.md` for detailed level requirements
- Check validator output for specific guidance

⟡⟦EXAMPLES⟧ · ⟡⟦GUIDE⟧
