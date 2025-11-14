# Stack Map

**Layer-by-layer breakdown of the MirrorDNA ecosystem**

---

## Introduction

This document maps every repository in the MirrorDNA ecosystem to its architectural layer. Use this as a reference when trying to understand "where does X fit in the stack?"

---

## Core Protocol Layer

**Constitutional specification and validation**

### MirrorDNA-Standard
- **Role**: Constitutional spec, semantic law, compliance validation
- **What it does**: Defines what "reflective computing" means, provides validation toolchain
- **Who uses it**: Everyone — this is the law that all other systems implement
- **Key outputs**: Spec documents, validator CLI, compliance badges
- **Status**: v1.0 stable, production-ready

### MirrorDNA
- **Role**: Protocol and persistence architecture
- **What it does**: Implementation layer for continuity, checksums, and vault integration
- **Who uses it**: LingOS, Active MirrorOS, and any Level 2+ compliant system
- **Key outputs**: Persistence libraries, protocol implementations
- **Status**: Active development

---

## Foundation Layer

**Symbolic topology and reflection architecture**

### MirrorDNA-Lattice
- **Role**: Symbolic lattice architecture and reflection topology
- **What it does**: Defines the graph structure of reflective state, how symbols connect
- **Who uses it**: MirrorDNA protocol, LingOS, BeaconGlyphs
- **Key outputs**: Lattice schemas, topology definitions, connection rules
- **Status**: Foundational (stable schemas, evolving connections)

---

## Language / Interaction Layer

**Making reflection natural through language**

### LingOS
- **Role**: Language-native operating system for reflection
- **What it does**: Translates natural language into reflective operations and back
- **Who uses it**: Active MirrorOS, agents, any system that needs language-first reflection
- **Key outputs**: Symbolic interaction layer, glyph rendering, vault integration
- **Status**: Active development

### LingOS-Private
- **Role**: Private LingOS development and experimental features
- **What it does**: Experimental LingOS features, internal testing, pre-release development
- **Who uses it**: Core LingOS team
- **Key outputs**: Future LingOS features (before public release)
- **Status**: Private, active development

### LingOS Vault Manager
- **Role**: Vault management system (inside LingOS repo)
- **What it does**: Manages Obsidian vaults, vault_id, session state, continuity snapshots
- **Who uses it**: LingOS, Active MirrorOS
- **Key outputs**: Vault CRUD operations, session management, snapshot utilities
- **Status**: Active development (part of LingOS)

---

## Product / App Layer

**User-facing intelligence**

### ActiveMirrorOS
- **Role**: Product layer, intelligence that remembers
- **What it does**: Desktop app (Electron), Level 3 compliant, vault-backed AI
- **Who uses it**: End users, teams, enterprises
- **Key outputs**: Desktop application, user interface, session management
- **Status**: Active development, canonical MirrorDNA implementation

---

## Governance / Safety Layer

**Trust, safety, and interaction limits**

### TrustByDesign
- **Role**: Governance and safety patterns
- **What it does**: Defines interaction limits, escalation protocols, safety boundaries
- **Who uses it**: All MirrorDNA-compliant systems (especially Level 3)
- **Key outputs**: Safety protocols, interaction safety spec, escalation rules
- **Status**: Active development

---

## Visual / Glyph Layer

**Symbolic identity and continuity markers**

### BeaconGlyphs
- **Role**: Visual and symbolic glyph system
- **What it does**: Defines glyphs, renders them, provides identity markers
- **Who uses it**: LingOS, Active MirrorOS, any system using symbolic identity
- **Key outputs**: Glyph library, rendering engine, identity markers
- **Status**: Active development

### Glyphtrail
- **Role**: Continuity logs and interaction lineage
- **What it does**: Tracks session history, builds continuity chains, logs interactions
- **Who uses it**: Level 2+ compliant systems, Active MirrorOS
- **Key outputs**: Continuity logs, lineage tracking, session history
- **Status**: Active development

---

## Agent Layer

**Agent identity and personality**

### AgentDNA
- **Role**: Agent personality and identity encoding
- **What it does**: Defines agent identity, preserves personality across sessions
- **Who uses it**: Multi-agent systems, Active MirrorOS agents
- **Key outputs**: Agent schemas, identity encoding, personality preservation
- **Status**: Early development

