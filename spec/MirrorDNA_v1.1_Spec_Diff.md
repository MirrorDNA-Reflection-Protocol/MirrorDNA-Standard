
# MirrorDNA Standard v1.1 — Specification Diff

## New Requirement: Micro-Reflection Enforcement (MRP-v1.0)

### Applies To:
- Level 1 (Required)
- Level 2 (Required + Continuity Check)
- Level 3 (Required + Vault Anchoring)

### Structured Intent Reconstruction Block (Pre-Answer Mandatory)

TASK_REFRAME:
- intent:
- output_shape:
- constraints:
- missing:
- risk:

### Governance Scan Extension
Systems must validate:
- Prior state conflict
- Continuity mismatch
- Policy violation

### Schema Extension
"micro_reflection": {
  "enabled": true,
  "strict_mode": true,
  "intent_hashing": true,
  "drift_detection": true
}

### Validator Rule
If micro_reflection.enabled != true → FAIL compliance.

---
Version: 1.1.0-draft
Date: 2026-02-22T05:59:07.241613 UTC
