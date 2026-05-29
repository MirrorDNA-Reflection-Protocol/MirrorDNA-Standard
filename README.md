# MirrorDNA-Standard

**Constitutional governance specification for AI systems that require verifiable compliance, anti-hallucination enforcement, and auditable continuity.**

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![MirrorDNA Compliant](badges/verified-reflective.svg)](spec/mirrorDNA-standard-v1.0.md)

---

MirrorDNA-Standard is the protocol layer of the MirrorDNA ecosystem. It defines what compliant reflective AI behavior means, provides machine-checkable JSON Schemas for configuration validation, and ships a Python CLI that verifies conformance against three graduated compliance levels.

This is a specification repository. It defines rules that products implement, not a product itself.

## What It Defines

The Standard codifies five immutable principles for v1.x:

1. **Reflection Over Prediction** -- Systems access actual state rather than simulating behavior. Outputs are grounded in verifiable sources.
2. **Continuity as Law** -- Session state is tracked, checksummed, and recoverable. Lineage is preserved across sessions.
3. **Cite or Silence** -- All factual claims must be cited or explicitly marked as unknown. Speculation is only permitted when labeled.
4. **Trust by Design** -- Verification is structural, not bolted on. Checksums validate artifact integrity. Glyph signatures provide semantic markers.
5. **Sovereign Identity** -- Users retain ownership of their vault and continuity data. No hidden dependencies or lock-in.

## Compliance Levels

Systems declare their level in a project manifest and are validated against that declaration.

| Level | Name | Requires |
|-------|------|----------|
| 1 | Basic Reflection | Anti-hallucination protocol, explicit uncertainty markers, basic session tracking, at least one trust marker |
| 2 | Continuity Aware | Everything in Level 1, plus persistent state storage, session lineage tracking, checksum validation, session recovery |
| 3 | Vault-Backed Sovereign | Everything in Levels 1 and 2, plus user-owned vault, sovereign identity binding, glyph signatures, full compliance reporting |

Detailed requirements: [`spec/compliance_levels.md`](spec/compliance_levels.md)

## Validator

The repository includes a Python CLI that checks project configurations against the Standard.

```bash
# Install
git clone https://github.com/MirrorDNA-Reflection-Protocol/MirrorDNA-Standard.git
cd MirrorDNA-Standard
pip install -r validators/requirements.txt

# Validate a Level 1 project
python -m validators.cli \
  --manifest mirrorDNA_manifest.yaml \
  --policy reflection_policy.yaml

# Validate a Level 2+ project
python -m validators.cli \
  --manifest mirrorDNA_manifest.yaml \
  --policy reflection_policy.yaml \
  --profile continuity_profile.yaml

# Machine-readable output
python -m validators.cli --manifest manifest.yaml --policy policy.yaml --json
```

The validator auto-detects actual compliance level versus declared level and returns a structured report with pass/fail status and actionable recommendations.

### Validator Architecture

```
CLI (cli.py)
  |
  v
Loader (loader.py) --- validates against JSON Schemas
  |
  v
Orchestrator (validator.py)
  |
  +--- reflection_checks.py      Level 1+ checks
  +--- continuity_checks.py      Level 2+ checks
  +--- trustbydesign_checks.py   Trust marker checks
  |
  v
Report (report.py) --- PASS / FAIL + recommendations
```

## Schemas

Eight JSON Schemas define the structural contracts for compliant configurations:

| Schema | Purpose |
|--------|---------|
| `project_manifest` | Project metadata and declared compliance level |
| `reflection_policy` | Uncertainty handling and anti-hallucination configuration |
| `continuity_profile` | Persistence and session recovery configuration |
| `identity` | Identity binding and sovereign ownership |
| `capability` | Capability declarations and constraints |
| `intent` | Intent tracking and verification |
| `ledger` | Audit ledger for compliance events |
| `dam` | Data access management |

All schemas are JSON Schema Draft-07, usable with any compliant validator in any language.

## Project Structure

```
MirrorDNA-Standard/
  spec/                       Canonical specifications (18 documents)
    mirrorDNA-standard-v1.0.md    Core specification
    principles.md                 Five immutable principles
    compliance_levels.md          L1, L2, L3 requirements
    glossary.md                   Canonical term definitions
    core_handshake.md             Protocol handshake definition
    ...
  validators/                 Python compliance checker
    cli.py                        Command-line interface
    loader.py                     YAML/JSON loading + schema validation
    validator.py                  Orchestrator
    checks/                       Modular compliance checks
  schema/                     JSON Schemas (8 schemas)
  examples/                   Working configurations for all levels
  tests/                      Pytest suite
  badges/                     SVG compliance badges for project READMEs
  tools/                      Checksum verifiers, enforcement scripts
  portable/                   Reference implementation (Electron launcher, Obsidian vault template)
  docs/                       Architecture, FAQ, integration guide
```

## CI Enforcement

Pull requests and pushes to main trigger a four-stage constitutional enforcement pipeline:

1. **Reflective Review** -- Scans specs and tools for principle violations
2. **Truth-State Enforcement** -- Validates changed markdown against anti-hallucination rules
3. **Vault Integrity** -- Verifies artifact checksums when a vault directory exists
4. **Compliance Validation** -- Runs the validator CLI against any manifests in the tree

Critical violations block merge. Results are posted as PR comments with full reports.

## Ecosystem Position

```
+-----------------------------------------------+
|  Products (ActiveMirrorOS, third-party apps)  |   Implement the standard
+-----------------------------------------------+
|  MirrorDNA-Standard (this repository)         |   Define the standard
|  Specification + Validator + Schemas           |
+-----------------------------------------------+
|  MirrorDNA (protocol implementation)          |   SDKs and protocol schemas
+-----------------------------------------------+
```

[MirrorDNA](https://github.com/MirrorDNA-Reflection-Protocol/MirrorDNA) provides the protocol implementation (Python and TypeScript SDKs). This repository provides the governance layer that defines what compliance means and how to verify it. The standard is open -- any system can implement it.

## Testing

```bash
pip install -r validators/requirements.txt

# Full suite
pytest tests/ -v

# Individual modules
pytest tests/test_checks.py -v
pytest tests/test_cli.py -v
pytest tests/test_loader.py -v
```

## Contributing

See [`CONTRIBUTING.md`](CONTRIBUTING.md). Key requirements:

- All specs under `/spec` follow lineage tracking (predecessor/successor fields)
- Run validators before submitting a pull request
- Run checksum verification: `./tools/checksums/verify_repo_checksums.sh`
- Follow AHP: cite or mark as unknown -- no ungrounded claims

## Documentation

- [Specification](spec/mirrorDNA-standard-v1.0.md) -- The full standard
- [Principles](spec/principles.md) -- Five foundational, immutable principles
- [Compliance Levels](spec/compliance_levels.md) -- Detailed L1, L2, L3 requirements
- [Architecture](docs/ARCHITECTURE.md) -- Repository design and component interaction
- [Integration Guide](docs/INTEGRATION.md) -- How to adopt MirrorDNA in your project
- [FAQ](docs/FAQ.md) -- Common questions
- [Glossary](spec/glossary.md) -- Canonical term definitions

## License

MIT. See [LICENSE](LICENSE) for terms.

---

Built by [Active Mirror](https://activemirror.ai). Governed AI for institutional work.
