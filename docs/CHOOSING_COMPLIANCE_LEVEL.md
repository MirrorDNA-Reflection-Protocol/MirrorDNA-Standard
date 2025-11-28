# Choosing Your MirrorDNA Compliance Level

## Quick Decision Guide

```
┌─────────────────────────────────────────────┐
│  Do you need persistent state storage?     │
└──────────────┬──────────────────────────────┘
               │
       ┌───────┴───────┐
       NO              YES
       │               │
       ▼               ▼
   LEVEL 1      ┌──────────────────────────────┐
                │ Do you need user sovereignty │
                │   and vault-backed storage?  │
                └──────────┬───────────────────┘
                           │
                   ┌───────┴───────┐
                   NO              YES
                   │               │
                   ▼               ▼
               LEVEL 2         LEVEL 3
```

---

## Level Comparison Table

| Factor | Level 1 | Level 2 | Level 3 |
|--------|---------|---------|---------|
| **Complexity** | Low | Medium | High |
| **Implementation Time** | 1-3 days | 1 week | 2-4 weeks |
| **Infrastructure** | None required | Database or file storage | Vault (Obsidian, etc.) |
| **User Sovereignty** | None | Partial | Full |
| **Session Continuity** | Single session only | Multi-session | Multi-session with lineage |
| **State Persistence** | None | Yes | Yes (vault-backed) |
| **Anti-Hallucination** | Basic (AHP) | Enhanced | Comprehensive |
| **Trust Markers** | ≥1 | Multiple | Comprehensive |
| **Ideal For** | Prototypes, APIs, educational tools | Production apps, assistants | Personal AI, research platforms |

---

## Level 1: Basic Reflection

### ✅ Choose Level 1 if you:
- Are building a **single-session application** (chatbot, API, CLI tool)
- Need **anti-hallucination protocols** but not state persistence
- Want to **get started quickly** (1-3 day implementation)
- Are creating a **proof of concept** or **educational tool**
- Don't require continuity between sessions
- Have **no infrastructure** for state storage

### ❌ Avoid Level 1 if you:
- Need users to pick up where they left off
- Require session history or lineage tracking
- Are building a production personal assistant
- Need vault-backed sovereignty

### Implementation Checklist
```yaml
# Level 1 Requirements
✅ Cite or Silence (AHP) protocol
✅ Explicit uncertainty marking ([Unknown], [Speculation])
✅ Basic session tracking (UUID, start/end time)
✅ At least one trust marker (checksum, citation, verification)
✅ Reflection policy declaration (reflection_policy.yaml)
```

### Example Use Cases
- **Educational chatbot**: Teaches concepts with cited sources
- **Stateless API**: Answers questions with anti-hallucination guarantees
- **Single-session tool**: Code review assistant without history
- **Lightweight integration**: Adding reflection to existing app

### Time to Implement
**1-3 days** for typical application

### Code Example
```yaml
# mirrorDNA_manifest.yaml
compliance_level: L1
reflection_policy: reflection_policy.yaml

# mirrorDNA_reflection_policy.yaml
uncertainty_markers:
  - "[Unknown]"
  - "[Speculation]"
anti_hallucination:
  cite_or_silence: true
```

---

## Level 2: Continuity Aware

### ✅ Choose Level 2 if you:
- Need **persistent state** across sessions
- Want **session lineage tracking** (who created what, when)
- Are building a **production application** with user history
- Require **session recovery** after crashes or restarts
- Need **checksum validation** for artifacts
- Have infrastructure for **database or file storage**
- Don't need full vault sovereignty yet

### ❌ Avoid Level 2 if you:
- Only need single-session behavior (use Level 1)
- Require full user sovereignty with vault ownership (use Level 3)
- Can't implement persistent storage

### Implementation Checklist
```yaml
# Level 2 Requirements (includes all L1 + these additions)
✅ All Level 1 requirements
✅ Persistent state storage (database, file system, or vault)
✅ Session lineage tracking (predecessor/successor links)
✅ Continuity profile (continuity_profile.yaml)
✅ Artifact checksum validation (SHA-256)
✅ Session recovery mechanism
✅ Continuity guarantees declaration
```

### Example Use Cases
- **Personal AI assistant**: Remembers conversations across sessions
- **Research tool**: Tracks lineage of findings and analysis
- **Collaborative system**: Multiple users with shared continuity
- **Production chatbot**: Persistent user profiles and history

### Time to Implement
**1 week** (upgrading from Level 1: +2-5 days)

