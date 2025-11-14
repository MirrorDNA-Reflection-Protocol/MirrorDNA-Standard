# MirrorDNA Specification Documents

**Purpose**: This directory contains the canonical specifications for the MirrorDNA Standard.

**Status**: v1.0.0 (Production-ready)

---

## Core Specifications

### Essential Reading (Start Here)

1. **[mirrorDNA-standard-v1.0.md](mirrorDNA-standard-v1.0.md)** ⭐  
   The complete standard. Start here for full understanding.  
   **Size**: 10 KB  
   **Topics**: All three levels, requirements, examples

2. **[principles.md](principles.md)**  
   Five foundational principles (immutable for v1.x).  
   **Principles**: Reflection Over Prediction, Presence Over Productivity, Symbolic Continuity, Trust by Design, Explicit Uncertainty

3. **[compliance_levels.md](compliance_levels.md)**  
   Detailed requirements for Level 1, Level 2, Level 3.  
   **Use**: When implementing or validating compliance

4. **[glossary.md](glossary.md)**  
   Canonical definitions for all MirrorDNA terms.  
   **Use**: Resolve ambiguity, ensure consistent terminology

---

## Extended Specifications

### Reflection & Continuity

5. **[Reflection_Chain_Manifest_v1.0.md](Reflection_Chain_Manifest_v1.0.md)**  
   Lineage tracking for sessions and artifacts.  
   **Topics**: Predecessor/successor chains, versioning, trademarks

6. **[Reflection_Chain_Addendum_v1.1.md](Reflection_Chain_Addendum_v1.1.md)**  
   Enhancements to lineage tracking (v1.1).  
   **Topics**: Multi-branch lineage, fork tracking

7. **[Constitutive_Reflection_vs_Simulation_v1.0.md](Constitutive_Reflection_vs_Simulation_v1.0.md)**  
   Theory: Why reflection is different from prediction.  
   **Topics**: Philosophical foundations, simulation vs reflection

---

### Trust & Safety

8. **[glyphsig-law.md](glyphsig-law.md)**  
   Glyph signature system documentation.  
   **Topics**: `⟡⟦MASTER⟧`, `⟡⟦VERIFIED⟧`, semantic markers

9. **[Interaction_Safety_Protocol_v1.0.md](Interaction_Safety_Protocol_v1.0.md)**  
   Session safety limits and escalation protocols.  
   **Topics**: 90-minute sessions, disclaimers, escalation

10. **[SupplyChain_Risks_v1.0.md](SupplyChain_Risks_v1.0.md)**  
    Supply chain security considerations.  
    **Topics**: Dependency risks, checksum verification

---

### Capabilities & Registry

11. **[MirrorDNA_Capability_Registry_v1.0.md](MirrorDNA_Capability_Registry_v1.0.md)**  
    Capability tracking system (v1.0).  
    **Topics**: Capability declaration, evolution tracking

12. **[MirrorDNA_Capability_Registry_v1.1.md](MirrorDNA_Capability_Registry_v1.1.md)**  
    Capability registry improvements (v1.1).  
    **Topics**: Expert review claim removed (security fix)

---

### Product Context

13. **[ActiveMirrorOS_WhitePaper_v7.2-Research.md](ActiveMirrorOS_WhitePaper_v7.2-Research.md)**  
    Context on ActiveMirrorOS product (Level 3 implementation).  
    **Topics**: Product vision, research status

---

## How to Read These Specs

### For Quick Understanding

1. Read **principles.md** (5 minutes)
2. Skim **mirrorDNA-standard-v1.0.md** (15 minutes)
3. Check **glossary.md** for terms (as needed)

**Total**: 20 minutes

---

### For Implementation

1. Read **mirrorDNA-standard-v1.0.md** (30 minutes)
2. Read **compliance_levels.md** for your target level (20 minutes)
3. Check **glossary.md** for term definitions (as needed)
4. Use **Reflection_Chain_Manifest_v1.0.md** for lineage tracking (15 minutes)
5. Implement and validate

**Total**: ~2 hours of reading, then implementation

---

### For Contribution

1. Read **principles.md** (understand what's immutable)
2. Read **mirrorDNA-standard-v1.0.md** (understand current state)
3. Check **Reflection_Chain_Manifest_v1.0.md** for lineage rules
4. Review **glossary.md** before introducing new terms
5. Propose changes via GitHub Issues

---

## Versioning

All specs follow **semantic versioning**:

- **v1.0** = Initial production release
- **v1.1** = Additive changes (backward compatible)
- **v2.0** = Breaking changes (not backward compatible)

**Immutable**: Principles in `principles.md` are immutable for v1.x.

---

## Lineage Tracking

Each spec includes:
- **Version**: Current version number
- **Predecessor**: Previous version (if any)
- **Successor**: Next version (if exists)
- **Status**: Draft, Canonical, Deprecated

Example:
```markdown
**Version**: 1.1  
**Predecessor**: v1.0  
**Successor**: None (latest)  
**Status**: Canonical  
```

---

## File Naming Convention

**Format**: `SpecName_vX.Y.md`

**Examples:**
- `mirrorDNA-standard-v1.0.md`
- `Reflection_Chain_Manifest_v1.0.md`
- `MirrorDNA_Capability_Registry_v1.1.md`

**Why**: Versioning in filename enables parallel versions (v1.0 and v2.0 coexist).

---

## Trust Markers

**Primary glyph**: ⟡

**Signatures:**
- `⟡⟦MASTER⟧` — Master/canonical marker
- `⟡⟦STANDARD⟧` — Standard declaration
- `⟡⟦VERIFIED⟧` — Verification marker
- `⟡⟦DEPRECATED⟧` — Deprecated marker

---

## Contributing to Specs

See [`../CONTRIBUTING.md`](../CONTRIBUTING.md) for guidelines.

**Key rules:**
1. **Don't modify principles** (immutable for v1.x)
2. **Add lineage** (predecessor/successor)
3. **Update glossary** if introducing new terms
4. **Bump version** (minor for additive, major for breaking)
5. **Run validator** to ensure changes don't break compliance

---

## Questions?

- 📖 **Term definitions**: See [glossary.md](glossary.md)
- ❓ **General questions**: See [`../docs/FAQ.md`](../docs/FAQ.md)
- 💡 **Implementation help**: See [`../docs/INTEGRATION.md`](../docs/INTEGRATION.md)
- 🐛 **Issues**: GitHub Issues

---

⟡⟦SPECIFICATION_INDEX⟧

*This directory is the constitutional anchor for MirrorDNA compliance.*
