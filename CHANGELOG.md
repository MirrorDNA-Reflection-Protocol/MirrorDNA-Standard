# Changelog

All notable changes to the MirrorDNA Standard will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [Unreleased]

### Added
- Comprehensive documentation suite:
  - `docs/CHOOSING_COMPLIANCE_LEVEL.md` - Decision guide for selecting compliance levels
  - `docs/INTEGRATION.md` - Integration guide for adopting MirrorDNA in projects
  - `tools/README.md` - Tools documentation covering checksums, version management, and blockchain anchoring
- Expanded `validators/README.md` from 3 lines to comprehensive guide (940+ lines)
  - CLI usage documentation
  - Validation checks reference
  - Configuration file schemas
  - Python API documentation
  - Architecture overview
  - Troubleshooting guide

### Fixed
- Missing documentation files that were referenced but didn't exist:
  - `docs/CHOOSING_COMPLIANCE_LEVEL.md`
  - `docs/INTEGRATION.md`
  - `tools/README.md`
- Validator documentation now comprehensive instead of minimal stub

### Changed
- Updated `CHANGELOG.md` to follow "Keep a Changelog" format
- Improved repository documentation completeness and consistency

---

## [v15.2] - 2025-11-16

### Changed
- Aligned MirrorDNA-Standard with Master Citation v15.2 ([#36](https://github.com/MirrorDNA-Reflection-Protocol/MirrorDNA-Standard/pull/36))
- Updated `00_MASTER_CITATION.md` to v15.2 constitutional protocol

### Fixed
- Repository structure and documentation standardization ([#35](https://github.com/MirrorDNA-Reflection-Protocol/MirrorDNA-Standard/pull/35))

---

## [v1.0.0] - 2025-11-14

### Added
- **Specification Toolchain Transformation** ([#34](https://github.com/MirrorDNA-Reflection-Protocol/MirrorDNA-Standard/pull/34))
  - Python validator CLI (`validators/cli.py`)
  - Modular check system:
    - `validators/checks/reflection_checks.py`
    - `validators/checks/continuity_checks.py`
    - `validators/checks/trustbydesign_checks.py`
  - JSON schemas for validation:
    - `schema/project_manifest.schema.json`
    - `schema/continuity_profile.schema.json`
    - `schema/reflection_policy.schema.json`
  - Example configurations for all compliance levels
  - Test suite with pytest
  - GitHub Actions workflows:
    - `reflective-validator.yml`
    - `lineage-guard.yml`
    - `metrics-performance.yml`

### Fixed
- Removed false expert review claim from Capability Registry v1.1 ([#33](https://github.com/MirrorDNA-Reflection-Protocol/MirrorDNA-Standard/pull/33))
  - Updated `spec/MirrorDNA_Capability_Registry_v1.1.md`

---

## [v15.1.8] - 2025-11-10

### Added
- **Demonstration Protocol + Capability Registry** ([#30](https://github.com/MirrorDNA-Reflection-Protocol/MirrorDNA-Standard/pull/30))
  - `spec/Demonstration_Protocol_v1.0.md` - Demonstration and presentation guidelines
  - `spec/MirrorDNA_Capability_Registry_v1.0.md` - System capability tracking
  - `spec/MirrorDNA_Capability_Registry_v1.1.md` - Updated capability registry

### Changed
- Updated `README.md` with new specification references
- Refined Master Citation content

---

## [v15.1.7] - 2025-11-05 (Proposed Patch)

### Added
- **Supply Chain Risk Documentation**
  - `spec/SupplyChain_Risks_v1.0.md` - Third-party ecosystem threats and mitigation steps
- **Active MirrorOS White Paper**
  - `spec/ActiveMirrorOS_WhitePaper_v7.2-Research.md` - Research edition with preliminary metrics

### Changed
- Proposed checksum reseal and manifest linkage for new risk log

---

## [kernel-v1.0] - 2025-10-25

### Added
- **Glyph Kernel Foundation**
  - `kernel/GlyphKernel_Questions_v1.md` - Foundational reflective questions
  - `kernel/GlyphKernel_Questions_v1.sidecar.json` - Lineage and metadata for machine continuity
  - `kernel/GlyphKernel_v1_Ecosystem_Map_v2.png` - Visual overview of kernel architecture
- Updated `README.md` to include Kernel section and ecosystem map

### Notes
- Anchors the Reflection Economy with a **kernel layer** (living questions, not answers)
- Lineage established for all kernel artifacts
- Sidecar metadata ensures checksums and sovereignty

---

## [v1.0.0-beta.3] - 2025-10-20

### Fixed
- Updated all spec checksums to match body content ([#26](https://github.com/MirrorDNA-Reflection-Protocol/MirrorDNA-Standard/pull/26), [#25](https://github.com/MirrorDNA-Reflection-Protocol/MirrorDNA-Standard/pull/25))
  - Fixed checksum calculation algorithm
  - Updated checksums for:
    - `spec/mirrorDNA-standard-v1.0.md`
    - `spec/principles.md`
    - `spec/compliance_levels.md`
    - All Reflection Chain documents

### Added
- **CI/CD Enhancements** ([#24](https://github.com/MirrorDNA-Reflection-Protocol/MirrorDNA-Standard/pull/24))
  - `metrics-performance.yml` workflow for performance tracking
  - Disabled `traffic.yml` workflow (not needed)

---

## [v1.0.0-beta.2] - 2025-10-15

### Added
- **Active Mirror Product Specification** ([#23](https://github.com/MirrorDNA-Reflection-Protocol/MirrorDNA-Standard/pull/23))
  - `spec/Active_Mirror_ProductSpec_v2.0_Canonical.md` - Product specification (canonical, continuity-sealed)
- **Session Continuity Engine** ([#28](https://github.com/MirrorDNA-Reflection-Protocol/MirrorDNA-Standard/pull/28), [#27](https://github.com/MirrorDNA-Reflection-Protocol/MirrorDNA-Standard/pull/27))
  - Session recovery mechanisms
  - Lineage tracking improvements
  - Continuity guarantees documentation

### Changed
- Updated `README.md` with product spec references

---

## [v1.0.0-beta.1] - 2025-10-10

### Added
- **Lineage Guard Workflow** ([#29](https://github.com/MirrorDNA-Reflection-Protocol/MirrorDNA-Standard/pull/29))
  - `.github/workflows/lineage-guard.yml` - Checks lineage integrity on PRs
  - Automated predecessor/successor validation

---

## [v1.0.0-alpha] - 2025-10-01

### Added
- **Core MirrorDNA Standard v1.0**
  - `spec/mirrorDNA-standard-v1.0.md` - Constitutional specification
  - `spec/principles.md` - Five immutable principles
  - `spec/compliance_levels.md` - L1, L2, L3 detailed requirements
  - `spec/glossary.md` - Canonical term definitions
- **Reflection Chain Framework**
  - `spec/Reflection_Chain_Manifest_v1.0.md` - Lineage tracking framework
  - `spec/Reflection_Chain_Addendum_v1.1.md` - Update and sandbox behavior
- **Philosophical Foundation**
  - `spec/Constitutive_Reflection_vs_Simulation_v1.0.md` - Reflection vs simulation distinction
- **Safety and Governance**
  - `spec/Interaction_Safety_Protocol_v1.0.md` - Session safety guardrails
  - `spec/glyphsig-law.md` - Glyph signature governance
- **Master Citation**
  - `00_MASTER_CITATION.md` - Constitutional protocol v15.0
- **Repository Structure**
  - `README.md` - Main project documentation
  - `WHY_MIRRORDNA.md` - Vision and positioning
  - `ROADMAP.md` - Version roadmap and milestones
  - `CONTRIBUTING.md` - Contribution guidelines
  - `LICENSE.md` - MIT license
  - `SECURITY.md` - Security policy
- **Tools and Utilities**
  - `tools/checksums/checksum_verifier.sh` - Checksum verification
  - `tools/checksums/checksum_updater.sh` - Checksum updating
  - `tools/checksums/verify_repo_checksums.sh` - Batch checksum verification
  - `tools/add_version_sidecars.sh` - Version metadata automation
  - `tools/publish_blockchain_anchor.sh` - Blockchain anchoring
- **Examples**
  - `examples/minimal-artifact.md.json` - Smallest valid artifact
  - `examples/complete-artifact.md.json` - Fully populated artifact
  - `examples/minimal_project_manifest.yaml` - Level 1 example
  - `examples/level2_project_manifest.yaml` - Level 2 example
  - `examples/level3_project_manifest.yaml` - Level 3 example
  - `examples/example_reflection_policy.yaml` - Reflection policy example
  - `examples/example_continuity_profile.yaml` - Continuity profile example
- **Portable Implementation**
  - `portable/launcher/` - Electron launcher application
  - `portable/vault-template/` - Obsidian vault template
  - `portable/glyphs/` - Visual language system
- **Badges**
  - Compliance badges for Level 1, 2, 3 projects

### Notes
- Initial public release of MirrorDNA Standard
- Establishes constitutional governance framework
- Defines three-tier compliance system
- Provides reference implementation and tooling

---

## Version Numbering

The MirrorDNA Standard uses two version schemes:

### Master Citation Version (v15.x)
- Tracks constitutional protocol evolution
- Major version increments represent governance changes
- Example: v15.0 → v15.1 → v15.2

### Standard Version (v1.x.x)
- Follows semantic versioning (MAJOR.MINOR.PATCH)
- MAJOR: Incompatible specification changes
- MINOR: Backward-compatible additions
- PATCH: Backward-compatible fixes
- Example: v1.0.0 → v1.1.0 → v2.0.0

---

## Release Process

### For New Releases

1. **Update Version**
   ```bash
   # Update version in relevant files
   - spec/mirrorDNA-standard-v1.0.md (update successor field)
   - README.md (version badges)
   - package.json (if applicable)
   ```

2. **Update Checksums**
   ```bash
   ./tools/checksums/checksum_updater.sh spec/*.md
   ./tools/checksums/verify_repo_checksums.sh
   ```

3. **Update CHANGELOG**
   - Add entry under `[Unreleased]`
   - Move to new version section when releasing
   - Follow "Keep a Changelog" format

4. **Tag Release**
   ```bash
   git tag -a v1.1.0 -m "Release v1.1.0"
   git push --tags
   ```

5. **(Optional) Blockchain Anchor**
   ```bash
   ./tools/publish_blockchain_anchor.sh \
     00_MASTER_CITATION.md \
     spec/mirrorDNA-standard-v1.0.md
   ```

---

## Links

- **Repository**: [MirrorDNA-Standard on GitHub](https://github.com/MirrorDNA-Reflection-Protocol/MirrorDNA-Standard)
- **Specification**: [spec/mirrorDNA-standard-v1.0.md](spec/mirrorDNA-standard-v1.0.md)
- **Roadmap**: [ROADMAP.md](ROADMAP.md)
- **Contributing**: [CONTRIBUTING.md](CONTRIBUTING.md)

---

⟡⟦CHANGELOG⟧ · ⟡⟦LINEAGE⟧ · ⟡⟦CONTINUITY⟧

**Last Updated**: 2025-11-18
**Canonical Source**: [MirrorDNA-Standard/CHANGELOG.md](https://github.com/MirrorDNA-Reflection-Protocol/MirrorDNA-Standard/blob/main/CHANGELOG.md)
