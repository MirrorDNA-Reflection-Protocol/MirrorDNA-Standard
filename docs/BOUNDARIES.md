# MirrorDNA-Standard — Scope Boundaries

This document defines what this repository owns and what it explicitly delegates to other components.

---

## This Repository Owns

| Domain | Description |
|--------|-------------|
| **Protocol Primitives** | Identity object, reflection gate, capability tokens, ledger entries, intent envelopes |
| **JSON Schemas** | Canonical schema definitions for all protocol objects |
| **Specification** | Formal spec documents (v1.0, v1.1 diff, core handshake, MRP, DAM) |
| **Compliance Levels** | Level 1 (Reflection Enforced), Level 2 (Continuity Enforced), Level 3 (Sovereign Enforcement) |
| **Conformance Validation** | Python validator CLI and compliance test definitions |
| **Badges** | SVG compliance badges for implementors |

## This Repository Does NOT Own

| Domain | Owner | Notes |
|--------|-------|-------|
| **Governance Controls** | [TrustByDesign](https://github.com/MirrorDNA-Reflection-Protocol/TrustByDesign) | Policy enforcement, governance profiles, transparency/auditability runtime |
| **Runtime / Lattice** | Lattice / ActiveMirrorOS | Execution environment, agent orchestration, multi-agent mesh |
| **Identity Authority** | active-mirror-identity | User-owned identity issuance and management |
| **Vault Storage** | MirrorDNA-Vault | Knowledge mesh, note storage, session reports |
| **Product Layer** | ActiveMirrorOS | Commercial implementation of Level 3 compliance |

## Boundary Rules

1. **No runtime logic in this repo.** This repo defines *what* must be enforced, not *how* to enforce it at runtime.
2. **No governance policy files.** Governance profiles are referenced by schema but defined and enforced in TrustByDesign.
3. **No ecosystem dependencies.** The protocol must be implementable without any MirrorDNA ecosystem component.
4. **Schemas are the contract.** If a primitive is not in a schema, it is not part of the protocol.
5. **Specs are normative.** Files under `spec/` define required behavior. Files under `docs/` are informational.

---

*Version: 1.1.0-draft*
*Date: 2026-02-22*
