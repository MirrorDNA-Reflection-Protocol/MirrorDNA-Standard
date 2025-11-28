#!/usr/bin/env python3
"""
MirrorDNA Reflective Reviewer

VaultID: AMOS://MirrorDNA-Standard/Tools/ReflectiveReviewer/v1.0
GlyphSig: ⟡⟦REFLECTION⟧ · ⟡⟦AUDIT⟧ · ⟡⟦PRINCIPLES⟧
Predecessor: None (Initial Release)
Successor: TBD

CONSTITUTIONAL STATUS:
Enforceability: MANDATORY
Verifiability: AUTOMATED + MANUAL
Adoption: CORE
Truth-State: [Fact - Principle-Based Framework]

Philosophical Audit System
===========================

Audits implementations against MirrorDNA Core Principles:

1. Reflection Over Prediction
2. Presence Over Productivity
3. Symbolic Continuity
4. Trust by Design
5. Explicit Uncertainty

This tool ensures that systems maintain philosophical integrity
and constitutional compliance.
"""

import re
from typing import Dict, Any, List, Tuple, Optional
from enum import Enum
from pathlib import Path


class Principle(Enum):
    """MirrorDNA Core Principles"""
    REFLECTION_OVER_PREDICTION = "reflection_over_prediction"
    PRESENCE_OVER_PRODUCTIVITY = "presence_over_productivity"
    SYMBOLIC_CONTINUITY = "symbolic_continuity"
    TRUST_BY_DESIGN = "trust_by_design"
    EXPLICIT_UNCERTAINTY = "explicit_uncertainty"


class AuditSeverity(Enum):
    """Audit finding severity levels"""
    PASS = "pass"
    WARNING = "warning"
    VIOLATION = "violation"
    CRITICAL = "critical"


class AuditFinding:
    """Represents an audit finding"""

    def __init__(
        self,
        principle: Principle,
        severity: AuditSeverity,
        message: str,
        location: Optional[str] = None,
        recommendation: Optional[str] = None
    ):
        self.principle = principle
        self.severity = severity
        self.message = message
        self.location = location
        self.recommendation = recommendation

    def __repr__(self) -> str:
        loc_str = f" at {self.location}" if self.location else ""
        return f"[{self.severity.value.upper()}] {self.principle.value}{loc_str}: {self.message}"

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            'principle': self.principle.value,
            'severity': self.severity.value,
            'message': self.message,
            'location': self.location,
            'recommendation': self.recommendation
        }