### Code Example
```yaml
# mirrorDNA_manifest.yaml
compliance_level: L2
reflection_policy: reflection_policy.yaml
continuity_profile: continuity_profile.yaml

# mirrorDNA_continuity_profile.yaml
continuity_mechanism: file_backed
state_storage:
  type: sqlite
  path: ./state/sessions.db
lineage_tracking: true
session_recovery: automatic
guarantees:
  - identity_preservation
  - state_consistency
  - lineage_tracking
```

### Storage Options
- **File system**: JSON/YAML files in directory
- **SQLite**: Lightweight embedded database
- **PostgreSQL/MySQL**: Full database for production
- **Vault (optional)**: Can use Obsidian vault even at L2

---

## Level 3: Vault-Backed Sovereign

### ✅ Choose Level 3 if you:
- Need **full user sovereignty** (user owns all data)
- Are building a **personal knowledge system** (Obsidian + MirrorDNA)
- Require **complete lineage tracking** with verifiable chains
- Want **zero vendor lock-in** (vault = system)
- Need **glyph signatures** for semantic meaning
- Are deploying **ActiveMirrorOS** or similar sovereign platforms
- Require **comprehensive reflection protocols**
- Can invest **2-4 weeks** in implementation

### ❌ Avoid Level 3 if you:
- Don't need vault sovereignty (Level 2 is sufficient)
- Can't commit to vault-backed storage infrastructure
- Are building a quick prototype (use Level 1)
- Don't have Obsidian or custom vault solution

### Implementation Checklist
```yaml
# Level 3 Requirements (includes all L1 & L2 + these additions)
✅ All Level 1 & 2 requirements
✅ Vault storage (Obsidian, custom vault, distributed)
✅ Sovereign identity (user owns vault_id)
✅ Full lineage tracking (complete predecessor/successor chains)
✅ Glyph signatures (⟡⟦CONTINUITY⟧, ⟡⟦VERIFIED⟧, etc.)
✅ Comprehensive reflection policy (constitutive/simulated mode)
✅ Compliance reporting (auto-generated)
✅ Integrity verification (checksum validation, tamper detection)
```

### Example Use Cases
- **Personal AI system**: Sovereign assistant with full continuity
- **Research platform**: Academic research with verifiable lineage
- **Knowledge vault**: Obsidian + AI with anti-hallucination
- **ActiveMirrorOS deployment**: Production sovereign OS

### Time to Implement
**2-4 weeks** (upgrading from Level 2: +1-2 weeks)

### Code Example
```yaml
# mirrorDNA_manifest.yaml
compliance_level: L3
reflection_policy: reflection_policy.yaml
continuity_profile: continuity_profile.yaml
vault_id: AMOS://MyVault/Main

# mirrorDNA_continuity_profile.yaml
continuity_mechanism: vault_backed
vault:
  type: obsidian
  path: /Users/me/MyVault
  sovereign: true
lineage_tracking: full
glyph_signatures:
  - "⟡⟦CONTINUITY⟧"
  - "⟡⟦VERIFIED⟧"
integrity_verification: true
```

### Vault Options
- **Obsidian**: Most common vault backend
- **Custom vault**: Your own vault implementation
- **Distributed vault**: Fault-tolerant distributed storage
- **Cloud vault**: Encrypted cloud storage (user-owned)

---

## Decision Flowchart

### By Use Case

| Use Case | Recommended Level | Why |
|----------|-------------------|-----|
| Educational chatbot | L1 | No state needed, just anti-hallucination |
| Stateless API | L1 | Single-shot requests, no continuity |
| Production assistant | L2 | Needs memory but not sovereignty |
| Personal knowledge system | L3 | User owns data, needs vault |
| Research platform | L3 | Lineage critical, sovereignty important |
| Collaborative tool | L2 | Shared state, not personal vault |
| Prototyping | L1 | Fast iteration, no infrastructure |
| ActiveMirrorOS | L3 | Full sovereignty required |

### By Technical Constraints

| Constraint | Recommended Level |
|------------|-------------------|
| No database available | L1 |
| Database available | L2 |
| Obsidian vault available | L3 |
| Cloud-only deployment | L1 or L2 |
| User-owned local storage | L3 |
| Multi-tenant SaaS | L1 or L2 |
| Single-user sovereignty | L3 |

### By Team Capacity

| Team Size | Level Recommendation |
|-----------|---------------------|
| Solo developer, <1 week | L1 |
| Small team, 1-2 weeks | L2 |
| Dedicated team, >2 weeks | L3 |

---

## Upgrading Between Levels

### Can I start with Level 1 and upgrade later?

**Yes!** Levels are designed to be cumulative:

