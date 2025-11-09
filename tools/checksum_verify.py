#!/usr/bin/env python3
"""
MirrorDNA Checksum Verification Suite

Cryptographic verification tool for vault integrity:
- Recursive SHA-256 on all files in target directory
- Compares against stored checksums.json manifest
- Detects: new files, modified files, deleted files
- Updates checksum manifest with consent
- Timestamps all changes

Usage:
    python checksum_verify.py --verify /path/to/vault
    python checksum_verify.py --update /path/to/vault --consent
    python checksum_verify.py --init /path/to/vault

Principles: Consent-first, tamper detection, audit trail
"""

import hashlib
import json
import logging
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Set

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


class ChecksumManager:
    """Manages checksums for vault integrity verification."""

    def __init__(self, vault_path: Path, config: Dict):
        self.vault_path = Path(vault_path)
        self.config = config
        self.checksum_config = config.get('checksum', {})
        self.algorithm = self.checksum_config.get('algorithm', 'sha256')
        self.manifest_file = self.vault_path / self.checksum_config.get('manifest_file', 'checksums.json')
        self.exclude_patterns = self.checksum_config.get('exclude_patterns', [])
        self.manifest: Dict[str, Dict] = {}
        self.current_checksums: Dict[str, Dict] = {}

    def load_manifest(self) -> bool:
        """Load existing checksum manifest."""
        if not self.manifest_file.exists():
            logger.warning(f"Manifest does not exist: {self.manifest_file}")
            return False

        try:
            with open(self.manifest_file, 'r') as f:
                self.manifest = json.load(f)
            logger.info(f"Loaded manifest with {len(self.manifest.get('files', {}))} entries")
            return True
        except Exception as e:
            logger.error(f"Failed to load manifest: {e}")
            return False

    def save_manifest(self, consent: bool = False) -> bool:
        """Save checksum manifest with consent check."""
        if not consent:
            logger.error("Cannot save manifest without --consent flag")
            return False

        manifest_data = {
            'version': '1.0',
            'algorithm': self.algorithm,
            'vault_path': str(self.vault_path),
            'last_updated': datetime.now().isoformat(),
            'files': self.current_checksums
        }

        try:
            with open(self.manifest_file, 'w') as f:
                json.dump(manifest_data, f, indent=2)
            logger.info(f"✅ Manifest saved: {self.manifest_file}")
            return True
        except Exception as e:
            logger.error(f"Failed to save manifest: {e}")
            return False

    def calculate_checksums(self) -> Dict[str, Dict]:
        """Calculate checksums for all files in vault."""
        if not self.vault_path.exists():
            logger.error(f"Vault path does not exist: {self.vault_path}")
            return {}

        logger.info(f"Calculating checksums for: {self.vault_path}")
        checksums = {}

        for file_path in self.vault_path.rglob('*'):
            if file_path.is_file() and not self._should_exclude(file_path):
                relative_path = file_path.relative_to(self.vault_path)
                checksum = self._calculate_file_checksum(file_path)

                if checksum:
                    checksums[str(relative_path)] = {
                        'checksum': checksum,
                        'size': file_path.stat().st_size,
                        'modified': datetime.fromtimestamp(file_path.stat().st_mtime).isoformat()
                    }

        logger.info(f"Calculated {len(checksums)} checksums")
        self.current_checksums = checksums
        return checksums

    def _should_exclude(self, file_path: Path) -> bool:
        """Check if file should be excluded from checksumming."""
        # Always exclude the manifest file itself
        if file_path == self.manifest_file:
            return True

        name = file_path.name
        path_str = str(file_path)

        for pattern in self.exclude_patterns:
            if pattern.startswith('*.'):
                if name.endswith(pattern[1:]):
                    return True
            elif pattern in path_str:
                return True

        return False

    def _calculate_file_checksum(self, file_path: Path) -> Optional[str]:
        """Calculate checksum for single file."""
        try:
            if self.algorithm == 'sha256':
                hash_obj = hashlib.sha256()
            elif self.algorithm == 'md5':
                hash_obj = hashlib.md5()
            else:
                logger.error(f"Unsupported algorithm: {self.algorithm}")
                return None

            with open(file_path, 'rb') as f:
                for byte_block in iter(lambda: f.read(4096), b""):
                    hash_obj.update(byte_block)

            return hash_obj.hexdigest()

        except Exception as e:
            logger.warning(f"Could not calculate checksum for {file_path}: {e}")
            return None

    def verify(self) -> Dict[str, List[str]]:
        """
        Verify current checksums against manifest.

        Returns:
            Dictionary with 'new', 'modified', 'deleted' file lists
        """
        if not self.manifest:
            logger.warning("No manifest loaded. Run with --init first.")
            return {'new': [], 'modified': [], 'deleted': []}

        # Calculate current checksums
        self.calculate_checksums()

        manifest_files = set(self.manifest.get('files', {}).keys())
        current_files = set(self.current_checksums.keys())

        # Find new files
        new_files = current_files - manifest_files

        # Find deleted files
        deleted_files = manifest_files - current_files

        # Find modified files
        modified_files = []
        for file_path in manifest_files & current_files:
            manifest_checksum = self.manifest['files'][file_path]['checksum']
            current_checksum = self.current_checksums[file_path]['checksum']

            if manifest_checksum != current_checksum:
                modified_files.append(file_path)

        return {
            'new': sorted(list(new_files)),
            'modified': sorted(modified_files),
            'deleted': sorted(list(deleted_files))
        }


