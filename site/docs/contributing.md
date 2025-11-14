# Contributing Guidelines

Thank you for considering contributing to MirrorDNA-Standard!

---

## How to Contribute

### 1. Fork the Repository

Create your own fork and work on changes in a dedicated branch.

```bash
# Fork on GitHub, then clone
git clone https://github.com/YOUR-USERNAME/MirrorDNA-Standard.git
cd MirrorDNA-Standard

# Create a feature branch
git checkout -b feature/your-feature-name
```

---

### 2. Coding Standards

#### General Principles

- **Clean, readable code** - Follow best practices for your language
- **Include comments** - Explain complex logic
- **Preserve symbolic anchors** - VaultIDs, GlyphSigs must remain intact

#### Python (validators/)

```python
# Good: Clear, documented
def check_cite_or_silence(policy):
    """
    Verify that cite-or-silence protocol is enabled.

    Args:
        policy (dict): Reflection policy configuration

    Returns:
        tuple: (status, message) where status is "PASSED" or "FAILED"
    """
    if not policy.get("uncertainty_handling", {}).get("cite_or_silence"):
        return ("FAILED", "cite_or_silence must be enabled")
    return ("PASSED", "Cite-or-silence protocol enabled")
```

#### YAML/JSON (configs)

```yaml
# Good: Well-structured, commented
# Example MirrorDNA Reflection Policy
# Suitable for Level 1 and Level 2 projects

policy_version: "1.0.0"

# Reflection mode: constitutive (actual state) or simulated
reflection_mode: "constitutive"

# How uncertainty is handled
uncertainty_handling:
  cite_or_silence: true  # Required for all levels
  unknown_marker: "[Unknown]"
```

---

### 3. Commit Messages

Use **concise, descriptive commit messages**.

#### Format

```
[TAG] Brief description

Detailed explanation if needed.
Explains why the change was made.
```

#### Tags

| Tag | Use For |
|-----|---------|
| `[CORE]` | Changes to core specifications |
| `[DOCS]` | Documentation updates |
| `[FIX]` | Bug fixes |
| `[TEST]` | Test additions or modifications |
| `[TOOL]` | Tooling and automation updates |
| `[BADGE]` | Badge-related changes |

#### Examples

```bash
# Good
git commit -m "[DOCS] Add examples for Level 2 continuity profiles"

git commit -m "[FIX] Correct schema validation for manifest version field

The validator was rejecting valid semantic versions like '1.0.0-beta'.
Updated regex pattern to accept pre-release versions per semver spec."

git commit -m "[CORE] Update compliance_levels.md with Level 2 requirements"

# Bad
git commit -m "fixed stuff"
git commit -m "update"
```

---

### 4. Pull Requests

#### Before Submitting

1. **Run the validator** - Ensure configs pass

```bash
python -m validators.cli \
  --manifest examples/minimal_project_manifest.yaml \
  --policy examples/example_reflection_policy.yaml
```

2. **Run checksum verification**

```bash
./tools/checksums/verify_repo_checksums.sh
```

3. **Run tests**

```bash
pytest tests/ -v
```

#### PR Guidelines

- **Clear title** - Describe what the PR does
- **Reference issues** - Link to related issues or Master Citation entries
- **One logical change per PR** - Don't combine unrelated changes
- **Include tests** - Add tests for new features
- **Update docs** - Document new features or changes

#### PR Template

```markdown
## Description
Brief description of what this PR does.

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Documentation update
- [ ] Code refactoring
- [ ] Other (specify)

## Changes Made
- Change 1
- Change 2
- Change 3

## Testing
- [ ] All tests pass (`pytest tests/ -v`)
- [ ] Validator passes on examples
- [ ] Checksums verified
- [ ] Manual testing performed

## Related Issues
Fixes #123
Related to #456

## Checklist
- [ ] Code follows style guidelines
- [ ] Self-review completed
- [ ] Comments added for complex code
- [ ] Documentation updated
- [ ] Tests added/updated
- [ ] All checks pass
```

