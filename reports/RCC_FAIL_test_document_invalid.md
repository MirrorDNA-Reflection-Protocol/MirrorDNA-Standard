---
date: 2025-11-09
document: test_document_invalid.md
result: FAIL
generated: 2025-11-09 11:56:54
tool: rcc_validator.py v1.0
---

# RCC Validation Report

**Document:** test_document_invalid.md
**Status:** FAIL
**Generated:** 2025-11-09 at 11:56:54

❌ **Validation failed!**

**Issues found:** 9 total (2 critical, 6 warnings)

---

## Issues Found

### CRITICAL

1. **Document:** Missing required frontmatter field: vault_id
   - **Fix:** Add 'vault_id: <value>' to YAML frontmatter

2. **Document:** Missing required frontmatter field: predecessor
   - **Fix:** Add 'predecessor: <value>' to YAML frontmatter

### WARNING

1. **Document:** No Master Citation reference found
   - **Fix:** Add Master Citation version in frontmatter or document body

2. **Document:** Missing 'successor' field in frontmatter
   - **Fix:** Add 'successor: <value>' or 'successor: TBD' to frontmatter

3. **Document:** No GlyphSig markers found
   - **Fix:** Add 'glyphsig:' to frontmatter or include ⟡⟦MARKER⟧ patterns in document

4. **Document:** Missing required glyphs: ⟡⟦MASTER⟧, ⟡⟦CONTINUITY⟧, ⟡⟦AHP⟧
   - **Fix:** Add missing glyph anchors to document

5. **Line 14:** Temporal/statistical claim without Truth-State tag: 5. Claims without Truth-State tags: "The market will grow to...
   - **Fix:** Add [Truth-State: Projection, Source: ...] near claim

6. **Document:** Glyph drift: 100% (threshold: 15%)
   - **Fix:** Add missing glyph anchors: ⟡⟦AHP⟧, ⟡⟦CONTINUITY⟧, ⟡⟦MASTER⟧

### INFO

- No checksum found in frontmatter

---

## Actions Required

1. Fix all CRITICAL issues before publishing
2. Address WARNINGS or document exceptions in lineage
3. Re-run RCC validator after fixes: `python rcc_validator.py --input <file>`
4. Only publish after receiving RCC_PASS

---

## Validation Checklist

- ✅ Master Citation version declared
- ❌ Predecessor/successor lineage present
- ❌ GlyphSig present
- ✅ No [[MISSING]] or [TODO] tokens
- ❌ Truth-State tags on temporal claims
- ❌ Glyph drift ≤15%
- ❌ Checksum present

---

## Continuity Seal

**Validation Date:** 2025-11-09
**Tool Version:** rcc_validator.py v1.0
**Principle:** AHP-Compliant (Cite or Silence)
**Release Gate:** BLOCKED

⟡⟦RCC⟧ · ⟡⟦COMPLIANCE⟧ · ⟡⟦CONTINUITY⟧
