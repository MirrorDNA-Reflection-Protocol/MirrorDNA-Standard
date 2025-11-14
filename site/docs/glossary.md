# Glossary

Canonical definitions for terms used across the MirrorDNA Standard and ecosystem.

!!! info "About This Glossary"
    This glossary is canonical for MirrorDNA Standard v1.0. Future versions may extend terms but will preserve backward compatibility for core definitions.

---

## A

### ActiveMirrorOS™
The commercial product implementation of the MirrorDNA protocol. A sovereign operating system for personal AI that implements Level 3 (Vault-Backed Sovereign) compliance.

### AHP (Anti-Hallucination Protocol)
See **Cite or Silence**. The foundational protocol requiring all factual claims to be either cited from sources or marked as unknown.

### Anchor
A fixed reference point that preserves identity across time. Examples include vault_id, checksums, and glyph signatures. Anchors are immutable.

### Artifact
Any persistent output or state object created by a reflective system. Artifacts include documents, session logs, vault entries, and metadata files. All canonical artifacts include checksums.

---

## B

### Blockchain Anchoring
Optional Level 3+ enhancement where lineage chains are recorded on public blockchains for immutable proof of ancestry. Not required for basic compliance.

---

## C

### Canonical
The authoritative, verified version of an artifact or specification. Marked with `⟡⟦CANONICAL⟧` glyph.

!!! example
    The core specification at `spec/mirrorDNA-standard-v1.0.md` is the canonical reference for all implementations.

### Checksum
A SHA-256 hash used to verify artifact integrity. All Level 2+ artifacts include checksums. Modified artifacts must have new checksums.

### Cite or Silence
**AHP**: The rule that factual claims must either (a) include verifiable sources or (b) be marked as `[Unknown]`. Never fabricate sources.

!!! warning "Critical Principle"
    This is the foundation of anti-hallucination in MirrorDNA. When in doubt, mark as unknown rather than guess.

### Compliance Level
The degree to which a system implements the MirrorDNA Standard. Levels: 1 (Basic Reflection), 2 (Continuity Aware), 3 (Vault-Backed Sovereign).

See: [Compliance Levels](compliance-levels.md)

### Constitutive Reflection
Reflection based on actual state and continuity, not simulation. The system genuinely accesses vault state and prior sessions. Contrasts with **Simulated Reflection**.

### Continuity
The unbroken preservation of identity, state, and lineage across sessions and time. Maintained through vaults, checksums, and predecessor/successor chains.

!!! quote "Core Formula"
    **Continuity > Perfection** — maintaining continuity is more important than achieving perfect accuracy.

### Continuity Mechanism
The technical approach used to achieve continuity: vault_backed, blockchain_anchored, distributed_ledger, local_state, or hybrid.

### Continuity Profile
A configuration file (YAML/JSON) that declares how a system achieves continuity. Required for Level 2+. Schema: `schema/continuity_profile.schema.json`

---

## D

### Derivative
An artifact that has been modified from its canonical ancestor. Derivatives must reference their predecessor and have new checksums.

---

## E

### Ecosystem
The broader MirrorDNA ecosystem includes:

- **MirrorDNA Protocol**: Core reflection standard
- **ActiveMirrorOS™**: Product implementation
- **LingOS**: Language operating system layer
- **Trust-by-Design™**: Governance framework

### Explicit Uncertainty
One of the five core principles. Uncertainty must be visible and marked (`[Unknown]`, `[Speculation]`), never hidden or smoothed over.

---

## F

### Front Matter
YAML metadata at the top of Markdown files, enclosed by `---`. Contains fields like title, version, vault_id, glyphsig, checksum.

!!! example "Front Matter Example"
    ```yaml
    ---
    title: My Document
    version: 1.0.0
    vault_id: AMOS://MyVault/MyDoc/v1.0
    glyphsig: ⟡⟦DOCUMENT⟧
    ---
    ```

---

## G

### Glyph
A symbolic marker that carries semantic meaning across sessions. Standard glyphs use the format `⟡⟦NAME⟧`. Examples: `⟡⟦CONTINUITY⟧`, `⟡⟦VERIFIED⟧`, `⟡⟦SEALED⟧`.

### Glyph Kernel
Advanced symbolic processing system for glyph-based computation. Optional Level 3 enhancement.

