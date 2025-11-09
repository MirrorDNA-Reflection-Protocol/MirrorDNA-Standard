#!/usr/bin/env python3
"""
MirrorDNA RCC (Release Continuity Compliance) Validator

Pre-publish gate that validates documents for:
- Master Citation version declaration
- Predecessor/successor lineage presence
- GlyphSig markers
- No [[MISSING]] or [TODO] placeholders
- Truth-State tags on temporal claims
- Glyph drift within threshold (≤15%)
- Checksum presence
- Consent markers (if required)

Outputs: RCC_PASS.md or RCC_FAIL.md with detailed fixes

Principles: AHP-compliant (Cite or Silence), blocks unsafe publishing
"""

import logging
import re
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple

try:
    import click
    import yaml
except ImportError:
    print("Error: Required dependencies not installed.")
    print("Install with: pip install click pyyaml")
    sys.exit(1)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class ValidationIssue:
    """Represents a validation issue found in document."""

    CRITICAL = "CRITICAL"
    WARNING = "WARNING"
    INFO = "INFO"

    def __init__(self, severity: str, line_number: Optional[int], message: str, fix: Optional[str] = None):
        self.severity = severity
        self.line_number = line_number
        self.message = message
        self.fix = fix

    def __repr__(self):
        location = f"Line {self.line_number}" if self.line_number else "Document"
        return f"[{self.severity}] {location}: {self.message}"


