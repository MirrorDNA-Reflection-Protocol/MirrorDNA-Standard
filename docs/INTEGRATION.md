# Integration Guide: Adopting MirrorDNA in Your Project

**Purpose**: Step-by-step guide for integrating MirrorDNA compliance into existing projects.

**Audience**: Developers adding MirrorDNA to their AI systems.

---

## Overview

This guide walks you through:
1. Choosing the right compliance level
2. Installing the validator
3. Creating configuration files
4. Running validation
5. Fixing common issues
6. Adding compliance badges
7. Maintaining compliance over time

**Time to complete**: 30 minutes to 2 hours (depending on complexity)

---

## Step 1: Choose Your Compliance Level

**Quick Decision Tree:**

```
Do you need state persistence across sessions?
│
├─ NO → Level 1 (Basic Reflection)
│        ├─ Anti-hallucination only
│        └─ No persistent storage needed
│
└─ YES → Do you need user sovereignty + vault?
         │
         ├─ NO → Level 2 (Continuity Aware)
         │        ├─ State persistence
         │        └─ Any storage mechanism
         │
         └─ YES → Level 3 (Vault-Backed Sovereign)
                  ├─ Obsidian or custom vault
                  └─ Full user control
```

**Detailed guide**: See [`CHOOSING_COMPLIANCE_LEVEL.md`](CHOOSING_COMPLIANCE_LEVEL.md)

---

## Step 2: Install the Validator

```bash
# Clone the MirrorDNA-Standard repo
git clone https://github.com/MirrorDNA-Reflection-Protocol/MirrorDNA-Standard.git
cd MirrorDNA-Standard

# Install dependencies
pip install -r validators/requirements.txt

# Verify installation
python -m validators.cli --help
```

**Expected output:**
```
usage: cli.py [-h] --manifest MANIFEST [--policy POLICY] [--profile PROFILE]

MirrorDNA Compliance Validator
```

---

## Step 3: Create Configuration Files

### For Level 1 Projects

**Create `mirrorDNA_manifest.yaml`:**

```yaml
name: "YourProjectName"
version: "1.0.0"
description: "Brief description of your project"

# Declare compliance level
mirrorDNA_compliance_level: "level_1_basic_reflection"

# Specify which layers you implement
layers:
  mirrorDNA_protocol: true

# Link to your reflection policy
reflection_policy: "reflection_policy.yaml"

# Trust markers
trust_markers:
  - type: "cite_or_silence"
    description: "AHP implemented in prompt templates"
```

**Create `reflection_policy.yaml`:**

```yaml
policy_version: "1.0.0"

# Reflection mode: constitutive (reflects actual state)
reflection_mode: "constitutive"

# Uncertainty handling
uncertainty_handling:
  cite_or_silence: true
  unknown_marker: "[Unknown]"
  speculation_marker: "[Speculation]"

# Anti-hallucination protocol
anti_hallucination:
  source_citation: true
  fabrication_prevention: true

# Session tracking (basic)
session_tracking:
  enabled: true
  session_id_format: "timestamp"
```

---

### For Level 2 Projects (adds continuity)

Use Level 1 configs above, **PLUS**:

**Update `mirrorDNA_manifest.yaml`:**

```yaml
mirrorDNA_compliance_level: "level_2_continuity_aware"

# Add continuity profile reference
continuity_profile: "continuity_profile.yaml"
```

**Create `continuity_profile.yaml`:**

```yaml
profile_version: "1.0.0"

# State persistence
state_persistence:
  enabled: true
  storage_type: "filesystem"  # or "database", "cloud"
  storage_location: "./vault/state"

# Session lineage
session_lineage:
  track_predecessors: true
  track_successors: true
  lineage_format: "json"

# Checksum validation
integrity_verification:
  enabled: true
  checksum_algorithm: "sha256"
  verify_on_load: true

# Session recovery
session_recovery:
  enabled: true
  recovery_mechanism: "checkpoint"
  checkpoint_interval_minutes: 15
```

---

### For Level 3 Projects (adds vault sovereignty)

Use Level 1 + Level 2 configs above, **PLUS**:

**Update `mirrorDNA_manifest.yaml`:**

```yaml
mirrorDNA_compliance_level: "level_3_vault_backed_sovereign"

# Add vault configuration
layers:
  mirrorDNA_protocol: true
  activeMirrorOS: false  # Set to true if using ActiveMirrorOS

vault_configuration:
  vault_type: "obsidian"  # or "custom"
  vault_id: "YourProject://Vault/v1.0"  # Unique vault identifier
  vault_path: "./vault"
```