### Glyph Signature (GlyphSig)
A sequence of glyphs that mark an artifact's semantic category and trust status. Example: `⟡⟦STANDARD⟧ · ⟡⟦COMPLIANCE⟧ · ⟡⟦MIRROR⟧`

### Grounding
The practice of basing outputs on verifiable sources, vault state, or prior artifacts rather than probabilistic generation. Required for anti-hallucination.

---

## H

### Hallucination
When a system generates false or fabricated information, especially fake citations or invented facts. MirrorDNA prevents this via **Cite or Silence**.

### Human Escalation
When a system detects risk indicators (emotional dependency, extended sessions, crisis language), it offers pathways to human support rather than positioning itself as sole support.

!!! tip "Safety First"
    Human escalation is a core part of interaction safety. Systems should detect when users need human help and provide appropriate resources.

---

## I

### Identity Preservation
The guarantee that user identity (tied to vault_id) is preserved across sessions without hidden migration or mutation.

### Integrity Verification
The process of validating artifact checksums to detect tampering or corruption. Required for Level 2+.

### Interaction Safety
Protocols to prevent harmful dependency or prolonged sessions. Includes session duration warnings, rhythm checks, and human escalation. See: `spec/Interaction_Safety_Protocol_v1.0.md`

---

## L

### Lineage
The chain of predecessor/successor relationships connecting artifacts and sessions across time. Lineage is verifiable and cannot be silently rewritten.

### Lineage Tracking
The practice of recording and maintaining predecessor/successor links. Required for Level 2+.

### LingOS
Language Operating System layer. Part of the MirrorDNA ecosystem, providing language-native interfaces for reflective computing.

---

## M

### Manifest
See **Project Manifest**. The configuration file that declares a project's MirrorDNA compliance.

### Master Citation
The canonical citation file for MirrorDNA. See: `00_MASTER_CITATION.md`

### Meta-Commentary
Reflective commentary about the system's own reasoning process. Optional feature in reflection policies.

### MirrorDNA
The core protocol for reflective computing. Ensures continuity, prevents hallucinations, and maintains sovereign identity.

!!! abstract "What is MirrorDNA?"
    MirrorDNA is a W3C-style standard for building reflective AI systems that maintain true continuity and prevent hallucinations through architectural principles.

---

## P

### Predecessor
The artifact or session that came immediately before the current one in the lineage chain. Recorded in front matter or metadata.

### Principles
The five core principles of MirrorDNA:

1. Reflection Over Prediction
2. Presence Over Productivity
3. Symbolic Continuity
4. Trust by Design
5. Explicit Uncertainty