---

### 5. Review Process

PRs will be reviewed for:

- **Alignment with MirrorDNA principles**
- **Code quality and clarity**
- **Test coverage**
- **Documentation completeness**
- **Checksum and validator compliance**

**Auto-checks** will run before merge:

- Schema validation
- Compliance checks
- Test suite
- Checksum verification

---

## Community Guidelines

### Respect Continuity and Sovereignty

- **Respect the vault** - Don't break continuity
- **No leaking PRIV or LOCK files** - Keep private data private
- **Follow Trust-by-Design™** - Maintain verification and auditability

### Code of Conduct

- **Be respectful** - Treat everyone with respect
- **Be constructive** - Offer helpful feedback
- **Be patient** - Remember everyone is learning
- **Be inclusive** - Welcome diverse perspectives

---

## Adding New Examples

We encourage contributors to add new artifacts under `/examples/` to expand test coverage.

### Rules for Valid Examples

#### Required Fields

Every example must include:

```yaml
# For manifest files
name: "ProjectName"
version: "1.0.0"
mirrorDNA_compliance_level: "level_X_..."
reflection_policy: "policy.yaml"

# For JSON sidecars
{
  "vault_id": "AMOS://...",
  "glyphsig": "⟡⟦...⟧",
  "version": "1.0.0",
  "checksum_sha256": "abc123..."
}
```

#### Checksum

Generate a valid `checksum_sha256` from the content:

```bash
# For JSON files
cat file.json | jq 'del(.checksum_sha256)' | shasum -a 256

# For YAML files
cat file.yaml | shasum -a 256
```

This ensures **lineage integrity**.

#### Naming Convention

- **Lowercase, hyphen-separated** names
- **Descriptive** of what the example demonstrates

**Examples:**

- `minimal-artifact.md`
- `level2-continuity-profile.yaml`
- `chatbot-reflection-policy.yaml`

### Edge-Case Examples

You may include **deliberately invalid files** to ensure the validator catches errors.

**Prefix these with `edgecase-`:**

- `edgecase-missing-checksum.md.json`
- `edgecase-invalid-level.yaml`