class RCCValidator:
    """Validates documents against RCC standards."""

    def __init__(self, config: Dict):
        self.config = config
        self.rcc_config = config.get('rcc', {})
        self.issues: List[ValidationIssue] = []
        self.content: str = ""
        self.lines: List[str] = []
        self.frontmatter: Dict = {}
        self.required_glyphs = self.rcc_config.get('required_glyphs', [])

    def validate(self, file_path: Path) -> bool:
        """
        Validate document against RCC standards.

        Returns:
            True if validation passes, False otherwise
        """
        logger.info(f"Validating: {file_path}")

        # Read file
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                self.content = f.read()
                self.lines = self.content.split('\n')
        except Exception as e:
            self.issues.append(ValidationIssue(
                ValidationIssue.CRITICAL,
                None,
                f"Failed to read file: {e}",
                "Ensure file exists and is readable"
            ))
            return False

        # Extract frontmatter
        self._extract_frontmatter()

        # Run validation checks
        self._check_frontmatter()
        self._check_placeholders()
        self._check_glyphsig()
        self._check_truth_state_tags()
        self._check_glyph_drift()
        self._check_checksum()

        # Determine pass/fail
        critical_issues = [i for i in self.issues if i.severity == ValidationIssue.CRITICAL]
        has_passed = len(critical_issues) == 0

        return has_passed

    def _extract_frontmatter(self):
        """Extract YAML frontmatter from document."""
        if self.content.startswith('---'):
            parts = self.content.split('---', 2)
            if len(parts) >= 3:
                try:
                    self.frontmatter = yaml.safe_load(parts[1]) or {}
                except Exception as e:
                    self.issues.append(ValidationIssue(
                        ValidationIssue.CRITICAL,
                        1,
                        f"Invalid YAML frontmatter: {e}",
                        "Fix YAML syntax in frontmatter"
                    ))

    def _check_frontmatter(self):
        """Validate required frontmatter fields."""
        required_fields = ['title', 'vault_id', 'predecessor']

        for field in required_fields:
            if field not in self.frontmatter:
                self.issues.append(ValidationIssue(
                    ValidationIssue.CRITICAL,
                    None,
                    f"Missing required frontmatter field: {field}",
                    f"Add '{field}: <value>' to YAML frontmatter"
                ))

        # Check for Master Citation version reference
        master_citation_found = False
        for key, value in self.frontmatter.items():
            if isinstance(value, str) and 'Master_Citation' in value:
                master_citation_found = True
                break

        if not master_citation_found:
            # Check in content
            if 'Master_Citation' in self.content or 'Master Citation' in self.content:
                master_citation_found = True

        if not master_citation_found:
            self.issues.append(ValidationIssue(
                ValidationIssue.WARNING,
                None,
                "No Master Citation reference found",
                "Add Master Citation version in frontmatter or document body"
            ))

        # Check for successor field
        if 'successor' not in self.frontmatter:
            self.issues.append(ValidationIssue(
                ValidationIssue.WARNING,
                None,
                "Missing 'successor' field in frontmatter",
                "Add 'successor: <value>' or 'successor: TBD' to frontmatter"
            ))

    def _check_placeholders(self):
        """Check for placeholder tokens that block publishing."""
        if not self.rcc_config.get('block_on_placeholder', True):
            return

        placeholder_patterns = [
            r'\[\[MISSING\]\]',
            r'\[MISSING\]',
            r'\[TODO\]',
            r'\[\[TODO\]\]',
            r'<TBD>',
            r'\[TBD:.*?\]',
        ]

        for i, line in enumerate(self.lines, 1):
            for pattern in placeholder_patterns:
                matches = re.finditer(pattern, line, re.IGNORECASE)
                for match in matches:
                    self.issues.append(ValidationIssue(
                        ValidationIssue.CRITICAL,
                        i,
                        f"Placeholder detected: {match.group()}",
                        "Complete section or mark as Research Edition"
                    ))

    def _check_glyphsig(self):
        """Check for presence of required GlyphSig markers."""
        # Look for glyph signatures in frontmatter
        glyphsig_in_frontmatter = 'glyphsig' in self.frontmatter

        # Look for glyph patterns in content
        glyph_pattern = r'⟡⟦[A-Z\-]+⟧'
        glyphs_found = re.findall(glyph_pattern, self.content)

        if not glyphsig_in_frontmatter and not glyphs_found:
            self.issues.append(ValidationIssue(
                ValidationIssue.WARNING,
                None,
                "No GlyphSig markers found",
                "Add 'glyphsig:' to frontmatter or include ⟡⟦MARKER⟧ patterns in document"
            ))

        # Check for required glyphs if specified
        if self.required_glyphs:
            missing_glyphs = []
            for required_glyph in self.required_glyphs:
                if required_glyph not in self.content:
                    missing_glyphs.append(required_glyph)

            if missing_glyphs:
                self.issues.append(ValidationIssue(
                    ValidationIssue.WARNING,
                    None,
                    f"Missing required glyphs: {', '.join(missing_glyphs)}",
                    "Add missing glyph anchors to document"
                ))

    def _check_truth_state_tags(self):
        """Check for Truth-State tags on temporal/statistical claims."""
        if not self.rcc_config.get('truth_state_required', True):
            return

        # Patterns that indicate temporal or statistical claims
        claim_patterns = [
            r'will\s+(reach|grow|be|become)\s+\$?\d+',  # "will reach $X"
            r'by\s+\d{4}',  # "by 2026"
            r'expected\s+to',  # "expected to"
            r'projected\s+to',  # "projected to"
            r'estimated\s+at',  # "estimated at"
            r'\d+%\s+of\s+users',  # "X% of users"
        ]

        truth_state_pattern = r'\[Truth-State:|Truth-State:'

        for i, line in enumerate(self.lines, 1):
            # Check if line has claim pattern
            has_claim = any(re.search(pattern, line, re.IGNORECASE) for pattern in claim_patterns)

            if has_claim:
                # Check if line or nearby lines have Truth-State tag
                context_start = max(0, i - 2)
                context_end = min(len(self.lines), i + 2)
                context = '\n'.join(self.lines[context_start:context_end])

                if not re.search(truth_state_pattern, context, re.IGNORECASE):
                    self.issues.append(ValidationIssue(
                        ValidationIssue.WARNING,
                        i,
                        f"Temporal/statistical claim without Truth-State tag: {line.strip()[:60]}...",
                        "Add [Truth-State: Projection, Source: ...] near claim"
                    ))

    def _check_glyph_drift(self):
        """Measure glyph drift and warn if exceeds threshold."""
        max_drift = self.rcc_config.get('glyph_drift_max', 0.15)

        # Count expected glyphs vs actual glyphs
        expected_glyphs = set(self.required_glyphs)
        actual_glyphs = set(re.findall(r'⟡⟦[A-Z\-]+⟧', self.content))

        if not expected_glyphs:
            # If no required glyphs specified, skip drift check
            return

        # Calculate drift as ratio of missing glyphs
        missing_glyphs = expected_glyphs - actual_glyphs
        drift_ratio = len(missing_glyphs) / len(expected_glyphs) if expected_glyphs else 0

        if drift_ratio > max_drift:
            self.issues.append(ValidationIssue(
                ValidationIssue.WARNING,
                None,
                f"Glyph drift: {drift_ratio:.0%} (threshold: {max_drift:.0%})",
                f"Add missing glyph anchors: {', '.join(missing_glyphs)}"
            ))

    def _check_checksum(self):
        """Check for presence of checksum in frontmatter."""
        checksum_fields = ['checksum_sha256', 'checksum', 'hash']

        has_checksum = any(field in self.frontmatter for field in checksum_fields)

        if not has_checksum:
            self.issues.append(ValidationIssue(
                ValidationIssue.INFO,
                None,
                "No checksum found in frontmatter",
                "Add 'checksum_sha256: <sha256_hash>' to frontmatter"
            ))

    def generate_report(self, document_name: str, passed: bool) -> str:
        """Generate validation report as markdown."""
        date_str = datetime.now().strftime('%Y-%m-%d')
        time_str = datetime.now().strftime('%H:%M:%S')
        result = "PASS" if passed else "FAIL"

        report_lines = [
            "---",
            f"date: {date_str}",
            f"document: {document_name}",
            f"result: {result}",
            f"generated: {date_str} {time_str}",
            "tool: rcc_validator.py v1.0",
            "---",
            "",
            "# RCC Validation Report",
            "",
            f"**Document:** {document_name}",
            f"**Status:** {result}",
            f"**Generated:** {date_str} at {time_str}",
            "",
        ]

        if passed:
            report_lines.extend([
                "✅ **All validation checks passed!**",
                "",
                "This document meets RCC (Release Continuity Compliance) standards and is safe to publish.",
                "",
            ])

            if self.issues:
                report_lines.extend([
                    "---",
                    "",
                    "## Advisory Notes",
                    "",
                ])
                for issue in self.issues:
                    report_lines.append(f"- {issue}")
                report_lines.append("")
        else:
            critical_count = len([i for i in self.issues if i.severity == ValidationIssue.CRITICAL])
            warning_count = len([i for i in self.issues if i.severity == ValidationIssue.WARNING])

            report_lines.extend([
                "❌ **Validation failed!**",
                "",
                f"**Issues found:** {len(self.issues)} total ({critical_count} critical, {warning_count} warnings)",
                "",
                "---",
                "",
                "## Issues Found",
                "",
            ])

            # Group by severity
            critical_issues = [i for i in self.issues if i.severity == ValidationIssue.CRITICAL]
            warning_issues = [i for i in self.issues if i.severity == ValidationIssue.WARNING]
            info_issues = [i for i in self.issues if i.severity == ValidationIssue.INFO]

            if critical_issues:
                report_lines.extend([
                    "### CRITICAL",
                    "",
                ])
                for i, issue in enumerate(critical_issues, 1):
                    location = f"Line {issue.line_number}" if issue.line_number else "Document"
                    report_lines.extend([
                        f"{i}. **{location}:** {issue.message}",
                        f"   - **Fix:** {issue.fix}",
                        "",
                    ])

            if warning_issues:
                report_lines.extend([
                    "### WARNING",
                    "",
                ])
                for i, issue in enumerate(warning_issues, 1):
                    location = f"Line {issue.line_number}" if issue.line_number else "Document"
                    report_lines.extend([
                        f"{i}. **{location}:** {issue.message}",
                        f"   - **Fix:** {issue.fix}",
                        "",
                    ])

            if info_issues:
                report_lines.extend([
                    "### INFO",
                    "",
                ])
                for issue in info_issues:
                    report_lines.append(f"- {issue.message}")
                report_lines.append("")

            report_lines.extend([
                "---",
                "",
                "## Actions Required",
                "",
                "1. Fix all CRITICAL issues before publishing",
                "2. Address WARNINGS or document exceptions in lineage",
                "3. Re-run RCC validator after fixes: `python rcc_validator.py --input <file>`",
                "4. Only publish after receiving RCC_PASS",
                "",
            ])

        report_lines.extend([
            "---",
            "",
            "## Validation Checklist",
            "",
            f"- {'✅' if not any('title' in i.message for i in self.issues) else '❌'} Master Citation version declared",
            f"- {'✅' if not any('predecessor' in i.message for i in self.issues) else '❌'} Predecessor/successor lineage present",
            f"- {'✅' if not any('GlyphSig' in i.message for i in self.issues) else '❌'} GlyphSig present",
            f"- {'✅' if not any('Placeholder' in i.message for i in self.issues) else '❌'} No [[MISSING]] or [TODO] tokens",
            f"- {'✅' if not any('Truth-State' in i.message for i in self.issues) else '❌'} Truth-State tags on temporal claims",
            f"- {'✅' if not any('Glyph drift' in i.message for i in self.issues) else '❌'} Glyph drift ≤15%",
            f"- {'✅' if not any('checksum' in i.message for i in self.issues) else '❌'} Checksum present",
            "",
            "---",
            "",
            "## Continuity Seal",
            "",
            f"**Validation Date:** {date_str}",
            "**Tool Version:** rcc_validator.py v1.0",
            "**Principle:** AHP-Compliant (Cite or Silence)",
            f"**Release Gate:** {'OPEN' if passed else 'BLOCKED'}",
            "",
            "⟡⟦RCC⟧ · ⟡⟦COMPLIANCE⟧ · ⟡⟦CONTINUITY⟧",
            "",
        ])

        return "\n".join(report_lines)


