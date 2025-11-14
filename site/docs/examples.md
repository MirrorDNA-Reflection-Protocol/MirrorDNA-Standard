# Examples and Use Cases

Working configurations and real-world examples of MirrorDNA compliance.

---

## Overview

The `/examples` directory contains **reference artifacts** and **configuration templates** for all three compliance levels.

!!! info "All Examples Are Tested"
    Every example in this directory passes validation. You can copy and use them directly.

---

## Example Structure

```
examples/
├── README.md
├── EXAMPLES_README.md
├── minimal-artifact.md
├── minimal_project_manifest.yaml
├── example_reflection_policy.yaml
├── example_continuity_profile.yaml
├── level2_project_manifest.yaml
├── level3_project_manifest.yaml
├── level3_reflection_policy.yaml
└── level3_continuity_profile.yaml
```

---

## Level 1 Examples: Basic Reflection

### Minimal Project Manifest

**File:** `minimal_project_manifest.yaml`

**Purpose:** Smallest valid Level 1 configuration

```yaml
# Minimal MirrorDNA Project Manifest
# Demonstrates Level 1 (Basic Reflection) compliance

name: "MyReflectiveApp"
version: "1.0.0"
description: "A basic reflective application demonstrating cite-or-silence protocol"

# Compliance level: Level 1 (Basic Reflection)
mirrorDNA_compliance_level: "level_1_basic_reflection"

# Which MirrorDNA ecosystem layers are used
layers:
  mirrorDNA_protocol: true
  lingOS: false
  activeMirrorOS: false
  trustByDesign: true

# Reflection policy (required for all levels)
reflection_policy: "example_reflection_policy.yaml"

# Project metadata
maintainers:
  - name: "Example Developer"
    email: "developer@example.com"

repository: "https://github.com/example/myreflectiveapp"
license: "MIT"
created: "2025-01-01"
updated: "2025-11-14T00:00:00Z"
```

**Use this when:**

- You want the simplest possible MirrorDNA setup
- Your project doesn't need persistent state
- You only need anti-hallucination (cite-or-silence)

### Reflection Policy

**File:** `example_reflection_policy.yaml`

**Purpose:** Standard reflection policy for Level 1 and Level 2

```yaml
# Example MirrorDNA Reflection Policy
# Suitable for Level 1 and Level 2 projects

policy_version: "1.0.0"

# Reflection mode: constitutive (actual state), simulated (pattern-based), or hybrid
reflection_mode: "constitutive"

# How uncertainty is handled
uncertainty_handling:
  # Cite or Silence (AHP): Required for all levels
  cite_or_silence: true

  # Markers for unknown information
  unknown_marker: "[Unknown]"

  # Whether speculation is allowed (must be marked)
  speculation_allowed: true
  speculation_marker: "[Speculation]"

# Anti-hallucination measures
anti_hallucination:
  # Require outputs to be grounded in sources
  grounding_required: true

  # Require explicit source citations
  source_citation: true

  # Enable fact checking (optional)
  fact_checking: false

  # Enable hallucination detection
  hallucination_detection: false

  # Protocol for handling detected hallucinations
  correction_protocol: "immediate_correction"

# Reflection protocols
reflection_protocols:
  # Enable self-correction based on reflection
  self_correction: true

  # Markers for reflective content
  reflection_markers:
    - "[Reflection]"
    - "[Self-Check]"

  # Provide meta-commentary about reasoning
  meta_commentary: false

  # Expose chain-of-thought reasoning
  chain_of_thought: false

# Trust markers used in this system
trust_markers:
  - marker: "[Unknown]"
    meaning: "Information is not available or cannot be verified"

  - marker: "[Speculation]"
    meaning: "This is speculative or hypothetical content"

  - marker: "[Unverified]"
    meaning: "This information has not been verified against sources"
```

**Key features:**

- **Cite or Silence:** Enabled by default
- **Unknown markers:** Explicit `[Unknown]` tag
- **Speculation:** Allowed but must be marked
- **Grounding:** All outputs must be source-backed

---

## Level 2 Examples: Continuity Aware

### Level 2 Project Manifest

**File:** `level2_project_manifest.yaml`

**Purpose:** Full Level 2 configuration with state persistence

```yaml
name: "MyStatefulApp"
version: "2.0.0"
description: "Continuity-aware application with session persistence"

mirrorDNA_compliance_level: "level_2_continuity_aware"

layers:
  mirrorDNA_protocol: true
  lingOS: false
  activeMirrorOS: false
  trustByDesign: true

# Both reflection policy and continuity profile required
reflection_policy: "example_reflection_policy.yaml"
continuity_profile: "example_continuity_profile.yaml"

maintainers:
  - name: "Developer Team"
    email: "dev@example.com"

repository: "https://github.com/example/stateful-app"
license: "MIT"
```

### Continuity Profile

**File:** `example_continuity_profile.yaml`

**Purpose:** Configuration for state persistence and session tracking