@click.group()
def cli():
    """MirrorDNA Checksum Verification Suite"""
    pass


@cli.command()
@click.argument('vault_path', type=click.Path(exists=True))
@click.option(
    '--config',
    type=click.Path(exists=True),
    default='tools/config/vault_automation.yaml',
    help='Path to configuration YAML file'
)
@click.option(
    '--verbose',
    is_flag=True,
    help='Enable verbose logging'
)
def init(vault_path: str, config: str, verbose: bool):
    """
    Initialize new checksum manifest for vault.

    Example:
        python checksum_verify.py init /path/to/vault
    """
    if verbose:
        logger.setLevel(logging.DEBUG)

    logger.info("MirrorDNA Checksum Verification Suite v1.0")
    logger.info("=" * 60)
    logger.info("MODE: Initialize")

    # Load configuration
    try:
        with open(config, 'r') as f:
            config_data = yaml.safe_load(f)
            config_data = config_data.get('vault_automation', config_data)
    except Exception as e:
        logger.error(f"Failed to load configuration: {e}")
        sys.exit(1)

    # Initialize manager
    manager = ChecksumManager(Path(vault_path), config_data)

    # Calculate checksums
    manager.calculate_checksums()

    # Save manifest with automatic consent for init
    if manager.save_manifest(consent=True):
        logger.info(f"✅ Initialized manifest with {len(manager.current_checksums)} files")
        logger.info(f"Manifest saved to: {manager.manifest_file}")
        sys.exit(0)
    else:
        logger.error("Failed to initialize manifest")
        sys.exit(1)


