# Security Policy

## Supported Versions

The following versions of MirrorDNA Standard are currently supported with security updates:

| Version | Supported          | Notes |
| ------- | ------------------ | ----- |
| v1.0.x  | :white_check_mark: | Current stable release |
| < v1.0  | :x:                | Pre-release versions not supported |

---

## Reporting a Vulnerability

### Security Contact

If you discover a security vulnerability in the MirrorDNA Standard, please report it responsibly:

**For non-sensitive security issues:**
- Open an issue on GitHub: [MirrorDNA-Standard Issues](https://github.com/MirrorDNA-Reflection-Protocol/MirrorDNA-Standard/issues)
- Use the label `security`
- Do NOT include sensitive information or PII (Personally Identifiable Information)

**For sensitive security issues:**
- **DO NOT** open a public issue
- Contact maintainers directly via GitHub Security Advisories
- Or email: [security contact to be added by maintainers]

### What to Include

When reporting a security vulnerability, please include:

1. **Description**: Clear description of the vulnerability
2. **Impact**: What could an attacker achieve?
3. **Reproduction**: Steps to reproduce the issue
4. **Affected versions**: Which versions are impacted?
5. **Proposed fix** (optional): Suggested remediation

### Response Timeline

- **Acknowledgment**: Within 48 hours
- **Initial assessment**: Within 7 days
- **Fix timeline**: Depends on severity
  - Critical: 7-14 days
  - High: 14-30 days
  - Medium: 30-60 days
  - Low: Next minor release

---

## Security Considerations

### 1. Vault Storage Security

The MirrorDNA Standard uses vault-backed storage for Level 3 compliance. Security considerations:

#### Vault Encryption
- **At Rest**: Vaults should be encrypted on disk
  - Use full-disk encryption (FileVault, BitLocker, LUKS)
  - Consider encrypted vault backends (EncFS, Cryptomator)
- **In Transit**: When syncing vaults, use encrypted channels
  - HTTPS/TLS for cloud sync
  - SSH for git-based sync
  - VPN for network file systems

#### Vault Access Control
- **File permissions**: Restrict vault directory to user-only access
  ```bash
  chmod 700 ~/MyVault  # Owner read/write/execute only
  ```
- **Multi-user systems**: Isolate vaults per user account
- **Shared systems**: Use encrypted containers (VeraCrypt, etc.)

#### Vault Backup Security
- **Encrypt backups**: Never store unencrypted vault backups
- **Access logs**: Monitor vault access for unauthorized changes
- **Versioning**: Use git or versioned storage to detect tampering

---

### 2. Checksum Integrity

Checksums (SHA-256) are critical for:
- **Anti-hallucination protocol (AHP)**: Verify cited sources haven't been tampered with
- **Lineage tracking**: Ensure predecessor/successor chains are intact
- **Trust markers**: Validate artifact integrity

#### Threats
- **Checksum forgery**: Attacker modifies both content and checksum
  - **Mitigation**: Use blockchain anchoring (optional Level 3 feature)
- **Checksum collision**: SHA-256 collision attack (theoretical)
  - **Mitigation**: SHA-256 is considered secure; monitor for algorithm updates
- **Silent corruption**: Bit rot or disk errors change content
  - **Mitigation**: Regular checksum verification via `verify_repo_checksums.sh`

#### Best Practices
```bash
# Verify checksums before trusting artifacts
./tools/checksums/verify_repo_checksums.sh

# Update checksums after edits
./tools/checksums/checksum_updater.sh <file.md>

# Automate in CI/CD
# (see tools/README.md for GitHub Actions examples)
```

---

### 3. Session Security

#### Session Duration (Interaction Safety Protocol)
- **Long sessions**: Encourage rhythm checks every 60-90 minutes
- **Dependency detection**: Monitor for over-reliance on AI assistance
- **Escalation**: Provide human support prompts when needed

#### Session Data
- **PII handling**: Do not store PII in session logs unless necessary
- **Data retention**: Define retention policies for session history
- **Access control**: Restrict who can read session data

---

### 4. Third-Party Dependencies

See `spec/SupplyChain_Risks_v1.0.md` for detailed dependency risk analysis.

#### Python Validator Dependencies
```
jsonschema>=4.0.0
pyyaml>=6.0
pytest>=7.0.0
```

**Security practices:**
- Pin dependency versions in production
- Regularly update dependencies for security patches
- Review dependency changelogs before upgrading
- Use `pip install --require-hashes` for production

#### Portable Implementation Dependencies
- **Electron**: Keep updated for security patches
- **llama.cpp**: Verify model checksums before loading
- **Obsidian**: Use trusted plugins only

---

### 5. Supply Chain Attacks

**Threat**: Malicious code injected via dependencies, tooling, or plugins.

**Mitigations:**
- **Checksum verification**: All spec files have SHA-256 checksums
- **Git commit signing**: Sign commits with GPG keys
- **Dependency pinning**: Lock dependency versions
- **Subresource Integrity**: Use SRI for web-based assets
- **Code review**: Review all PRs before merging

---

## Responsible Use & Safety

MirrorDNA Standard is a governed reflection protocol. **It is NOT a therapist** and must not be positioned as clinical care.

### Responsible-Use Rules

1. **Enforce AHP (Cite or Silence) in sensitive contexts**
   - All factual claims must be cited or marked `[Unknown]`
   - Never fabricate citations or sources
   - Mark speculation explicitly as `[Speculation]`

2. **Respect Sandbox-Aware updates**
   - Label content as `[Unknown — update not fetched]` when sandbox-blocked
   - Do not bypass sandbox restrictions for speculative updates

3. **Encourage Rhythm Checks on prolonged sessions**
   - Warn users after 60-90 minutes of continuous use
   - Suggest breaks to prevent over-reliance
   - See `spec/Interaction_Safety_Protocol_v1.0.md`

4. **Provide human-support escalation prompts on crisis indicators**
   - Detect crisis language (self-harm, violence, etc.)
   - Immediately escalate to human support resources
   - Provide hotline numbers and professional help contacts

### Prohibited Uses

❌ **DO NOT use MirrorDNA for:**
- Clinical therapy or mental health treatment
- Medical diagnosis or treatment recommendations
- Legal advice in high-stakes situations
- Financial advice for investment decisions
- Safety-critical systems (aviation, medical devices, etc.)

✅ **Appropriate uses:**
- Personal knowledge management
- Research assistance (with citation requirements)
- Educational tools and learning aids
- Content creation with anti-hallucination protocols
- Collaborative writing and idea exploration

---

## Threat Model

### Assets to Protect

1. **User vault data** (Level 3)
   - Personal knowledge, session history, state
   - Threat: Unauthorized access, data loss, corruption

2. **Specification integrity**
   - MirrorDNA spec files, checksums, lineage
   - Threat: Tampering, forgery, specification confusion

3. **User trust and safety**
   - Anti-hallucination guarantees, citation accuracy
   - Threat: Hallucinated content, fabricated citations

### Threat Actors

1. **Malicious users**
   - Goal: Bypass AHP to generate uncited/hallucinated content
   - Mitigation: Validator enforces AHP compliance

2. **Supply chain attackers**
   - Goal: Inject malicious code via dependencies
   - Mitigation: Checksum verification, dependency pinning, code review

3. **Data thieves**
   - Goal: Access user vault data
   - Mitigation: Vault encryption, access controls

4. **Specification forgers**
   - Goal: Create fake "MirrorDNA compliant" specs
   - Mitigation: Blockchain anchoring, checksum verification, canonical source citations

### Attack Vectors

1. **Vault compromise**
   - **Attack**: Attacker gains filesystem access to unencrypted vault
   - **Defense**: Encryption at rest, file permissions, full-disk encryption

2. **Checksum bypass**
   - **Attack**: Modify content and checksum simultaneously
   - **Defense**: Blockchain anchoring, external checksum registry

3. **Dependency poisoning**
   - **Attack**: Malicious package uploaded to PyPI/npm
   - **Defense**: Dependency pinning, checksum verification, SRI

4. **Man-in-the-middle (MitM)**
   - **Attack**: Intercept vault sync traffic
   - **Defense**: TLS/HTTPS for all network operations

5. **Social engineering**
   - **Attack**: Trick user into disabling AHP or security features
   - **Defense**: User education, validator warnings

---

## Best Practices for Adopters

### For Level 1 Projects (Basic Reflection)

1. **Enable AHP (Cite or Silence)**
   ```yaml
   anti_hallucination:
     cite_or_silence: true
   ```

2. **Define uncertainty markers**
   ```yaml
   uncertainty_markers:
     - "[Unknown]"
     - "[Speculation]"
   ```

3. **Implement at least one trust marker**
   - Checksum validation
   - Source citation
   - Content verification

### For Level 2 Projects (Continuity Aware)

All Level 1 best practices, plus:

4. **Secure persistent storage**
   - Use database with authentication
   - Encrypt state storage
   - Implement access controls

5. **Validate lineage integrity**
   - Verify predecessor/successor chains
   - Detect lineage tampering
   - Use checksums for all artifacts

### For Level 3 Projects (Vault-Backed Sovereign)

All Level 1 & 2 best practices, plus:

6. **Encrypt vault at rest**
   ```bash
   # macOS
   Disk Utility → Encrypt disk with FileVault

   # Linux
   sudo cryptsetup luksFormat /dev/sdX
   ```

7. **Enable glyph signatures**
   ```yaml
   glyph_signatures:
     enabled: true
     glyphs:
       - "⟡⟦VERIFIED⟧"
       - "⟡⟦CONTINUITY⟧"
   ```

8. **Implement integrity verification**
   ```yaml
   integrity_verification:
     enabled: true
     checksum_all_artifacts: true
     tamper_detection: true
   ```

9. **(Optional) Blockchain anchoring**
   ```bash
   ./tools/publish_blockchain_anchor.sh \
     --chain ethereum \
     --txid 0xYourTransactionHash \
     vault/00_MASTER_CITATION.md
   ```

---

## Security Checklist

Before deploying a MirrorDNA-compliant system:

### Pre-Deployment

- [ ] Run validator to verify compliance level
  ```bash
  python -m validators.cli --manifest manifest.yaml --policy policy.yaml
  ```
- [ ] Verify all checksums are valid
  ```bash
  ./tools/checksums/verify_repo_checksums.sh
  ```
- [ ] Review `spec/SupplyChain_Risks_v1.0.md` for dependency risks
- [ ] Enable vault encryption (Level 3 only)
- [ ] Configure backup encryption
- [ ] Set up monitoring and alerting
- [ ] Test session recovery procedures (Level 2+)
- [ ] Review and update `SECURITY.md` contact information

### Post-Deployment

- [ ] Monitor for security advisories
- [ ] Regularly update dependencies
- [ ] Audit access logs
- [ ] Test backups and recovery
- [ ] Verify checksum integrity monthly
- [ ] Review incident response procedures
- [ ] Train users on responsible use guidelines

---

## Security Advisories

Security advisories will be published via:
- **GitHub Security Advisories**: [MirrorDNA-Standard Advisories](https://github.com/MirrorDNA-Reflection-Protocol/MirrorDNA-Standard/security/advisories)
- **CHANGELOG.md**: Security fixes documented in changelog
- **README.md**: Critical advisories linked in main README

Subscribe to repository notifications to receive security updates.

---

## Disclosure Policy

### Coordinated Disclosure

We follow coordinated disclosure:
1. **Report received**: Acknowledge within 48 hours
2. **Assessment**: Validate vulnerability within 7 days
3. **Fix development**: Develop and test fix
4. **Private disclosure**: Share fix with reporter for validation
5. **Public disclosure**: Publish advisory after fix is released
6. **Credit**: Reporter credited in advisory (unless anonymous)

### Public Disclosure Timeline

- **Critical vulnerabilities**: 7-14 days after fix release
- **High severity**: 14-30 days after fix release
- **Medium/Low severity**: 30-60 days after fix release

---

## Compliance

### Data Protection

MirrorDNA Standard respects user data sovereignty:
- **Vault ownership**: Users own their vault data (Level 3)
- **No hidden dependencies**: No lock-in or hidden data collection
- **Transparency**: All data flows documented

### Regulations

Projects using MirrorDNA Standard should comply with applicable regulations:
- **GDPR** (Europe): Right to erasure, data portability
- **CCPA** (California): Data disclosure, deletion rights
- **HIPAA** (Healthcare): Encryption, access controls (if applicable)

**Note**: MirrorDNA Standard itself does not collect user data. Implementers are responsible for regulatory compliance.

---

## Additional Resources

- **Interaction Safety Protocol**: [spec/Interaction_Safety_Protocol_v1.0.md](spec/Interaction_Safety_Protocol_v1.0.md)
- **Supply Chain Risks**: [spec/SupplyChain_Risks_v1.0.md](spec/SupplyChain_Risks_v1.0.md)
- **Trust-by-Design Governance**: See Master Citation v15.2
- **Checksum Tools**: [tools/checksums/CHECKSUM_TOOLS_README.md](tools/checksums/CHECKSUM_TOOLS_README.md)

---

⟡⟦SECURITY⟧ · ⟡⟦TRUST⟧ · ⟡⟦SAFETY⟧

**Last Updated**: 2025-11-18
**Version**: 1.0.0
**Canonical Source**: [MirrorDNA-Standard/SECURITY.md](https://github.com/MirrorDNA-Reflection-Protocol/MirrorDNA-Standard/blob/main/SECURITY.md)