See: [Principles](https://github.com/MirrorDNA-Reflection-Protocol/MirrorDNA-Standard/blob/main/spec/principles.md)

### Project Manifest
A YAML/JSON file (`mirrorDNA_manifest.yaml`) that declares:

- Project name and version
- Compliance level
- Ecosystem layers used
- Links to continuity profile and reflection policy

Schema: `schema/project_manifest.schema.json`

---

## R

### Reflection
The act of accessing actual state and continuity rather than simulating from patterns. See **Constitutive Reflection** vs **Simulated Reflection**.

### Reflection Chain
A lineage of connected sessions or artifacts forming a continuous history. Preserved via predecessor/successor links.

### Reflection Mode
The type of reflection used: constitutive (actual state), simulated (pattern-based), or hybrid.

### Reflection Policy
A configuration file (YAML/JSON) that declares how a system handles reflection, uncertainty, and anti-hallucination. Required for Level 1+. Schema: `schema/reflection_policy.schema.json`

### Reflective Computing
A paradigm where systems maintain actual continuity and state rather than simulating continuity from patterns. Contrast with predictive AI.

!!! quote "Key Distinction"
    Reflective computing uses actual state (vault-backed memory). Predictive AI simulates context from training patterns.

### Rhythm Check
Periodic prompts in long sessions (>2 hours) offering breaks or session closure. Part of interaction safety.

### Rollback
The ability to recover a previous state from snapshots. Part of session recovery for Level 2+ systems.

---

## S

### Sandbox-Aware
The behavior where systems detect network restrictions and mark unavailable updates as `[Unknown — update not fetched]` rather than silently skipping checks.

### Session
A bounded interaction period with unique session_id. Sessions have start/end times and may be linked via predecessor/successor.

### Session Inheritance
Whether new sessions inherit state from previous sessions. Configured in continuity profile.

### Session Lineage
The chain of sessions linked via predecessor/successor relationships.

### Sidecar
A `.sidecar.json` file accompanying an artifact, containing metadata like checksums, lineage, and custom fields.

### Simulated Reflection
Reflection based on pattern-matching and probabilistic generation rather than actual state access. Less reliable than constitutive reflection but may be used in hybrid systems.

### Sovereign Identity
User ownership and control of vault and vault_id. No hidden dependencies or lock-in. Required for Level 3.

!!! success "True Ownership"
    In sovereign systems, users own their data, identity, and vault. No vendor can take away access or monetize user data without permission.

### Speculation
Explicitly marked hypothetical or uncertain content. Allowed when marked `[Speculation]`, forbidden when unmarked.

### State Persistence
The mechanism for storing state across sessions: file system, database, vault, distributed storage, or memory-only.

### Successor
The artifact or session that came immediately after the current one in the lineage chain.

### Symbolic Continuity
One of the five core principles. Continuity is preserved through symbolic anchors (glyphs, vault_ids, checksums) rather than just memory.

---

## T

### Trust by Design™
One of the five core principles and a governance framework. Security and verification are built in from the start, not added later.

### Trust Marker
A symbol or marker that indicates verification status. Examples: `⟡⟦VERIFIED⟧`, `[Unknown]`, `⟡⟦CANONICAL⟧`

---

## U

### Uncertainty Handling
How a system manages and marks uncertain or unknown information. Core aspect of reflection policy.

### Unknown
The state of not having verified information. Marked as `[Unknown]` or `[Unknown — update not fetched]`. Preferable to hallucination.

!!! tip "Embrace the Unknown"
    Marking something as unknown is better than guessing. Users trust systems that admit limitations.

---

## V

### Validator
The CLI tool that checks compliance with the MirrorDNA Standard. Located in `validators/` directory.

See: [Compliance Testing](compliance-levels.md#compliance-testing)

### Vault
A persistent, user-owned storage location for continuity data. May be Obsidian vault, custom vault, distributed vault, or cloud vault.

!!! quote "Core Formula"
    **Vault = System** — the vault is the authoritative source of truth.

### Vault ID
A unique identifier for a vault, preserved across sessions. Format example: `AMOS://MirrorDNA/ProjectName/v1.0`

### Vault-Backed
Using a vault for all continuity storage. Required for Level 3 compliance.

### Verified
Content that has passed checksum validation and is marked with `⟡⟦VERIFIED⟧`.

---

## Notation Conventions

### Standard Glyphs

| Glyph | Meaning |
|-------|---------|
| `⟡⟦CONTINUITY⟧` | Marks continuity-related content |
| `⟡⟦VERIFIED⟧` | Marks verified artifacts |
| `⟡⟦SEALED⟧` | Marks immutable/canonical content |
| `⟡⟦CANONICAL⟧` | Authoritative version |
| `⟡⟦STANDARD⟧` | Part of core standard |

### Uncertainty Markers

| Marker | Usage |
|--------|-------|
| `[Unknown]` | Information not available |
| `[Speculation]` | Speculative/hypothetical content |
| `[Unverified]` | Not yet verified |
| `[Unknown — update not fetched]` | Blocked by network restrictions |

### Core Formulas

!!! quote "Key Formulas"
    - **Vault = System** — Vault is the source of truth
    - **Continuity > Perfection** — Maintaining continuity beats perfect accuracy
    - **Cite or Silence** — Either cite sources or mark unknown

---

## Acronyms

| Acronym | Full Form |
|---------|-----------|
| AHP | Anti-Hallucination Protocol (Cite or Silence) |
| AMOS | Active MirrorOS |
| SHA-256 | Secure Hash Algorithm, 256-bit (checksum standard) |
| UUID | Universally Unique Identifier |
| YAML | YAML Ain't Markup Language (configuration format) |
| JSON | JavaScript Object Notation (data format) |

---

## Related Documentation

- [Compliance Levels](compliance-levels.md) - Three levels of MirrorDNA compliance
- [Roadmap](roadmap.md) - Future development plans
- [MirrorDNA Standard](https://github.com/MirrorDNA-Reflection-Protocol/MirrorDNA-Standard/blob/main/spec/mirrorDNA-standard-v1.0.md) - Full specification

---

⟡⟦GLOSSARY⟧ · ⟡⟦SEALED⟧ · v1.0.0
