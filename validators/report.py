"""
Compliance report generation for MirrorDNA validators.

Aggregates check results and produces user-friendly reports.
"""

from typing import Dict, Any, List
from dataclasses import dataclass, field


@dataclass
class ComplianceResult:
    """Results from a compliance check."""
    check_name: str
    passed: bool
    errors: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)


@dataclass
class ComplianceReport:
    """Complete compliance report."""
    project_name: str
    declared_level: str
    detected_level: str
    overall_passed: bool
    results: List[ComplianceResult] = field(default_factory=list)
    recommendations: List[str] = field(default_factory=list)

    def add_result(self, result: ComplianceResult):
        """Add a check result to the report."""
        self.results.append(result)
        if not result.passed:
            self.overall_passed = False

    def add_recommendation(self, recommendation: str):
        """Add a recommendation."""
        self.recommendations.append(recommendation)

    def get_total_errors(self) -> int:
        """Get total number of errors."""
        return sum(len(r.errors) for r in self.results)

    def get_total_warnings(self) -> int:
        """Get total number of warnings."""
        return sum(len(r.warnings) for r in self.results)

    def format_text(self) -> str:
        """Format report as plain text."""
        lines = []
        lines.append("=" * 70)
        lines.append("MirrorDNA Compliance Report")
        lines.append("=" * 70)
        lines.append("")
        lines.append(f"Project: {self.project_name}")
        lines.append(f"Declared Level: {self.declared_level}")
        lines.append(f"Detected Level: {self.detected_level}")
        lines.append("")

        # Overall status
        status = "✓ PASSED" if self.overall_passed else "✗ FAILED"
        lines.append(f"Overall Status: {status}")
        lines.append(f"Total Errors: {self.get_total_errors()}")
        lines.append(f"Total Warnings: {self.get_total_warnings()}")
        lines.append("")

        # Individual checks
        lines.append("-" * 70)
        lines.append("Check Results")
        lines.append("-" * 70)

        for result in self.results:
            status_icon = "✓" if result.passed else "✗"
            lines.append(f"{status_icon} {result.check_name}")

            if result.errors:
                lines.append("  Errors:")
                for error in result.errors:
                    lines.append(f"    - {error}")

            if result.warnings:
                lines.append("  Warnings:")
                for warning in result.warnings:
                    lines.append(f"    - {warning}")

            lines.append("")

        # Recommendations
        if self.recommendations:
            lines.append("-" * 70)
            lines.append("Recommendations")
            lines.append("-" * 70)
            for rec in self.recommendations:
                lines.append(f"  • {rec}")
            lines.append("")

        lines.append("=" * 70)
        return "\n".join(lines)

    def to_dict(self) -> Dict[str, Any]:
        """Convert report to dictionary for JSON/YAML output."""
        return {
            'project_name': self.project_name,
            'declared_level': self.declared_level,
            'detected_level': self.detected_level,
            'overall_passed': self.overall_passed,
            'summary': {
                'total_errors': self.get_total_errors(),
                'total_warnings': self.get_total_warnings(),
                'total_checks': len(self.results),
                'checks_passed': sum(1 for r in self.results if r.passed),
                'checks_failed': sum(1 for r in self.results if not r.passed)
            },
            'results': [
                {
                    'check_name': r.check_name,
                    'passed': r.passed,
                    'errors': r.errors,
                    'warnings': r.warnings
                }
                for r in self.results
            ],
            'recommendations': self.recommendations
        }

    def format_colored(self) -> str:
        """Format report with ANSI color codes."""
        # ANSI color codes
        RESET = "\033[0m"
        RED = "\033[31m"
        GREEN = "\033[32m"
        YELLOW = "\033[33m"
        CYAN = "\033[36m"
        BOLD = "\033[1m"

        lines = []
        lines.append(BOLD + "=" * 70 + RESET)
        lines.append(BOLD + CYAN + "MirrorDNA Compliance Report" + RESET)
        lines.append(BOLD + "=" * 70 + RESET)
        lines.append("")
        lines.append(f"{BOLD}Project:{RESET} {self.project_name}")
        lines.append(f"{BOLD}Declared Level:{RESET} {self.declared_level}")
        lines.append(f"{BOLD}Detected Level:{RESET} {self.detected_level}")
        lines.append("")

        # Overall status
        if self.overall_passed:
            status = f"{GREEN}{BOLD}✓ PASSED{RESET}"
        else:
            status = f"{RED}{BOLD}✗ FAILED{RESET}"

        lines.append(f"{BOLD}Overall Status:{RESET} {status}")
        lines.append(f"{BOLD}Total Errors:{RESET} {RED}{self.get_total_errors()}{RESET}")
        lines.append(f"{BOLD}Total Warnings:{RESET} {YELLOW}{self.get_total_warnings()}{RESET}")
        lines.append("")

        # Individual checks
        lines.append(BOLD + "-" * 70 + RESET)
        lines.append(BOLD + "Check Results" + RESET)
        lines.append(BOLD + "-" * 70 + RESET)

        for result in self.results:
            if result.passed:
                status_icon = f"{GREEN}✓{RESET}"
            else:
                status_icon = f"{RED}✗{RESET}"

            lines.append(f"{status_icon} {BOLD}{result.check_name}{RESET}")

            if result.errors:
                lines.append(f"  {RED}Errors:{RESET}")
                for error in result.errors:
                    lines.append(f"    {RED}- {error}{RESET}")

            if result.warnings:
                lines.append(f"  {YELLOW}Warnings:{RESET}")
                for warning in result.warnings:
                    lines.append(f"    {YELLOW}- {warning}{RESET}")

            lines.append("")

        # Recommendations
        if self.recommendations:
            lines.append(BOLD + "-" * 70 + RESET)
            lines.append(BOLD + "Recommendations" + RESET)
            lines.append(BOLD + "-" * 70 + RESET)
            for rec in self.recommendations:
                lines.append(f"  {CYAN}• {rec}{RESET}")
            lines.append("")

        lines.append(BOLD + "=" * 70 + RESET)
        return "\n".join(lines)


