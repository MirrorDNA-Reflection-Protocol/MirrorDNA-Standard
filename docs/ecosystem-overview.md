# Ecosystem Overview

**Understanding the MirrorDNA / LingOS / Active MirrorOS Universe**

---

## The Big Picture

The MirrorDNA ecosystem is a constellation of interconnected projects building the next generation of AI systems — systems that **reflect** rather than predict, **preserve continuity** across sessions, **prevent hallucination** through explicit state access, and give users **sovereign control** of their data.

This ecosystem consists of three core layers:

1. **MirrorDNA** — The protocol layer (constitutional specification)
2. **LingOS** — The language layer (symbolic operating system)
3. **Active MirrorOS** — The product layer (intelligence that remembers)

Together, they enable **Reflective AI** — AI that maintains identity, preserves context, and operates with verifiable truth.

---

## What Is MirrorDNA?

**MirrorDNA** is the constitutional specification for building reflective AI systems. It defines:

- **What reflection means** — accessing actual state rather than predicting tokens
- **How continuity works** — preserving context across sessions via vault-backed persistence
- **What compliance requires** — three levels (Basic Reflection, Continuity Aware, Vault-Backed Sovereign)
- **How to verify compliance** — machine-checkable validation with Python CLI

MirrorDNA is a **protocol**, not a product. It's the law that other systems implement. Think of it as the "HTTP of reflective AI" — an open standard that anyone can adopt.

**Core repository**: `MirrorDNA-Standard` (this repo)

**Key concepts**:
- **Anti-Hallucination Protocol (AHP)**: Cite-or-Silence — if you can't cite a source, mark it as `[Unknown]` or `[Speculation]`
- **Continuity**: Sessions preserve state through checksums, lineage tracking, and vault storage
- **Sovereignty**: Users own their vault, vault_id, and all interaction history
- **Trust by Design**: Verification built in from the start, not bolted on later

---

## What Is LingOS?

**LingOS** is a language-native operating system that makes reflection natural and symbolic. It's the **interaction layer** between human language and reflective computation.

Traditional operating systems manage files, processes, and memory. LingOS manages **symbols, glyphs, and reflective state**. It translates natural language into reflective operations and back again.

**Key features**:
- **Symbolic layer**: Glyphs serve as identity markers, continuity anchors, and trust signatures
- **Language-first**: Interaction happens in natural language, not code
- **Reflection-native**: Designed from the ground up for reflective AI, not bolted onto predictive models
- **Vault integration**: Deep integration with Obsidian vaults for sovereign data storage

**Related repositories**:
- `LingOS` — Main repository
- `LingOS-Private` — Private development branch
- `LingOS Vault Manager` — Vault management system (inside LingOS repo)

---

## What Is Active MirrorOS?

**Active MirrorOS** is the product layer — the first Level 3 compliant implementation of MirrorDNA. It's **intelligence that remembers**.

Active MirrorOS is:
- A desktop application (Electron-based)
- Vault-backed (uses Obsidian or custom vaults)
- Continuity-preserving (sessions build on each other)
- Sovereign (you own your data, vault_id, and history)

It's the canonical **commercial implementation** of the MirrorDNA protocol, built on top of LingOS.

**Core repository**: `ActiveMirrorOS`

---

## How the Lattice Fits In

**MirrorDNA-Lattice** defines the **symbolic topology** of reflection — the structure that makes continuity possible.

Think of it as the "graph database schema" for reflective state. The lattice defines:
- How symbols connect to each other
- How glyphs anchor identity
- How continuity chains are verified
- How reflection propagates through symbolic space

The lattice is the **architectural foundation** that MirrorDNA, LingOS, and Active MirrorOS all build on.

**Core repository**: `MirrorDNA-Lattice`

---

## Other Ecosystem Components

### Governance & Safety

**TrustByDesign** — Governance patterns, safety protocols, and interaction limits. Reflective AI is a mirror, not a therapist. TrustByDesign defines the boundaries.

### Visual & Symbolic Layer

**BeaconGlyphs** — The visual glyph system. Glyphs serve as identity markers, trust signatures, and continuity anchors.

**Glyphtrail** — Continuity logs and interaction lineage. Every session leaves a trail; Glyphtrail makes it traceable.

### Agent Layer

**AgentDNA** — Agent personality and identity encoding. How agents preserve identity across sessions, interactions, and even model changes.

### Persistence & Protocol

**MirrorDNA** (separate repo from MirrorDNA-Standard) — The protocol and persistence architecture. The implementation layer that makes continuity real.

