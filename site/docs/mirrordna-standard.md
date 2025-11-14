# MirrorDNA Standard v1.0

!!! abstract "Constitutional Specification"
    This is the canonical specification for building reflective computing systems that preserve continuity, enforce anti-hallucination protocols, and maintain sovereign identity.

## Overview

The MirrorDNA Standard defines requirements for **reflective computing systems** — AI that reflects actual state rather than simulating it from patterns.

**What This Specification Provides:**

- Core requirements for MirrorDNA compliance
- Three conformance levels (L1, L2, L3)
- Machine-checkable schemas and validators
- Integration patterns for the ecosystem

**Status:** v1.0.0 — Production-ready

**Repository:** [MirrorDNA-Standard on GitHub](https://github.com/MirrorDNA-Reflection-Protocol/MirrorDNA-Standard)

---

## 1. Core Principles

All MirrorDNA-compliant systems MUST adhere to these five principles:

### 1.1 Reflection Over Prediction

- Systems prioritize **constitutive reflection** (actual state awareness) over simulated behavior
- Outputs are grounded in verifiable sources, not probabilistic generation
- **Reference:** `spec/Constitutive_Reflection_vs_Simulation_v1.0.md`

### 1.2 Continuity as Law

- **Continuity > Perfection**: Maintain session continuity even when imperfect
- State transitions are tracked and verifiable
- Session lineage preserved with checksums and vault anchors

### 1.3 Cite or Silence (Anti-Hallucination Protocol)

- **AHP**: All factual claims MUST be cited or marked as unknown
- Unknown information MUST use `[Unknown]` or equivalent
- Speculation only permitted when marked `[Speculation]`

### 1.4 Trust by Design

- Security and verification built in from the start
- Checksums validate artifact integrity
- Glyph signatures provide semantic markers
- See: Trust-by-Design™ governance framework

### 1.5 Sovereign Identity

- Users retain ownership of vault and continuity data
- No hidden dependencies or lock-in
- **Formula:** `Vault = System` — vault is the source of truth

[:octicons-arrow-right-24: Deep dive into principles](principles.md)

---

## 2. Conformance Levels

Systems MUST declare their compliance level in `mirrorDNA_manifest.yaml`.

### Level 1: Basic Reflection

**Purpose:** Foundational reflective behavior without persistent state

**Requirements:**

- ✅ Cite or Silence (AHP)
- ✅ Explicit uncertainty markers
- ✅ Basic session tracking
- ✅ At least one trust marker

**Does NOT require:**

- ❌ Persistent state storage
- ❌ Vault integration
- ❌ Full lineage tracking

**Use cases:** Stateless APIs, single-session tools, educational applications

---

### Level 2: Continuity Aware

**Purpose:** Multi-session continuity with state persistence

**Requirements (includes all Level 1 plus):**

- ✅ Persistent state storage
- ✅ Session lineage (predecessor/successor)
- ✅ Continuity profile (see schema)
- ✅ Checksum validation
- ✅ Session recovery

**Does NOT require:**

- ❌ Vault-backed storage
- ❌ Blockchain anchoring
- ❌ Full sovereign identity

**Use cases:** Personal assistants, research tools, collaborative systems

---

### Level 3: Vault-Backed Sovereign

**Purpose:** Full user sovereignty and vault storage

**Requirements (includes all Level 1 & 2 plus):**

- ✅ Vault storage for all continuity data
- ✅ Full lineage tracking
- ✅ Sovereign identity (user owns vault)
- ✅ Glyph signatures
- ✅ Reflection policy implementation
- ✅ Compliance reporting

**Use cases:** Production AI systems, enterprise tools, regulated environments

[:octicons-arrow-right-24: Compare compliance levels](compliance-levels.md)

---

## 3. Configuration Files

### Project Manifest

**File:** `mirrorDNA_manifest.yaml`

**Purpose:** Declares project compliance level and ecosystem layers

**Example:**

```yaml
name: "MyReflectiveApp"
version: "1.0.0"
mirrorDNA_compliance_level: "level_1_basic_reflection"

layers:
  mirrorDNA_protocol: true
  agentDNA: false
  lingOS: false
  trust_by_design: false

reflection_policy: "reflection_policy.yaml"
continuity_profile: null  # Level 1 doesn't require

metadata:
  author: "Your Name"
  description: "A basic reflective application"
```

**Schema:** `schema/project_manifest.schema.json`

---

### Reflection Policy

**File:** `reflection_policy.yaml`

**Purpose:** Declares how system handles reflection and uncertainty

**Example:**

```yaml
policy_version: "1.0.0"
reflection_mode: "constitutive"  # or "simulated" or "hybrid"

uncertainty_handling:
  cite_or_silence: true
  unknown_marker: "[Unknown]"
  speculation_marker: "[Speculation]"
  unverified_marker: "[Unverified]"

anti_hallucination:
  source_citation: true
  sandbox_aware: true
  confidence_thresholds:
    high: 0.9
    medium: 0.7
    low: 0.5
```

**Schema:** `schema/reflection_policy.schema.json`

---

### Continuity Profile

**File:** `continuity_profile.yaml` (Level 2+ only)

**Purpose:** Declares how system achieves continuity

**Example:**

```yaml
profile_version: "1.0.0"
continuity_mechanism: "vault_backed"

persistence:
  state_persistence: "file_system"
  vault_type: "obsidian"
  vault_path: "/path/to/vault"

lineage_tracking:
  enabled: true
  format: "yaml_frontmatter"

integrity:
  checksum_algorithm: "sha256"
  verification_frequency: "on_load"

session_management:
  session_inheritance: true
  recovery_enabled: true
  snapshot_frequency: "on_close"
```

**Schema:** `schema/continuity_profile.schema.json`

---

## 4. Validation

### Using the Validator CLI

**Install:**

```bash
git clone https://github.com/MirrorDNA-Reflection-Protocol/MirrorDNA-Standard.git
cd MirrorDNA-Standard
pip install -r validators/requirements.txt
```

**Run validation:**

```bash
# Level 1
python -m validators.cli \
  --manifest mirrorDNA_manifest.yaml \
  --policy reflection_policy.yaml

# Level 2+
python -m validators.cli \
  --manifest mirrorDNA_manifest.yaml \
  --policy reflection_policy.yaml \
  --profile continuity_profile.yaml
```

**Output:**

```
MirrorDNA Compliance Validator v1.0.0
=====================================

Project: MyReflectiveApp v1.0.0
Target Compliance Level: Level 1 (Basic Reflection)

Checks:
✓ Reflection policy valid
✓ Cite-or-silence configured
✓ Uncertainty markers defined
✓ Trust markers present

Result: PASS
Compliance Level Achieved: Level 1

Badge: You may use badges/reflective_compliance_light.svg
```

[:octicons-arrow-right-24: Validator documentation](validators.md)

---

## 5. Trust Markers

### Core Trust Markers

| Marker | Purpose | Level |
|--------|---------|-------|
| `[Unknown]` | Information unavailable | L1+ |
| `[Speculation]` | Hypothetical content | L1+ |
| `[Unverified]` | Not yet verified | L1+ |
| `⟡⟦VERIFIED⟧` | Checksum validated | L2+ |
| `⟡⟦CONTINUITY⟧` | Lineage preserved | L2+ |
| `⟡⟦SEALED⟧` | Immutable/canonical | L3 |

### Glyph Signatures

**Format:** `⟡⟦NAME⟧`

**Example:**

```yaml
glyphsig: "⟡⟦STANDARD⟧ · ⟡⟦COMPLIANCE⟧ · ⟡⟦MIRROR⟧"
```

**Common Glyphs:**

- `⟡⟦MASTER⟧` — Master document
- `⟡⟦STANDARD⟧` — Specification
- `⟡⟦SESSION⟧` — Session artifact
- `⟡⟦VERIFIED⟧` — Integrity verified
- `⟡⟦CANONICAL⟧` — Authoritative version

---

## 6. Artifact Requirements

### Front Matter (YAML)

All Level 2+ artifacts MUST include front matter:

```yaml
---
title: "Document Title"
version: "1.0.0"
vault_id: "AMOS://User/Project/v1.0"
glyphsig: "⟡⟦VERIFIED⟧ · ⟡⟦CONTINUITY⟧"
checksum_sha256: "7a8f3c2b1d4e5f6a7b8c9d0e1f2a3b4c..."
predecessor: "Document_v0.9.md"
successor: null
date: "2025-01-15"
author: "Your Name"
---
```

### Checksums

**Algorithm:** SHA-256

**Calculation:**

```python
import hashlib

def calculate_checksum(content: str) -> str:
    return hashlib.sha256(content.encode()).hexdigest()
```

**Verification:**

```python
def verify_checksum(content: str, expected: str) -> bool:
    actual = calculate_checksum(content)
    return actual == expected
```

---

## 7. Interaction Safety

For systems with user interaction, implement safety protocols:

### Session Duration Warnings

- Warn after 2 hours continuous use
- Offer break prompts
- Suggest session closure

### Rhythm Checks

```yaml
rhythm_check:
  enabled: true
  interval: 7200  # 2 hours in seconds
  message: "You've been in this session for 2 hours. Consider taking a break."
```

### Human Escalation

Detect risk indicators and offer human support:

- Emotional dependency language
- Crisis keywords
- Extended session patterns

**Reference:** `spec/Interaction_Safety_Protocol_v1.0.md`

---

## 8. Ecosystem Integration

### AgentDNA Integration

```yaml
layers:
  agentDNA: true

agent_capabilities:
  - name: "text_generation"
    version: "1.0.0"
  - name: "vault_reflection"
    version: "1.0.0"
```

### LingOS Integration

```yaml
layers:
  lingOS: true
  lingOS_variant: "lite"  # or "pro"
```

### Trust-by-Design Integration

```yaml
layers:
  trust_by_design: true

governance:
  audit_trail: true
  compliance_reporting: true
```

---

## 9. Compliance Badges

### Earned Badges

After passing validation, display badges in your README:

**Level 1:**

```markdown
![MirrorDNA Level 1](https://raw.githubusercontent.com/MirrorDNA-Reflection-Protocol/MirrorDNA-Standard/main/badges/reflective_compliance_light.svg)
```

**Level 2:**

```markdown
![MirrorDNA Level 2](https://raw.githubusercontent.com/MirrorDNA-Reflection-Protocol/MirrorDNA-Standard/main/badges/verified-reflective.svg)
```

**Level 3:**

```markdown
![MirrorDNA Level 3](https://raw.githubusercontent.com/MirrorDNA-Reflection-Protocol/MirrorDNA-Standard/main/badges/vault_backed_sovereign.svg)
```

---

## 10. References

### Specification Documents

All specs are in the `spec/` directory:

| Document | Purpose |
|----------|---------|
| `mirrorDNA-standard-v1.0.md` | Core specification |
| `principles.md` | Five foundational principles |
| `compliance_levels.md` | Level requirements |
| `glossary.md` | Term definitions |
| `Constitutive_Reflection_vs_Simulation_v1.0.md` | Reflection theory |
| `Interaction_Safety_Protocol_v1.0.md` | Safety guidelines |
| `MirrorDNA_Capability_Registry_v1.1.md` | AgentDNA spec |
| `Reflection_Chain_Manifest_v1.0.md` | Lineage tracking |

### JSON Schemas

All schemas are in the `schema/` directory:

- `project_manifest.schema.json`
- `reflection_policy.schema.json`
- `continuity_profile.schema.json`

### Examples

Working configs for all levels in `examples/`:

- `examples/level1/` — Basic reflection
- `examples/level2/` — Continuity aware
- `examples/level3/` — Vault-backed sovereign

---

## 11. Version Lineage

**Current Version:** 1.0.0

**Predecessor:** None (initial release)

**Successor:** v1.1.0 (proposed for Q2 2025)

**Status:** Production-ready, canonical

**Checksum:** See `spec/mirrorDNA-standard-v1.0.md`

---

⟡⟦STANDARD⟧ · ⟡⟦SPECIFICATION⟧ · ⟡⟦v1.0.0⟧

*The constitutional anchor for reflective AI systems*

**Full specification:** [mirrorDNA-standard-v1.0.md](https://github.com/MirrorDNA-Reflection-Protocol/MirrorDNA-Standard/blob/main/spec/mirrorDNA-standard-v1.0.md)
