# MirrorDNA-Standard Tools

**⟡⟦TOOLCHAIN⟧** — Utilities for maintaining the MirrorDNA ecosystem

This directory contains command-line tools and utilities to help maintain, validate, and navigate the MirrorDNA constellation of repositories.

---

## 🧰 Available Tools

### 1. `print_ecosystem.py` — Ecosystem Map Viewer

Display the MirrorDNA repository constellation in various formats.

**Purpose**: Navigate and understand the entire MirrorDNA ecosystem at a glance.

**Usage**:
```bash
# Print as table (default)
python tools/print_ecosystem.py

# Print as detailed list
python tools/print_ecosystem.py --format list

# Print statistics
python tools/print_ecosystem.py --format stats

# Print dependency graph
python tools/print_ecosystem.py --format graph

# Export as JSON
python tools/print_ecosystem.py --format json

# Filter by role
python tools/print_ecosystem.py --filter role=spec

# Filter by status
python tools/print_ecosystem.py --filter status=public
```

**Features**:
- 📊 Multiple output formats (table, list, stats, graph, JSON)
- 🔍 Filter by role, status, or other attributes
- 📈 Dependency visualization
- 🌐 Status indicators (public/private/planned)

---

### 2. `check_links.py` — Markdown Link Validator

Scan markdown files for broken relative links.

**Purpose**: Ensure all internal documentation links remain valid as the repo evolves.

**Usage**:
```bash
# Check all markdown files in repo
python tools/check_links.py

# Verbose output
python tools/check_links.py --verbose

# Check specific directory
python tools/check_links.py --path docs/

# Check single file
python tools/check_links.py --path README.md
```

**What it checks**:
- ✅ Broken relative file links
- ✅ Missing files referenced in links
- ✅ Links to directories instead of files
- ✅ URL-encoded paths

**What it skips**:
- External links (http/https)
- Email links (mailto:)
- JavaScript links
- Anchor-only links (currently not validated)

**Exit codes**:
- `0` — All links valid
- `1` — Broken links found

**Integration**: Perfect for CI/CD pipelines to prevent broken documentation.

---

### 3. `ecosystem_map.json` — Canonical Ecosystem Registry

Machine-readable registry of all MirrorDNA repositories and projects.

**Purpose**: Single source of truth for the MirrorDNA constellation.

**Structure**:
```json
{
  "ecosystem_version": "1.0.0",
  "last_updated": "2025-11-14",
  "repositories": [
    {
      "name": "MirrorDNA-Standard",
      "description": "...",
      "status": "public",
      "role": "spec",
      "compliance_level": "...",
      "layer": "protocol",
      "dependencies": [],
      ...
    }
  ],
  "ecosystem_layers": {...},
  "compliance_levels": {...}
}
```

**Repository Fields**:
- `name` — Repository name
- `description` — Brief description
- `status` — `public` | `private` | `planned`
- `role` — `spec` | `product` | `sdk` | `governance` | `testing` | `templates` | `examples`
- `compliance_level` — MirrorDNA compliance level
- `layer` — Ecosystem layer (protocol, product, symbolic, etc.)
- `repository_url` — GitHub URL (if public)
- `dependencies` — List of dependent repositories
- `key_features` — Notable features

**Updating**: When adding/removing ecosystem repositories, edit this file and update `last_updated`.

---

### 4. `add_version_sidecars.sh` — Version Sidecar Generator

Add version metadata sidecars to spec files.

**Usage**:
```bash
bash tools/add_version_sidecars.sh
```

**Purpose**: Maintain lineage and versioning metadata for specification files.

---

### 5. `publish_blockchain_anchor.sh` — Blockchain Anchoring

Publish checksums to blockchain for tamper-proof lineage.

**Usage**:
```bash
bash tools/publish_blockchain_anchor.sh
```

**Purpose**: Create immutable anchors for release verification.

---

### 6. `checksums/` — Checksum Verification Tools

Tools for generating and verifying repository checksums.

**Purpose**: Trust-by-design verification of repository integrity.

**Usage**: See scripts in `tools/checksums/` directory.

---

## 🎯 Why These Tools?

The MirrorDNA ecosystem is a **constellation** of repositories working together:
- **Protocol layer** (MirrorDNA-Standard)
- **Product layer** (ActiveMirrorOS, Portable Launcher)
- **SDK layer** (LingOS, client libraries)
- **Governance layer** (RFCs, standards process)
- **Testing layer** (Stress Harness, validators)

