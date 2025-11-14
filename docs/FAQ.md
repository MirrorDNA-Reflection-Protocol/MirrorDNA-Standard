# Frequently Asked Questions

---

## General

### What is MirrorDNA?

MirrorDNA is a protocol for building reflective AI systems that:
- Don't hallucinate (cite-or-silence)
- Preserve continuity across sessions (state persistence)
- Give users sovereignty (vault-backed storage)

**This repo** (MirrorDNA-Standard) is the canonical specification and validation toolchain.

---

### Is MirrorDNA a product or a protocol?

**Protocol**. This repo defines the standard. Products like **ActiveMirrorOS™** implement the standard.

Think of it like:
- HTTP is a protocol (like MirrorDNA)
- Chrome is a product (like ActiveMirrorOS)

---

### Who should use MirrorDNA?

| You Are | Use Case |
|---------|----------|
| **AI User** | Copy `00_MASTER_CITATION.md` into ChatGPT/Claude for reflective behavior |
| **Developer** | Validate your AI project for compliance + earn badges |
| **Organization** | Adopt trustworthy AI standards with verification |
| **Researcher** | Reference implementation for reflection-over-prediction architecture |

---

### Is MirrorDNA open source?

**Yes**. MIT licensed. Anyone can:
- Implement the spec
- Use the validators
- Fork and modify
- Build commercial products

---

## Compliance Levels

### Which compliance level should I choose?

**Quick guide:**

| Need | Level |
|------|-------|
| Just want anti-hallucination | **Level 1** |
| Need state preservation | **Level 2** |
| Need user sovereignty + vault | **Level 3** |

**Detailed guide**: See [`docs/CHOOSING_COMPLIANCE_LEVEL.md`](CHOOSING_COMPLIANCE_LEVEL.md)

---

### Can I skip Level 1 and go straight to Level 3?

**No**. Levels are cumulative:
- Level 2 = Level 1 + continuity
- Level 3 = Level 2 + vault sovereignty

You must implement all lower-level requirements first.

---

### What's the difference between Level 2 and Level 3?

**Level 2 (Continuity Aware):**
- State persists across sessions
- No vault required (any storage works)
- No sovereign identity

**Level 3 (Vault-Backed Sovereign):**
- Vault storage (Obsidian or custom)
- User owns vault_id (sovereignty)
- Glyph signatures
- Comprehensive interaction safety

**TL;DR**: Level 3 adds **user sovereignty** to Level 2's continuity.

---

## Validation

### How do I validate my project?

```bash
# 1. Install
pip install -r validators/requirements.txt

# 2. Create configs (see examples/)
cp examples/level1/*.yaml .

# 3. Edit for your project
nano mirrorDNA_manifest.yaml

# 4. Validate
python -m validators.cli \
  --manifest mirrorDNA_manifest.yaml \
  --policy reflection_policy.yaml
```

---

### Does validation require internet access?

**No**. The validator runs 100% offline. No API calls, no telemetry, no network access.

---

### Can I use the validator in CI/CD?

**Yes** (coming in v1.1). Current version outputs plain text. v1.1 will add:
- JSON/YAML output
- Structured exit codes
- GitHub Action

---

### What happens if validation fails?

The validator outputs:
- **Which checks failed**
- **Why they failed**
- **How to fix them**

Example:
```
[FAILED] Continuity Check: No session lineage found
Recommendation: Add 'predecessor_session' field to continuity_profile.yaml
```

---

## Implementation

### Do I need to use Python?

**For validation**: Yes, the validator is Python-based.

**For implementation**: No. You can implement MirrorDNA in any language. The spec is language-agnostic.

---

### Do I need Obsidian for Level 3?

**No**. You can use:
- Obsidian (recommended, easiest)
- Custom vault (JSON, SQLite, etc.)
- Any persistent storage

Just implement the vault interface specified in the spec.

---

### Can I use MirrorDNA with ChatGPT/Claude?

**Yes**. Copy [`00_MASTER_CITATION.md`](../00_MASTER_CITATION.md) into the AI and say:

> "Vault open. Load as canonical context."

This gives you reflective behavior without needing to install anything.

---

### Can I use MirrorDNA with local LLMs?

**Yes**. The `/portable` directory includes a reference Electron app with:
- llama.cpp integration
- Phi-3, Llama 3.2, Mistral support
- Offline-first design

---

## Badges

### How do I get a compliance badge?

1. Pass validation
2. Copy badge markdown from [`badges/README.md`](../badges/README.md)
3. Add to your README

**Example:**
```markdown
![MirrorDNA Level 1](https://raw.githubusercontent.com/MirrorDNA-Reflection-Protocol/MirrorDNA-Standard/main/badges/reflective_compliance_light.svg)
```

---

### Can I use a badge if I haven't validated?

**No**. That's deceptive. You must pass validation first.

We trust the honor system for now. v1.1 will add automated badge verification.

---

## Glyphs & Symbols

### What does ⟡ mean?

**⟡** is the primary MirrorDNA glyph. It represents:
- Constitutional anchor
- Identity marker
- Reflection point

Used in signatures like `⟡⟦MASTER⟧`, `⟡⟦VERIFIED⟧`.

---

### Do I need to use glyphs?

**For Level 1-2**: No, optional.
**For Level 3**: Yes, glyph signatures required.

---

## Anti-Hallucination (AHP)