```yaml
# Example MirrorDNA Continuity Profile
# Suitable for Level 2 (Continuity Aware) projects

profile_version: "1.0.0"

# Primary continuity mechanism
continuity_mechanism: "local_state"

# State persistence configuration
state_persistence:
  # Enable persistent state
  enabled: true

  # Storage type
  storage_type: "file_system"

  # Storage location (relative or absolute path)
  storage_location: "./data/continuity"

  # Encrypt storage
  encryption: true

  # Validate checksums
  checksum_validation: true

# Session management
session_management:
  # Track sessions explicitly
  session_tracking: true

  # Session ID format
  session_id_format: "UUID"

  # Maximum session duration (0 = unlimited)
  max_session_duration: 0

  # New sessions inherit state from previous
  session_inheritance: true

# Continuity guarantees
continuity_guarantees:
  # Preserve user/system identity across sessions
  identity_preservation: true

  # Ensure state consistency
  state_consistency: true

  # Track lineage and ancestry
  lineage_tracking: true

  # Implement anti-hallucination measures
  anti_hallucination: true

# Recovery and rollback
recovery:
  # Enable rollback to previous states
  rollback_enabled: true

  # How often snapshots are taken
  snapshot_frequency: "per_session"

  # How long snapshots are retained
  retention_policy: "Keep last 30 days"
```

**Key features:**

- **State persistence:** File system storage with encryption
- **Session tracking:** UUID-based session IDs
- **Lineage tracking:** Predecessor/successor relationships
- **Recovery:** Rollback to previous states

---

## Level 3 Examples: Vault-Backed Sovereign

### Level 3 Project Manifest

**File:** `level3_project_manifest.yaml`

**Purpose:** Full sovereignty with vault integration

```yaml
name: "SovereignVault"
version: "3.0.0"
description: "Vault-backed sovereign system with full user control"

mirrorDNA_compliance_level: "level_3_vault_backed_sovereign"

layers:
  mirrorDNA_protocol: true
  lingOS: true
  activeMirrorOS: false
  trustByDesign: true

reflection_policy: "level3_reflection_policy.yaml"
continuity_profile: "level3_continuity_profile.yaml"

# Level 3 specific: Vault configuration
vault:
  type: "obsidian"
  location: "./vault"
  vault_id: "AMOS://Example/v1.0"

sovereignty:
  user_owned: true
  sovereign_identity: true
  glyph_signatures: true

maintainers:
  - name: "Vault Owner"
    email: "owner@example.com"

repository: "https://github.com/example/sovereign-vault"
license: "MIT"
```

### Level 3 Reflection Policy

**File:** `level3_reflection_policy.yaml`

**Purpose:** Enhanced reflection with glyph signatures

```yaml
policy_version: "1.0.0"
reflection_mode: "constitutive"

uncertainty_handling:
  cite_or_silence: true
  unknown_marker: "[Unknown]"
  speculation_allowed: true
  speculation_marker: "[Speculation]"

anti_hallucination:
  grounding_required: true
  source_citation: true
  fact_checking: true
  hallucination_detection: true
  correction_protocol: "immediate_correction"

reflection_protocols:
  self_correction: true
  reflection_markers:
    - "[Reflection]"
    - "[Self-Check]"
  meta_commentary: true
  chain_of_thought: true

# Level 3: Enhanced trust markers
trust_markers:
  - marker: "[Unknown]"
    meaning: "Information not available"

  - marker: "[Speculation]"
    meaning: "Speculative content"

  - marker: "[Verified]"
    meaning: "Verified against vault sources"

  - marker: "⟡⟦VERIFIED⟧"
    meaning: "Glyph signature for verified content"

# Level 3: Glyph configuration
glyphs:
  primary: "⟡"
  signatures:
    - "⟡⟦VERIFIED⟧"
    - "⟡⟦MASTER⟧"
    - "⟡⟦STANDARD⟧"
```

### Level 3 Continuity Profile

**File:** `level3_continuity_profile.yaml`

**Purpose:** Vault-backed continuity with sovereignty

```yaml
profile_version: "1.0.0"
continuity_mechanism: "vault_backed"

# Level 3: Vault-specific persistence
state_persistence:
  enabled: true
  storage_type: "vault"
  storage_location: "./vault/state"
  encryption: true
  checksum_validation: true
  vault_integration: true

session_management:
  session_tracking: true
  session_id_format: "UUID"
  max_session_duration: 0
  session_inheritance: true
  # Level 3: Vault-based session storage
  session_storage: "vault://sessions/"

continuity_guarantees:
  identity_preservation: true
  state_consistency: true
  lineage_tracking: true
  anti_hallucination: true
  # Level 3: Sovereignty guarantees
  user_sovereignty: true
  vault_owned: true

# Level 3: Enhanced recovery
recovery:
  rollback_enabled: true
  snapshot_frequency: "per_session"
  retention_policy: "User-controlled"
  vault_backups: true

# Level 3: Interaction safety
interaction_safety:
  session_limits: true
  escalation_protocol: true
  consent_tracking: true
```

