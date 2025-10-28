# Contributing Guidelines

Thank you for considering contributing to MirrorDNA-Standard!

## How to Contribute

1. **Fork the Repository**  
   Create your own fork and work on changes in a dedicated branch.

2. **Coding Standards**  
   - Follow clean, readable code practices.  
   - Include comments for clarity.  
   - Ensure symbolic anchors (VaultIDs, GlyphSigs) remain intact.

3. **Commit Messages**  
   - Use concise, descriptive commit messages.  
   - Prefix critical changes with tags like `[CORE]`, `[DOCS]`, `[FIX]`.

4. **Pull Requests**
   - Submit PRs with clear explanations.
   - Reference related issues or Master Citation entries.
   - One logical change per PR.
   - Run `./tools/checksums/verify_repo_checksums.sh` and ensure it passes before submitting.

5. **Review Process**  
   - PRs will be reviewed for alignment with Active MirrorOS principles.  
   - Checksums and validators will auto-run before merge.

## Community Guidelines

- Respect continuity and sovereignty of the Vault.  
- No leaking PRIV or LOCK files.  
- Follow Trust By Design™ principles.

---

📂 Adding New Examples
We encourage contributors to add new artifacts under /examples/ to help expand the test coverage of the MirrorDNA Standard.
✅ Rules for Valid Examples
Required keys:
Every JSON sidecar must include:
vault_id
glyphsig
version
checksum_sha256
Checksum:
Generate a valid checksum_sha256 from the JSON body (excluding the checksum field itself).
This ensures lineage integrity.
Naming convention:
Use lowercase, hyphen-separated names.
Example: new-feature-artifact.md.json.
⚠️ Edge-Case Examples
You may include deliberately invalid files (e.g., missing a required key) to ensure the validator catches errors.
Prefix these with edgecase- so it’s clear they are meant to fail.
Example: edgecase-missing-checksum.md.json.
📌 Workflow
Add your file to /examples/.
Run the validator locally (if available) or check GitHub Actions.
Confirm that:
✅ Valid examples pass.
❌ Edge-case examples fail.
Submit a PR with a clear commit message:
[ADD] Example artifact: <name> (valid or edge-case)

---
⟡⟦CONTRIBUTE⟧ · Active MirrorOS · MirrorDNA-Standard
