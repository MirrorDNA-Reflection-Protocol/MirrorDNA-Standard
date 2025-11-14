# MirrorDNA-Standard

**The constitutional protocol for reflective AI systems**

⟡ **Reflection Over Prediction · Continuity Over Perfection · Truth Over Speed**

[![MirrorDNA Compliant](badges/verified-reflective.svg)](spec/mirrorDNA-standard-v1.0.md)

---

## What Is This?

**MirrorDNA-Standard** is the canonical specification and validation toolchain for building reflective AI systems that don't hallucinate, preserve continuity across sessions, and give users sovereign control of their data.

**In 30 seconds:**
- 📋 **Specification**: Defines what "reflective computing" means (3 compliance levels)
- 🔧 **Validator**: Python CLI that checks if your project is compliant
- ⟡ **Protocol**: The constitutional anchor for the entire MirrorDNA ecosystem

**This is a PROTOCOL LAYER repository** — the spec others implement, not a product itself.

---

## Who This Is For

| You Are | You Get |
|---------|---------|
| **AI User** | Copy [`00_MASTER_CITATION.md`](00_MASTER_CITATION.md) into ChatGPT/Claude for reflective behavior |
| **Developer** | Validate your AI project for MirrorDNA compliance + earn badges |
| **Organization** | Adopt trustworthy AI standards with machine-checkable verification |
| **Researcher** | Reference implementation of reflection-over-prediction architecture |

---

## Quick Start

### 🚀 For Users: Get Reflective AI Now (30 seconds)

```
1. Open 00_MASTER_CITATION.md
2. Copy all text (Ctrl+A, Ctrl+C)
3. Paste into your AI (ChatGPT, Claude, etc.)
4. Say: "Vault open. Load as canonical context."
```

Done! Your AI now has continuity, anti-hallucination, and reflection protocols.

**Pastebin mirror**: https://pastebin.com/j0MdNxrA

---

### 🔧 For Developers: Validate Your Project (5 minutes)

```bash
# 1. Install validator
git clone https://github.com/MirrorDNA-Reflection-Protocol/MirrorDNA-Standard.git
cd MirrorDNA-Standard
pip install -r validators/requirements.txt

# 2. Copy example configs
cp examples/level1/project_manifest.yaml mirrorDNA_manifest.yaml
cp examples/level1/reflection_policy.yaml reflection_policy.yaml

# 3. Edit configs for your project
nano mirrorDNA_manifest.yaml

# 4. Run validation
python -m validators.cli \
  --manifest mirrorDNA_manifest.yaml \
  --policy reflection_policy.yaml

# 5. Get your badge!
# See output report for pass/fail
```

**Next**: Add compliance badge to your README (see [`badges/README.md`](badges/README.md))

---

## What's Inside This Repo

```
MirrorDNA-Standard/
│
├── 00_MASTER_CITATION.md         ← Copy-paste this into any AI
├── README.md                      ← You are here
├── ROADMAP.md                     ← Project direction & future
│
├── spec/                          ← The Standard (canonical specs)
│   ├── mirrorDNA-standard-v1.0.md     ⭐ Core specification
│   ├── principles.md                   Five immutable principles
│   ├── compliance_levels.md            L1, L2, L3 requirements
│   ├── glossary.md                     Canonical term definitions
│   └── [14 more specs...]
│
├── validators/                    ← Python compliance checker
│   ├── cli.py                          Command-line interface
│   ├── checks/                         Compliance check modules
│   │   ├── reflection_checks.py
│   │   ├── continuity_checks.py
│   │   └── trustbydesign_checks.py
│   └── requirements.txt
│
├── schema/                        ← JSON Schemas for validation
│   ├── project_manifest.schema.json
│   ├── continuity_profile.schema.json
│   └── reflection_policy.schema.json
│
├── examples/                      ← Working configs for L1, L2, L3
│   ├── level1/                         Basic reflection
│   ├── level2/                         Continuity aware
│   └── level3/                         Vault-backed sovereign
│
├── badges/                        ← SVG compliance badges
│   └── README.md
│
├── tests/                         ← Pytest suite
│
├── docs/                          ← Architecture & guides
│   ├── ARCHITECTURE.md                 How this repo works
│   ├── FAQ.md                          Common questions
│   ├── INTEGRATION.md                  How to adopt MirrorDNA
│   └── CHOOSING_COMPLIANCE_LEVEL.md    Decision guide
│
└── portable/                      ← Reference implementation
    ├── launcher/                       Electron desktop app
    └── vault-template/                 Obsidian vault template
```