def detect_compliance_level(
    manifest: Dict[str, Any],
    profile: Dict[str, Any],
    policy: Dict[str, Any],
    errors_by_level: Dict[str, int]
) -> str:
    """
    Detect the actual compliance level achieved.

    Args:
        manifest: Project manifest
        profile: Continuity profile
        policy: Reflection policy
        errors_by_level: Map of level to error count

    Returns:
        Detected compliance level string
    """
    declared = manifest.get('mirrorDNA_compliance_level', 'unknown')

    # Start from highest level and work down
    # If a level has errors, the project doesn't meet that level

    # Check Level 3
    if profile and profile.get('continuity_mechanism') == 'vault_backed':
        if 'vault_configuration' in profile and policy.get('glyph_signatures', {}).get('enabled'):
            if errors_by_level.get('level_3', 0) == 0:
                return 'level_3_vault_backed_sovereign'

    # Check Level 2
    if profile and profile.get('state_persistence', {}).get('enabled'):
        if errors_by_level.get('level_2', 0) == 0:
            return 'level_2_continuity_aware'

    # Check Level 1
    if policy.get('uncertainty_handling', {}).get('cite_or_silence'):
        if errors_by_level.get('level_1', 0) == 0:
            return 'level_1_basic_reflection'

    # Failed to meet any level
    return 'non_compliant'


def generate_recommendations(
    declared_level: str,
    detected_level: str,
    report: ComplianceReport
) -> List[str]:
    """
    Generate recommendations based on compliance gaps.

    Args:
        declared_level: Declared compliance level
        detected_level: Detected compliance level
        report: Current report with results

    Returns:
        List of recommendations
    """
    recommendations = []

    # If detected < declared, recommend fixes
    level_order = [
        'non_compliant',
        'level_1_basic_reflection',
        'level_2_continuity_aware',
        'level_3_vault_backed_sovereign'
    ]

    try:
        declared_idx = level_order.index(declared_level)
        detected_idx = level_order.index(detected_level)

        if detected_idx < declared_idx:
            recommendations.append(
                f"Project declares {declared_level} but only achieves {detected_level}. "
                f"Fix errors to meet declared level."
            )

        # Specific recommendations based on gaps
        if detected_level == 'non_compliant':
            recommendations.append("Start by implementing cite_or_silence (AHP) and basic reflection policy")

        elif detected_level == 'level_1_basic_reflection' and declared_idx > 1:
            recommendations.append("To reach Level 2, add state persistence and continuity profile")

        elif detected_level == 'level_2_continuity_aware' and declared_idx > 2:
            recommendations.append("To reach Level 3, migrate to vault storage and add glyph signatures")

    except ValueError:
        # Unknown level
        recommendations.append("Declare a valid mirrorDNA_compliance_level in manifest")

    # Add specific recommendations from errors
    all_errors = []
    for result in report.results:
        all_errors.extend(result.errors)

    if any('vault' in e.lower() for e in all_errors):
        recommendations.append("Configure vault_configuration in continuity profile for Level 3")

    if any('glyph' in e.lower() for e in all_errors):
        recommendations.append("Enable glyph_signatures in reflection policy for Level 3")

    if any('cite_or_silence' in e.lower() or 'ahp' in e.lower() for e in all_errors):
        recommendations.append("Enable cite_or_silence (AHP) in uncertainty_handling")

    return recommendations
