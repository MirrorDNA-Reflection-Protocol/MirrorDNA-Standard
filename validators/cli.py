#!/usr/bin/env python3
"""
MirrorDNA Compliance Validator CLI

Command-line interface for validating MirrorDNA compliance.
"""

import sys
import argparse
from pathlib import Path
from typing import Optional

from .loader import (
    load_and_validate_manifest,
    load_and_validate_profile,
    load_and_validate_policy
)
from .checks import (
    check_continuity_compliance,
    check_reflection_compliance,
    check_trustbydesign_compliance
)
from .report import (
    ComplianceReport,
    ComplianceResult,
    detect_compliance_level,
    generate_recommendations
)


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description='MirrorDNA Standard Compliance Validator',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Validate Level 1 project (manifest + policy only)
  %(prog)s --manifest manifest.yaml --policy reflection_policy.yaml

  # Validate Level 2+ project (all files)
  %(prog)s --manifest manifest.yaml --profile continuity_profile.yaml --policy reflection_policy.yaml

  # Validate with custom paths
  %(prog)s -m ./config/manifest.yaml -f ./config/profile.yaml -p ./config/policy.yaml

For more information, see: https://github.com/MirrorDNA-Reflection-Protocol/MirrorDNA-Standard
        """
    )

    parser.add_argument(
        '-m', '--manifest',
        required=True,
        help='Path to project manifest (YAML or JSON)'
    )
    parser.add_argument(
        '-f', '--profile',
        help='Path to continuity profile (YAML or JSON, required for Level 2+)'
    )
    parser.add_argument(
        '-p', '--policy',
        help='Path to reflection policy (YAML or JSON, required for all levels)'
    )
    parser.add_argument(
        '--no-color',
        action='store_true',
        help='Disable colored output'
    )
    parser.add_argument(
        '--json',
        action='store_true',
        help='Output report as JSON'
    )
    parser.add_argument(
        '-v', '--verbose',
        action='store_true',
        help='Verbose output'
    )

    args = parser.parse_args()

    # Load manifest
    if args.verbose:
        print(f"Loading manifest from {args.manifest}...")

    manifest, manifest_errors = load_and_validate_manifest(args.manifest)

    if manifest_errors:
        print("Error loading manifest:")
        for error in manifest_errors:
            print(f"  - {error}")
        return 1

    # Initialize report
    project_name = manifest.get('name', 'Unknown Project')
    declared_level = manifest.get('mirrorDNA_compliance_level', 'unknown')

    report = ComplianceReport(
        project_name=project_name,
        declared_level=declared_level,
        detected_level='unknown',
        overall_passed=True
    )

    # Track errors by level for detection
    errors_by_level = {
        'level_1': 0,
        'level_2': 0,
        'level_3': 0
    }

    # Load continuity profile (optional for Level 1)
    profile = {}
    if args.profile:
        if args.verbose:
            print(f"Loading continuity profile from {args.profile}...")

        profile, profile_errors = load_and_validate_profile(args.profile)

        if profile_errors:
            result = ComplianceResult(
                check_name="Continuity Profile Schema",
                passed=False,
                errors=profile_errors
            )
            report.add_result(result)
            errors_by_level['level_2'] += len(profile_errors)
            errors_by_level['level_3'] += len(profile_errors)
    elif declared_level in ['level_2_continuity_aware', 'level_3_vault_backed_sovereign']:
        error = "Continuity profile required for Level 2+"
        result = ComplianceResult(
            check_name="Continuity Profile",
            passed=False,
            errors=[error]
        )
        report.add_result(result)
        errors_by_level['level_2'] += 1
        errors_by_level['level_3'] += 1

    # Load reflection policy (required for all levels)
    policy = {}
    if args.policy:
        if args.verbose:
            print(f"Loading reflection policy from {args.policy}...")

        policy, policy_errors = load_and_validate_policy(args.policy)

        if policy_errors:
            result = ComplianceResult(
                check_name="Reflection Policy Schema",
                passed=False,
                errors=policy_errors
            )
            report.add_result(result)
            errors_by_level['level_1'] += len(policy_errors)
            errors_by_level['level_2'] += len(policy_errors)
            errors_by_level['level_3'] += len(policy_errors)
    else:
        error = "Reflection policy required for all compliance levels"
        result = ComplianceResult(
            check_name="Reflection Policy",
            passed=False,
            errors=[error]
        )
        report.add_result(result)
        errors_by_level['level_1'] += 1
        errors_by_level['level_2'] += 1
        errors_by_level['level_3'] += 1

    # Run compliance checks
    if args.verbose:
        print("Running compliance checks...")

    # Continuity checks
    passed, errors, warnings = check_continuity_compliance(manifest, profile)
    result = ComplianceResult(
        check_name="Continuity Compliance",
        passed=passed,
        errors=errors,
        warnings=warnings
    )
    report.add_result(result)
    if not passed:
        if declared_level in ['level_2_continuity_aware', 'level_3_vault_backed_sovereign']:
            errors_by_level['level_2'] += len(errors)
            errors_by_level['level_3'] += len(errors)

    # Reflection checks
    passed, errors, warnings = check_reflection_compliance(manifest, policy)
    result = ComplianceResult(
        check_name="Reflection Compliance",
        passed=passed,
        errors=errors,
        warnings=warnings
    )
    report.add_result(result)
    if not passed:
        errors_by_level['level_1'] += len(errors)
        errors_by_level['level_2'] += len(errors)
        errors_by_level['level_3'] += len(errors)

    # Trust-by-Design checks
    passed, errors, warnings = check_trustbydesign_compliance(manifest, policy)
    result = ComplianceResult(
        check_name="Trust-by-Design Compliance",
        passed=passed,
        errors=errors,
        warnings=warnings
    )
    report.add_result(result)
    if not passed:
        errors_by_level['level_1'] += len(errors)
        errors_by_level['level_2'] += len(errors)
        errors_by_level['level_3'] += len(errors)

    # Detect actual compliance level
    detected_level = detect_compliance_level(manifest, profile, policy, errors_by_level)
    report.detected_level = detected_level

    # Generate recommendations
    recommendations = generate_recommendations(declared_level, detected_level, report)
    for rec in recommendations:
        report.add_recommendation(rec)

    # Output report
    if args.json:
        import json
        print(json.dumps(report.to_dict(), indent=2))
    elif args.no_color:
        print(report.format_text())
    else:
        print(report.format_colored())

    # Return exit code
    if report.overall_passed:
        return 0
    else:
        return 1


if __name__ == '__main__':
    sys.exit(main())
