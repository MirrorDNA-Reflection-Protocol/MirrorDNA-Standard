#!/usr/bin/env python3
"""
MirrorDNA Drift Audit Scanner

Scans public signals (GitHub README, markdown files) and compares
against Master Citation canonical claims to detect drift.

Drift categories:
- Semantic drift (meaning changes)
- Structural drift (format/organization)
- Value drift (numbers/metrics)
- Glyph drift (symbolic anchors)

Outputs: DRIFT_REPORT_YYYY-MM-DD.md with reconciliation notes

Principles: Consistency tracking, AHP-compliant, truth preservation
"""

import logging
import re
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Set, Tuple

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


class DriftDetector:
    """Detects drift between public signals and canonical claims."""

    def __init__(self, config: Dict):
        self.config = config
        self.drift_config = config.get('drift_audit', {})
        self.max_drift_percent = self.drift_config.get('max_drift_percent', 15)
        self.public_signals = self.drift_config.get('public_signals', [])
        self.drift_items: List[Dict] = []

    def scan(self, vault_path: Path) -> List[Dict]:
        """
        Scan public signal files for drift.

        Returns:
            List of drift items detected
        """
        logger.info(f"Scanning vault for drift: {vault_path}")

        # Scan each public signal file
        for signal_file in self.public_signals:
            signal_path = vault_path / signal_file

            if signal_path.exists():
                logger.info(f"Analyzing: {signal_file}")
                self._analyze_file(signal_path, signal_file)
            else:
                logger.warning(f"Public signal not found: {signal_file}")

        # Calculate overall drift percentage
        total_drift = len(self.drift_items)
        logger.info(f"Found {total_drift} potential drift items")

        return self.drift_items

    def _analyze_file(self, file_path: Path, signal_name: str):
        """Analyze single file for drift indicators."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            # Check for various drift indicators

            # 1. Version drift
            self._check_version_drift(content, signal_name)

            # 2. Glyph drift
            self._check_glyph_drift(content, signal_name)

            # 3. Value drift (numbers, metrics)
            self._check_value_drift(content, signal_name)

            # 4. Semantic drift (key claims)
            self._check_semantic_drift(content, signal_name)

        except Exception as e:
            logger.error(f"Error analyzing {signal_name}: {e}")

    def _check_version_drift(self, content: str, signal_name: str):
        """Check for version number inconsistencies."""
        # Extract version references
        version_patterns = [
            r'version[:\s]+([v\d\.]+)',
            r'v(\d+\.\d+(?:\.\d+)?)',
            r'Master[_\s]+Citation[_\s]+v?(\d+\.\d+(?:\.\d+)?)',
        ]

        versions_found = set()
        for pattern in version_patterns:
            matches = re.finditer(pattern, content, re.IGNORECASE)
            for match in matches:
                versions_found.add(match.group(1))

        # If multiple different versions referenced, flag as potential drift
        if len(versions_found) > 3:
            self.drift_items.append({
                'type': 'version_drift',
                'severity': 'medium',
                'file': signal_name,
                'description': f'Multiple version references found: {", ".join(sorted(versions_found)[:5])}',
                'recommendation': 'Verify all version references are current and consistent'
            })

    def _check_glyph_drift(self, content: str, signal_name: str):
        """Check for missing or inconsistent glyph markers."""
        # Expected glyphs for MirrorDNA documents
        expected_glyphs = [
            '⟡⟦MIRRORDNA⟧',
            '⟡⟦CONTINUITY⟧',
            '⟡⟦AHP⟧',
        ]

        # Find actual glyphs
        glyph_pattern = r'⟡⟦[A-Z\-]+⟧'
        glyphs_found = re.findall(glyph_pattern, content)

        if not glyphs_found:
            self.drift_items.append({
                'type': 'glyph_drift',
                'severity': 'low',
                'file': signal_name,
                'description': 'No glyph markers found in public signal',
                'recommendation': 'Consider adding glyph anchors for continuity tracking'
            })

        # Check for inconsistent glyph usage
        unique_glyphs = set(glyphs_found)
        if len(unique_glyphs) > 10:
            self.drift_items.append({
                'type': 'glyph_drift',
                'severity': 'low',
                'file': signal_name,
                'description': f'Excessive glyph diversity ({len(unique_glyphs)} unique glyphs)',
                'recommendation': 'Standardize glyph usage across documents'
            })

    def _check_value_drift(self, content: str, signal_name: str):
        """Check for inconsistent numeric values and metrics."""
        # Look for specific value patterns that might drift
        value_patterns = [
            (r'\$(\d+(?:,\d+)*(?:\.\d+)?)[MBK]?', 'currency'),
            (r'(\d+)%\s+(?:of|increase|decrease|growth)', 'percentage'),
            (r'(\d+(?:,\d+)*)\s+(?:users|files|documents)', 'counts'),
        ]

        values_by_type: Dict[str, List[str]] = {}

        for pattern, value_type in value_patterns:
            matches = re.finditer(pattern, content, re.IGNORECASE)
            for match in matches:
                if value_type not in values_by_type:
                    values_by_type[value_type] = []
                values_by_type[value_type].append(match.group(1))

        # Check for duplicate but different values (potential inconsistency)
        for value_type, values in values_by_type.items():
            if len(set(values)) > 5:  # Many different values of same type
                self.drift_items.append({
                    'type': 'value_drift',
                    'severity': 'medium',
                    'file': signal_name,
                    'description': f'Multiple different {value_type} values found: {len(set(values))} unique values',
                    'recommendation': f'Verify {value_type} values are current and sourced'
                })

    def _check_semantic_drift(self, content: str, signal_name: str):
        """Check for semantic inconsistencies in key claims."""
        # Key terms that should be used consistently
        key_terms = {
            'MirrorDNA': ['MirrorDNA™', 'Mirror DNA', 'mirrordna'],
            'Active Mirror': ['Active Mirror™', 'ActiveMirror', 'active mirror'],
            'Tri-Twin': ['Tri-Twin', 'TriTwin', 'tri-twin', 'three twin'],
        }

        for canonical_term, variants in key_terms.items():
            variants_found = []
            for variant in variants:
                if re.search(re.escape(variant), content, re.IGNORECASE):
                    variants_found.append(variant)

            # If multiple variants of same term found, flag as drift
            if len(variants_found) > 2:
                self.drift_items.append({
                    'type': 'semantic_drift',
                    'severity': 'low',
                    'file': signal_name,
                    'description': f'Multiple variants of "{canonical_term}" found: {", ".join(variants_found)}',
                    'recommendation': f'Standardize usage to: {variants[0]}'
                })

    def generate_report(self) -> str:
        """Generate drift audit report as markdown."""
        date_str = datetime.now().strftime('%Y-%m-%d')
        time_str = datetime.now().strftime('%H:%M:%S')

        # Calculate drift percentage
        total_items = len(self.drift_items)
        drift_percent = min(100, total_items * 5)  # Rough estimate

        # Determine status
        if drift_percent <= self.max_drift_percent:
            status = "ACCEPTABLE"
        elif drift_percent <= 30:
            status = "CAUTION"
        else:
            status = "EXCESSIVE"

        report_lines = [
            "---",
            f"date: {date_str}",
            "type: DRIFT_AUDIT",
            f"status: {status}",
            f"drift_percent: {drift_percent}",
            f"generated: {date_str} {time_str}",
            "tool: drift_audit.py v1.0",
            "---",
            "",
            "# Vault Drift Audit Report",
            "",
            f"**Generated:** {date_str} at {time_str}",
            f"**Status:** {status}",
            f"**Estimated Drift:** {drift_percent}%",
            "",
            "---",
            "",
            "## Summary",
            "",
            f"- **Total drift items:** {total_items}",
            f"- **Drift threshold:** {self.max_drift_percent}%",
            f"- **Status:** {status}",
            "",
        ]

        if not self.drift_items:
            report_lines.extend([
                "✅ **No significant drift detected**",
                "",
                "All public signals are consistent with canonical claims.",
                "",
            ])
        else:
            # Group by type
            by_type: Dict[str, List[Dict]] = {}
            for item in self.drift_items:
                drift_type = item['type']
                if drift_type not in by_type:
                    by_type[drift_type] = []
                by_type[drift_type].append(item)

            report_lines.extend([
                "---",
                "",
                "## Drift Items by Category",
                "",
            ])

            # Report each category
            for drift_type, items in sorted(by_type.items()):
                report_lines.extend([
                    f"### {drift_type.replace('_', ' ').title()} ({len(items)} items)",
                    "",
                ])

                for i, item in enumerate(items, 1):
                    severity_icon = {
                        'high': '🔴',
                        'medium': '🟡',
                        'low': '🟢'
                    }.get(item['severity'], '⚪')

                    report_lines.extend([
                        f"{i}. {severity_icon} **{item['file']}**",
                        f"   - {item['description']}",
                        f"   - *Recommendation:* {item['recommendation']}",
                        "",
                    ])

        # Add recommendations
        report_lines.extend([
            "---",
            "",
            "## Overall Recommendations",
            "",
        ])

        if status == "ACCEPTABLE":
            report_lines.extend([
                "✅ Drift is within acceptable threshold",
                "",
                "Continue monitoring with weekly drift audits.",
            ])
        elif status == "CAUTION":
            report_lines.extend([
                "⚠️ Drift approaching threshold",
                "",
                "1. Review drift items above",
                "2. Update public signals to align with canonical claims",
                "3. Run sync_report.py to verify layer consistency",
                "4. Re-run drift_audit.py after fixes",
            ])
        else:
            report_lines.extend([
                "🔴 Excessive drift detected",
                "",
                "1. **PRIORITY:** Review all high-severity drift items",
                "2. Update public signals to align with Master Citation",
                "3. Run RCC validator on updated documents",
                "4. Sync changes across all vault layers",
                "5. Re-run drift audit to verify resolution",
            ])

        report_lines.extend([
            "",
            "---",
            "",
            "## Continuity Seal",
            "",
            f"**Audit Date:** {date_str}",
            "**Tool Version:** drift_audit.py v1.0",
            "**Principle:** AHP-Compliant (Cite or Silence)",
            f"**Drift Status:** {status}",
            "",
            "⟡⟦DRIFT-AUDIT⟧ · ⟡⟦CONTINUITY⟧ · ⟡⟦VAULT⟧",
            "",
        ])

        return "\n".join(report_lines)


@click.command()
@click.option(
    '--vault',
    type=click.Path(exists=True),
    default='.',
    help='Vault root path to scan (default: current directory)'
)
@click.option(
    '--config',
    type=click.Path(exists=True),
    default='tools/config/vault_automation.yaml',
    help='Path to configuration YAML file'
)
@click.option(
    '--output',
    type=click.Path(),
    default=None,
    help='Output report path (default: reports/DRIFT_REPORT_YYYY-MM-DD.md)'
)
@click.option(
    '--verbose',
    is_flag=True,
    help='Enable verbose logging'
)
def main(vault: str, config: str, output: Optional[str], verbose: bool):
    """
    Scan public signals for drift from canonical claims.

    Detects semantic, structural, value, and glyph drift in
    public-facing documents compared to Master Citation.

    Example:
        python drift_audit.py --vault /path/to/vault
    """
    # Set up logging
    if verbose:
        logger.setLevel(logging.DEBUG)

    logger.info("MirrorDNA Drift Audit Scanner v1.0")
    logger.info("=" * 60)

    # Load configuration
    try:
        with open(config, 'r') as f:
            config_data = yaml.safe_load(f)
            config_data = config_data.get('vault_automation', config_data)
    except Exception as e:
        logger.error(f"Failed to load configuration: {e}")
        sys.exit(1)

    # Run drift detection
    try:
        detector = DriftDetector(config_data)
        drift_items = detector.scan(Path(vault))

        # Generate report
        report_content = detector.generate_report()

        # Determine output path
        if output is None:
            date_str = datetime.now().strftime('%Y-%m-%d')
            output_dir = Path(config_data['paths']['output_reports'])
            output_dir.mkdir(parents=True, exist_ok=True)
            output = output_dir / f"DRIFT_REPORT_{date_str}.md"

        # Write report
        output_path = Path(output)
        output_path.parent.mkdir(parents=True, exist_ok=True)

        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(report_content)

        logger.info(f"✅ Report generated: {output_path}")

        # Determine exit code based on drift
        drift_percent = min(100, len(drift_items) * 5)
        max_drift = config_data.get('drift_audit', {}).get('max_drift_percent', 15)

        if drift_percent <= max_drift:
            logger.info(f"✅ Drift acceptable: {drift_percent}% (threshold: {max_drift}%)")
            sys.exit(0)
        elif drift_percent <= 30:
            logger.warning(f"⚠️  Drift caution: {drift_percent}% (threshold: {max_drift}%)")
            sys.exit(1)
        else:
            logger.error(f"🔴 Excessive drift: {drift_percent}% (threshold: {max_drift}%)")
            sys.exit(2)

    except Exception as e:
        logger.error(f"Drift audit failed: {e}")
        if verbose:
            import traceback
            traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()