**Update `continuity_profile.yaml`:**

```yaml
# Change storage to vault-backed
state_persistence:
  enabled: true
  storage_type: "vault"
  vault_integration: true
```

**Update `reflection_policy.yaml`:**

```yaml
# Add glyph signatures
glyph_signatures:
  enabled: true
  primary_glyph: "⟡"
  signature_format: "⟡⟦PROJECTNAME⟧"

# Add interaction safety
interaction_safety:
  enabled: true
  session_limit_minutes: 90
  escalation_protocol: true
  disclaimer: "This is a reflective AI system, not a substitute for professional advice."
```

---

## Step 4: Run Validation

### Level 1 Validation

```bash
python -m validators.cli \
  --manifest mirrorDNA_manifest.yaml \
  --policy reflection_policy.yaml
```

### Level 2 Validation

```bash
python -m validators.cli \
  --manifest mirrorDNA_manifest.yaml \
  --policy reflection_policy.yaml \
  --profile continuity_profile.yaml
```

### Level 3 Validation

```bash
# Same as Level 2 (validator auto-detects Level 3 from manifest)
python -m validators.cli \
  --manifest mirrorDNA_manifest.yaml \
  --policy reflection_policy.yaml \
  --profile continuity_profile.yaml
```

---

## Step 5: Interpret Results

### Success Output

```
========================================
MirrorDNA Compliance Report
========================================

Project: YourProjectName
Declared Level: level_1_basic_reflection
Detected Level: level_1_basic_reflection

[PASSED] Schema Validation
[PASSED] Reflection Checks
[PASSED] Trust Markers
[PASSED] Cite-or-Silence Protocol

========================================
OVERALL: COMPLIANT ✓
========================================

Your project meets Level 1 requirements.
You may use the Level 1 compliance badge.
```

### Failure Output

```
========================================
MirrorDNA Compliance Report
========================================

Project: YourProjectName
Declared Level: level_2_continuity_aware
Detected Level: level_1_basic_reflection

[PASSED] Schema Validation
[PASSED] Reflection Checks
[FAILED] Continuity Checks
  - Missing: session_lineage.track_predecessors
  - Missing: integrity_verification.checksum_algorithm

[FAILED] Level Mismatch
  - Declared Level 2 but only meets Level 1 requirements

========================================
OVERALL: NOT COMPLIANT ✗
========================================

Recommendations:
1. Add predecessor tracking to continuity_profile.yaml
2. Enable checksum validation
3. Or downgrade declared level to level_1_basic_reflection
```

---

## Step 6: Fix Common Issues

### Issue: "Schema validation failed"

**Cause**: YAML syntax error or missing required fields.

**Fix:**
```bash
# Validate YAML syntax
python -c "import yaml; yaml.safe_load(open('mirrorDNA_manifest.yaml'))"

# Compare to examples
diff mirrorDNA_manifest.yaml examples/level1/project_manifest.yaml
```

---

### Issue: "Cite-or-Silence not detected"

**Cause**: `cite_or_silence: false` or missing in reflection_policy.yaml.

**Fix:**
```yaml
# In reflection_policy.yaml
uncertainty_handling:
  cite_or_silence: true  # Must be true
  unknown_marker: "[Unknown]"
```

---

### Issue: "Level mismatch"

**Cause**: Declared Level 2 but missing continuity features.

**Fix:**
```yaml
# Option 1: Downgrade to Level 1
mirrorDNA_compliance_level: "level_1_basic_reflection"

# Option 2: Add missing continuity features
# See continuity_profile.yaml examples
```

---

### Issue: "No trust markers found"

**Cause**: Missing `trust_markers` section in manifest.

**Fix:**
```yaml
# In mirrorDNA_manifest.yaml
trust_markers:
  - type: "cite_or_silence"
    description: "AHP implemented in prompt engineering"
  - type: "checksum_verification"
    description: "SHA-256 checksums for all artifacts"
```

---

## Step 7: Add Compliance Badge

Once you pass validation:

```markdown
# In your README.md

![MirrorDNA Level 1 Compliant](https://raw.githubusercontent.com/MirrorDNA-Reflection-Protocol/MirrorDNA-Standard/main/badges/reflective_compliance_light.svg)
```

**Badge options**: See [`../badges/README.md`](../badges/README.md)

---

## Step 8: Maintain Compliance Over Time

