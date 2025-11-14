# MirrorDNA Ecosystem Maintenance Toolkit

This directory contains tools to help maintain coherence across the MirrorDNA ecosystem repositories.

## Tools

### 1. `ecosystem_map.json`

A structured JSON file that maps all repositories in the MirrorDNA ecosystem with metadata:

- **name**: Repository name
- **visibility**: `public` or `private`
- **role**: Repository role (`spec`, `product`, `sdk`, `docs`, `playground`, `r&d`)
- **description**: Short description of the repository's purpose

This file serves as the single source of truth for the ecosystem structure.

### 2. `print_ecosystem.py`

Displays a formatted view of the ecosystem map, grouped by role with statistics.

#### Usage

```bash
python tools/print_ecosystem.py
```

#### Output

- Repositories grouped by role (Specifications, Products, SDKs, etc.)
- Visibility indicators for each repository
- Summary statistics (total count, public/private breakdown, count by role)

#### Example

```
================================================================================
                          MirrorDNA ECOSYSTEM MAP
================================================================================

SPECIFICATIONS
--------------------------------------------------------------------------------
  🔓 MirrorDNA-Reflection-Protocol        [ public]
     Reflection protocol specifications and reference implementations

  🔓 MirrorDNA-Standard                   [ public]
     Core specification and standard definitions for MirrorDNA protocol

...
```

### 3. `check_markdown_links.py`

Scans all markdown files in the repository and checks for broken relative links.

#### Usage

```bash
python tools/check_markdown_links.py
```

#### What it checks

- Markdown-style links: `[text](url)`
- HTML-style links: `<a href="url">`
- Reference-style links: `[ref]: url`

#### What it reports

- Files containing relative links
- Specific line numbers of broken links
- Summary statistics of the scan

#### Example output

```
================================================================================
                          MARKDOWN LINK CHECK
================================================================================

📄 docs/getting-started.md
   ❌ Line 15: ./missing-file.md
   ❌ Line 42: ../non-existent.md

================================================================================
                               SUMMARY
================================================================================

  Total markdown files scanned:    25
  Files with relative links:       12
  Total relative links checked:    89
  Broken links found:              2

  ⚠️  2 broken link(s) found!
```

## Maintenance Workflows

### Updating the Ecosystem Map

When adding or removing repositories from the ecosystem:

1. Edit `ecosystem_map.json`
2. Add/remove/update repository entries
3. Run `print_ecosystem.py` to verify the changes
4. Commit the updated map

### Regular Link Checking

Before releases or major documentation updates:

1. Run `check_markdown_links.py`
2. Fix any broken links reported
3. Re-run to verify all links are valid

### Cross-Repository Coherence

Use these tools to:

- Ensure all repositories are documented in the ecosystem map
- Verify documentation links remain valid as the codebase evolves
- Maintain a clear picture of the ecosystem structure

## Requirements

- Python 3.6 or higher (no external dependencies required)

## Future Enhancements

Potential additions to this toolkit:

- Version compatibility checker across SDKs
- License compliance validator
- README.md template consistency checker
- Cross-repository dependency graph generator
- Automated changelog aggregator
