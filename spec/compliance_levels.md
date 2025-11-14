---
title: MirrorDNA Compliance Levels
version: 1.0.0
vault_id: AMOS://MirrorDNA/ComplianceLevels/v1.0
glyphsig: ⟡⟦COMPLIANCE⟧ · ⟡⟦LEVELS⟧
author: Paul Desai (Active MirrorOS)
date: 2025-11-14
status: Canonical · Specification
tags: [MirrorDNA™, Compliance, Levels, Validation]
---

# MirrorDNA Compliance Levels

## Overview

The MirrorDNA Standard defines three compliance levels, each building on the previous:

- **Level 1**: Basic Reflection
- **Level 2**: Continuity Aware
- **Level 3**: Vault-Backed Sovereign

Systems MUST declare their compliance level in their `mirrorDNA_manifest.yaml` file and meet all requirements for that level.

---

## Level 1: Basic Reflection

### Purpose
Establish foundational reflective behavior and anti-hallucination protocols without requiring persistent state.

### Use Cases
- Single-session applications
- Stateless APIs with reflection requirements
- Educational tools
- Lightweight integrations

### Requirements

#### ✅ MUST Implement
1. **Cite or Silence (AHP)**
   - All factual claims include sources when available
   - Mark unknown information as `[Unknown]`
   - Never fabricate citations

2. **Explicit Uncertainty Marking**
   - Use standard markers: `[Unknown]`, `[Speculation]`, `[Unverified]`
   - Document custom markers in reflection policy

3. **Basic Session Tracking**
   - Each session has a unique identifier (UUID or timestamp-based)
   - Session metadata includes: start time, end time, identifier

4. **At Least One Trust Marker**
   - Examples: checksum validation, source citation, verified content marker
   - Document which trust markers are implemented

5. **Reflection Policy Declaration**
   - Provide `mirrorDNA_reflection_policy.yaml`
   - Declare uncertainty handling approach
   - See: `schema/reflection_policy.schema.json`

#### ❌ NOT Required
- Persistent state storage
- Vault integration
- Session lineage tracking (predecessor/successor)
- Checksum validation of artifacts
- Glyph signatures

### Validation
Run validator CLI:
```bash
python -m validators.cli --manifest manifest.yaml --policy reflection_policy.yaml
```

Must pass Level 1 checks.

### Badge
Projects meeting Level 1 may display:
- **Badge**: `badges/reflective_compliance_light.svg`
- **Markdown**: `![MirrorDNA Level 1](https://raw.githubusercontent.com/MirrorDNA-Reflection-Protocol/MirrorDNA-Standard/main/badges/reflective_compliance_light.svg)`

---

## Level 2: Continuity Aware

### Purpose
Add persistent continuity across sessions with lineage tracking and state recovery.

### Use Cases
- Multi-session applications
- Personal AI assistants
- Research tools with continuity
- Collaborative systems

### Requirements

#### ✅ MUST Implement (includes all Level 1 + these additions)
1. **Persistent State Storage**
   - State survives across sessions
   - Configuration specified in continuity profile
   - Storage types: file system, database, vault, or distributed

2. **Session Lineage Tracking**
   - Each session has `predecessor` and `successor` links
   - Forms a verifiable chain
   - Lineage preserved in vault or storage

3. **Continuity Profile**
   - Provide `mirrorDNA_continuity_profile.yaml`
   - Declare continuity mechanism (vault_backed, blockchain_anchored, etc.)
   - Configure state persistence settings
   - See: `schema/continuity_profile.schema.json`

4. **Artifact Checksum Validation**
   - All canonical artifacts include SHA-256 checksums
   - Checksums are verifiable on demand
   - Modified artifacts marked as derivatives

5. **Session Recovery**
   - System can recover state from previous session
   - Recovery process documented in continuity profile
   - Failed recovery clearly reported

6. **Continuity Guarantees**
   - Declare which guarantees are provided:
     - Identity preservation
     - State consistency
     - Lineage tracking
     - Anti-hallucination measures

