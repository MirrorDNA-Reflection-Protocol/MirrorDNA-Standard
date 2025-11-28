#!/usr/bin/env python3
"""
MirrorDNA Vault Manager

VaultID: AMOS://MirrorDNA-Standard/Tools/VaultManager/v1.0
GlyphSig: ⟡⟦VAULT⟧ · ⟡⟦CONTINUITY⟧ · ⟡⟦LINEAGE⟧
Predecessor: None (Initial Release)
Successor: TBD

CONSTITUTIONAL STATUS:
Enforceability: MANDATORY
Verifiability: AUTOMATED
Adoption: CORE
Truth-State: [Fact - Core Infrastructure]

Vault Continuity Management System
===================================

Implements vault governance as defined in Master Citation v15.2:
- VaultID generation and tracking
- SHA-256 checksum computation and verification
- Lineage management (predecessor/successor chains)
- Vault state integrity validation
- Manifest enforcement

Core Formula: Vault = System

The vault is the source of truth, not ephemeral context.
All continuity flows through the vault.
"""

import hashlib
import json
import re
import unicodedata
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, List, Optional, Tuple
from dataclasses import dataclass, asdict


@dataclass
class VaultID:
    """
    Represents a MirrorDNA VaultID following AMOS:// URI format.

    Format: AMOS://[Domain]/[Resource]/[Version]
    Example: AMOS://MirrorDNA-Standard/Tools/VaultManager/v1.0
    """
    domain: str
    resource: str
    version: str

    def __str__(self) -> str:
        return f"AMOS://{self.domain}/{self.resource}/{self.version}"

    @classmethod
    def parse(cls, vault_id_str: str) -> 'VaultID':
        """Parse VaultID from string."""
        if not vault_id_str.startswith('AMOS://'):
            raise ValueError(f"Invalid VaultID format: {vault_id_str}")

        parts = vault_id_str[7:].split('/')
        if len(parts) < 3:
            raise ValueError(f"VaultID must have domain/resource/version: {vault_id_str}")

        domain = parts[0]
        version = parts[-1]
        resource = '/'.join(parts[1:-1])

        return cls(domain=domain, resource=resource, version=version)

    @classmethod
    def generate(
        cls,
        domain: str,
        resource: str,
        major: int = 1,
        minor: int = 0,
        patch: Optional[int] = None
    ) -> 'VaultID':
        """Generate a new VaultID with semantic versioning."""
        if patch is not None:
            version = f"v{major}.{minor}.{patch}"
        else:
            version = f"v{major}.{minor}"

        return cls(domain=domain, resource=resource, version=version)


@dataclass
class LineageChain:
    """
    Represents lineage relationship between vault artifacts.
    """
    vault_id: str
    predecessor: Optional[str] = None
    successor: Optional[str] = None
    branch_point: Optional[str] = None  # For forks
    merge_point: Optional[str] = None   # For merges

    def is_root(self) -> bool:
        """Check if this is a root node (no predecessor)."""
        return self.predecessor is None

    def is_leaf(self) -> bool:
        """Check if this is a leaf node (no successor)."""
        return self.successor is None

    def is_fork(self) -> bool:
        """Check if this represents a fork point."""
        return self.branch_point is not None

    def is_merge(self) -> bool:
        """Check if this represents a merge point."""
        return self.merge_point is not None


