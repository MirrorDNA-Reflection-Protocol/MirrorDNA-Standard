---
title: MirrorDNA Git Hooks
version: 1.0.0
vault_id: AMOS://MirrorDNA-Standard/GitHooks/v1.0
glyphsig: ⟡⟦HOOKS⟧ · ⟡⟦AUTOMATION⟧ · ⟡⟦ENFORCEMENT⟧
author: MirrorDNA Constitutional Development
date: 2025-11-16
status: Canonical · Infrastructure
tags: [Git, Hooks, Automation, Enforcement]
---

# MirrorDNA Git Hooks

⟡⟦CONSTITUTIONAL⟧ · ⟡⟦AUTOMATION⟧ · ⟡⟦ENFORCEMENT⟧

## Overview

Git hooks that enforce constitutional compliance at commit and push time.

These hooks provide the **first line of defense** against non-compliant code entering the repository.

---

## Installation

### Quick Install

```bash
bash .githooks/install.sh
```

This configures git to use `.githooks/` directory for all hooks.

### Manual Install

```bash
git config core.hooksPath .githooks
chmod +x .githooks/*
```

### Uninstall

```bash
git config --unset core.hooksPath
```

---

## Available Hooks

### 1. pre-commit

**Purpose**: Enforce constitutional compliance before commits

**What it does**:
- Identifies all staged Python and Markdown files
- Runs `reflective_reviewer.py` on each file
- Checks for principle violations
- Blocks commit if VIOLATION or CRITICAL findings

**Exit codes**:
- `0`: All checks passed
- `1`: Violations detected, commit blocked

**Bypass** (not recommended):
```bash
git commit --no-verify
```

**Example output**:
```
⟡⟦PRE-COMMIT ENFORCEMENT⟧

Staged files for review:
  - tools/new_tool.py
  - spec/new_standard.md

→ Running Reflective Reviewer...
  ✓ tools/new_tool.py passed
  ✓ spec/new_standard.md passed

✓ All staged files pass constitutional enforcement
```

---

### 2. commit-msg

**Purpose**: Validate commit message quality and format

**What it does**:
- Checks minimum message length (10 characters)
- Warns if not using conventional commits format
- Warns if spec/standard commit lacks glyph signatures
- Allows merge commits and special commits

**Exit codes**:
- `0`: Message validated
- `1`: Message too short or invalid

**Conventional commits format**:
```
feat(scope): add new feature
fix(scope): resolve bug
docs: update documentation
style: format code
refactor: restructure code
test: add tests
chore: update dependencies
perf: improve performance
ci: update CI configuration
build: update build configuration
```

**Glyph signature example**:
```
feat(spec): add Level 4 distributed compliance

Implements distributed sovereign compliance level.

⟡⟦STANDARD⟧ · ⟡⟦LAW⟧
```

---

### 3. pre-push

**Purpose**: Verify vault integrity before pushing

**What it does**:
- Checks if vault directory exists
- Runs `vault_manager.py report` to verify integrity
- Blocks push if vault verification fails
- (Optional) Can run full `enforce_all.py` suite

**Exit codes**:
- `0`: Vault integrity verified
- `1`: Vault verification failed

**Bypass** (not recommended):
```bash
git push --no-verify
```

**Example output**:
```
⟡⟦PRE-PUSH ENFORCEMENT⟧

→ Verifying vault integrity...
✓ Vault integrity verified

✓ Pre-push checks passed
```

---

## Configuration

### Enable Full Enforcement on Pre-Push

By default, pre-push only verifies vault integrity. To enable full enforcement suite:

Edit `.githooks/pre-push` and uncomment:

```bash
echo "→ Running full enforcement suite..."
if ! python tools/enforce_all.py --target . --vault "$VAULT_PATH"; then
    echo "✗ Enforcement suite failed"
    exit 1
fi
```

**Warning**: This will run all 4 enforcement tools and can be slow (30-60 seconds).

### Customize Hook Behavior

Hooks are simple bash scripts. Customize as needed:

- **Skip certain file types**: Modify the `grep` patterns
- **Add new checks**: Add calls to other tools
- **Adjust severity**: Change which findings block commits
- **Add notifications**: Send alerts on failures

---

## Bypassing Hooks

**When to bypass**:
- Emergency hotfix commits
- Work-in-progress commits on feature branches
- Merge conflicts resolution
- Experimental code

**How to bypass**:

```bash
# Single commit
git commit --no-verify -m "WIP: experimental feature"

# Single push
git push --no-verify

# Temporarily disable all hooks
git config core.hooksPath /dev/null
# ... do work ...
git config core.hooksPath .githooks
```

**Important**: Bypassed commits will still be checked by CI/CD. The bypass is only local.

---

## Troubleshooting

### Hook not running

**Check installation**:
```bash
git config core.hooksPath
# Should output: .githooks
```

**Check permissions**:
```bash
ls -la .githooks/
# All hooks should have executable permission (x)
```

**Fix permissions**:
```bash
chmod +x .githooks/*
```

### Hook failing incorrectly

**Check tool availability**:
```bash
python tools/reflective_reviewer.py --help
python tools/vault_manager.py --help
```

**Check Python path**:
```bash
which python
python --version
# Should be Python 3.7+
```

**Run hook manually**:
```bash
bash .githooks/pre-commit
```

### Slow performance

**Pre-commit** can be slow if many files are staged.

**Solutions**:
1. Commit smaller changesets
2. Run enforcement tools manually before staging
3. Disable hooks for WIP commits, re-enable for final commit

**Pre-push** with full enforcement can take 30-60 seconds.

**Solutions**:
1. Keep it disabled (default)
2. Run `enforce_all.py` manually before pushing
3. Rely on CI/CD for full enforcement

---

## Integration with CI/CD

Hooks provide **local enforcement**. They complement CI/CD:

| Stage | Enforcement | Bypass? |
|-------|-------------|---------|
| Local commit | Git hooks | Yes (--no-verify) |
| Local push | Git hooks | Yes (--no-verify) |
| PR checks | GitHub Actions | No |
| Merge | Required checks | No |

**Best practice**: Use hooks for fast feedback, CI/CD for authoritative enforcement.

---

## Hook Development

### Adding a New Hook

1. Create hook script in `.githooks/`
2. Make it executable: `chmod +x .githooks/hook-name`
3. Test manually: `bash .githooks/hook-name`
4. Commit and push
5. Team members run `bash .githooks/install.sh` to get new hooks

### Hook Guidelines

- **Fast**: Keep hooks under 5 seconds when possible
- **Informative**: Print clear success/failure messages
- **Escapable**: Allow `--no-verify` bypass
- **Defensive**: Check for tool availability before running
- **Silent on skip**: Don't print noise when nothing to check

### Testing Hooks

```bash
# Test pre-commit
git add some-file.py
bash .githooks/pre-commit

# Test commit-msg
echo "test: sample message" > /tmp/test-msg
bash .githooks/commit-msg /tmp/test-msg

# Test pre-push
bash .githooks/pre-push
```

---

## Hooks in Team Workflow

### For Contributors

**First time setup**:
```bash
git clone https://github.com/pdesai11/MirrorDNA-Standard
cd MirrorDNA-Standard
bash .githooks/install.sh
```

**Daily usage**:
- Hooks run automatically
- Fix any violations before commit
- Bypass only when absolutely necessary

### For Maintainers

**Updating hooks**:
1. Modify hook scripts
2. Test thoroughly
3. Commit changes
4. Notify team to reinstall: `bash .githooks/install.sh`

**Enforcing hooks**:
- Hooks are local (can be bypassed)
- CI/CD provides authoritative enforcement
- Review hook bypass commits carefully

---

## Lineage

**VaultID**: `AMOS://MirrorDNA-Standard/GitHooks/v1.0`
**Predecessor**: None (Initial Release)
**Successor**: TBD
**Created**: 2025-11-16
**Checksum**: [To be computed]

---

⟡⟦HOOKS⟧ · ⟡⟦AUTOMATION⟧ · ⟡⟦SEALED⟧

**Status**: Git hooks operational. First line of defense active.