These should **fail validation** (that's the point).

### Workflow

1. **Add your file** to `/examples/`

```bash
cp my-example.yaml examples/my-example.yaml
```

2. **Test locally**

```bash
# Valid example should pass
python -m validators.cli \
  --manifest examples/my-example.yaml \
  --policy examples/example_reflection_policy.yaml

# Edge-case example should fail
python -m validators.cli \
  --manifest examples/edgecase-invalid.yaml \
  --policy examples/example_reflection_policy.yaml
```

3. **Update README**

Add entry to `examples/README.md`:

```markdown
### ✅ `my-example.yaml`
- **Purpose:** Demonstrates feature X
- **Compliance:** Level 2
- **Use case:** Shows how to configure Y
```

4. **Submit PR**

```bash
git add examples/my-example.yaml examples/README.md
git commit -m "[EXAMPLES] Add example for feature X"
git push origin feature/add-example
```

---

## Contribution Areas

### Documentation

- **Fix typos** - Even small fixes are welcome
- **Improve clarity** - Make docs easier to understand
- **Add examples** - Show real-world usage
- **Translate** - Help make MirrorDNA accessible globally

### Code

- **Fix bugs** - Check [Issues](https://github.com/MirrorDNA-Reflection-Protocol/MirrorDNA-Standard/issues)
- **Add tests** - Improve test coverage
- **Enhance validator** - Add new compliance checks
- **Optimize performance** - Speed improvements welcome

### Specifications

- **Propose improvements** - Open an issue first to discuss
- **Clarify ambiguities** - Help make the spec clearer
- **Add use cases** - Document real-world scenarios

### Examples and Templates

- **Share configs** - Your working configurations help others
- **Document patterns** - Common integration patterns
- **Case studies** - How you use MirrorDNA in practice

---

## Development Setup

### Local Development

```bash
# Clone
git clone https://github.com/MirrorDNA-Reflection-Protocol/MirrorDNA-Standard.git
cd MirrorDNA-Standard

# Install dependencies
pip install -r validators/requirements.txt

# Run tests
pytest tests/ -v

# Run validator on examples
python -m validators.cli \
  --manifest examples/minimal_project_manifest.yaml \
  --policy examples/example_reflection_policy.yaml
```

### Running Tests

```bash
# All tests
pytest tests/ -v

# Specific test file
pytest tests/test_checks.py -v

# With coverage
pytest tests/ --cov=validators --cov-report=html

# Watch mode (requires pytest-watch)
ptw tests/
```

### Code Style

```bash
# Python formatting (if using Black)
black validators/ tests/

# Linting (if using flake8)
flake8 validators/ tests/

# Type checking (if using mypy)
mypy validators/
```

---

## Proposing New Features

### New Compliance Level

Want to propose Level 4?

1. **Open a GitHub issue** with:
   - **Use case** - Why is it needed?
   - **Requirements** - What does it check?
   - **Backward compatibility** - Doesn't break L1-L3?

2. **Draft specification** - Write the requirements clearly

3. **Community discussion** - Get feedback and consensus

4. **Implementation** - Add checks, schemas, examples

5. **Version bump** - New levels = minor version (v1.1.0)

### New Compliance Check

1. **Identify the requirement** - What should be checked?

2. **Write the check function**

```python
# validators/checks/my_checks.py
def check_my_feature(config):
    """Check if feature X is implemented."""
    if not config.get("feature_x"):
        return ("FAILED", "Feature X is required for Level Y")
    return ("PASSED", "Feature X detected")
```

3. **Add test**

```python
# tests/test_my_checks.py
def test_my_feature_check():
    config = {"feature_x": True}
    status, message = check_my_feature(config)
    assert status == "PASSED"
```

4. **Update docs**

```markdown
### Feature X Check

**Requirement:** Projects must implement feature X

**Level:** 2+

**Fix:** Add `feature_x: true` to your manifest
```

---

## Release Process

(For maintainers)

### Version Bumps

- **Patch (1.0.1)** - Bug fixes, typos
- **Minor (1.1.0)** - New features, new checks
- **Major (2.0.0)** - Breaking changes

### Checklist

- [ ] All tests pass
- [ ] All examples validate
- [ ] Checksums verified
- [ ] CHANGELOG.md updated
- [ ] Version numbers updated
- [ ] Git tag created
- [ ] GitHub release published

---

## Recognition

All contributors will be:

- **Listed in CONTRIBUTORS.md**
- **Credited in release notes**
- **Mentioned in relevant documentation**

Significant contributions may be recognized with:

- **Co-author credit** in commit messages
- **Special thanks** in release announcements
- **Maintainer status** (for ongoing contributors)

---

## Getting Help

### Questions?

- **GitHub Discussions** - For general questions
- **GitHub Issues** - For bugs or feature requests
- **Documentation** - Check [docs/](https://github.com/MirrorDNA-Reflection-Protocol/MirrorDNA-Standard/tree/main/docs)

### Stuck?

Open an issue with:

- What you're trying to do
- What you've tried
- Where you're stuck

We're here to help!

---

## License

By contributing, you agree that your contributions will be licensed under the **MIT License**.

See [LICENSE](https://github.com/MirrorDNA-Reflection-Protocol/MirrorDNA-Standard/blob/main/LICENSE) for details.

---

## Thank You!

Every contribution, no matter how small, helps make MirrorDNA better for everyone.

**⟡⟦CONTRIBUTE⟧** · Active MirrorOS · MirrorDNA-Standard

---

!!! quote "Community-Driven"
    MirrorDNA is built by the community, for the community. Your contributions shape the future of reflective AI.