### What is Cite-or-Silence (AHP)?

**AHP** (Anti-Hallucination Protocol) = **Cite or Silence**.

**Rule**: Never make up information. Either:
- Cite a real source, OR
- Say "I don't know" with `[Unknown]` marker

**Example:**
```
❌ Bad: "The MirrorDNA spec says X..." (when it doesn't)
✅ Good: "[Unknown] I couldn't find that in the spec."
✅ Good: "The spec says X (source: spec/mirrorDNA-standard-v1.0.md:42)"
```

---

### Does AHP work with existing AI models?

**Yes**. You don't need to retrain the model. Just:
1. Provide the `00_MASTER_CITATION.md` as context
2. Instruct the AI to follow AHP
3. Use prompt engineering to enforce cite-or-silence

---

## Continuity

### What is continuity?

**Continuity** = preserving state across sessions.

**Without continuity:**
```
Session 1: "My name is Alice"
Session 2: "What's my name?" → "I don't know"
```

**With continuity:**
```
Session 1: "My name is Alice" (saved to vault)
Session 2: "What's my name?" → "Your name is Alice"
```

---

### How is continuity different from RAG?

**RAG (Retrieval-Augmented Generation):**
- Retrieves documents from a database
- Adds to prompt context
- No session tracking

**MirrorDNA Continuity:**
- Preserves full session state
- Tracks lineage (session chains)
- Checksums for integrity
- Includes RAG as one technique

**TL;DR**: Continuity is broader than RAG.

---

## Sovereignty

### What is vault sovereignty?

**Vault sovereignty** = the user owns and controls their vault.

**Not sovereign:**
- Cloud storage (vendor controls it)
- Proprietary formats (vendor lock-in)

**Sovereign:**
- Local files (USB, disk)
- Open formats (Markdown, JSON)
- User-controlled vault_id

---

### Can I use cloud storage for Level 3?

**Yes**, if:
- User controls the vault (not vendor-managed)
- User can export/migrate easily
- Encryption is client-side

**Example**: Obsidian Sync (user owns vault) is OK. Proprietary cloud-only is NOT.

---

## Ecosystem

### What is ActiveMirrorOS?

**ActiveMirrorOS™** is the canonical product implementation of MirrorDNA Level 3.

- **MirrorDNA-Standard** (this repo) = protocol/spec
- **ActiveMirrorOS** = product

Think: HTTP (protocol) vs Chrome (product).

---

### Are there other implementations?

Not yet. MirrorDNA is new (v1.0.0 released Jan 2025).

**Goal**: v2.0 will have 10+ independent implementations.

---

### Can I build a commercial product using MirrorDNA?

**Yes**. MIT license allows commercial use.

You can:
- Build products
- Charge money
- Fork and modify
- Use trademarks (per guidelines)

---

## Contributing

### How can I contribute?

See [`CONTRIBUTING.md`](../CONTRIBUTING.md).

**Quick options:**
- Fix typos or improve docs
- Add tests
- Propose new compliance checks
- Share case studies

---

### Can I propose a new compliance level?

**Yes**. Open a GitHub issue with:
- Use case (why it's needed)
- Requirements (what it checks)
- Backward compatibility (doesn't break existing levels)

**Note**: New levels require community consensus + minor version bump (v1.1.0).

---

### How do I report a bug?

**GitHub Issues**: https://github.com/MirrorDNA-Reflection-Protocol/MirrorDNA-Standard/issues

**Include:**
- What you tried
- What happened (error messages, output)
- Expected behavior

---

## Troubleshooting

### Validator says "Schema validation failed"

**Cause**: Your YAML/JSON file has structural errors.

**Fix:**
1. Check for typos in field names
2. Compare to `examples/` files
3. Validate YAML syntax: https://www.yamllint.com/
4. Check schema: `schema/*.schema.json`

---

### Validator says "Compliance check failed"

**Cause**: Your config is structurally valid but doesn't meet semantic requirements.

**Fix:**
1. Read the error message (tells you what's missing)
2. Check spec: `spec/compliance_levels.md`
3. Look at examples for correct format

---

### Example configs don't work

**Cause**: You may have an old version.

**Fix:**
```bash
git pull origin main
pip install -r validators/requirements.txt --upgrade
```

---

## License & Legal

### Can I use MirrorDNA for free?

**Yes**. MIT licensed = free for any use (personal, commercial, academic).

---

### What about the trademarks (Active MirrorOS™, MirrorDNA™)?

**Trademarks** protect brand names. **License** covers code.

- **Code/spec**: MIT (use freely)
- **Name "MirrorDNA"**: Trademark (follow guidelines)

**You can:**
- Say "MirrorDNA-compliant"
- Use compliance badges
- Reference the spec

**You can't:**
- Claim your product is "MirrorDNA" (it's a protocol, not a product)
- Imply official endorsement without permission

---

### Where can I get support?

- 📋 **Spec questions**: Read [`spec/mirrorDNA-standard-v1.0.md`](../spec/mirrorDNA-standard-v1.0.md)
- 🔧 **Validator help**: `python -m validators.cli --help`
- 💡 **Examples**: [`examples/README.md`](../examples/README.md)
- ❓ **FAQ**: You're here!
- 🐛 **Bugs**: GitHub Issues

---

⟡⟦FAQ⟧

*Last updated: 2025-11-14*