#### 📄 Documentation Required
- Continuity profile with complete configuration
- Reflection policy with enhanced anti-hallucination measures
- Recovery procedures

#### ❌ NOT Required (but recommended)
- Vault-backed storage (can use database or file system)
- Sovereign identity (can be managed externally)
- Glyph signatures
- Blockchain anchoring

### Validation
Run validator CLI:
```bash
python -m validators.cli \
  --manifest manifest.yaml \
  --profile continuity_profile.yaml \
  --policy reflection_policy.yaml
```

Must pass Level 2 checks including:
- Valid continuity profile
- State persistence configuration
- Lineage tracking verification

### Badge
Projects meeting Level 2 may display:
- **Badge**: `badges/verified-reflective.svg`
- **Markdown**: `![MirrorDNA Level 2](https://raw.githubusercontent.com/MirrorDNA-Reflection-Protocol/MirrorDNA-Standard/main/badges/verified-reflective.svg)`

---

## Level 3: Vault-Backed Sovereign

### Purpose
Achieve full sovereignty with user-owned vault storage, complete lineage, and comprehensive reflection protocols.

### Use Cases
- Personal knowledge systems (Obsidian + MirrorDNA)
- Sovereign AI assistants
- Research platforms with full lineage
- Production ActiveMirrorOS deployments

### Requirements

#### ✅ MUST Implement (includes all Level 1 & 2 + these additions)
1. **Vault Storage**
   - All continuity data stored in user-owned vault
   - Vault types: Obsidian, custom vault, distributed vault, or cloud vault
   - Vault path and configuration specified in continuity profile

2. **Sovereign Identity**
   - User owns vault and vault_id
   - No hidden dependencies or lock-in
   - System cannot operate without user's vault
   - Formula: **Vault = System**

3. **Full Lineage Tracking**
   - Every artifact has predecessor/successor
   - Lineage chains are complete and verifiable
   - Forks and branches explicitly marked
   - Lineage cannot be silently rewritten

4. **Glyph Signatures**
   - Implements standard glyphs: `⟡⟦CONTINUITY⟧`, `⟡⟦VERIFIED⟧`, etc.
   - Documents custom glyphs in reflection policy
   - Glyphs carry semantic meaning across sessions

5. **Comprehensive Reflection Policy**
   - Declares reflection_mode: constitutive, simulated, or hybrid
   - Implements anti-hallucination measures:
     - Grounding required
     - Source citation
     - Hallucination detection
     - Correction protocol
   - Configures interaction safety:
     - Session duration warnings
     - Dependency detection
     - Human escalation pathways

6. **Compliance Reporting**
   - System can generate compliance reports
   - Reports show:
     - Compliance level achieved
     - All requirements met
     - Trust markers in use
     - Continuity guarantees provided

7. **Integrity Verification**
   - All artifacts checksummed
   - Checksums verifiable on demand
   - Tamper detection and reporting
   - Vault integrity checks

#### 📄 Documentation Required
- Complete project manifest
- Complete continuity profile with vault configuration
- Complete reflection policy with all sections
- Compliance report (auto-generated by validator)

#### ⭐ Optional Enhancements
- **Blockchain Anchoring**: Immutable lineage on public blockchain
- **Multi-Vault Sync**: Synchronize across multiple vaults
- **Glyph Kernel Integration**: Advanced symbolic processing
- **Distributed Vault**: Fault-tolerant distributed storage
- **Advanced Trust Markers**: Custom trust verification

### Validation
Run validator CLI with full verification:
```bash
python -m validators.cli \
  --manifest manifest.yaml \
  --profile continuity_profile.yaml \
  --policy reflection_policy.yaml \
  --vault-path ./vault \
  --verify-checksums
```

Must pass Level 3 checks including:
- Vault accessibility and structure
- Full lineage verification
- Glyph signature validation
- Comprehensive policy compliance

