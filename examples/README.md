# Examples — MirrorDNA Standard

**Copy-paste ready configuration files for all compliance levels**

This folder contains working examples demonstrating how to configure MirrorDNA-compliant projects.

---

## At a Glance

**What's included:**
- ✅ **Level 1 configs** — Basic Reflection (anti-hallucination)
- ✅ **Level 2 configs** — Continuity Aware (state persistence)
- ✅ **Level 3 configs** — Vault-Backed Sovereign (full sovereignty)
- ✅ **Sample artifacts** — Example JSON outputs
- ⚠️ **Test cases** — Invalid examples for validator testing

**How to use**: Copy the files for your target compliance level, edit for your project, then run the validator.

---

## 📋 Configuration Files by Level

### Level 1: Basic Reflection

**Goal**: Anti-hallucination without persistence

**Files to copy:**
- `minimal_project_manifest.yaml` — Project metadata and compliance declaration
- `example_reflection_policy.yaml` — Cite-or-Silence and uncertainty handling

**Validation command:**
```bash
python -m validators.cli \
  --manifest minimal_project_manifest.yaml \
  --policy example_reflection_policy.yaml
```

---

### Level 2: Continuity Aware

**Goal**: State preservation across sessions

**Files to copy:**
- `level2_project_manifest.yaml` — L2 project declaration
- `example_reflection_policy.yaml` — Reflection protocols
- `example_continuity_profile.yaml` — State persistence configuration

**Validation command:**
```bash
python -m validators.cli \
  --manifest level2_project_manifest.yaml \
  --policy example_reflection_policy.yaml \
  --profile example_continuity_profile.yaml
```

---

### Level 3: Vault-Backed Sovereign

**Goal**: Full user sovereignty with vault storage

**Files to copy:**
- `level3_project_manifest.yaml` — L3 project declaration
- `level3_reflection_policy.yaml` — Full reflection policy
- `level3_continuity_profile.yaml` — Advanced continuity with vault

**Validation command:**
```bash
python -m validators.cli \
  --manifest level3_project_manifest.yaml \
  --policy level3_reflection_policy.yaml \
  --profile level3_continuity_profile.yaml
```

---

## 📦 Sample Artifacts (JSON)

### ✅ `minimal-artifact.md.json`
- **Purpose:** Shows the smallest valid artifact
- **Compliance:** Passes validation (L1)
- **Use case:** Quick reference for schema implementers

### ✅ `complete-artifact.md.json`
- **Purpose:** Fully populated artifact with lineage, consent, compliance, metadata
- **Compliance:** Passes validation (L2)
- **Use case:** Educational reference for real-world adoption

### ⚠️ `edgecase-invalid-artifact.md.json`
- **Purpose:** Deliberately broken artifact (missing required fields)
- **Compliance:** Expected to FAIL validation
- **Use case:** Ensures validator correctly rejects non-compliant artifacts

---

## 🔎 Why Keep a Failing Example?

The edge-case file proves the validator is working correctly.

**Expected CI behavior:**
- ✅ Minimal + Complete → should PASS
- ❌ Edge-case → should FAIL

This is intentional, not an error.

---

## 🚀 Quick Start

**Step 1: Choose your compliance level**
- Level 1 if you only need anti-hallucination
- Level 2 if you need state persistence
- Level 3 if you need full user sovereignty

**Step 2: Copy the relevant files**
```bash
# Example for Level 1:
cp examples/minimal_project_manifest.yaml my_project/mirrorDNA_manifest.yaml
cp examples/example_reflection_policy.yaml my_project/reflection_policy.yaml
```

**Step 3: Edit for your project**
- Update project name, version, description
- Configure vault paths (if applicable)
- Set your reflection policies

**Step 4: Validate**
```bash
cd my_project
python -m validators.cli --manifest mirrorDNA_manifest.yaml --policy reflection_policy.yaml
```

---

## 📌 Contribution Notes

**When adding new examples:**
- Always include `vault_id` and `checksum_sha256` in valid examples
- Use the `glyphsig` field to anchor symbolic continuity
- Ensure all examples pass validation before committing
- Add test cases to verify your examples work

**File naming convention:**
- `minimal_*.yaml` — Level 1 (basic)
- `level2_*.yaml` — Level 2 (continuity)
- `level3_*.yaml` — Level 3 (sovereign)

---

**For more details**, see:
- [Core Specification](../spec/mirrorDNA-standard-v1.0.md)
- [Compliance Levels](../spec/compliance_levels.md)
- [Validator Documentation](../validators/README.md)