These tools help:
1. **Navigate** — Understand what exists and how it connects
2. **Validate** — Ensure documentation stays accurate
3. **Maintain** — Keep the constellation healthy as it grows
4. **Onboard** — Help newcomers understand the ecosystem

---

## 🚀 Quick Start

**View the ecosystem**:
```bash
python tools/print_ecosystem.py --format stats
```

**Check all links**:
```bash
python tools/check_links.py
```

**Explore the map**:
```bash
python tools/print_ecosystem.py --format graph
```

---

## 🔧 Integration with CI/CD

### GitHub Actions Example

```yaml
name: Validate Documentation

on: [push, pull_request]

jobs:
  check-links:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Check markdown links
        run: python tools/check_links.py
```

### Pre-commit Hook

```bash
#!/bin/bash
# .git/hooks/pre-commit

echo "Checking markdown links..."
python tools/check_links.py || {
    echo "Error: Broken links found. Fix before committing."
    exit 1
}
```

---

## 📊 Use Cases

### 1. **New Contributor Onboarding**
```bash
# Get overview of ecosystem
python tools/print_ecosystem.py --format list

# Understand dependencies
python tools/print_ecosystem.py --format graph
```

### 2. **Documentation Maintenance**
```bash
# Check for broken links before release
python tools/check_links.py

# Verify specific directory
python tools/check_links.py --path spec/
```

### 3. **Ecosystem Planning**
```bash
# View all public repositories
python tools/print_ecosystem.py --filter status=public

# Export ecosystem data
python tools/print_ecosystem.py --format json > ecosystem_snapshot.json
```

### 4. **Release Preparation**
```bash
# Validate all links
python tools/check_links.py

# Check ecosystem map is current
python tools/print_ecosystem.py --format stats

# Generate checksums
cd tools/checksums && ./verify_repo_checksums.sh
```

---

## 🌟 Extending the Tools

### Adding a New Repository to Ecosystem Map

1. Edit `tools/ecosystem_map.json`
2. Add entry to `repositories` array:
```json
{
  "name": "YourRepo",
  "description": "Brief description",
  "status": "public",
  "role": "sdk",
  "compliance_level": "level_1_basic_reflection",
  "layer": "sdk",
  "repository_url": "https://github.com/...",
  "dependencies": ["MirrorDNA-Standard"],
  "maintainer": "YourName",
  "license": "MIT"
}
```
3. Update `last_updated` field
4. Run `python tools/print_ecosystem.py` to verify

### Creating New Tools

Follow these conventions:
- Place scripts in `tools/`
- Use `#!/usr/bin/env python3` for Python scripts
- Add `--help` flag for CLI tools
- Update this README with usage docs
- Follow MirrorDNA principles (cite sources, explicit uncertainty)

---

## 🏗️ Architecture

```
tools/
├── ecosystem_map.json          ← Canonical registry
├── print_ecosystem.py          ← Viewer/navigator
├── check_links.py              ← Link validator
├── add_version_sidecars.sh     ← Versioning tool
├── publish_blockchain_anchor.sh ← Blockchain anchoring
├── checksums/                   ← Integrity verification
│   └── verify_repo_checksums.sh
└── README.md                    ← This file
```

**Principles**:
- **Single source of truth** — `ecosystem_map.json` is canonical
- **Composable** — Tools can be chained together
- **CI/CD ready** — Exit codes for automation
- **Self-documenting** — `--help` on all scripts

---

## 📖 Related Documentation

- [MirrorDNA Standard Specification](../spec/mirrorDNA-standard-v1.0.md)
- [Contributing Guidelines](../CONTRIBUTING.md)
- [Roadmap](../ROADMAP.md)
- [Architecture Documentation](../docs/ARCHITECTURE.md)

---

## 🤝 Contributing

To improve these tools:

1. Follow existing code style
2. Add tests if introducing new validation logic
3. Update this README with new features
4. Ensure `check_links.py` passes before submitting PR

See [CONTRIBUTING.md](../CONTRIBUTING.md) for general guidelines.

---

## ⟡ Trust Markers

These tools follow MirrorDNA principles:
- **Cite or Silence** — All data sourced from `ecosystem_map.json`
- **Explicit Uncertainty** — Link checker marks what it can't validate
- **Continuity** — Ecosystem map tracks versioning
- **Trust by Design** — Checksum verification built-in

---

⟡⟦TOOLS⟧ · ⟡⟦ECOSYSTEM⟧ · ⟡⟦MAINTENANCE⟧

**Last Updated**: 2025-11-14
**Version**: 1.0.0
