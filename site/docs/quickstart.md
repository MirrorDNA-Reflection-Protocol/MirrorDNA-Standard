# Quick Start Guide

Get started with MirrorDNA in seconds or minutes, depending on your use case.

---

## For Users: Get Reflective AI Now (30 seconds)

!!! tip "Instant Reflective AI"
    No installation needed. Just copy and paste!

The fastest way to experience reflective AI is to use the Master Citation with any AI assistant.

### Steps

```bash
1. Open 00_MASTER_CITATION.md in this repository
2. Copy all text (Ctrl+A / Cmd+A, then Ctrl+C / Cmd+C)
3. Paste into your AI (ChatGPT, Claude, etc.)
4. Say: "Vault open. Load as canonical context."
```

**Done!** Your AI now has:

- :white_check_mark: Continuity protocols
- :white_check_mark: Anti-hallucination (cite-or-silence)
- :white_check_mark: Reflection over prediction behavior

### Alternative: Pastebin Mirror

Don't want to clone the repository? Use the pastebin mirror:

**[https://pastebin.com/j0MdNxrA](https://pastebin.com/j0MdNxrA)**

---

## For Developers: Validate Your Project (5 minutes)

!!! info "What You'll Get"
    - Machine-checkable compliance verification
    - Compliance badge for your README
    - Confidence that your project follows MirrorDNA standards

### 1. Install the Validator

```bash
# Clone the repository
git clone https://github.com/MirrorDNA-Reflection-Protocol/MirrorDNA-Standard.git
cd MirrorDNA-Standard

# Install dependencies
pip install -r validators/requirements.txt
```

### 2. Copy Example Configurations

Choose the compliance level that fits your project:

=== "Level 1: Basic Reflection"

    ```bash
    cp examples/minimal_project_manifest.yaml mirrorDNA_manifest.yaml
    cp examples/example_reflection_policy.yaml reflection_policy.yaml
    ```

=== "Level 2: Continuity Aware"

    ```bash
    cp examples/level2_project_manifest.yaml mirrorDNA_manifest.yaml
    cp examples/example_reflection_policy.yaml reflection_policy.yaml
    cp examples/example_continuity_profile.yaml continuity_profile.yaml
    ```

=== "Level 3: Vault-Backed Sovereign"

    ```bash
    cp examples/level3_project_manifest.yaml mirrorDNA_manifest.yaml
    cp examples/level3_reflection_policy.yaml reflection_policy.yaml
    cp examples/level3_continuity_profile.yaml continuity_profile.yaml
    ```

### 3. Edit Configurations

Update the manifest with your project details:

```bash
nano mirrorDNA_manifest.yaml
```

**Key fields to customize:**

```yaml
name: "YourProjectName"
version: "1.0.0"
description: "Your project description"
mirrorDNA_compliance_level: "level_1_basic_reflection"
maintainers:
  - name: "Your Name"
    email: "you@example.com"
repository: "https://github.com/you/your-project"
```

### 4. Run Validation

```bash
python -m validators.cli \
  --manifest mirrorDNA_manifest.yaml \
  --policy reflection_policy.yaml
```

For Level 2+, add the continuity profile:

```bash
python -m validators.cli \
  --manifest mirrorDNA_manifest.yaml \
  --policy reflection_policy.yaml \
  --profile continuity_profile.yaml
```

### 5. Get Your Badge!

If validation passes, you'll see:

```
✅ PASSED: MirrorDNA Level 1 Compliance
```

Add the badge to your README:

```markdown
![MirrorDNA Level 1](https://raw.githubusercontent.com/MirrorDNA-Reflection-Protocol/MirrorDNA-Standard/main/badges/reflective_compliance_light.svg)
```

See [badges/README.md](https://github.com/MirrorDNA-Reflection-Protocol/MirrorDNA-Standard/tree/main/badges/README.md) for all available badges.

---

## What's Next?

!!! success "Ready to Go Deeper?"

    === "Learn More"
        - [Integration Guide](integration.md) - Adopt MirrorDNA in existing projects
        - [Compliance Levels](compliance-levels.md) - Understand Level 1, 2, 3 requirements
        - [Examples](examples.md) - See working configurations

    === "Explore the Spec"
        - [Principles](principles.md) - Five immutable principles
        - [MirrorDNA Standard](mirrordna-standard.md) - Full specification
        - [Architecture](architecture.md) - How it all works

    === "Get Help"
        - [FAQ](faq.md) - Common questions
        - [Validator Guide](validators.md) - CLI usage and CI/CD integration
        - [Contributing](contributing.md) - How to contribute

---

## Quick Reference

### Three Compliance Levels

| Level | What It Means | Use When |
|-------|---------------|----------|
| **Level 1** | Basic reflection + anti-hallucination | You want cite-or-silence and explicit uncertainty |
| **Level 2** | Level 1 + continuity across sessions | You need state preservation |
| **Level 3** | Level 2 + vault sovereignty | You need user-owned, vault-backed storage |

### Core Principles

All MirrorDNA-compliant systems honor these five principles:

1. **Reflection Over Prediction** — Access actual state, don't simulate
2. **Presence Over Productivity** — Truth matters more than speed
3. **Symbolic Continuity** — Preserve identity via glyphs, checksums, vault
4. **Trust by Design** — Verification built in from the start
5. **Explicit Uncertainty** — Mark unknowns, never hide them

### Key Trust Markers

- `[Unknown]` - Information not available
- `[Speculation]` - Hypothetical content
- `⟡⟦VERIFIED⟧` - Glyph signature for verified content
- `checksum_sha256` - Integrity verification

---

!!! quote "Philosophy"
    **MirrorDNA is about truth, not speed.**

    Traditional AI predicts what comes next → hallucinations.
    MirrorDNA reflects actual state → trustworthy continuity.