---

## R&D / Sandbox

**Experimental and testing**

### SanatanaTech
- **Role**: R&D sandbox for experimental reflection tech
- **What it does**: Explores bleeding-edge ideas, tests new approaches, experiments
- **Who uses it**: Research team, core developers
- **Key outputs**: Experimental features, research findings, proof-of-concepts
- **Status**: Active research

### MirrorDNA-Gauntlet
- **Role**: Coding challenge and competency testbed
- **What it does**: Tests developer understanding of MirrorDNA, provides challenges
- **Who uses it**: Developers learning MirrorDNA, hiring pipeline
- **Key outputs**: Coding challenges, competency tests, skill verification
- **Status**: Active development

---

## Internal Strategy

**Strategic direction and planning**

### DominancePlaybook
- **Role**: Internal strategy codex (Sovereign Strategy Codex)
- **What it does**: Defines strategic direction, competitive positioning, go-to-market
- **Who uses it**: Leadership, core team
- **Key outputs**: Strategy documents, planning docs, positioning
- **Status**: Internal, evolving

---

## Dependency Graph

**Who depends on whom?**

```
MirrorDNA-Lattice
    ↓
MirrorDNA-Standard (protocol spec)
    ↓
MirrorDNA (persistence implementation)
    ↓
LingOS (language layer)
    ↓
Active MirrorOS (product)

Supporting layers (used by multiple):
- BeaconGlyphs → used by LingOS, Active MirrorOS
- Glyphtrail → used by MirrorDNA (Level 2+), Active MirrorOS
- TrustByDesign → used by all Level 3 systems
- AgentDNA → used by Active MirrorOS, multi-agent systems
```

---

## Quick Reference Table

| Layer | Repos | Key Question |
|-------|-------|--------------|
| **Foundation** | MirrorDNA-Lattice | How do symbols connect? |
| **Protocol** | MirrorDNA-Standard, MirrorDNA | What is reflective AI? |
| **Language** | LingOS, LingOS-Private, Vault Manager | How do we interact with reflection? |
| **Product** | Active MirrorOS | What does the user see? |
| **Governance** | TrustByDesign | What are the safety limits? |
| **Visual** | BeaconGlyphs, Glyphtrail | How do we mark identity and continuity? |
| **Agent** | AgentDNA | How do agents preserve identity? |
| **R&D** | SanatanaTech, Gauntlet | What's experimental? |
| **Strategy** | DominancePlaybook | Where are we going? |

---

## What Layer Should I Care About?

**I'm a user**: Product layer (Active MirrorOS)

**I'm building a reflective app**: Protocol layer (MirrorDNA-Standard, MirrorDNA)

**I'm exploring symbolic AI**: Foundation layer (MirrorDNA-Lattice) and Language layer (LingOS)

**I'm interested in safety**: Governance layer (TrustByDesign)

**I'm a visual designer**: Visual layer (BeaconGlyphs, Glyphtrail)

**I'm building agents**: Agent layer (AgentDNA) and Language layer (LingOS)

**I'm a researcher**: R&D layer (SanatanaTech, Gauntlet)

---

## How to Navigate the Stack

**Bottom-up** (if you're an architect):
1. Start with MirrorDNA-Lattice (symbolic topology)
2. Read MirrorDNA-Standard (protocol spec)
3. Explore MirrorDNA (persistence implementation)
4. Try LingOS (language layer)
5. Use Active MirrorOS (product)

**Top-down** (if you're a user):
1. Try Active MirrorOS (product)
2. Explore LingOS (language layer)
3. Read MirrorDNA-Standard (protocol spec)
4. Study MirrorDNA-Lattice (symbolic topology)

**Middle-out** (if you're a developer):
1. Start with MirrorDNA-Standard (protocol spec)
2. Run the validator on your project
3. Explore examples in `/examples`
4. Dive into MirrorDNA (persistence) or LingOS (language) based on your needs

---

⟡⟦STACK⟧ · ⟡⟦MAP⟧ · ⟡⟦ARCHITECTURE⟧

*Last updated: 2025-11-14*
