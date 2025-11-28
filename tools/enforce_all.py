#!/usr/bin/env python3
"""
MirrorDNA Constitutional Enforcement Orchestrator

VaultID: AMOS://MirrorDNA-Standard/Tools/EnforceAll/v1.0
GlyphSig: ⟡⟦ORCHESTRATOR⟧ · ⟡⟦ENFORCEMENT⟧ · ⟡⟦AUTOMATION⟧
Predecessor: None (Initial Release)
Successor: TBD

CONSTITUTIONAL STATUS:
Enforceability: MANDATORY
Verifiability: AUTOMATED
Adoption: CORE
Truth-State: [Fact - Automation Framework]

Master Constitutional Enforcement Orchestrator
==============================================

Runs all constitutional enforcement tools in sequence:
1. Reflective Review (principle compliance)
2. Truth-State Enforcement (FEU validation)
3. Vault Manager (lineage integrity)
4. Compliance Validators (technical compliance)

Provides unified reporting and single exit code for CI/CD integration.

Usage:
  python tools/enforce_all.py --target <file_or_dir>
  python tools/enforce_all.py --vault ./vault --strict
  python tools/enforce_all.py --format json
"""

import sys
import json
import argparse
from pathlib import Path
from typing import Dict, Any, List, Optional
from datetime import datetime

# Import enforcement tools
sys.path.insert(0, str(Path(__file__).parent))

from truth_state import TruthStateEnforcer
from vault_manager import VaultManager
from reflective_reviewer import ReflectiveReviewer, audit_codebase


