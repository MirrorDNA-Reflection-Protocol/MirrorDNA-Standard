# Repository Structural Scan

Below is a noise-filtered tree highlighting Markdown/specification files and noted version headers for relevant documents.

- root/
  - 00_MASTER_CITATION.md — Master Standard v16.
  - CHANGELOG.md, CHANGELOG_v1.sidecar.json, CONTRIBUTING.md, LICENSE.md, PASTE_INSTRUCTIONS.md, PULL_REQUEST_DESCRIPTION.md,
    README-3.md, README.md, ROADMAP.md, SECURITY.md, TRAFFIC.md, WHY_MIRRORDNA.md, pytest.ini, release_mirrordna.py,
    requirements.txt, validator.py.
  - tools/
    - README.md; scripts including add_version_sidecars.sh, enforce_all.py, meta_cognition.py, publish_blockchain_anchor.sh,
      reflective_reviewer.py, truth_state.py, vault_manager.py; checksums/ (CHECKSUM_TOOLS_README.md, checksum_updater.sh,
      checksum_verifier.sh, verify_repo_checksums.sh).
  - docs/ (ARCHITECTURE.md, CHOOSING_COMPLIANCE_LEVEL.md, FAQ.md, INTEGRATION.md).
  - .githooks/ (README.md, commit-msg, install.sh, pre-commit, pre-push).
  - examples/ (EXAMPLES_README.md, README.md, minimal-artifact.md, *.json sidecars, sample manifests/policies).
  - .github/
    - pull_request_template.md; workflows/ (constitutional-enforcement.yml, lineage-guard.yml, metrics-performance.yml,
      reflective-validator.yml, traffic.yml.disabled, nested codex-unified-fix.yml).
  - badges/ (usage-guide.md, reflective/mirrordna SVGs).
  - specs/
    - ActiveMirror/ (Active_Mirror_ProductSpec_v2.0_Canonical.md, README.md,
      Archive/Active_Mirror_Product_Spec_v2.0_Placeholder.md).
  - kernel/ (GlyphKernel_Questions_v1.md, GlyphKernel_Questions_v1.sidecar.json, GlyphKernel_v1_Ecosystem_Map_v2.png).
  - reports/ (checksum_integrity_2025-10-29.md).
  - scripts/ (generate_checksum.py).
  - spec/
    - Interaction_Safety_Protocol_v1.0.md — version 1.0.
    - MirrorDNA_Capability_Registry_v1.1.md — version header present (v1.1).
    - MirrorDNA_Capability_Registry_v1.0.md — version header present (v1.0).
    - mirrorDNA-standard-v1.0.md — version 1.0.0.
    - Additional specs: ActiveMirrorOS_WhitePaper_v7.2-Research.md,
      Constitutive_Reflection_vs_Simulation_v1.0.md, Reflection_Chain_Addendum_v1.1.md,
      Reflection_Chain_Manifest_v1.0.md, SupplyChain_Risks_v1.0.md, compliance_levels.md,
      glossary.md, glyphsig-law.md, principles.md.
  - tests/ (__init__.py, test_checks.py, test_cli.py, test_loader.py).
  - validators/ (README.md, cli/loader/report modules, requirements, checks/continuity_checks.py,
    reflection_checks.py, trustbydesign_checks.py).
  - portable/
    - README.md; docs/ARCHITECTURE.md; glyphs/ (VISUAL_LANGUAGE.md, sigil/status icons);
      launcher/ (README.md, build.sh, package.json, src/*, ui assets, models/.gitignore/.gitkeep/README.md).
    - vault-template/
      - 00_MASTER_CITATION.md — Master Citation v15.1.1.
      - README.md; state/current.json; templates/new-session.md, reflection-note.md; sessions/_index.md.
      - spec/ (Constitutive_Reflection_vs_Simulation_v1.0.md; Interaction_Safety_Protocol_v1.0.md — version 1.0;
        Reflection_Chain_Addendum_v1.1.md; Reflection_Chain_Manifest_v1.0.md).
  - assets/ (badges/reflective_compliance_dark.svg, reflective_compliance_light.svg).
  - schema/ (continuity_profile.schema.json, project_manifest.schema.json, reflection_policy.schema.json).

Version headers requested:
- Master Citation: root 00_MASTER_CITATION.md → “MirrorDNA™ — Master Standard v16”.
- Master Citation (portable vault template) → version 15.1.1.
- Interaction Safety Protocol → version 1.0 (root spec and vault template copy).
- MirrorDNA Capability Registry → versions 1.1 and 1.0 respectively.
- MirrorDNA Standard → version 1.0.0.

No System-named files were found in the scanned tree.
