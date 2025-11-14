# Compliance Levels

The MirrorDNA Standard defines three compliance levels, each building on the previous to create progressively more sophisticated reflective AI systems.

!!! abstract "Three Levels of Compliance"
    - **Level 1**: Basic Reflection - Foundational anti-hallucination without persistent state
    - **Level 2**: Continuity Aware - Persistent state with session lineage
    - **Level 3**: Vault-Backed Sovereign - Full sovereignty with user-owned storage

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

=== "Must Implement"

    #### ✅ Core Requirements

    **1. Cite or Silence (AHP)**

    - All factual claims include sources when available
    - Mark unknown information as `[Unknown]`
    - Never fabricate citations

    **2. Explicit Uncertainty Marking**

    - Use standard markers: `[Unknown]`, `[Speculation]`, `[Unverified]`
    - Document custom markers in reflection policy

    **3. Basic Session Tracking**

    - Each session has a unique identifier (UUID or timestamp-based)
    - Session metadata includes: start time, end time, identifier

    **4. At Least One Trust Marker**

    - Examples: checksum validation, source citation, verified content marker
    - Document which trust markers are implemented

    **5. Reflection Policy Declaration**

    - Provide `mirrorDNA_reflection_policy.yaml`
    - Declare uncertainty handling approach
    - See: `schema/reflection_policy.schema.json`

=== "Not Required"

    #### ❌ Optional for Level 1

    - Persistent state storage
    - Vault integration
    - Session lineage tracking (predecessor/successor)
    - Checksum validation of artifacts
    - Glyph signatures

### Validation

Run the validator CLI to check compliance:

```bash
python -m validators.cli --manifest manifest.yaml --policy reflection_policy.yaml
```

!!! success "Level 1 Validation"
    The validator will check that your project meets all Level 1 requirements. Fix any reported issues and re-run validation.

### Badge

Projects meeting Level 1 may display:

![MirrorDNA Level 1](https://raw.githubusercontent.com/MirrorDNA-Reflection-Protocol/MirrorDNA-Standard/main/badges/reflective_compliance_light.svg)

```markdown
![MirrorDNA Level 1](https://raw.githubusercontent.com/MirrorDNA-Reflection-Protocol/MirrorDNA-Standard/main/badges/reflective_compliance_light.svg)
```

!!! tip "Next Steps"
    Ready to add persistent state? Learn about [Level 2](#level-2-continuity-aware) compliance.

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

=== "Must Implement"

    #### ✅ Core Requirements (includes all Level 1 + additions)

    **1. Persistent State Storage**

    - State survives across sessions
    - Configuration specified in continuity profile
    - Storage types: file system, database, vault, or distributed

    **2. Session Lineage Tracking**

    - Each session has `predecessor` and `successor` links
    - Forms a verifiable chain
    - Lineage preserved in vault or storage

    **3. Continuity Profile**

    - Provide `mirrorDNA_continuity_profile.yaml`
    - Declare continuity mechanism (vault_backed, blockchain_anchored, etc.)
    - Configure state persistence settings
    - See: `schema/continuity_profile.schema.json`

    **4. Artifact Checksum Validation**

    - All canonical artifacts include SHA-256 checksums
    - Checksums are verifiable on demand
    - Modified artifacts marked as derivatives

    **5. Session Recovery**

    - System can recover state from previous session
    - Recovery process documented in continuity profile
    - Failed recovery clearly reported

    **6. Continuity Guarantees**

    Declare which guarantees are provided:

    - Identity preservation
    - State consistency
    - Lineage tracking
    - Anti-hallucination measures

=== "Documentation Required"

    #### 📄 Required Documentation

    - Continuity profile with complete configuration
    - Reflection policy with enhanced anti-hallucination measures
    - Recovery procedures

=== "Not Required"

    #### ❌ Optional for Level 2

    - Vault-backed storage (can use database or file system)
    - Sovereign identity (can be managed externally)
    - Glyph signatures
    - Blockchain anchoring

### Validation

Run validator CLI with continuity checks:

```bash
python -m validators.cli \
  --manifest manifest.yaml \
  --profile continuity_profile.yaml \
  --policy reflection_policy.yaml
```

!!! warning "Level 2 Validation Requirements"
    Level 2 validation checks:

    - Valid continuity profile
    - State persistence configuration
    - Lineage tracking verification

### Badge

Projects meeting Level 2 may display:

![MirrorDNA Level 2](https://raw.githubusercontent.com/MirrorDNA-Reflection-Protocol/MirrorDNA-Standard/main/badges/verified-reflective.svg)

```markdown
![MirrorDNA Level 2](https://raw.githubusercontent.com/MirrorDNA-Reflection-Protocol/MirrorDNA-Standard/main/badges/verified-reflective.svg)
```

!!! tip "Next Steps"
    Want full sovereignty with vault-backed storage? Learn about [Level 3](#level-3-vault-backed-sovereign).

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

=== "Must Implement"

    #### ✅ Core Requirements (includes all Level 1 & 2 + additions)

    **1. Vault Storage**

    - All continuity data stored in user-owned vault
    - Vault types: Obsidian, custom vault, distributed vault, or cloud vault
    - Vault path and configuration specified in continuity profile

    **2. Sovereign Identity**

    - User owns vault and vault_id
    - No hidden dependencies or lock-in
    - System cannot operate without user's vault
    - Formula: **Vault = System**

    **3. Full Lineage Tracking**

    - Every artifact has predecessor/successor
    - Lineage chains are complete and verifiable
    - Forks and branches explicitly marked
    - Lineage cannot be silently rewritten

    **4. Glyph Signatures**

    - Implements standard glyphs: `⟡⟦CONTINUITY⟧`, `⟡⟦VERIFIED⟧`, etc.
    - Documents custom glyphs in reflection policy
    - Glyphs carry semantic meaning across sessions

    **5. Comprehensive Reflection Policy**

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

    **6. Compliance Reporting**

    - System can generate compliance reports
    - Reports show:
        - Compliance level achieved
        - All requirements met
        - Trust markers in use
        - Continuity guarantees provided

    **7. Integrity Verification**

    - All artifacts checksummed
    - Checksums verifiable on demand
    - Tamper detection and reporting
    - Vault integrity checks

=== "Documentation Required"

    #### 📄 Required Documentation

    - Complete project manifest
    - Complete continuity profile with vault configuration
    - Complete reflection policy with all sections
    - Compliance report (auto-generated by validator)

=== "Optional Enhancements"

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

!!! warning "Level 3 Validation Requirements"
    Level 3 validation includes comprehensive checks:

    - Vault accessibility and structure
    - Full lineage verification
    - Glyph signature validation
    - Comprehensive policy compliance

### Badge

Projects meeting Level 3 may display:

![MirrorDNA Level 3 - Vault-Backed Sovereign](https://raw.githubusercontent.com/MirrorDNA-Reflection-Protocol/MirrorDNA-Standard/main/badges/verified-reflective.svg)

```markdown
![MirrorDNA Level 3 - Vault-Backed Sovereign](https://raw.githubusercontent.com/MirrorDNA-Reflection-Protocol/MirrorDNA-Standard/main/badges/verified-reflective.svg)
```

!!! success "Level 3 Achievement"
    Congratulations! Level 3 represents the highest current compliance standard, providing full sovereignty and comprehensive reflection protocols.

---

## Compliance Matrix

Quick reference showing which features are required at each level:

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

!!! info "Cumulative Requirements"
    Compliance levels are cumulative. Level 3 systems implement ALL requirements from Levels 1, 2, and 3.

---

## Upgrading Between Levels

### Level 1 → Level 2

=== "Migration Steps"

    1. Implement persistent state storage
    2. Add session lineage tracking (predecessor/successor)
    3. Create continuity profile
    4. Implement checksum validation for artifacts
    5. Add session recovery mechanism
    6. Run validator to verify Level 2 compliance

=== "Estimated Effort"

    **2-5 days** for typical application

    Complexity depends on:

    - Existing state management
    - Database/storage infrastructure
    - Team size and experience

### Level 2 → Level 3

=== "Migration Steps"

    1. Migrate storage to vault (Obsidian or custom)
    2. Implement vault_id and sovereign identity
    3. Add glyph signatures
    4. Enhance reflection policy to comprehensive level
    5. Implement compliance reporting
    6. Add integrity verification and tamper detection
    7. Run full validator with vault verification

=== "Estimated Effort"

    **1-2 weeks** for typical application

    Key challenges:

    - Vault integration and configuration
    - Glyph signature implementation
    - Comprehensive policy documentation
    - Integrity verification systems

---

## Future Levels

The MirrorDNA Standard reserves the right to introduce additional levels in future versions:

!!! note "Potential Level 4: Distributed Sovereign (v2.0+)"
    - Multi-vault synchronization
    - Distributed consensus for lineage
    - Blockchain-anchored immutability
    - Federation protocols

!!! note "Potential Level 5: Ecosystem Participant (v2.0+)"
    - Integration with broader MirrorDNA ecosystem
    - Cross-project lineage
    - Shared glyph kernel
    - Consortium membership

**These are not yet specified** and are subject to future standardization.

---

## Compliance Testing

### Automated Validation

Use the validator CLI to check compliance at any level:

=== "Level 1"

    ```bash
    # Basic check (Level 1)
    python -m validators.cli --manifest manifest.yaml
    ```

=== "Level 2"

    ```bash
    # Full check (Level 2+)
    python -m validators.cli \
      --manifest manifest.yaml \
      --profile continuity_profile.yaml \
      --policy reflection_policy.yaml
    ```

=== "Level 3"

    ```bash
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

!!! tip "Best Practices"
    Combine automated validation with manual review for critical systems. The validator catches common issues, but human review ensures semantic correctness.

### Certification (Future)

Future versions may introduce formal certification:

- Third-party audit
- Consortium review
- Public registry of certified systems

---

## Related Documentation

- [Glossary](glossary.md) - Definitions of key terms
- [Roadmap](roadmap.md) - Future compliance features
- [MirrorDNA Standard](https://github.com/MirrorDNA-Reflection-Protocol/MirrorDNA-Standard/blob/main/spec/mirrorDNA-standard-v1.0.md) - Full specification

---

⟡⟦COMPLIANCE⟧ · ⟡⟦LEVELS⟧ · ⟡⟦SEALED⟧