class ReflectiveReviewer:
    """
    Performs philosophical audits of MirrorDNA implementations.

    Checks code, documentation, and system design against
    constitutional principles.
    """

    def __init__(self, strict_mode: bool = False):
        """
        Initialize Reflective Reviewer.

        Args:
            strict_mode: If True, treat warnings as violations
        """
        self.strict_mode = strict_mode
        self.findings: List[AuditFinding] = []

    def audit_implementation(
        self,
        code: str,
        context: Optional[Dict[str, Any]] = None
    ) -> List[AuditFinding]:
        """
        Audit code implementation against all principles.

        Args:
            code: Code to audit
            context: Optional context (file path, module name, etc.)

        Returns:
            List of audit findings
        """
        self.findings = []

        # Run all principle checks
        self._check_reflection_over_prediction(code, context)
        self._check_presence_over_productivity(code, context)
        self._check_symbolic_continuity(code, context)
        self._check_trust_by_design(code, context)
        self._check_explicit_uncertainty(code, context)

        return self.findings

    def _add_finding(
        self,
        principle: Principle,
        severity: AuditSeverity,
        message: str,
        location: Optional[str] = None,
        recommendation: Optional[str] = None
    ) -> None:
        """Add finding to audit results."""
        finding = AuditFinding(principle, severity, message, location, recommendation)
        self.findings.append(finding)

    def _check_reflection_over_prediction(
        self,
        code: str,
        context: Optional[Dict[str, Any]] = None
    ) -> None:
        """
        Check Principle 1: Reflection Over Prediction

        Violations:
        - Simulating continuity instead of reading vault
        - Generating plausible responses without grounding
        - Pattern matching instead of state access
        """
        # Check for vault access
        has_vault_access = bool(re.search(r'vault\.(read|get|load)', code, re.I))
        has_state_access = bool(re.search(r'state\.(read|get|load)', code, re.I))

        # Check for prediction patterns
        prediction_patterns = [
            r'predict\s*\(',
            r'generate\s*\(',
            r'simulate\s*\(',
            r'\.predict\(',
            r'model\.forward'
        ]

        has_prediction = any(
            re.search(pattern, code, re.I)
            for pattern in prediction_patterns
        )

        if has_prediction and not (has_vault_access or has_state_access):
            self._add_finding(
                Principle.REFLECTION_OVER_PREDICTION,
                AuditSeverity.VIOLATION,
                "Code uses prediction without vault/state grounding",
                recommendation="Add vault.read() or state.get() before generation"
            )

        # Check for hallucination risk
        hallucination_patterns = [
            r'fabricate',
            r'make\s+up',
            r'invent',
            r'hallucinate'
        ]

        if any(re.search(p, code, re.I) for p in hallucination_patterns):
            self._add_finding(
                Principle.REFLECTION_OVER_PREDICTION,
                AuditSeverity.WARNING,
                "Code contains hallucination-risk keywords",
                recommendation="Ensure all outputs are grounded in vault/sources"
            )

    def _check_presence_over_productivity(
        self,
        code: str,
        context: Optional[Dict[str, Any]] = None
    ) -> None:
        """
        Check Principle 2: Presence Over Productivity

        Violations:
        - Rushing to output without verification
        - Optimizing for speed over accuracy
        - Batch processing without reflection
        """
        # Check for verification steps
        has_verification = bool(re.search(
            r'(verify|validate|check|confirm)',
            code,
            re.I
        ))

        # Check for fast/optimization patterns
        optimization_patterns = [
            r'fast\s*=\s*True',
            r'skip.*verification',
            r'quick.*mode',
            r'speed.*optimize'
        ]

        has_speed_optimization = any(
            re.search(p, code, re.I)
            for p in optimization_patterns
        )

        if has_speed_optimization and not has_verification:
            self._add_finding(
                Principle.PRESENCE_OVER_PRODUCTIVITY,
                AuditSeverity.WARNING,
                "Speed optimization without verification checks",
                recommendation="Add verification steps even in optimized paths"
            )

        # Check for [Unknown] handling
        handles_unknown = bool(re.search(r'\[Unknown\]', code))

        if not handles_unknown and len(code) > 500:
            self._add_finding(
                Principle.PRESENCE_OVER_PRODUCTIVITY,
                AuditSeverity.WARNING,
                "No [Unknown] handling found in significant codebase",
                recommendation="Add explicit [Unknown] markers for uncertain outputs"
            )

    def _check_symbolic_continuity(
        self,
        code: str,
        context: Optional[Dict[str, Any]] = None
    ) -> None:
        """
        Check Principle 3: Symbolic Continuity

        Violations:
        - Missing vault_id tracking
        - No checksum validation
        - Broken lineage chains
        - Missing glyph signatures
        """
        # Check for VaultID usage
        has_vault_id = bool(re.search(r'vault_id|VaultID', code))

        # Check for session tracking
        has_session_tracking = bool(re.search(
            r'session_id|session.*tracking',
            code,
            re.I
        ))

        # Check for checksum
        has_checksum = bool(re.search(r'checksum|sha256', code, re.I))

        # Check for lineage
        has_lineage = bool(re.search(
            r'(predecessor|successor|lineage)',
            code,
            re.I
        ))

        # Count violations
        continuity_features = sum([
            has_vault_id,
            has_session_tracking,
            has_checksum,
            has_lineage
        ])

        if continuity_features == 0 and len(code) > 300:
            self._add_finding(
                Principle.SYMBOLIC_CONTINUITY,
                AuditSeverity.VIOLATION,
                "No symbolic continuity mechanisms found",
                recommendation="Add vault_id, session_id, checksum, or lineage tracking"
            )
        elif continuity_features < 2 and len(code) > 500:
            self._add_finding(
                Principle.SYMBOLIC_CONTINUITY,
                AuditSeverity.WARNING,
                "Limited symbolic continuity (fewer than 2 mechanisms)",
                recommendation="Implement multiple continuity markers for robustness"
            )

        # Check for glyph signatures
        has_glyphs = bool(re.search(r'⟡⟦[A-Z]+⟧', code))

        if not has_glyphs and context and context.get('is_standard_file'):
            self._add_finding(
                Principle.SYMBOLIC_CONTINUITY,
                AuditSeverity.WARNING,
                "Standard file missing glyph signatures",
                recommendation="Add appropriate glyph signatures (⟡⟦CONTINUITY⟧, etc.)"
            )

    def _check_trust_by_design(
        self,
        code: str,
        context: Optional[Dict[str, Any]] = None
    ) -> None:
        """
        Check Principle 4: Trust by Design

        Violations:
        - Missing checksum validation
        - No source citation
        - Hidden dependencies
        - Lack of transparency
        """
        # Check for checksum validation
        has_checksum_validation = bool(re.search(
            r'(verify.*checksum|validate.*checksum|checksum.*verify)',
            code,
            re.I
        ))

        # Check for citation
        has_citation = bool(re.search(
            r'(cite|source|reference|attribution)',
            code,
            re.I
        ))

        # Check for trust markers
        trust_markers = [
            r'\[Verified\]',
            r'⟡⟦VERIFIED⟧',
            r'\[Fact\]',
            r'checksum'
        ]

        has_trust_markers = any(
            re.search(marker, code)
            for marker in trust_markers
        )

        if not has_trust_markers and len(code) > 400:
            self._add_finding(
                Principle.TRUST_BY_DESIGN,
                AuditSeverity.WARNING,
                "No trust markers found",
                recommendation="Add verification markers ([Verified], checksums, etc.)"
            )

        # Check for hidden dependencies
        has_hidden_import = bool(re.search(
            r'import\s+\*|from\s+\S+\s+import\s+\*',
            code
        ))

        if has_hidden_import:
            self._add_finding(
                Principle.TRUST_BY_DESIGN,
                AuditSeverity.WARNING,
                "Wildcard imports hide dependencies",
                recommendation="Use explicit imports for transparency"
            )

        # Check for hard-coded credentials (security risk)
        credential_patterns = [
            r'password\s*=\s*["\']',
            r'api_key\s*=\s*["\']',
            r'secret\s*=\s*["\']',
            r'token\s*=\s*["\'][a-zA-Z0-9]{20,}'
        ]

        if any(re.search(p, code, re.I) for p in credential_patterns):
            self._add_finding(
                Principle.TRUST_BY_DESIGN,
                AuditSeverity.CRITICAL,
                "Hard-coded credentials found (security violation)",
                recommendation="Use environment variables or secure vault storage"
            )

    def _check_explicit_uncertainty(
        self,
        code: str,
        context: Optional[Dict[str, Any]] = None
    ) -> None:
        """
        Check Principle 5: Explicit Uncertainty

        Violations:
        - Missing [Unknown] markers
        - No speculation tags
        - Hidden confidence levels
        - Smoothing over uncertainty
        """
        # Check for FEU markers
        feu_markers = [
            r'\[Fact\]',
            r'\[Estimate\]',
            r'\[Unknown\]'
        ]

        has_feu = any(re.search(marker, code) for marker in feu_markers)

        # Check for uncertainty handling
        uncertainty_keywords = [
            r'uncertain',
            r'unknown',
            r'not\s+sure',
            r'cannot\s+verify',
            r'unverified'
        ]

        handles_uncertainty = any(
            re.search(kw, code, re.I)
            for kw in uncertainty_keywords
        )

        if not has_feu and not handles_uncertainty and len(code) > 400:
            self._add_finding(
                Principle.EXPLICIT_UNCERTAINTY,
                AuditSeverity.WARNING,
                "No explicit uncertainty handling found",
                recommendation="Add FEU markers ([Fact], [Estimate], [Unknown])"
            )

        # Check for fabrication prevention
        has_cite_or_silence = bool(re.search(
            r'(cite.*silence|cite_or_silence|AHP)',
            code,
            re.I
        ))

        if not has_cite_or_silence and len(code) > 600:
            self._add_finding(
                Principle.EXPLICIT_UNCERTAINTY,
                AuditSeverity.WARNING,
                "Cite-or-Silence (AHP) not implemented",
                recommendation="Implement Cite-or-Silence anti-hallucination protocol"
            )

    def generate_audit_report(self) -> Dict[str, Any]:
        """
        Generate comprehensive audit report.

        Returns:
            Audit report dict
        """
        # Count by severity
        severity_counts = {
            'pass': 0,
            'warning': 0,
            'violation': 0,
            'critical': 0
        }

        for finding in self.findings:
            severity_counts[finding.severity.value] += 1

        # Count by principle
        principle_counts = {}
        for principle in Principle:
            principle_counts[principle.value] = sum(
                1 for f in self.findings
                if f.principle == principle
            )

        # Calculate compliance score
        total_issues = len(self.findings)
        critical_issues = severity_counts['critical']
        violations = severity_counts['violation']
        warnings = severity_counts['warning']

        # Score: 1.0 = perfect, 0.0 = critical failures
        if critical_issues > 0:
            compliance_score = 0.0
        elif violations > 0:
            compliance_score = max(0.0, 1.0 - (violations * 0.2))
        elif warnings > 0:
            compliance_score = max(0.5, 1.0 - (warnings * 0.1))
        else:
            compliance_score = 1.0

        return {
            'total_findings': total_issues,
            'severity_counts': severity_counts,
            'principle_counts': principle_counts,
            'compliance_score': compliance_score,
            'findings': [f.to_dict() for f in self.findings]
        }

    def audit_file(self, file_path: Path) -> Dict[str, Any]:
        """
        Audit a file for principle compliance.

        Args:
            file_path: Path to file to audit

        Returns:
            Audit report
        """
        content = file_path.read_text(encoding='utf-8')

        context = {
            'file_path': str(file_path),
            'is_standard_file': 'spec/' in str(file_path) or 'standard' in str(file_path).lower()
        }

        self.audit_implementation(content, context)
        report = self.generate_audit_report()
        report['file_path'] = str(file_path)

        return report