class VaultManager:
    """
    Manages vault continuity, checksums, and lineage.

    Responsibilities:
    1. Generate and validate VaultIDs
    2. Compute and verify SHA-256 checksums
    3. Track lineage chains
    4. Enforce vault integrity
    5. Manage vault manifests
    """

    def __init__(self, vault_path: Path):
        """
        Initialize Vault Manager.

        Args:
            vault_path: Path to vault root directory
        """
        self.vault_path = Path(vault_path)
        self.manifest_path = self.vault_path / "vault_manifest.json"
        self.lineage_path = self.vault_path / "lineage_graph.json"

        # Load or initialize manifest
        self.manifest: Dict[str, Any] = self._load_manifest()
        self.lineage_graph: Dict[str, LineageChain] = self._load_lineage()

    def _load_manifest(self) -> Dict[str, Any]:
        """Load vault manifest or create default."""
        if self.manifest_path.exists():
            with open(self.manifest_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        else:
            return {
                'vault_version': '1.0',
                'created_at': datetime.utcnow().isoformat(),
                'artifacts': {},
                'checksums': {},
                'lineage_chains': {}
            }

    def _load_lineage(self) -> Dict[str, LineageChain]:
        """Load lineage graph or create empty."""
        if self.lineage_path.exists():
            with open(self.lineage_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return {
                    k: LineageChain(**v) for k, v in data.items()
                }
        else:
            return {}

    def _save_manifest(self) -> None:
        """Save manifest to disk."""
        self.vault_path.mkdir(parents=True, exist_ok=True)
        with open(self.manifest_path, 'w', encoding='utf-8') as f:
            json.dump(self.manifest, f, indent=2, ensure_ascii=False)
            f.write('\n')

    def _save_lineage(self) -> None:
        """Save lineage graph to disk."""
        self.vault_path.mkdir(parents=True, exist_ok=True)
        data = {k: asdict(v) for k, v in self.lineage_graph.items()}
        with open(self.lineage_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
            f.write('\n')

    def compute_checksum(
        self,
        content: str,
        canonicalize: bool = True
    ) -> str:
        """
        Compute SHA-256 checksum with optional canonicalization.

        Args:
            content: Content to hash
            canonicalize: Apply canonicalization (UTF-8, LF, NFC, trim)

        Returns:
            64-character hex digest
        """
        if canonicalize:
            content = self._canonicalize_content(content)

        return hashlib.sha256(content.encode('utf-8')).hexdigest()

    def _canonicalize_content(self, content: str) -> str:
        """
        Canonicalize content for consistent hashing.

        Per Master Citation v15.2 requirements:
        - UTF-8 encoding
        - LF line endings
        - NFC Unicode normalization
        - Trim trailing whitespace
        """
        # Normalize to NFC
        content = unicodedata.normalize('NFC', content)

        # Convert to LF line endings
        content = content.replace('\r\n', '\n').replace('\r', '\n')

        # Trim trailing whitespace per line
        lines = content.split('\n')
        lines = [line.rstrip() for line in lines]
        content = '\n'.join(lines)

        # Trim trailing newlines at end of file
        content = content.rstrip('\n') + '\n'

        return content

    def compute_file_checksum(self, file_path: Path) -> str:
        """
        Compute checksum for a file.

        Args:
            file_path: Path to file

        Returns:
            SHA-256 checksum
        """
        content = file_path.read_text(encoding='utf-8')
        return self.compute_checksum(content)

    def verify_checksum(
        self,
        content: str,
        expected_checksum: str
    ) -> Tuple[bool, Optional[str]]:
        """
        Verify content against expected checksum.

        Args:
            content: Content to verify
            expected_checksum: Expected SHA-256 checksum

        Returns:
            Tuple of (is_valid, actual_checksum)
        """
        actual = self.compute_checksum(content)
        is_valid = actual == expected_checksum
        return is_valid, actual

    def register_artifact(
        self,
        vault_id: str,
        file_path: Path,
        predecessor: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None
    ) -> str:
        """
        Register an artifact in the vault with checksum and lineage.

        Args:
            vault_id: VaultID for the artifact
            file_path: Path to artifact file
            predecessor: VaultID of predecessor (for lineage)
            metadata: Optional metadata dict

        Returns:
            Computed checksum
        """
        # Compute checksum
        checksum = self.compute_file_checksum(file_path)

        # Register in manifest
        self.manifest['artifacts'][vault_id] = {
            'file_path': str(file_path),
            'registered_at': datetime.utcnow().isoformat(),
            'metadata': metadata or {}
        }

        self.manifest['checksums'][vault_id] = checksum

        # Register lineage
        lineage = LineageChain(
            vault_id=vault_id,
            predecessor=predecessor
        )
        self.lineage_graph[vault_id] = lineage

        # Update predecessor's successor if it exists
        if predecessor and predecessor in self.lineage_graph:
            self.lineage_graph[predecessor].successor = vault_id

        # Save updates
        self._save_manifest()
        self._save_lineage()

        return checksum

    def verify_artifact(self, vault_id: str) -> Tuple[bool, List[str]]:
        """
        Verify artifact integrity.

        Args:
            vault_id: VaultID to verify

        Returns:
            Tuple of (is_valid, issues)
        """
        issues = []

        # Check if registered
        if vault_id not in self.manifest['artifacts']:
            return False, [f"VaultID {vault_id} not registered in manifest"]

        # Get artifact info
        artifact = self.manifest['artifacts'][vault_id]
        file_path = Path(artifact['file_path'])

        # Check file exists
        if not file_path.exists():
            issues.append(f"Artifact file not found: {file_path}")
            return False, issues

        # Verify checksum
        expected_checksum = self.manifest['checksums'].get(vault_id)
        if not expected_checksum:
            issues.append("No checksum recorded for artifact")
            return False, issues

        actual_checksum = self.compute_file_checksum(file_path)
        if actual_checksum != expected_checksum:
            issues.append(
                f"Checksum mismatch: expected {expected_checksum}, "
                f"got {actual_checksum}"
            )
            return False, issues

        return True, []

    def trace_lineage(
        self,
        vault_id: str,
        direction: str = 'backward'
    ) -> List[str]:
        """
        Trace lineage chain from a VaultID.

        Args:
            vault_id: Starting VaultID
            direction: 'backward' (to root) or 'forward' (to leaf)

        Returns:
            List of VaultIDs in lineage chain
        """
        if vault_id not in self.lineage_graph:
            return []

        chain = [vault_id]
        current = vault_id

        if direction == 'backward':
            # Trace to root
            while True:
                lineage = self.lineage_graph[current]
                if lineage.predecessor is None:
                    break
                chain.append(lineage.predecessor)
                current = lineage.predecessor
                if current not in self.lineage_graph:
                    break
        else:
            # Trace to leaf
            while True:
                lineage = self.lineage_graph[current]
                if lineage.successor is None:
                    break
                chain.append(lineage.successor)
                current = lineage.successor
                if current not in self.lineage_graph:
                    break

        return chain

    def validate_lineage_chain(self, vault_id: str) -> Tuple[bool, List[str]]:
        """
        Validate complete lineage chain for a VaultID.

        Args:
            vault_id: VaultID to validate

        Returns:
            Tuple of (is_valid, issues)
        """
        issues = []

        if vault_id not in self.lineage_graph:
            return False, [f"VaultID {vault_id} not in lineage graph"]

        # Trace backward to root
        backward_chain = self.trace_lineage(vault_id, 'backward')

        # Verify each link
        for i, vid in enumerate(backward_chain):
            if i == 0:
                continue

            current_lineage = self.lineage_graph.get(vid)
            if not current_lineage:
                issues.append(f"Missing lineage entry for {vid}")
                continue

            expected_successor = backward_chain[i - 1]
            if current_lineage.successor != expected_successor:
                issues.append(
                    f"Lineage break at {vid}: "
                    f"expected successor {expected_successor}, "
                    f"got {current_lineage.successor}"
                )

        return len(issues) == 0, issues

    def generate_lineage_report(self) -> Dict[str, Any]:
        """
        Generate comprehensive lineage report.

        Returns:
            Lineage report dict
        """
        report = {
            'total_artifacts': len(self.lineage_graph),
            'root_nodes': [],
            'leaf_nodes': [],
            'fork_points': [],
            'chains': {}
        }

        # Identify special nodes
        for vault_id, lineage in self.lineage_graph.items():
            if lineage.is_root():
                report['root_nodes'].append(vault_id)
            if lineage.is_leaf():
                report['leaf_nodes'].append(vault_id)
            if lineage.is_fork():
                report['fork_points'].append(vault_id)

        # Trace chains from each root
        for root in report['root_nodes']:
            chain = self.trace_lineage(root, 'forward')
            report['chains'][root] = chain

        return report

    def export_vault_state(self) -> Dict[str, Any]:
        """
        Export complete vault state for backup or transfer.

        Returns:
            Complete vault state dict
        """
        return {
            'manifest': self.manifest,
            'lineage_graph': {
                k: asdict(v) for k, v in self.lineage_graph.items()
            },
            'exported_at': datetime.utcnow().isoformat(),
            'vault_checksum': self.compute_vault_state_hash()
        }

    def compute_vault_state_hash(self) -> str:
        """
        Compute hash of entire vault state.

        Returns:
            SHA-256 hash of vault state
        """
        state = {
            'artifacts': sorted(self.manifest['artifacts'].items()),
            'checksums': sorted(self.manifest['checksums'].items())
        }
        state_json = json.dumps(state, sort_keys=True, ensure_ascii=False)
        return hashlib.sha256(state_json.encode('utf-8')).hexdigest()


def generate_vault_id(
    domain: str,
    resource: str,
    version: str = "v1.0"
) -> str:
    """
    Convenience function to generate VaultID string.

    Args:
        domain: Domain (e.g., 'MirrorDNA-Standard')
        resource: Resource path (e.g., 'Tools/VaultManager')
        version: Version string (e.g., 'v1.0')

    Returns:
        VaultID string in AMOS:// format
    """
    return f"AMOS://{domain}/{resource}/{version}"


if __name__ == "__main__":
    import sys
    import argparse

    parser = argparse.ArgumentParser(description="MirrorDNA Vault Manager")
    parser.add_argument('--vault', required=True, help='Path to vault')

    subparsers = parser.add_subparsers(dest='command', help='Commands')

    # Register command
    register_parser = subparsers.add_parser('register', help='Register artifact')
    register_parser.add_argument('--vault-id', required=True, help='VaultID')
    register_parser.add_argument('--file', required=True, help='File path')
    register_parser.add_argument('--predecessor', help='Predecessor VaultID')

    # Verify command
    verify_parser = subparsers.add_parser('verify', help='Verify artifact')
    verify_parser.add_argument('--vault-id', required=True, help='VaultID to verify')

    # Lineage command
    lineage_parser = subparsers.add_parser('lineage', help='Trace lineage')
    lineage_parser.add_argument('--vault-id', required=True, help='VaultID')
    lineage_parser.add_argument('--direction', choices=['backward', 'forward'],
                               default='backward', help='Trace direction')

    # Report command
    subparsers.add_parser('report', help='Generate lineage report')

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    manager = VaultManager(Path(args.vault))

    if args.command == 'register':
        checksum = manager.register_artifact(
            vault_id=args.vault_id,
            file_path=Path(args.file),
            predecessor=args.predecessor
        )
        print(f"✓ Registered {args.vault_id}")
        print(f"  Checksum: {checksum}")

    elif args.command == 'verify':
        is_valid, issues = manager.verify_artifact(args.vault_id)
        if is_valid:
            print(f"✓ {args.vault_id} verified")
        else:
            print(f"✗ {args.vault_id} verification failed:")
            for issue in issues:
                print(f"  - {issue}")
            sys.exit(1)

    elif args.command == 'lineage':
        chain = manager.trace_lineage(args.vault_id, args.direction)
        print(f"Lineage chain ({args.direction}):")
        for i, vault_id in enumerate(chain):
            print(f"  {i}. {vault_id}")

    elif args.command == 'report':
        report = manager.generate_lineage_report()
        print(json.dumps(report, indent=2))