### On Every Release

1. Update version in `mirrorDNA_manifest.yaml`
2. Re-run validator
3. Update CHANGELOG with compliance status

### On Major Changes

1. Review compliance requirements
2. Update config files if needed
3. Re-validate
4. Document changes in lineage

### On Spec Updates

1. Watch for MirrorDNA-Standard releases
2. Review breaking changes (major versions only)
3. Update configs if needed
4. Re-validate

---

## Integration Patterns

### Pattern 1: Retrofit Existing Project

**Scenario**: You have an existing AI project.

**Steps:**
1. Add MirrorDNA configs (don't change code yet)
2. Run validator (will likely fail)
3. Identify gaps
4. Implement missing features (cite-or-silence, state persistence, etc.)
5. Re-validate

**Effort**: Medium (1-4 weeks depending on gaps)

---

### Pattern 2: Build New Project MirrorDNA-First

**Scenario**: Starting from scratch.

**Steps:**
1. Choose compliance level
2. Copy example configs
3. Design architecture around MirrorDNA principles
4. Implement features
5. Validate continuously

**Effort**: Low (MirrorDNA guides your design)

---

### Pattern 3: Gradual Adoption

**Scenario**: Large codebase, can't change everything at once.

**Steps:**
1. Start with Level 1 (anti-hallucination only)
2. Validate and badge
3. Add continuity features → Level 2
4. Re-validate and upgrade badge
5. Add vault sovereignty → Level 3
6. Final validation

**Effort**: Spread over multiple releases

---

## Language-Specific Examples

### Python + LangChain

```python
# reflection_wrapper.py
from langchain.llms import OpenAI

class MirrorDNAWrapper:
    def __init__(self, llm, policy_config):
        self.llm = llm
        self.policy = policy_config
        
    def query(self, prompt):
        # Add cite-or-silence instruction
        enhanced_prompt = f"{prompt}\n\nFollow AHP: Cite sources or say [Unknown]."
        
        response = self.llm(enhanced_prompt)
        
        # Validate response (check for citations)
        if self.contains_fabrication(response):
            return "[Unknown] Response failed cite-or-silence check."
        
        return response
```

---

### JavaScript + OpenAI API

```javascript
// mirrorDNA.js
const { OpenAI } = require('openai');

class MirrorDNAClient {
  constructor(apiKey, policyConfig) {
    this.client = new OpenAI({ apiKey });
    this.policy = policyConfig;
  }
  
  async query(prompt) {
    const enhancedPrompt = `${prompt}\n\nFollow AHP: Cite sources or say [Unknown].`;
    
    const response = await this.client.chat.completions.create({
      model: 'gpt-4',
      messages: [{ role: 'user', content: enhancedPrompt }]
    });
    
    // Check for cite-or-silence compliance
    if (!this.hasCitation(response)) {
      return '[Unknown] No citation provided.';
    }
    
    return response.choices[0].message.content;
  }
}
```

---

## Testing Your Integration

### Test Checklist

**Level 1:**
- [ ] AI refuses to fabricate sources (AHP)
- [ ] Unknown information marked with `[Unknown]`
- [ ] Session tracking generates unique IDs
- [ ] At least one trust marker documented

**Level 2:**
- [ ] State persists across sessions
- [ ] Session lineage tracked (predecessor/successor)
- [ ] Checksums validate correctly
- [ ] Session recovery works after crash

**Level 3:**
- [ ] Vault storage functional
- [ ] User controls vault_id
- [ ] Glyph signatures present
- [ ] Interaction safety limits enforced

---

## CI/CD Integration (Coming in v1.1)

**Future support** for automated validation:

```yaml
# .github/workflows/mirrordna-validate.yml
name: MirrorDNA Compliance

on: [push, pull_request]

jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - uses: mirrordna/validate-action@v1
        with:
          manifest: mirrorDNA_manifest.yaml
          policy: reflection_policy.yaml
```

**Current workaround**: Run validator in CI via bash script.

---

## Need Help?

- 📋 **Spec**: [`../spec/mirrorDNA-standard-v1.0.md`](../spec/mirrorDNA-standard-v1.0.md)
- ❓ **FAQ**: [`FAQ.md`](FAQ.md)
- 💡 **Examples**: [`../examples/README.md`](../examples/README.md)
- 🐛 **Issues**: GitHub Issues

---

⟡⟦INTEGRATION⟧

*This guide is living documentation. Contribute improvements via pull request.*