@cli.command()
@click.argument('vault_path', type=click.Path(exists=True))
@click.option(
    '--config',
    type=click.Path(exists=True),
    default='tools/config/vault_automation.yaml',
    help='Path to configuration YAML file'
)
@click.option(
    '--verbose',
    is_flag=True,
    help='Enable verbose logging'
)
def verify(vault_path: str, config: str, verbose: bool):
    """
    Verify vault integrity against checksum manifest.

    Example:
        python checksum_verify.py verify /path/to/vault
    """
    if verbose:
        logger.setLevel(logging.DEBUG)

    logger.info("MirrorDNA Checksum Verification Suite v1.0")
    logger.info("=" * 60)
    logger.info("MODE: Verify")

    # Load configuration
    try:
        with open(config, 'r') as f:
            config_data = yaml.safe_load(f)
            config_data = config_data.get('vault_automation', config_data)
    except Exception as e:
        logger.error(f"Failed to load configuration: {e}")
        sys.exit(1)

    # Initialize manager
    manager = ChecksumManager(Path(vault_path), config_data)

    # Load manifest
    if not manager.load_manifest():
        logger.error("No manifest found. Run with 'init' command first.")
        sys.exit(1)

    # Verify
    results = manager.verify()

    # Report results
    total_changes = len(results['new']) + len(results['modified']) + len(results['deleted'])

    logger.info("")
    logger.info("=" * 60)
    logger.info("VERIFICATION RESULTS")
    logger.info("=" * 60)
    logger.info(f"New files: {len(results['new'])}")
    logger.info(f"Modified files: {len(results['modified'])}")
    logger.info(f"Deleted files: {len(results['deleted'])}")
    logger.info("")

    if total_changes == 0:
        logger.info("✅ Vault integrity verified - No changes detected")
        sys.exit(0)
    else:
        logger.warning(f"⚠️  {total_changes} changes detected")

        if results['new']:
            logger.info("")
            logger.info("NEW FILES:")
            for f in results['new'][:10]:  # Show first 10
                logger.info(f"  + {f}")
            if len(results['new']) > 10:
                logger.info(f"  ... and {len(results['new']) - 10} more")

        if results['modified']:
            logger.info("")
            logger.info("MODIFIED FILES:")
            for f in results['modified'][:10]:
                logger.info(f"  ~ {f}")
            if len(results['modified']) > 10:
                logger.info(f"  ... and {len(results['modified']) - 10} more")

        if results['deleted']:
            logger.info("")
            logger.info("DELETED FILES:")
            for f in results['deleted'][:10]:
                logger.info(f"  - {f}")
            if len(results['deleted']) > 10:
                logger.info(f"  ... and {len(results['deleted']) - 10} more")

        logger.info("")
        logger.info("To update manifest, run:")
        logger.info(f"  python checksum_verify.py update {vault_path} --consent")

        sys.exit(1)


@cli.command()
@click.argument('vault_path', type=click.Path(exists=True))
@click.option(
    '--config',
    type=click.Path(exists=True),
    default='tools/config/vault_automation.yaml',
    help='Path to configuration YAML file'
)
@click.option(
    '--consent',
    is_flag=True,
    help='Consent to update manifest (required)'
)
@click.option(
    '--verbose',
    is_flag=True,
    help='Enable verbose logging'
)
def update(vault_path: str, config: str, consent: bool, verbose: bool):
    """
    Update checksum manifest with current vault state.

    Requires --consent flag for safety.

    Example:
        python checksum_verify.py update /path/to/vault --consent
    """
    if verbose:
        logger.setLevel(logging.DEBUG)

    logger.info("MirrorDNA Checksum Verification Suite v1.0")
    logger.info("=" * 60)
    logger.info("MODE: Update")

    if not consent:
        logger.error("Update requires --consent flag for safety")
        logger.error("Run: python checksum_verify.py update <path> --consent")
        sys.exit(1)

    # Load configuration
    try:
        with open(config, 'r') as f:
            config_data = yaml.safe_load(f)
            config_data = config_data.get('vault_automation', config_data)
    except Exception as e:
        logger.error(f"Failed to load configuration: {e}")
        sys.exit(1)

    # Initialize manager
    manager = ChecksumManager(Path(vault_path), config_data)

    # Load existing manifest
    manager.load_manifest()

    # Calculate current checksums
    manager.calculate_checksums()

    # Save updated manifest
    if manager.save_manifest(consent=True):
        logger.info(f"✅ Manifest updated with {len(manager.current_checksums)} files")
        sys.exit(0)
    else:
        logger.error("Failed to update manifest")
        sys.exit(1)


if __name__ == '__main__':
    cli()