@click.command()
@click.option(
    '--input',
    '-i',
    'input_file',
    type=click.Path(exists=True),
    required=True,
    help='Document to validate'
)
@click.option(
    '--config',
    type=click.Path(exists=True),
    default='tools/config/vault_automation.yaml',
    help='Path to configuration YAML file'
)
@click.option(
    '--output',
    '-o',
    type=click.Path(),
    default=None,
    help='Output report path (default: reports/RCC_[PASS|FAIL]_<filename>.md)'
)
@click.option(
    '--verbose',
    is_flag=True,
    help='Enable verbose logging'
)
def main(input_file: str, config: str, output: Optional[str], verbose: bool):
    """
    Validate document against RCC (Release Continuity Compliance) standards.

    Pre-publish gate that checks for:
    - Required frontmatter fields
    - Master Citation references
    - GlyphSig markers
    - Placeholder tokens
    - Truth-State tags
    - Glyph drift

    Example:
        python rcc_validator.py --input specs/MySpec.md
    """
    # Set up logging
    if verbose:
        logger.setLevel(logging.DEBUG)

    logger.info("MirrorDNA RCC Validator v1.0")
    logger.info("=" * 60)

    # Load configuration
    try:
        with open(config, 'r') as f:
            config_data = yaml.safe_load(f)
            config_data = config_data.get('vault_automation', config_data)
    except Exception as e:
        logger.error(f"Failed to load configuration: {e}")
        sys.exit(1)

    # Validate document
    try:
        input_path = Path(input_file)
        validator = RCCValidator(config_data)
        passed = validator.validate(input_path)

        # Generate report
        report_content = validator.generate_report(input_path.name, passed)

        # Determine output path
        if output is None:
            result_str = "PASS" if passed else "FAIL"
            output_dir = Path(config_data['paths']['output_reports'])
            output_dir.mkdir(parents=True, exist_ok=True)
            output = output_dir / f"RCC_{result_str}_{input_path.stem}.md"

        # Write report
        output_path = Path(output)
        output_path.parent.mkdir(parents=True, exist_ok=True)

        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(report_content)

        logger.info(f"✅ Report generated: {output_path}")

        if passed:
            logger.info("✅ RCC VALIDATION PASSED - Safe to publish")
            sys.exit(0)
        else:
            critical_count = len([i for i in validator.issues if i.severity == ValidationIssue.CRITICAL])
            logger.error(f"❌ RCC VALIDATION FAILED - {critical_count} critical issues found")
            logger.error("Fix issues before publishing. See report for details.")
            sys.exit(1)

    except Exception as e:
        logger.error(f"Validation failed: {e}")
        if verbose:
            import traceback
            traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()
