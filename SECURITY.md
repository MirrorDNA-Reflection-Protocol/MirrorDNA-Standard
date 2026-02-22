# Security Policy

## Supported Versions

| Version | Supported |
|---------|-----------|
| 1.x     | Yes       |
| < 1.0   | No        |

## Reporting a Vulnerability

If you discover a security vulnerability in the MirrorDNA protocol specification, schemas, validator, or reference implementation, please report it responsibly.

**DO NOT** open a public GitHub issue for security vulnerabilities.

### Contact

Email: **security@activemirror.ai**

### What to Include

- Description of the vulnerability
- Steps to reproduce (if applicable)
- Affected component (schema, validator, spec, runtime)
- Severity assessment (Critical / High / Medium / Low)

### Response Timeline

- **Acknowledgement**: Within 48 hours of receipt
- **Initial Assessment**: Within 5 business days
- **Resolution Target**: Within 30 days for Critical/High severity

### Severity Definitions

| Severity | Description |
|----------|-------------|
| **Critical** | Allows identity spoofing, ledger tampering, or capability escalation |
| **High** | Bypasses reflection gate, breaks hash chain integrity, or enables silent drift |
| **Medium** | Validator false-positive/negative, schema validation bypass |
| **Low** | Documentation errors, non-exploitable edge cases |

### Policy

- Vulnerabilities exposing user identity data or enabling unconsented identity drift are treated as Critical.
- We follow coordinated disclosure. Please allow 90 days before public disclosure.
- Contributors who report valid vulnerabilities will be credited (unless anonymity is requested).

## Architecture Note

MirrorDNA is designed as a local-first protocol. The user holds identity keys and data. This architectural choice mitigates many classes of remote exploitation.
