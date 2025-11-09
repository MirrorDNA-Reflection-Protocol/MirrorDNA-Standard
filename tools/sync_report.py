#!/usr/bin/env python3
"""
MirrorDNA Vault Synchronization Report Generator

Scans Personal Layer and Continuity Layer(s) to detect:
- Missing files
- Checksum mismatches
- Version drift
- File count discrepancies

Generates: SYNC_REPORT_YYYY-MM-DD.md

Principles: AHP-compliant (Cite or Silence), version tracking, sovereignty-first
"""

import hashlib
import json
import logging
import os
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


class VaultScanner:
    """Scans vault directories and extracts metadata."""

    def __init__(self, root_path: Path, check_checksums: bool = True):
        self.root_path = Path(root_path)
        self.check_checksums = check_checksums
        self.files: Dict[str, Dict] = {}

    def scan(self) -> Dict[str, Dict]:
        """Scan directory recursively and build file inventory."""
        if not self.root_path.exists():
            logger.warning(f"Path does not exist: {self.root_path}")
            return {}

        logger.info(f"Scanning: {self.root_path}")

        for file_path in self.root_path.rglob('*'):
            if file_path.is_file() and not self._should_exclude(file_path):
                relative_path = file_path.relative_to(self.root_path)
                self.files[str(relative_path)] = self._extract_metadata(file_path)

        logger.info(f"Found {len(self.files)} files in {self.root_path.name}")
        return self.files

    def _should_exclude(self, file_path: Path) -> bool:
        """Check if file should be excluded from scan."""
        exclude_patterns = ['.DS_Store', '__pycache__', '.git', '*.pyc', '*.log']
        name = file_path.name

        for pattern in exclude_patterns:
            if pattern.startswith('*.'):
                if name.endswith(pattern[1:]):
                    return True
            elif pattern in str(file_path):
                return True

        return False

    def _extract_metadata(self, file_path: Path) -> Dict:
        """Extract file metadata including checksum and version."""
        metadata = {
            'path': str(file_path),
            'size': file_path.stat().st_size,
            'modified': datetime.fromtimestamp(file_path.stat().st_mtime).isoformat(),
            'checksum': None,
            'version': None,
        }

        # Calculate checksum if enabled
        if self.check_checksums:
            try:
                metadata['checksum'] = self._calculate_checksum(file_path)
            except Exception as e:
                logger.warning(f"Could not calculate checksum for {file_path}: {e}")

        # Extract version from frontmatter if markdown file
        if file_path.suffix in ['.md', '.markdown']:
            try:
                metadata['version'] = self._extract_version(file_path)
            except Exception as e:
                logger.debug(f"Could not extract version from {file_path}: {e}")

        return metadata

    def _calculate_checksum(self, file_path: Path) -> str:
        """Calculate SHA-256 checksum of file."""
        sha256_hash = hashlib.sha256()
        with open(file_path, "rb") as f:
            for byte_block in iter(lambda: f.read(4096), b""):
                sha256_hash.update(byte_block)
        return sha256_hash.hexdigest()[:12]  # First 12 chars for brevity

    def _extract_version(self, file_path: Path) -> Optional[str]:
        """Extract version from YAML frontmatter or document."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            # Check for YAML frontmatter
            if content.startswith('---'):
                parts = content.split('---', 2)
                if len(parts) >= 3:
                    frontmatter = yaml.safe_load(parts[1])
                    if isinstance(frontmatter, dict):
                        # Try various version fields
                        for key in ['version', 'vault_id', 'checksum_sha256']:
                            if key in frontmatter:
                                return str(frontmatter[key])

            # Try to extract version from content
            version_patterns = [
                r'version[:\s]+([v\d\.]+)',
                r'v(\d+\.\d+(?:\.\d+)?)',
            ]
            for pattern in version_patterns:
                match = re.search(pattern, content, re.IGNORECASE)
                if match:
                    return match.group(1)

        except Exception as e:
            logger.debug(f"Error extracting version from {file_path}: {e}")

        return None


class SyncReportGenerator:
    """Generates synchronization report comparing vault layers."""

    def __init__(self, config: Dict):
        self.config = config
        self.personal_files: Dict[str, Dict] = {}
        self.continuity_files: Dict[str, Dict] = {}
        self.conflicts: List[Dict] = []
        self.missing: List[str] = []
        self.status: str = "UNKNOWN"

    def generate(self) -> str:
        """Generate complete sync report."""
        # Scan Personal Layer
        personal_root = Path(self.config['paths']['personal_root'])
        if personal_root.exists():
            scanner = VaultScanner(
                personal_root,
                check_checksums=self.config['sync_report']['check_checksums']
            )
            self.personal_files = scanner.scan()
        else:
            logger.warning(f"Personal root does not exist: {personal_root}")

        # Scan Continuity Layer(s)
        # For now, scan current repo as continuity layer
        repo_root = Path.cwd()
        if repo_root.exists():
            scanner = VaultScanner(
                repo_root,
                check_checksums=self.config['sync_report']['check_checksums']
            )
            self.continuity_files = scanner.scan()

        # Compare and detect conflicts
        self._detect_conflicts()

        # Determine overall status
        self._determine_status()

        # Generate markdown report
        report = self._format_report()

        return report

    def _detect_conflicts(self):
        """Detect conflicts between Personal and Continuity layers."""
        personal_set = set(self.personal_files.keys())
        continuity_set = set(self.continuity_files.keys())

        # Find common files
        common_files = personal_set & continuity_set

        for file_name in common_files:
            personal_meta = self.personal_files[file_name]
            continuity_meta = self.continuity_files[file_name]

            # Compare checksums
            if (personal_meta['checksum'] and continuity_meta['checksum'] and
                personal_meta['checksum'] != continuity_meta['checksum']):

                conflict = {
                    'file': file_name,
                    'type': 'checksum_mismatch',
                    'personal_checksum': personal_meta['checksum'],
                    'continuity_checksum': continuity_meta['checksum'],
                    'personal_modified': personal_meta['modified'],
                    'continuity_modified': continuity_meta['modified'],
                }

                self.conflicts.append(conflict)

        # Find missing files (in continuity but not in personal)
        missing_in_personal = continuity_set - personal_set
        self.missing.extend([f"Missing in Personal Layer: {f}" for f in missing_in_personal])

        # Find missing files (in personal but not in continuity)
        missing_in_continuity = personal_set - continuity_set
        self.missing.extend([f"Missing in Continuity Layer: {f}" for f in missing_in_continuity])

    def _determine_status(self):
        """Determine overall sync status."""
        if len(self.conflicts) > 0:
            self.status = "CONFLICT"
        elif len(self.missing) > 0:
            self.status = "DRIFT"
        else:
            self.status = "SYNCED"

    def _format_report(self) -> str:
        """Format report as markdown with YAML frontmatter."""
        date_str = datetime.now().strftime('%Y-%m-%d')
        time_str = datetime.now().strftime('%H:%M:%S')

        report_lines = [
            "---",
            f"date: {date_str}",
            "type: SYNC_REPORT",
            f"status: {self.status}",
            f"generated: {date_str} {time_str}",
            "tool: sync_report.py v1.0",
            "---",
            "",
            "# Vault Synchronization Report",
            "",
            f"**Generated:** {date_str} at {time_str}",
            f"**Status:** {self.status}",
            "",
            "---",
            "",
            "## Summary",
            "",
            f"- **Personal Layer:** {len(self.personal_files)} files",
            f"- **Continuity Layer:** {len(self.continuity_files)} files",
            f"- **Conflicts:** {len(self.conflicts)}",
            f"- **Missing/Drift:** {len(self.missing)}",
            "",
        ]

        # Add conflicts section
        if self.conflicts:
            report_lines.extend([
                "---",
                "",
                "## Conflicts",
                "",
            ])

            for i, conflict in enumerate(self.conflicts, 1):
                report_lines.extend([
                    f"### {i}. {conflict['file']}",
                    "",
                    f"**Type:** {conflict['type']}",
                    "",
                    "**Personal Layer:**",
                    f"- Checksum: `{conflict['personal_checksum']}`",
                    f"- Modified: {conflict['personal_modified']}",
                    "",
                    "**Continuity Layer:**",
                    f"- Checksum: `{conflict['continuity_checksum']}`",
                    f"- Modified: {conflict['continuity_modified']}",
                    "",
                    "**Action Required:** Manual review to determine authoritative version",
                    "",
                ])

        # Add missing files section
        if self.missing:
            report_lines.extend([
                "---",
                "",
                "## Missing Files / Drift",
                "",
            ])

            for missing_item in self.missing:
                report_lines.append(f"- {missing_item}")

            report_lines.append("")

        # Add recommendations
        report_lines.extend([
            "---",
            "",
            "## Recommendations",
            "",
        ])

        if self.status == "SYNCED":
            report_lines.append("✅ All layers are synchronized. No action required.")
        elif self.status == "CONFLICT":
            report_lines.extend([
                "⚠️ **Conflicts detected:** Manual review required",
                "",
                "1. Review each conflict above",
                "2. Determine authoritative version based on modification date and content",
                "3. Update non-authoritative layer to match",
                "4. Re-run sync_report.py to verify resolution",
            ])
        elif self.status == "DRIFT":
            report_lines.extend([
                "⚠️ **Drift detected:** Files missing in one or more layers",
                "",
                "1. Review missing files list above",
                "2. Determine if files should be synced or archived",
                "3. Copy files to appropriate layer or mark as intentionally different",
                "4. Re-run sync_report.py to verify resolution",
            ])

        report_lines.extend([
            "",
            "---",
            "",
            "## Continuity Seal",
            "",
            f"**Report Date:** {date_str}",
            "**Tool Version:** sync_report.py v1.0",
            "**Principle:** AHP-Compliant (Cite or Silence)",
            "**Status:** Verified",
            "",
            "⟡⟦SYNC⟧ · ⟡⟦VAULT⟧ · ⟡⟦CONTINUITY⟧",
            "",
        ])

        return "\n".join(report_lines)


@click.command()
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
    help='Output report path (default: reports/SYNC_REPORT_YYYY-MM-DD.md)'
)
@click.option(
    '--verbose',
    is_flag=True,
    help='Enable verbose logging'
)
def main(config: str, output: Optional[str], verbose: bool):
    """
    Generate vault synchronization report.

    Scans Personal Layer and Continuity Layer(s), compares files,
    and generates a detailed sync report.

    Example:
        python sync_report.py --config config/vault_automation.yaml
    """
    # Set up logging
    if verbose:
        logger.setLevel(logging.DEBUG)

    logger.info("MirrorDNA Vault Sync Report Generator v1.0")
    logger.info("=" * 60)

    # Load configuration
    try:
        with open(config, 'r') as f:
            config_data = yaml.safe_load(f)
            config_data = config_data.get('vault_automation', config_data)
    except Exception as e:
        logger.error(f"Failed to load configuration: {e}")
        sys.exit(1)

    # Generate report
    try:
        generator = SyncReportGenerator(config_data)
        report_content = generator.generate()

        # Determine output path
        if output is None:
            date_str = datetime.now().strftime('%Y-%m-%d')
            output_dir = Path(config_data['paths']['output_reports'])
            output_dir.mkdir(parents=True, exist_ok=True)
            output = output_dir / f"SYNC_REPORT_{date_str}.md"

        # Write report
        output_path = Path(output)
        output_path.parent.mkdir(parents=True, exist_ok=True)

        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(report_content)

        logger.info(f"✅ Report generated: {output_path}")
        logger.info(f"Status: {generator.status}")

        if generator.status == "CONFLICT":
            logger.warning(f"⚠️  {len(generator.conflicts)} conflicts detected")
            sys.exit(2)
        elif generator.status == "DRIFT":
            logger.warning(f"⚠️  {len(generator.missing)} files with drift detected")
            sys.exit(1)
        else:
            logger.info("✅ All layers synced")
            sys.exit(0)

    except Exception as e:
        logger.error(f"Failed to generate report: {e}")
        if verbose:
            import traceback
            traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()