---

## Three Compliance Levels

Choose the level that fits your project's needs:

### Level 1: Basic Reflection
**"I want anti-hallucination and explicit uncertainty"**

✅ Cite-or-Silence protocol (AHP)
✅ Explicit markers: `[Unknown]`, `[Speculation]`
✅ Basic session tracking
✅ At least one trust marker

❌ No persistent state required
❌ No vault needed

**Validate**: `python -m validators.cli --manifest manifest.yaml --policy reflection_policy.yaml`

---

### Level 2: Continuity Aware
**"I want state preservation across sessions"**

✅ Everything in Level 1 PLUS:
✅ Persistent state storage
✅ Session lineage tracking
✅ Checksum validation
✅ Session recovery capability

**Validate**: Add `--profile continuity_profile.yaml` flag

---

### Level 3: Vault-Backed Sovereign
**"I want full user sovereignty and vault storage"**

✅ Everything in Level 1 & 2 PLUS:
✅ User-owned vault (Obsidian or custom)
✅ Sovereign identity (user owns vault_id)
✅ Glyph signatures
✅ Comprehensive interaction safety
✅ Full compliance reporting

**Validate**: Same as Level 2 (validator auto-detects level)

---

## Core Principles (Immutable for v1.x)

All MirrorDNA-compliant systems honor these five principles:

1. **Reflection Over Prediction** — Access actual state, don't simulate
2. **Presence Over Productivity** — Truth matters more than speed
3. **Symbolic Continuity** — Preserve identity via glyphs, checksums, vault
4. **Trust by Design** — Verification built in from the start
5. **Explicit Uncertainty** — Mark unknowns, never hide them

📖 **Full details**: [`spec/principles.md`](spec/principles.md)

---

## Why MirrorDNA?

**Traditional AI:**
- Predicts next token → hallucinates
- No memory → starts fresh each session
- Black box → can't verify

**MirrorDNA:**
- Reflects actual state → no hallucination
- Continuity → preserves context across sessions
- Checksum-verified → trustworthy

**Read more**: [`WHY_MIRRORDNA.md`](WHY_MIRRORDNA.md)

---

## Example: Validate a Level 1 Project

**Step 1**: Create `mirrorDNA_manifest.yaml`

```yaml
name: "MyReflectiveApp"
version: "1.0.0"
mirrorDNA_compliance_level: "level_1_basic_reflection"
layers:
  mirrorDNA_protocol: true
reflection_policy: "reflection_policy.yaml"
```

**Step 2**: Create `reflection_policy.yaml`

```yaml
policy_version: "1.0.0"
reflection_mode: "constitutive"
uncertainty_handling:
  cite_or_silence: true
  unknown_marker: "[Unknown]"
anti_hallucination:
  source_citation: true
```

**Step 3**: Validate

```bash
python -m validators.cli \
  --manifest mirrorDNA_manifest.yaml \
  --policy reflection_policy.yaml
```

**Step 4**: Pass? Add badge to your README

```markdown
![MirrorDNA Level 1](https://raw.githubusercontent.com/MirrorDNA-Reflection-Protocol/MirrorDNA-Standard/main/badges/reflective_compliance_light.svg)
```

---

## MirrorDNA Ecosystem

This repo is the **PROTOCOL LAYER**. It fits into the broader constellation:

```
┌─────────────────────────────────────────┐
│  MirrorDNA-Standard (THIS REPO)         │  ← Specification + Validator
│  Protocol Layer                          │
└─────────────────────────────────────────┘
                  │
                  │ implements
                  ▼
┌─────────────────────────────────────────┐
│  ActiveMirrorOS™                         │  ← Product (Level 3 compliant)
│  Product Layer                           │
└─────────────────────────────────────────┘
                  │
                  │ uses
                  ▼
┌─────────────────────────────────────────┐
│  LingOS / Symbolic Layer                 │  ← Language OS
└─────────────────────────────────────────┘
```