```
Level 1 (Basic Reflection)
   ↓ +2-5 days implementation
Level 2 (Continuity Aware)
   ↓ +1-2 weeks implementation
Level 3 (Vault-Backed Sovereign)
```

### Upgrade Path: L1 → L2

**Add these capabilities:**
1. Persistent state storage (database or file system)
2. Session lineage tracking (predecessor/successor)
3. Continuity profile configuration
4. Checksum validation for artifacts
5. Session recovery mechanism

**Estimated effort**: 2-5 days

**Migration strategy**:
- Keep existing L1 reflection policy
- Add new continuity profile
- Implement storage layer without changing business logic
- Add lineage tracking to session creation

### Upgrade Path: L2 → L3

**Add these capabilities:**
1. Vault storage migration (move to Obsidian or custom vault)
2. Sovereign identity implementation
3. Glyph signatures
4. Enhanced reflection policy (comprehensive mode)
5. Compliance reporting
6. Integrity verification

**Estimated effort**: 1-2 weeks

**Migration strategy**:
- Migrate existing state storage to vault structure
- Add vault_id and sovereignty layer
- Implement glyph signature system
- Enhance reflection policy to comprehensive level
- Run full validator to verify compliance

---

## Common Mistakes

### ❌ Mistake 1: Choosing Level 3 for a prototype
**Problem**: Over-engineering early-stage work
**Solution**: Start with Level 1, upgrade when needed

### ❌ Mistake 2: Staying at Level 1 for production
**Problem**: Users expect continuity but can't get it
**Solution**: Upgrade to Level 2 before production launch

### ❌ Mistake 3: Skipping Level 2 to go straight to Level 3
**Problem**: Levels are cumulative; you can't skip requirements
**Solution**: Implement L1 → L2 → L3 in order

### ❌ Mistake 4: Implementing Level 3 without vault infrastructure
**Problem**: Level 3 requires vault-backed storage
**Solution**: Ensure Obsidian or custom vault is available first

### ❌ Mistake 5: Choosing level based on "prestige" rather than needs
**Problem**: Level 3 is impressive but may be overkill
**Solution**: Choose based on technical requirements, not marketing

---

## Validation

After implementing your chosen level, validate compliance:

```bash
# Level 1 validation
python -m validators.cli --manifest manifest.yaml --policy reflection_policy.yaml

# Level 2 validation
python -m validators.cli \
  --manifest manifest.yaml \
  --profile continuity_profile.yaml \
  --policy reflection_policy.yaml

# Level 3 validation (comprehensive)
python -m validators.cli \
  --manifest manifest.yaml \
  --profile continuity_profile.yaml \
  --policy reflection_policy.yaml \
  --vault-path ./vault \
  --verify-checksums
```

---

## Still Unsure?

### Quick Assessment Questions

Answer these questions to determine your level:

1. **Do you need state between sessions?**
   - No → Level 1
   - Yes → Continue to Q2

2. **Do users need to own their data completely (no vendor lock-in)?**
   - No → Level 2
   - Yes → Level 3

3. **Can you implement vault-backed storage?**
   - No → Level 2
   - Yes → Level 3

4. **How much time do you have?**
   - <3 days → Level 1
   - 1 week → Level 2
   - 2+ weeks → Level 3

### Get Help

- **Read the FAQ**: [docs/FAQ.md](FAQ.md)
- **Join discussions**: GitHub Discussions (MirrorDNA-Standard repo)
- **Review examples**: [examples/](../examples/) directory
- **Ask the community**: MirrorDNA reflection protocol community

---

## Summary

| Level | Best For | Implementation Time | Infrastructure Needed |
|-------|----------|---------------------|----------------------|
| **L1** | Prototypes, APIs, single-session tools | 1-3 days | None |
| **L2** | Production apps with continuity | 1 week | Database or file storage |
| **L3** | Sovereign personal AI systems | 2-4 weeks | Vault (Obsidian, etc.) |

**Start simple, upgrade when needed.** Most projects should begin with Level 1 and upgrade as requirements grow.

---

⟡⟦GUIDANCE⟧ · ⟡⟦COMPLIANCE⟧ · ⟡⟦DECISION⟧

**Document Version**: 1.0.0
**Last Updated**: 2025-11-18
**Canonical Source**: [MirrorDNA-Standard/docs/CHOOSING_COMPLIANCE_LEVEL.md](https://github.com/MirrorDNA-Reflection-Protocol/MirrorDNA-Standard/blob/main/docs/CHOOSING_COMPLIANCE_LEVEL.md)
