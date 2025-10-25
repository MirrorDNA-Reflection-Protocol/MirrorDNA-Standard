# Examples — MirrorDNA Standard

This folder contains **reference artifacts** used to test and demonstrate the MirrorDNA Standard validator.

---

## 📂 Files

### ✅ `minimal-artifact.md.json`
- **Purpose:** Shows the **smallest valid artifact**.
- **Compliance:** Passes validation (L1).
- **Use case:** Quick reference for schema implementers.

---

### ✅ `complete-artifact.md.json`
- **Purpose:** Demonstrates a **fully populated artifact** with lineage, consent, compliance, and metadata.
- **Compliance:** Passes validation (L2).
- **Use case:** Educational and reference for real-world adoption.

---

### ⚠️ `edgecase-invalid-artifact.md.json`
- **Purpose:** Deliberately broken artifact (e.g., missing checksum).
- **Compliance:** Expected to **fail validation**.
- **Use case:** Ensures the validator correctly rejects non-compliant artifacts.

---

## 🔎 Why Keep a Failing Example?

The **edge-case file** exists to prove the validator is working.  
When CI runs:
- ✅ Minimal + Complete → should pass  
- ❌ Edge-case → should fail  

This is intentional, not an error.

---

## 📌 Contribution Notes
- Always include a **VaultID** and **checksum_sha256** in valid examples.  
- Use the **glyphsig** field to anchor symbolic continuity.  
- Add new examples in the same style if you want to demonstrate other compliance tiers.