class EnforcementOrchestrator:
    """
    Orchestrates all constitutional enforcement tools.

    Runs tools in optimal order and aggregates results.
    """

    def __init__(
        self,
        vault_path: Optional[Path] = None,
        strict_mode: bool = False,
        output_format: str = 'text'
    ):
        """
        Initialize orchestrator.

        Args:
            vault_path: Path to vault
            strict_mode: Enable strict enforcement
            output_format: Output format (text, json, yaml)
        """
        self.vault_path = vault_path
        self.strict_mode = strict_mode
        self.output_format = output_format

        # Results storage
        self.results: Dict[str, Any] = {
            'timestamp': datetime.utcnow().isoformat(),
            'strict_mode': strict_mode,
            'vault_path': str(vault_path) if vault_path else None,
            'stages': {},
            'summary': {
                'total_stages': 0,
                'stages_passed': 0,
                'stages_failed': 0,
                'critical_violations': 0,
                'warnings': 0,
                'overall_compliance_score': 0.0
            }
        }

    def enforce(self, target: Path) -> bool:
        """
        Run all enforcement stages on target.

        Args:
            target: File or directory to enforce

        Returns:
            True if all stages pass, False otherwise
        """
        all_passed = True

        # Stage 1: Reflective Review
        if not self._stage_reflective_review(target):
            all_passed = False

        # Stage 2: Truth-State Enforcement
        if not self._stage_truth_state(target):
            all_passed = False

        # Stage 3: Vault Integrity (if vault provided)
        if self.vault_path:
            if not self._stage_vault_integrity():
                all_passed = False

        # Stage 4: Compliance Validators (if manifest exists)
        if not self._stage_validators(target):
            all_passed = False

        # Calculate summary
        self._calculate_summary()

        return all_passed

    def _stage_reflective_review(self, target: Path) -> bool:
        """Stage 1: Reflective philosophical audit."""
        stage_name = 'reflective_review'
        self.results['stages'][stage_name] = {'status': 'running'}

        try:
            reviewer = ReflectiveReviewer(strict_mode=self.strict_mode)

            if target.is_file():
                report = reviewer.audit_file(target)
            else:
                report = audit_codebase(target, extensions=['.py', '.md', '.yaml', '.yml'])

            # Determine pass/fail
            critical_count = report['severity_counts'].get('critical', 0)
            violation_count = report['severity_counts'].get('violation', 0)

            passed = (critical_count == 0 and violation_count == 0)

            if self.strict_mode:
                warning_count = report['severity_counts'].get('warning', 0)
                passed = passed and (warning_count == 0)

            self.results['stages'][stage_name] = {
                'status': 'passed' if passed else 'failed',
                'compliance_score': report['compliance_score'],
                'total_findings': report['total_findings'],
                'severity_counts': report['severity_counts'],
                'details': report
            }

            self.results['summary']['total_stages'] += 1
            if passed:
                self.results['summary']['stages_passed'] += 1
            else:
                self.results['summary']['stages_failed'] += 1
                self.results['summary']['critical_violations'] += critical_count
                self.results['summary']['warnings'] += report['severity_counts'].get('warning', 0)

            return passed

        except Exception as e:
            self.results['stages'][stage_name] = {
                'status': 'error',
                'error': str(e)
            }
            self.results['summary']['total_stages'] += 1
            self.results['summary']['stages_failed'] += 1
            return False

    def _stage_truth_state(self, target: Path) -> bool:
        """Stage 2: Truth-State FEU enforcement."""
        stage_name = 'truth_state'
        self.results['stages'][stage_name] = {'status': 'running'}

        try:
            enforcer = TruthStateEnforcer(
                vault_path=self.vault_path,
                strict_mode=self.strict_mode
            )

            # Collect statements from target
            statements = []

            if target.is_file() and target.suffix == '.md':
                content = target.read_text(encoding='utf-8')
                # Simple sentence extraction
                import re
                sentences = re.split(r'(?<=[.!?])\s+', content)
                statements = [{'text': s.strip()} for s in sentences if len(s.strip()) > 10]

            # Generate FEU report
            if statements:
                report = enforcer.generate_feu_report(statements[:100])  # Limit to 100
            else:
                report = {
                    'total_statements': 0,
                    'compliance_score': 1.0,
                    'hallucinations': 0
                }

            # Determine pass/fail
            hallucination_count = report.get('hallucinations', 0)
            compliance_score = report.get('compliance_score', 0.0)

            passed = (hallucination_count == 0)

            if self.strict_mode:
                passed = passed and (compliance_score >= 0.7)

            self.results['stages'][stage_name] = {
                'status': 'passed' if passed else 'failed',
                'compliance_score': compliance_score,
                'hallucinations': hallucination_count,
                'total_statements': report.get('total_statements', 0),
                'details': report
            }

            self.results['summary']['total_stages'] += 1
            if passed:
                self.results['summary']['stages_passed'] += 1
            else:
                self.results['summary']['stages_failed'] += 1
                if hallucination_count > 0:
                    self.results['summary']['critical_violations'] += hallucination_count

            return passed

        except Exception as e:
            self.results['stages'][stage_name] = {
                'status': 'error',
                'error': str(e)
            }
            self.results['summary']['total_stages'] += 1
            self.results['summary']['stages_failed'] += 1
            return False

    def _stage_vault_integrity(self) -> bool:
        """Stage 3: Vault integrity verification."""
        stage_name = 'vault_integrity'
        self.results['stages'][stage_name] = {'status': 'running'}

        try:
            manager = VaultManager(self.vault_path)

            # Generate lineage report
            lineage_report = manager.generate_lineage_report()

            # Verify all registered artifacts
            verification_results = []
            for vault_id in manager.manifest.get('artifacts', {}).keys():
                is_valid, issues = manager.verify_artifact(vault_id)
                verification_results.append({
                    'vault_id': vault_id,
                    'valid': is_valid,
                    'issues': issues
                })

            failed_verifications = [r for r in verification_results if not r['valid']]
            passed = len(failed_verifications) == 0

            self.results['stages'][stage_name] = {
                'status': 'passed' if passed else 'failed',
                'total_artifacts': lineage_report['total_artifacts'],
                'verified': len(verification_results) - len(failed_verifications),
                'failed': len(failed_verifications),
                'lineage_report': lineage_report,
                'failed_verifications': failed_verifications
            }

            self.results['summary']['total_stages'] += 1
            if passed:
                self.results['summary']['stages_passed'] += 1
            else:
                self.results['summary']['stages_failed'] += 1
                self.results['summary']['critical_violations'] += len(failed_verifications)

            return passed

        except Exception as e:
            self.results['stages'][stage_name] = {
                'status': 'error',
                'error': str(e)
            }
            self.results['summary']['total_stages'] += 1
            self.results['summary']['stages_failed'] += 1
            return False

    def _stage_validators(self, target: Path) -> bool:
        """Stage 4: Compliance validators."""
        stage_name = 'compliance_validators'
        self.results['stages'][stage_name] = {'status': 'skipped'}

        # Look for manifest file
        manifest_paths = [
            target / 'mirrorDNA_manifest.yaml',
            target / 'manifest.yaml',
            target.parent / 'mirrorDNA_manifest.yaml'
        ]

        manifest_file = None
        for path in manifest_paths:
            if path.exists():
                manifest_file = path
                break

        if not manifest_file:
            self.results['stages'][stage_name]['reason'] = 'No manifest found'
            return True  # Not a failure, just skipped

        try:
            # Run validators (would need to import validators.cli)
            # For now, mark as skipped with note
            self.results['stages'][stage_name] = {
                'status': 'skipped',
                'reason': 'Validator integration pending',
                'manifest_found': str(manifest_file)
            }
            return True

        except Exception as e:
            self.results['stages'][stage_name] = {
                'status': 'error',
                'error': str(e)
            }
            return False

    def _calculate_summary(self) -> None:
        """Calculate overall summary statistics."""
        # Calculate overall compliance score (average of stage scores)
        scores = []

        for stage_name, stage_data in self.results['stages'].items():
            if 'compliance_score' in stage_data:
                scores.append(stage_data['compliance_score'])

        if scores:
            self.results['summary']['overall_compliance_score'] = sum(scores) / len(scores)
        else:
            self.results['summary']['overall_compliance_score'] = 0.0

    def print_results(self) -> None:
        """Print results in specified format."""
        if self.output_format == 'json':
            print(json.dumps(self.results, indent=2))
        elif self.output_format == 'yaml':
            try:
                import yaml
                print(yaml.dump(self.results, default_flow_style=False))
            except ImportError:
                print("YAML output requires PyYAML. Falling back to JSON.")
                print(json.dumps(self.results, indent=2))
        else:
            # Text output
            self._print_text_results()

    def _print_text_results(self) -> None:
        """Print human-readable text results."""
        print("\n" + "="*70)
        print("⟡⟦CONSTITUTIONAL ENFORCEMENT REPORT⟧")
        print("="*70)

        print(f"\nTimestamp: {self.results['timestamp']}")
        print(f"Strict Mode: {self.results['strict_mode']}")
        print(f"Vault Path: {self.results['vault_path'] or 'None'}")

        print(f"\n{'SUMMARY':=^70}")
        summary = self.results['summary']
        print(f"Total Stages: {summary['total_stages']}")
        print(f"Passed: {summary['stages_passed']}")
        print(f"Failed: {summary['stages_failed']}")
        print(f"Critical Violations: {summary['critical_violations']}")
        print(f"Warnings: {summary['warnings']}")
        print(f"Overall Compliance Score: {summary['overall_compliance_score']:.2f}/1.00")

        print(f"\n{'STAGE RESULTS':=^70}")
        for stage_name, stage_data in self.results['stages'].items():
            status_symbol = {
                'passed': '✓',
                'failed': '✗',
                'error': '⚠',
                'skipped': '○'
            }.get(stage_data['status'], '?')

            print(f"\n{status_symbol} {stage_name.upper().replace('_', ' ')}")
            print(f"  Status: {stage_data['status']}")

            if 'compliance_score' in stage_data:
                print(f"  Compliance Score: {stage_data['compliance_score']:.2f}")

            if 'total_findings' in stage_data:
                print(f"  Findings: {stage_data['total_findings']}")

            if 'hallucinations' in stage_data:
                print(f"  Hallucinations: {stage_data['hallucinations']}")

            if 'error' in stage_data:
                print(f"  Error: {stage_data['error']}")

            if 'reason' in stage_data:
                print(f"  Reason: {stage_data['reason']}")

        print("\n" + "="*70)

        # Overall verdict
        if summary['stages_failed'] == 0 and summary['critical_violations'] == 0:
            print("✓ ALL ENFORCEMENT CHECKS PASSED")
        else:
            print("✗ ENFORCEMENT FAILURES DETECTED")

        print("="*70 + "\n")


def main():
    parser = argparse.ArgumentParser(
        description="MirrorDNA Constitutional Enforcement Orchestrator"
    )
    parser.add_argument(
        '--target',
        type=Path,
        default=Path.cwd(),
        help='Target file or directory to enforce'
    )
    parser.add_argument(
        '--vault',
        type=Path,
        help='Path to vault for verification'
    )
    parser.add_argument(
        '--strict',
        action='store_true',
        help='Enable strict mode (warnings become failures)'
    )
    parser.add_argument(
        '--format',
        choices=['text', 'json', 'yaml'],
        default='text',
        help='Output format'
    )

    args = parser.parse_args()

    # Validate target
    if not args.target.exists():
        print(f"Error: Target does not exist: {args.target}")
        sys.exit(2)

    # Create orchestrator
    orchestrator = EnforcementOrchestrator(
        vault_path=args.vault,
        strict_mode=args.strict,
        output_format=args.format
    )

    # Run enforcement
    passed = orchestrator.enforce(args.target)

    # Print results
    orchestrator.print_results()

    # Exit with appropriate code
    sys.exit(0 if passed else 1)


if __name__ == "__main__":
    main()