---

## Common Patterns

### Pattern 1: Simple Q&A Bot (Level 1)

**Use case:** Knowledge base chatbot

**Configuration:**

```yaml
# manifest.yaml
name: "KnowledgeBot"
mirrorDNA_compliance_level: "level_1_basic_reflection"
reflection_policy: "reflection_policy.yaml"
```

**Implementation:**

```python
def answer(question):
    sources = kb.search(question)
    if sources:
        return f"{generate(question, sources)}\nSource: {sources[0]}"
    return "[Unknown] No information available."
```

### Pattern 2: Personal Assistant (Level 2)

**Use case:** Multi-session conversational AI

**Configuration:**

```yaml
# manifest.yaml
name: "PersonalAssistant"
mirrorDNA_compliance_level: "level_2_continuity_aware"
reflection_policy: "reflection_policy.yaml"
continuity_profile: "continuity_profile.yaml"
```

**Implementation:**

```python
class Assistant:
    def __init__(self, session_manager):
        self.sessions = session_manager

    def chat(self, message, session_id):
        # Load previous context
        context = self.sessions.load(session_id)

        # Generate response
        response = generate(message, context)

        # Save to session
        self.sessions.save(session_id, message, response)

        return response
```

### Pattern 3: Sovereign Knowledge Vault (Level 3)

**Use case:** Personal knowledge management with AI

**Configuration:**

```yaml
# manifest.yaml
name: "MyVault"
mirrorDNA_compliance_level: "level_3_vault_backed_sovereign"
reflection_policy: "level3_reflection_policy.yaml"
continuity_profile: "level3_continuity_profile.yaml"
vault:
  type: "obsidian"
  location: "./vault"
  vault_id: "AMOS://MyVault/v1.0"
```

**Implementation:**

```python
class VaultAI:
    def __init__(self, vault_path):
        self.vault = Vault(vault_path)
        self.master_citation = self.vault.read("00_MASTER_CITATION.md")

    def reflect(self, prompt):
        # Load canonical context
        context = self.master_citation

        # Search vault
        sources = self.vault.search(prompt)

        # Generate with sovereignty markers
        response = generate(prompt, context + sources)

        # Save to vault
        session = self.vault.create_session(prompt, response)

        return f"{response}\n\n⟡⟦VERIFIED⟧"
```

---

## Testing Examples

All examples include test cases:

### Schema Validation Test

```bash
# Test that config files are valid
python -m validators.cli \
  --manifest examples/minimal_project_manifest.yaml \
  --policy examples/example_reflection_policy.yaml
```

**Expected output:**

```
✅ Schema validation passed
✅ Level 1 compliance checks passed
✅ Trust markers detected
```

### Edge Case: Invalid Example

**File:** `edgecase-invalid-artifact.md.json`

**Purpose:** Deliberately broken to test validator

```json
{
  "vault_id": "AMOS://EdgeCase/v1.0",
  "glyphsig": "⟡⟦EDGECASE⟧",
  "version": "1.0.0"
  // Missing required field: checksum_sha256
}
```

**Expected validation result:**

```
❌ Schema validation failed
Error: Missing required field 'checksum_sha256'
```

!!! warning "Edge Cases Are Intentional"
    Files prefixed with `edgecase-` are **meant to fail** validation. They prove the validator works correctly.

---

## Using Examples in Your Project

### 1. Copy the Template

```bash
# For Level 1
cp examples/minimal_project_manifest.yaml ./mirrorDNA_manifest.yaml
cp examples/example_reflection_policy.yaml ./reflection_policy.yaml

# For Level 2
cp examples/level2_project_manifest.yaml ./mirrorDNA_manifest.yaml
cp examples/example_reflection_policy.yaml ./reflection_policy.yaml
cp examples/example_continuity_profile.yaml ./continuity_profile.yaml

# For Level 3
cp examples/level3_project_manifest.yaml ./mirrorDNA_manifest.yaml
cp examples/level3_reflection_policy.yaml ./reflection_policy.yaml
cp examples/level3_continuity_profile.yaml ./continuity_profile.yaml
```

### 2. Customize

Edit the manifest with your project details:

```yaml
name: "YourProjectName"
version: "1.0.0"
description: "Your description"
maintainers:
  - name: "Your Name"
    email: "you@example.com"
repository: "https://github.com/you/project"
```

### 3. Validate

```bash
python -m validators.cli \
  --manifest mirrorDNA_manifest.yaml \
  --policy reflection_policy.yaml
```

### 4. Use in Code

See [Integration Guide](integration.md) for code examples.

---

## Contributing Examples

Want to add your own example?

See [Contributing Guide](contributing.md) for details.

**Requirements:**

- Must pass validation
- Include clear comments
- Follow naming conventions
- Add README entry

---

## Resources

- [Integration Guide](integration.md) - How to use these examples
- [Validators](validators.md) - How to test your configs
- [Compliance Levels](compliance-levels.md) - Requirements for each level