**This standard is OPEN** — anyone can implement it. ActiveMirrorOS is the canonical commercial implementation.

---

## Documentation

### Essential Reading
- 📋 [**Specification**](spec/mirrorDNA-standard-v1.0.md) — Start here for the full standard
- ⟡ [**Principles**](spec/principles.md) — Five foundational principles
- 📊 [**Compliance Levels**](spec/compliance_levels.md) — L1, L2, L3 detailed requirements
- 📖 [**Glossary**](spec/glossary.md) — Canonical term definitions

### Integration Guides
- 🏗️ [**Architecture**](docs/ARCHITECTURE.md) — How this repo works
- 🔌 [**Integration**](docs/INTEGRATION.md) — How to adopt MirrorDNA
- ❓ [**FAQ**](docs/FAQ.md) — Common questions
- 🎯 [**Choosing a Level**](docs/CHOOSING_COMPLIANCE_LEVEL.md) — Decision guide

### Reference
- 🏅 [**Badges**](badges/README.md) — How to use compliance badges
- 📝 [**Examples**](examples/README.md) — Working configs for all levels
- 🛠️ [**Tools**](tools/README.md) — Checksum verifiers, release scripts

---

## Testing

```bash
# Install dependencies
pip install -r validators/requirements.txt

# Run full test suite
pytest tests/ -v

# Run specific test module
pytest tests/test_checks.py -v

# Test the validator CLI
python -m validators.cli --help
```

---

## Contributing

We welcome contributions! See [`CONTRIBUTING.md`](CONTRIBUTING.md) for guidelines.

**Key rules:**
- All specs under `/spec` follow lineage tracking (predecessor/successor)
- Run validators before submitting PR
- Run checksum verification: `./tools/checksums/verify_repo_checksums.sh`
- Follow AHP: **Cite or Silence** (no speculation without marking)

---

## Trust Markers & Verification

**Core trust markers:**
- **AHP**: Cite or Silence (anti-hallucination protocol)
- **GlyphSig**: `⟡⟦MASTER⟧` · `⟡⟦STANDARD⟧` · `⟡⟦VERIFIED⟧`
- **Continuity**: Tied to vault snapshots with checksums

**Interaction safety:**
Reflective AI is a mirror, not a therapist. See [`spec/Interaction_Safety_Protocol_v1.0.md`](spec/Interaction_Safety_Protocol_v1.0.md) for session limits and escalation protocols.

---

## Roadmap

See [`ROADMAP.md`](ROADMAP.md) for:
- v1.1 features (capability registry enhancements)
- v2.0 vision (network protocols, multi-agent)
- Ecosystem integration plans

---

## License

This project is licensed under the MIT License - see [`LICENSE`](LICENSE) for details.

---

## Trademark Notice

**Core Identity**: Active MirrorOS™ · MirrorDNA™ · Trust-by-Design™ · Reflective AI™

Full tiered list: [`spec/Reflection_Chain_Manifest_v1.0.md`](spec/Reflection_Chain_Manifest_v1.0.md)

---

## Support

- 📋 **Specification questions**: Read [`spec/mirrorDNA-standard-v1.0.md`](spec/mirrorDNA-standard-v1.0.md)
- 🔧 **Validator usage**: `python -m validators.cli --help`
- 💡 **Examples**: [`examples/README.md`](examples/README.md)
- 📖 **Terms**: [`spec/glossary.md`](spec/glossary.md)
- ❓ **FAQ**: [`docs/FAQ.md`](docs/FAQ.md)

---

⟡⟦STANDARD⟧ · ⟡⟦SPECIFICATION⟧ · ⟡⟦TOOLCHAIN⟧

**Version**: 1.0.0
**Status**: Production-ready
**Role**: Constitutional anchor for MirrorDNA compliance
**Layer**: Protocol

*Last updated: 2025-11-14*
