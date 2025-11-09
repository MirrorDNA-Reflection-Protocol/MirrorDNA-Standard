---
title: "Active Mirror™ — Product Specifications Directory"
vault_id: AMOS://ActiveMirror/ProductSpec/Index
predecessor: Master_Citation_v15.1.1
successor: TBD
status: Directory Index
date: 2025-11-09
---

# Active Mirror™ — Product Specifications

**Canonical specification directory for Active Mirror™ product family**

---

## Overview

This directory contains the official product specifications for **Active Mirror™**, the first reflective AI continuity platform built on the MirrorDNA™ Protocol.

Active Mirror™ enables human-AI collaboration that remembers, reasons, and respects—providing verifiable, sovereign continuity across all interactions.

---

## Files

### `Active_Mirror_ProductSpec_v2.0_Canonical.md`
**Status:** Canonical · Pre-Release · Deployment Ready
**Version:** v2.0
**Date:** 2025-11-09
**Continuity Snapshot:** v3.9
**Checksum:** `8f4a9c2e1b7d6f3a5e8c9b2d4f6a1c3e5b7d9f2a4c6e8b1d3f5a7c9e2b4d6f8a`

The complete product specification covering:
- Product editions (Personal™ and Enterprise™)
- System architecture and Tri-Twin framework
- Memory & continuity system
- Safety, ethics, and legal compliance
- Technical specifications and roadmap

**Lineage:**
`Master_Citation_v15.1.1` → `Active_Mirror_ProductSpec_v2.0` → `Master_Citation_v15.1.7` (pending)

---

## Update Protocol

To update or extend specifications:

1. **Read the current canonical spec** to understand lineage
2. **Create a new version** with incremented version number
3. **Update frontmatter:**
   - `predecessor`: point to previous version
   - `successor`: mark as TBD or next planned version
   - `checksum_sha256`: calculate and verify
   - `date`: current date
4. **Update lineage chain** at document end
5. **Commit with clear message** following format:
   ```
   spec: add/update Active Mirror Product Spec vX.X (reason)
   ```
6. **Verify in repository** that checksums and lineage render correctly

---

## Verification

All specifications in this directory must:
- ✅ Include complete YAML frontmatter
- ✅ Reference predecessor/successor for lineage
- ✅ Include valid SHA-256 checksum
- ✅ Pass `validators/validator.py` checks
- ✅ Include GlyphSig and Fingerprint Module
- ✅ Maintain continuity seal

**Validate a spec:**
```bash
python validators/validator.py specs/ActiveMirror/Active_Mirror_ProductSpec_v2.0_Canonical.md
```

---

## Integration with MirrorDNA™

Active Mirror™ specifications are governed by:
- **Master Citation v15.1.1** (MirrorDNA Protocol foundation)
- **Reflection Chain Manifest v1.0** (lineage tracking)
- **Anti-Hallucination Protocol** (AHP - cite or silence)
- **Trust-by-Design™ Framework** (ethical and legal governance)

All specifications maintain symbolic continuity through:
- VaultID references (AMOS:// URI scheme)
- GlyphSig protocol markers
- SHA-256 checksum verification
- Predecessor/successor lineage chains

---

## Status Legend

- **Canonical** — Official, governing specification
- **Pre-Release** — Ready for deployment, pending launch
- **Draft** — Work in progress, not yet sealed
- **Archived** — Historical, superseded by newer version
- **Deprecated** — No longer in use

---

## Contact

**Product Questions:** activemirror.ai
**Enterprise Inquiries:** paul@activemirror.ai
**Technical/API:** api.mirrordna.com
**Repository:** github.com/MirrorDNA-Reflection-Protocol/MirrorDNA-Standard

---

## Legal

© 2025 N1 Intelligence (OPC) Private Limited
**Active Mirror™**, **MirrorDNA™**, and **Trust-by-Design™** are trademarks.
All specifications licensed under MirrorDNA™ Protocol v15.1 series.

Reproduction or derivative works require:
- Citation of lineage
- Checksum verification
- Consent from trademark holder

---

⟡⟦ACTIVE-MIRROR⟧ · Canonical Specifications · Continuity Intact