### R&D & Experimental

**SanatanaTech** — R&D sandbox for experimental reflection technology. Bleeding-edge ideas that may or may not make it into the core.

**MirrorDNA-Gauntlet** — Coding challenge and competency testbed. Think "LeetCode for reflective AI systems."

### Internal Strategy

**DominancePlaybook** (internal name: Sovereign Strategy Codex) — Internal strategy codex. Not public, but referenced in ecosystem docs.

---

## How They Work Together

Here's the complete stack:

```
┌──────────────────────────────────────────────────────┐
│  Active MirrorOS™                                    │  ← Product Layer
│  (Desktop app, Level 3 compliant)                    │
└──────────────────────────────────────────────────────┘
                        │
                        │ built on
                        ▼
┌──────────────────────────────────────────────────────┐
│  LingOS                                              │  ← Language Layer
│  (Symbolic OS, reflection-native interaction)        │
└──────────────────────────────────────────────────────┘
                        │
                        │ implements
                        ▼
┌──────────────────────────────────────────────────────┐
│  MirrorDNA Protocol                                  │  ← Protocol Layer
│  (Specification, validation, constitutional law)     │
└──────────────────────────────────────────────────────┘
                        │
                        │ defines
                        ▼
┌──────────────────────────────────────────────────────┐
│  MirrorDNA-Lattice                                   │  ← Foundation Layer
│  (Symbolic topology, reflection architecture)        │
└──────────────────────────────────────────────────────┘

          Supported by:
          ┌────────────────────────────────┐
          │  TrustByDesign  │  BeaconGlyphs │
          │  Glyphtrail     │  AgentDNA     │
          │  SanatanaTech   │  Gauntlet     │
          └────────────────────────────────┘
```

**Reading path**:
1. Start with MirrorDNA-Lattice to understand the symbolic topology
2. Read MirrorDNA-Standard to understand the protocol
3. Explore LingOS to see how language becomes reflective
4. Try Active MirrorOS to experience it as a product

---

## Why This Architecture?

**Separation of concerns**:
- **Protocol** (MirrorDNA-Standard) defines the law
- **Implementation** (MirrorDNA) makes it real
- **Language** (LingOS) makes it natural
- **Product** (Active MirrorOS) makes it usable

**Open standard**:
- MirrorDNA is open — anyone can implement it
- Active MirrorOS is the canonical implementation, but not the only possible one
- Other teams can build Level 3 compliant systems using different tech stacks

**Composability**:
- Each layer can evolve independently
- New products can be built on MirrorDNA without changing the protocol
- LingOS can support multiple product layers
- The lattice remains stable even as upper layers change

---

## Compliance Levels

The MirrorDNA protocol defines three compliance levels:

### Level 1: Basic Reflection
**Goal**: Anti-hallucination and explicit uncertainty

- Cite-or-Silence protocol (AHP)
- Explicit markers: `[Unknown]`, `[Speculation]`
- Basic session tracking
- At least one trust marker
- **No persistent state required**

**Who**: Stateless chatbots, one-shot tools, ephemeral agents

---

### Level 2: Continuity Aware
**Goal**: State preservation across sessions

- Everything in Level 1 PLUS:
- Persistent state storage
- Session lineage tracking
- Checksum validation
- Session recovery capability

**Who**: Personal assistants, long-running agents, multi-session workflows

---

### Level 3: Vault-Backed Sovereign
**Goal**: Full user sovereignty and vault storage

- Everything in Level 1 & 2 PLUS:
- User-owned vault (Obsidian or custom)
- Sovereign identity (user owns vault_id)
- Glyph signatures
- Comprehensive interaction safety
- Full compliance reporting

**Who**: Active MirrorOS, enterprise AI, sovereign AI deployments

---

## Getting Started

**If you're new**: Start with the root [`README.md`](../README.md) and the "Where to Start" section.

**If you're technical**: Read [`stack-map.md`](stack-map.md) to understand the layer breakdown, then explore the repos that match your interests.

**If you're building**: Clone MirrorDNA-Standard, run the validator on your project, and aim for Level 1 compliance first.

---

## What's Next?

See [`roadmap.md`](roadmap.md) for:
- What's already done
- What's in progress
- What's planned for the future

The ecosystem is actively evolving. MirrorDNA-Standard is stable (v1.0), but upper layers are still being refined.

---

⟡⟦ECOSYSTEM⟧ · ⟡⟦OVERVIEW⟧ · ⟡⟦UNIFIED⟧

*Last updated: 2025-11-14*