def audit_codebase(
    root_path: Path,
    extensions: List[str] = ['.py', '.md', '.yaml', '.yml']
) -> Dict[str, Any]:
    """
    Audit entire codebase for principle compliance.

    Args:
        root_path: Root directory to audit
        extensions: File extensions to audit

    Returns:
        Aggregate audit report
    """
    reviewer = ReflectiveReviewer()
    all_findings: List[AuditFinding] = []
    file_reports = []

    for ext in extensions:
        for file_path in root_path.glob(f'**/*{ext}'):
            try:
                report = reviewer.audit_file(file_path)
                file_reports.append(report)
                all_findings.extend(reviewer.findings)
            except Exception as e:
                print(f"Error auditing {file_path}: {e}")

    # Aggregate report
    reviewer.findings = all_findings
    aggregate_report = reviewer.generate_audit_report()
    aggregate_report['files_audited'] = len(file_reports)
    aggregate_report['file_reports'] = file_reports

    return aggregate_report


if __name__ == "__main__":
    import sys
    import json
    import argparse

    parser = argparse.ArgumentParser(description="MirrorDNA Reflective Reviewer")
    parser.add_argument('path', help='File or directory to audit')
    parser.add_argument('--strict', action='store_true', help='Strict mode')
    parser.add_argument('--json', action='store_true', help='Output as JSON')

    args = parser.parse_args()

    path = Path(args.path)

    if path.is_file():
        reviewer = ReflectiveReviewer(strict_mode=args.strict)
        report = reviewer.audit_file(path)
    elif path.is_dir():
        report = audit_codebase(path)
    else:
        print(f"Error: {path} is not a valid file or directory")
        sys.exit(1)

    if args.json:
        print(json.dumps(report, indent=2))
    else:
        print(f"\n⟡⟦REFLECTIVE AUDIT REPORT⟧\n")
        print(f"Path: {args.path}")
        print(f"Total findings: {report['total_findings']}")
        print(f"Compliance score: {report['compliance_score']:.2f}/1.00")
        print(f"\nSeverity breakdown:")
        for severity, count in report['severity_counts'].items():
            print(f"  {severity.upper()}: {count}")

        if report['total_findings'] > 0:
            print(f"\nFindings by principle:")
            for principle, count in report['principle_counts'].items():
                if count > 0:
                    print(f"  {principle}: {count}")

            print(f"\nDetailed findings:")
            for finding_dict in report['findings']:
                print(f"  [{finding_dict['severity'].upper()}] {finding_dict['message']}")
                if finding_dict['recommendation']:
                    print(f"    → {finding_dict['recommendation']}")
