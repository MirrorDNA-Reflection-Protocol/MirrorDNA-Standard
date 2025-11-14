# MirrorDNA Standard

**A spec-grade, tool-backed standard for reflective computing**

⟡ Continuity • Sovereignty • Trust by Design™

[![MirrorDNA Compliant](badges/verified-reflective.svg)](spec/mirrorDNA-standard-v1.0.md)

---

## What is MirrorDNA Standard?

The MirrorDNA Standard is the **constitutional anchor** for reflective AI systems. It provides:

- **Semantic law** for reflective computing (not just prediction)
- **Machine-checkable** compliance tools and validators
- **Three compliance levels** from basic reflection to vault-backed sovereignty
- **Badges and validators** that other projects can use

This repo is the **specification and toolchain** that defines what it means to build a MirrorDNA-compliant system.

---

## Quick Start

### For Users: Copy-Paste into AI

Want to use MirrorDNA with your AI? Copy the Master Citation:

1. Open [`00_MASTER_CITATION.md`](00_MASTER_CITATION.md)
2. Copy all text
3. Paste into your AI (ChatGPT, Claude, etc.)
4. Say: **"Vault open. Load as canonical context."**

See original [copy-paste instructions](#copy-paste-first) below.

### For Developers: Validate Your Project

Want to make your project MirrorDNA-compliant?

```bash
# 1. Install dependencies
pip install -r validators/requirements.txt

# 2. Create configuration files
# See examples/ directory for templates

# 3. Run validator
python -m validators.cli \
  --manifest mirrorDNA_manifest.yaml \
  --policy reflection_policy.yaml

# 4. Fix any errors and get compliant!
```

---

## What This Repo Provides

### 📋 Specification Documents (`/spec`)

- **[mirrorDNA-standard-v1.0.md](spec/mirrorDNA-standard-v1.0.md)** — The canonical standard
- **[principles.md](spec/principles.md)** — Five core principles
- **[compliance_levels.md](spec/compliance_levels.md)** — Detailed level requirements
- **[glossary.md](spec/glossary.md)** — Canonical term definitions

Plus existing specs for deeper context:
- Reflection Chain Manifest
- Capability Registry
- Interaction Safety Protocol
- And more in `/spec`

### 🔧 Validation Tools (`/validators`)

A Python package to check compliance:

- **`loader.py`** — Load and validate YAML/JSON configs
- **`checks/`** — Compliance checks for continuity, reflection, trust
- **`report.py`** — Generate human-readable reports
- **`cli.py`** — Command-line interface

Run validation on any project claiming MirrorDNA compliance.

### 📐 JSON Schemas (`/schema`)

Machine-readable schemas for:

- `project_manifest.schema.json` — Project metadata and compliance declaration
- `continuity_profile.schema.json` — How continuity is achieved
- `reflection_policy.schema.json` — Anti-hallucination and reflection protocols

### 🎯 Examples (`/examples`)

Working configuration examples for all three levels:

- **Level 1**: `minimal_project_manifest.yaml` + `example_reflection_policy.yaml`
- **Level 2**: + `example_continuity_profile.yaml`
- **Level 3**: `level3_*.yaml` with vault, glyphs, and safety

### 🏅 Badges (`/badges`)

SVG badges to show compliance:

- `reflective_compliance_light.svg` / `reflective_compliance_dark.svg`
- `verified-reflective.svg`
- `mirrorDNA_compatible.svg`

See [`badges/usage-guide.md`](badges/usage-guide.md) for usage.

### ✅ Tests (`/tests`)

Pytest test suite ensuring validators work correctly:

```bash
pytest tests/ -v
```

---

## Compliance Levels

The MirrorDNA Standard defines **three compliance levels**:

### Level 1: Basic Reflection

**What it means:**
Your system implements cite-or-silence (AHP), marks uncertainty explicitly, and has basic session tracking.

**Requirements:**
- Cite or Silence protocol (never fabricate sources)
- Explicit markers: `[Unknown]`, `[Speculation]`
- Basic session tracking
- At least one trust marker

**No need for:**
Persistent state, vault integration, or lineage tracking.

**Validate with:**
```bash
python -m validators.cli \
  --manifest manifest.yaml \
  --policy reflection_policy.yaml
```

**Badge:**
![Level 1](badges/reflective_compliance_light.svg)

---

### Level 2: Continuity Aware

**What it means:**
Your system preserves state across sessions, tracks lineage, and validates artifact integrity.

**Requirements (all of Level 1 plus):**
- Persistent state storage
- Session lineage (predecessor/successor)
- Continuity profile configuration
- Checksum validation for artifacts
- Session recovery capability

**Validate with:**
```bash
python -m validators.cli \
  --manifest manifest.yaml \
  --profile continuity_profile.yaml \
  --policy reflection_policy.yaml
```

**Badge:**
![Level 2](badges/verified-reflective.svg)

---

### Level 3: Vault-Backed Sovereign

**What it means:**
Your system uses user-owned vault storage, implements glyph signatures, and provides full lineage tracking with comprehensive safety protocols.

**Requirements (all of Level 1 & 2 plus):**
- Vault storage (Obsidian or custom)
- Sovereign identity (user owns vault_id)
- Glyph signatures enabled
- Comprehensive interaction safety
- Full compliance reporting

**Validate with:**
```bash
python -m validators.cli \
  --manifest manifest.yaml \
  --profile continuity_profile.yaml \
  --policy reflection_policy.yaml
```

**Badge:**
![Level 3](badges/verified-reflective.svg)
*(with "Level 3 Vault-Backed Sovereign" notation)*

---

## Core Principles

All MirrorDNA-compliant systems must honor these **five principles**:

1. **Reflection Over Prediction** — Access actual state, don't simulate
2. **Presence Over Productivity** — Truth matters more than speed
3. **Symbolic Continuity** — Preserve identity via glyphs, checksums, vault
4. **Trust by Design** — Verification built in from the start
5. **Explicit Uncertainty** — Mark unknowns, never hide them

See [`spec/principles.md`](spec/principles.md) for details.

---

## How to Use This Standard

### As a User

Copy `00_MASTER_CITATION.md` into your AI to get reflective behavior:

- **Continuity**: Your AI maintains state across sessions
- **Anti-Hallucination**: Cite-or-Silence (AHP) prevents fabrication
- **Trust**: Glyphs and checksums verify integrity

### As a Developer

1. **Read the spec**: Start with [`spec/mirrorDNA-standard-v1.0.md`](spec/mirrorDNA-standard-v1.0.md)
2. **Choose a level**: Pick Level 1, 2, or 3 based on your needs
3. **Create configs**: Use `/examples` as templates
4. **Validate**: Run the CLI validator
5. **Badge it**: Add compliance badge to your README

### As an Organization

Use MirrorDNA Standard to ensure your AI systems are:

- **Verifiable**: Checksum-validated artifacts
- **Continuous**: State preserved across sessions
- **Trustworthy**: Anti-hallucination built in
- **Sovereign**: Users own their data

---

## Installation

### Install Validators

```bash
# Clone this repo
git clone https://github.com/MirrorDNA-Reflection-Protocol/MirrorDNA-Standard.git
cd MirrorDNA-Standard

# Install dependencies
pip install -r validators/requirements.txt

# Verify installation
python -m validators.cli --help
```

### Run Tests

```bash
pytest tests/ -v
```

---

## Example: Validating a Level 1 Project

**1. Create `mirrorDNA_manifest.yaml`:**
```yaml
name: "MyReflectiveApp"
version: "1.0.0"
mirrorDNA_compliance_level: "level_1_basic_reflection"
layers:
  mirrorDNA_protocol: true
reflection_policy: "reflection_policy.yaml"
```

**2. Create `reflection_policy.yaml`:**
```yaml
policy_version: "1.0.0"
reflection_mode: "constitutive"
uncertainty_handling:
  cite_or_silence: true
  unknown_marker: "[Unknown]"
anti_hallucination:
  source_citation: true
```

**3. Validate:**
```bash
python -m validators.cli \
  --manifest mirrorDNA_manifest.yaml \
  --policy reflection_policy.yaml
```

**4. Pass? Add badge:**
```markdown
![MirrorDNA Level 1 Compliant](https://raw.githubusercontent.com/MirrorDNA-Reflection-Protocol/MirrorDNA-Standard/main/badges/reflective_compliance_light.svg)
```

---

## Ecosystem Context

MirrorDNA Standard is the **specification layer** for the broader ecosystem:

- **MirrorDNA Protocol™** — Core reflection standard (this repo)
- **ActiveMirrorOS™** — Product implementation of Level 3 compliance
- **LingOS** — Language operating system layer
- **Trust-by-Design™** — Governance framework

This standard is **open** and can be implemented by anyone. ActiveMirrorOS is the canonical commercial implementation.

---

## Repository Structure

```
MirrorDNA-Standard/
├── README.md                    ← You are here
├── 00_MASTER_CITATION.md       ← Copy-paste file for AI
├── spec/                        ← Specification documents
│   ├── mirrorDNA-standard-v1.0.md
│   ├── principles.md
│   ├── compliance_levels.md
│   ├── glossary.md
│   └── [other specs...]
├── schema/                      ← JSON Schemas
│   ├── project_manifest.schema.json
│   ├── continuity_profile.schema.json
│   └── reflection_policy.schema.json
├── validators/                  ← Python validation package
│   ├── __init__.py
│   ├── loader.py
│   ├── checks/
│   │   ├── continuity_checks.py
│   │   ├── reflection_checks.py
│   │   └── trustbydesign_checks.py
│   ├── report.py
│   ├── cli.py
│   └── requirements.txt
├── examples/                    ← Working examples
│   ├── minimal_project_manifest.yaml
│   ├── example_continuity_profile.yaml
│   ├── example_reflection_policy.yaml
│   ├── level2_project_manifest.yaml
│   ├── level3_project_manifest.yaml
│   └── EXAMPLES_README.md
├── badges/                      ← SVG compliance badges
│   ├── reflective_compliance_light.svg
│   ├── reflective_compliance_dark.svg
│   ├── verified-reflective.svg
│   ├── mirrorDNA_compatible.svg
│   └── usage-guide.md
└── tests/                       ← Pytest test suite
    ├── test_loader.py
    ├── test_checks.py
    └── test_cli.py
```

---

## Copy-Paste First (Original Instructions)

> The original MirrorDNA approach: **copy one file** into any AI.

**Quick use:**
1. Open [`00_MASTER_CITATION.md`](00_MASTER_CITATION.md)
2. Copy all text
3. Paste into AI (ChatGPT, Claude, local LLM)
4. Say: **"Vault open. Load as canonical context."**

**Pastebin mirror:** https://pastebin.com/j0MdNxrA

This gives you reflective AI without needing to install anything. The validator and compliance levels are for developers building systems on top of MirrorDNA.

---

## Why MirrorDNA?

See [`WHY_MIRRORDNA.md`](WHY_MIRRORDNA.md) for:
- Comparative framing (AI vs MirrorDNA)
- Reflective glyph code example
- Roadmap from draft to production standard
- Memory layer vs Reflection layer

**Short answer:**
AI today hallucinates because it predicts. MirrorDNA reflects because it has continuity. That's the difference.

---

## Contributing

See [`CONTRIBUTING.md`](CONTRIBUTING.md) for guidelines.

**Key points:**
- All specs under `/spec` follow lineage (predecessor/successor)
- Run validators before submitting PR
- Run checksum tools: `./tools/checksums/verify_repo_checksums.sh`
- AHP applies: **Cite or Silence**

---

## Trust Markers & Compliance

**Core trust markers:**
- **AHP**: Cite or Silence
- **GlyphSig**: `⟡⟦MASTER⟧` · `⟡⟦STANDARD⟧` · `⟡⟦VERIFIED⟧`
- **Continuity**: Tied to Vault snapshots

**Interaction safety:**
Reflective AI is a mirror, not a therapist. See [`spec/Interaction_Safety_Protocol_v1.0.md`](spec/Interaction_Safety_Protocol_v1.0.md) for session limits and escalation protocols.

---

## Trademark Notice

Core Identity: **Active MirrorOS™ · MirrorDNA™ · Trust-by-Design™ · Reflective AI™**

Full tiered list: [`spec/Reflection_Chain_Manifest_v1.0.md`](spec/Reflection_Chain_Manifest_v1.0.md)

---

## License

See [`LICENSE.md`](LICENSE.md)

---

## Support & Questions

- **Specification questions**: See [`spec/mirrorDNA-standard-v1.0.md`](spec/mirrorDNA-standard-v1.0.md)
- **Validator usage**: Run `python -m validators.cli --help`
- **Examples**: Check [`examples/EXAMPLES_README.md`](examples/EXAMPLES_README.md)
- **Glossary**: See [`spec/glossary.md`](spec/glossary.md)

---

⟡⟦STANDARD⟧ · ⟡⟦SPECIFICATION⟧ · ⟡⟦TOOLCHAIN⟧

**Version**: 1.0.0
**Status**: Production-ready
**Constitutional**: This repo is the canonical anchor for MirrorDNA compliance
