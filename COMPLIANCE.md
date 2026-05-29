# Compliance & Regulatory Mapping

## Overview

This project is part of the Active Mirror governed AI ecosystem, built by N1 Intelligence (OPC) Pvt Ltd. All components are designed for deployment in regulated industries where AI accountability is a legal requirement.

## Regulatory Frameworks

### EU AI Act (Regulation 2024/1689)

| Requirement | Implementation | Location |
|---|---|---|
| Risk classification | High-risk classification support for BFSI, health, civic | Architecture docs |
| Conformity assessment | Auto-generated from deployment telemetry via MirrorGate | `docs.activemirror.ai` |
| Technical documentation | Model cards, data sheets, governance artifacts | Generated at runtime |
| Human oversight | Decision logs with human-in-the-loop checkpoints | Audit chain middleware |
| Transparency | Structured JSON logging, explainable decisions | Logging layer |
| Accuracy & robustness | Continuous bias monitoring, confidence scoring | Inference pipeline |

### India Digital Personal Data Protection Act (DPDP 2023)

| Requirement | Implementation | Location |
|---|---|---|
| Consent management | Purpose-specific consent capture and storage | MirrorSeed identity layer |
| Data localisation | Sovereign deployment models (air-gap, edge, VPC) | Deployment config |
| Purpose limitation | Policy-driven inference routing | MirrorGate proxy |
| Data principal rights | Erasure, correction, grievance redressal interfaces | API endpoints |
| Data breach notification | Automated incident detection and notification | Monitoring pipeline |

### SOC 2 Type II Control Mapping

| Trust Service Criteria | Control | Status |
|---|---|---|
| CC6.1 — Logical access | Ed25519 identity, no shared credentials | Implemented |
| CC6.2 — System operations | Structured logging, health monitoring | Implemented |
| CC6.3 — Change management | Git-based config, signed commits, PR reviews | Implemented |
| CC7.1 — Risk assessment | Continuous bias auditing, confidence scoring | Implemented |
| CC8.1 — Monitoring | Real-time dashboards (MirrorDash), alert pipelines | Implemented |

### ISO 27001:2022 Annex A Mapping

| Control | Implementation |
|---|---|
| A.5.1 Information security policies | Governance-by-construction, policy-as-code |
| A.8.2 Privileged access rights | Ed25519 key management, role-based access |
| A.8.5 Secure authentication | MirrorSeed deterministic identity |
| A.8.9 Configuration management | MANIFEST.yaml, body lattice sync |
| A.8.15 Logging | Hash-linked audit chains, structured JSON |
| A.8.16 Monitoring | MirrorDash cognitive dashboards |

## Cryptographic Standards

| Component | Standard | Usage |
|---|---|---|
| Identity signing | Ed25519 (RFC 8032) | All model outputs, decision logs, governance artifacts |
| Audit chain | SHA-256 hash linking | Immutable, verifiable audit trails |
| Key derivation | Deterministic from seed | MirrorSeed identity layer |

## Evidence Generation

Compliance evidence is generated continuously from production telemetry, not assembled before audits:

- **Model cards**: Auto-generated per deployment
- **Audit trails**: Hash-linked, tamper-evident
- **Decision logs**: Per-inference with reasoning chain
- **Bias reports**: Continuous monitoring with drift detection
- **Consent records**: Per-interaction with purpose binding

## Contact

- **Compliance inquiries**: paul@activemirror.ai
- **Security vulnerabilities**: security@n1intelligence.com
- **Entity**: N1 Intelligence (OPC) Pvt Ltd, Goa, India

---

*Part of the [Active Mirror Ecosystem](https://activemirror.ai) · [N1 Intelligence (OPC) Pvt Ltd](https://github.com/MirrorDNA-Reflection-Protocol)*