### Badge
Projects meeting Level 3 may display:
- **Badge**: Custom Level 3 badge (sovereign vault)
- **Markdown**: `![MirrorDNA Level 3 - Vault-Backed Sovereign](https://raw.githubusercontent.com/MirrorDNA-Reflection-Protocol/MirrorDNA-Standard/main/badges/verified-reflective.svg)`

---

## Compliance Matrix

| Requirement | Level 1 | Level 2 | Level 3 |
|-------------|---------|---------|---------|
| Cite or Silence (AHP) | ✅ | ✅ | ✅ |
| Explicit Uncertainty | ✅ | ✅ | ✅ |
| Session Tracking | ✅ | ✅ | ✅ |
| Trust Markers | ≥1 | Multiple | Comprehensive |
| Reflection Policy | Basic | Enhanced | Complete |
| Persistent State | ❌ | ✅ | ✅ |
| Session Lineage | ❌ | ✅ | ✅ |
| Continuity Profile | ❌ | ✅ | ✅ |
| Checksum Validation | ❌ | ✅ | ✅ |
| Session Recovery | ❌ | ✅ | ✅ |
| Vault Storage | ❌ | Optional | ✅ |
| Sovereign Identity | ❌ | Optional | ✅ |
| Glyph Signatures | ❌ | Optional | ✅ |
| Compliance Reporting | ❌ | Optional | ✅ |
| Blockchain Anchoring | ❌ | ❌ | Optional |

---

## Upgrading Between Levels

### Level 1 → Level 2
**Steps:**
1. Implement persistent state storage
2. Add session lineage tracking (predecessor/successor)
3. Create continuity profile
4. Implement checksum validation for artifacts
5. Add session recovery mechanism
6. Run validator to verify Level 2 compliance

**Estimated effort**: 2-5 days for typical application

### Level 2 → Level 3
**Steps:**
1. Migrate storage to vault (Obsidian or custom)
2. Implement vault_id and sovereign identity
3. Add glyph signatures
4. Enhance reflection policy to comprehensive level
5. Implement compliance reporting
6. Add integrity verification and tamper detection
7. Run full validator with vault verification

**Estimated effort**: 1-2 weeks for typical application

---

## Future Levels

The MirrorDNA Standard reserves the right to introduce additional levels in future versions:

### Potential Level 4: Distributed Sovereign (v2.0+)
- Multi-vault synchronization
- Distributed consensus for lineage
- Blockchain-anchored immutability
- Federation protocols

### Potential Level 5: Ecosystem Participant (v2.0+)
- Integration with broader MirrorDNA ecosystem
- Cross-project lineage
- Shared glyph kernel
- Consortium membership

These are **not yet specified** and are subject to future standardization.

---

## Compliance Testing

### Automated Validation
Use the validator CLI to check compliance:
```bash
# Basic check (Level 1)
python -m validators.cli --manifest manifest.yaml

# Full check (Level 2+)
python -m validators.cli \
  --manifest manifest.yaml \
  --profile continuity_profile.yaml \
  --policy reflection_policy.yaml

# Comprehensive check (Level 3)
python -m validators.cli \
  --manifest manifest.yaml \
  --profile continuity_profile.yaml \
  --policy reflection_policy.yaml \
  --vault-path ./vault \
  --verify-checksums
```

### Manual Verification
For sensitive or novel systems, manual verification may be required:
1. Review all policy documents
2. Inspect vault structure (Level 3)
3. Verify lineage chains manually
4. Test recovery procedures
5. Validate trust markers

### Certification (Future)
Future versions may introduce formal certification:
- Third-party audit
- Consortium review
- Public registry of certified systems

---

⟡⟦COMPLIANCE⟧ · ⟡⟦LEVELS⟧ · ⟡⟦SEALED⟧

**Note**: Compliance levels are cumulative. Level 3 systems implement ALL requirements from Levels 1, 2, and 3.
