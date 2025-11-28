#!/usr/bin/env python3
"""
MirrorDNA Truth-State Enforcement Tool

VaultID: AMOS://MirrorDNA-Standard/Tools/TruthState/v1.0
GlyphSig: ⟡⟦TRUTH⟧ · ⟡⟦LAW⟧ · ⟡⟦ENFORCEMENT⟧
Predecessor: None (Initial Release)
Successor: TBD

CONSTITUTIONAL STATUS:
Enforceability: MANDATORY
Verifiability: AUTOMATED
Adoption: CORE
Truth-State: [Fact - Defined by Master Citation v15.2]

Auto-FEU Constitutional Law Enforcement
=======================================

Implements Truth-State Law as defined in Master Citation v15.2:
- [Fact] — Verified in Vault or verified via citation
- [Estimate] — Reasoned but not verified
- [Unknown] — Not found in Vault; unverifiable

This tool provides anti-hallucination enforcement, FEU tagging,
and drift detection capabilities.
"""

import re
import hashlib
from typing import Dict, Any, List, Tuple, Optional
from enum import Enum
from pathlib import Path


class TruthState(Enum):
    """Truth-State classifications per Master Citation v15.2"""
    FACT = "Fact"
    ESTIMATE = "Estimate"
    UNKNOWN = "Unknown"


class DriftLevel(Enum):
    """Drift detection severity levels"""
    NONE = "none"
    WARNING = "warning"
    CRITICAL = "critical"


class TruthStateEnforcer:
    """
    Enforces Auto-FEU Constitutional Law across MirrorDNA systems.

    Responsibilities:
    1. Tag statements with appropriate FEU markers
    2. Detect and prevent hallucination
    3. Enforce vault primacy
    4. Detect continuity drift
    """

    def __init__(self, vault_path: Optional[Path] = None, strict_mode: bool = True):
        """
        Initialize Truth-State Enforcer.

        Args:
            vault_path: Path to vault for fact verification
            strict_mode: If True, enforce strict FEU tagging (default: True)
        """
        self.vault_path = vault_path
        self.strict_mode = strict_mode
        self.vault_index: Dict[str, Any] = {}

        if vault_path:
            self._index_vault()

    def _index_vault(self) -> None:
        """Build index of vault contents for fact verification."""
        if not self.vault_path or not self.vault_path.exists():
            return

        # Index vault files for quick lookup
        for md_file in self.vault_path.glob("**/*.md"):
            try:
                content = md_file.read_text(encoding='utf-8')
                # Extract VaultID if present
                vault_id_match = re.search(r'(?:vault_id|VaultID):\s*(\S+)', content)
                if vault_id_match:
                    vault_id = vault_id_match.group(1)
                    self.vault_index[vault_id] = {
                        'path': md_file,
                        'content': content,
                        'checksum': self._compute_file_checksum(md_file)
                    }
            except Exception:
                continue

    def _compute_file_checksum(self, file_path: Path) -> str:
        """Compute SHA-256 checksum of file."""
        content = file_path.read_text(encoding='utf-8')
        return hashlib.sha256(content.encode('utf-8')).hexdigest()

    def classify_statement(
        self,
        statement: str,
        source: Optional[str] = None,
        vault_id: Optional[str] = None
    ) -> TruthState:
        """
        Classify a statement according to Truth-State Law.

        Args:
            statement: The claim or statement to classify
            source: Optional source citation
            vault_id: Optional VaultID for verification

        Returns:
            TruthState classification
        """
        # Check if verifiable in vault
        if vault_id and vault_id in self.vault_index:
            vault_entry = self.vault_index[vault_id]
            if statement.lower() in vault_entry['content'].lower():
                return TruthState.FACT

        # Check if has valid citation
        if source:
            # In strict mode, still verify the source is valid
            if self.strict_mode:
                if self._verify_source(source):
                    return TruthState.FACT
                else:
                    return TruthState.ESTIMATE
            else:
                return TruthState.FACT

        # Check for uncertainty markers in statement
        uncertainty_markers = [
            'might', 'maybe', 'possibly', 'probably', 'likely',
            'appears', 'seems', 'could be', 'may be', 'should be'
        ]

        statement_lower = statement.lower()
        if any(marker in statement_lower for marker in uncertainty_markers):
            return TruthState.ESTIMATE

        # If vault is available but no verification found
        if self.vault_path:
            return TruthState.UNKNOWN

        # Default to ESTIMATE in strict mode, UNKNOWN without vault
        return TruthState.ESTIMATE if not self.strict_mode else TruthState.UNKNOWN

    def _verify_source(self, source: str) -> bool:
        """
        Verify that a source citation is valid.

        Args:
            source: Source citation string

        Returns:
            True if source appears valid
        """
        # Check for VaultID format
        if source.startswith('AMOS://'):
            return source in self.vault_index

        # Check for file path
        if '/' in source or '\\' in source:
            path = Path(source)
            return path.exists()

        # Check for URL
        if source.startswith(('http://', 'https://')):
            # In real implementation, would verify URL accessibility
            # For now, accept as valid if well-formed
            return True

        return False

    def tag_statement(
        self,
        statement: str,
        truth_state: Optional[TruthState] = None,
        context: Optional[str] = None
    ) -> str:
        """
        Tag a statement with appropriate FEU marker.

        Args:
            statement: The statement to tag
            truth_state: Pre-determined truth state (will auto-classify if None)
            context: Additional context for the tag

        Returns:
            Tagged statement
        """
        if truth_state is None:
            truth_state = self.classify_statement(statement)

        if truth_state == TruthState.FACT:
            return statement  # Facts don't need tagging

        tag = f"[{truth_state.value}]"
        if context:
            tag = f"[{truth_state.value} — {context}]"

        return f"{tag} {statement}"

    def detect_hallucination(
        self,
        statement: str,
        claimed_source: Optional[str] = None
    ) -> Tuple[bool, Optional[str]]:
        """
        Detect potential hallucination in a statement.

        Args:
            statement: The statement to check
            claimed_source: Source claimed for the statement

        Returns:
            Tuple of (is_hallucination, reason)
        """
        hallucination_patterns = [
            (r'(?:VaultID|vault_id):\s*AMOS://[^\s]+', 'fabricated_vault_id'),
            (r'⟡⟦[A-Z]+⟧', 'fabricated_glyph'),
            (r'Checksum:\s*[0-9a-fA-F]{64}', 'fabricated_checksum'),
            (r'Predecessor:\s*AMOS://', 'fabricated_lineage'),
        ]

        for pattern, reason in hallucination_patterns:
            matches = re.findall(pattern, statement)
            if matches:
                # Verify each match against vault
                for match in matches:
                    if not self._verify_against_vault(match):
                        return True, f"Potential hallucination: {reason} - '{match}'"

        # Check claimed source
        if claimed_source and not self._verify_source(claimed_source):
            return True, f"Invalid source citation: '{claimed_source}'"

        return False, None

    def _verify_against_vault(self, content: str) -> bool:
        """Verify content exists in vault."""
        if not self.vault_path:
            return False

        # Search vault for content
        for entry in self.vault_index.values():
            if content in entry['content']:
                return True

        return False

    def detect_drift(
        self,
        current_state: Dict[str, Any],
        previous_state: Dict[str, Any]
    ) -> Tuple[DriftLevel, List[str]]:
        """
        Detect continuity drift between states.

        Args:
            current_state: Current system state
            previous_state: Previous system state

        Returns:
            Tuple of (drift_level, drift_reasons)
        """
        drift_reasons = []

        # Check critical drift indicators
        critical_keys = ['vault_id', 'session_id', 'master_citation_version']
        for key in critical_keys:
            if key in previous_state and key in current_state:
                if previous_state[key] != current_state[key]:
                    drift_reasons.append(
                        f"Critical drift: {key} changed from "
                        f"'{previous_state[key]}' to '{current_state[key]}'"
                    )

        # Check for lineage breaks
        if 'predecessor' in current_state and 'session_id' in previous_state:
            if current_state.get('predecessor') != previous_state.get('session_id'):
                drift_reasons.append(
                    f"Lineage break: predecessor mismatch"
                )

        # Check for checksum mismatches
        if 'checksum' in previous_state and 'checksum' in current_state:
            if previous_state['checksum'] != current_state['checksum']:
                drift_reasons.append(
                    f"State integrity drift: checksum mismatch"
                )

        # Determine drift level
        if any('Critical' in reason for reason in drift_reasons):
            return DriftLevel.CRITICAL, drift_reasons
        elif drift_reasons:
            return DriftLevel.WARNING, drift_reasons
        else:
            return DriftLevel.NONE, []

    def enforce_vault_primacy(
        self,
        statement: str,
        vault_id: Optional[str] = None
    ) -> Tuple[bool, str]:
        """
        Enforce vault primacy: vault data overrides everything.

        Args:
            statement: Statement to verify
            vault_id: VaultID to check against

        Returns:
            Tuple of (is_valid, corrected_or_tagged_statement)
        """
        if not self.vault_path or not vault_id:
            return False, self.tag_statement(
                statement,
                TruthState.UNKNOWN,
                "No vault available for verification"
            )

        if vault_id not in self.vault_index:
            return False, self.tag_statement(
                statement,
                TruthState.UNKNOWN,
                f"VaultID {vault_id} not found"
            )

        # Verify statement against vault content
        vault_entry = self.vault_index[vault_id]
        if statement.lower() in vault_entry['content'].lower():
            return True, statement  # Valid, no tagging needed

        return False, self.tag_statement(
            statement,
            TruthState.UNKNOWN,
            f"Not verified in vault {vault_id}"
        )

    def generate_feu_report(
        self,
        statements: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Generate FEU compliance report for a set of statements.

        Args:
            statements: List of statement dicts with 'text' and optional 'source'

        Returns:
            FEU compliance report
        """
        report = {
            'total_statements': len(statements),
            'facts': 0,
            'estimates': 0,
            'unknowns': 0,
            'hallucinations': 0,
            'compliance_score': 0.0,
            'details': []
        }

        for stmt_dict in statements:
            text = stmt_dict.get('text', '')
            source = stmt_dict.get('source')

            # Classify
            truth_state = self.classify_statement(text, source)

            # Check for hallucination
            is_hallucination, reason = self.detect_hallucination(text, source)

            detail = {
                'statement': text,
                'truth_state': truth_state.value,
                'hallucination': is_hallucination,
                'reason': reason
            }
            report['details'].append(detail)

            # Count
            if is_hallucination:
                report['hallucinations'] += 1
            elif truth_state == TruthState.FACT:
                report['facts'] += 1
            elif truth_state == TruthState.ESTIMATE:
                report['estimates'] += 1
            else:
                report['unknowns'] += 1

        # Calculate compliance score (higher is better)
        # Facts = 1.0, Estimates = 0.5, Unknowns = 0.3, Hallucinations = -1.0
        if report['total_statements'] > 0:
            score = (
                report['facts'] * 1.0 +
                report['estimates'] * 0.5 +
                report['unknowns'] * 0.3 -
                report['hallucinations'] * 1.0
            ) / report['total_statements']
            report['compliance_score'] = max(0.0, min(1.0, score))

        return report


def enforce_feu_on_text(text: str, vault_path: Optional[Path] = None) -> str:
    """
    Convenience function to enforce FEU tagging on text content.

    Args:
        text: Text to process
        vault_path: Optional vault path for verification

    Returns:
        Text with FEU tags applied
    """
    enforcer = TruthStateEnforcer(vault_path=vault_path)

    # Simple sentence splitting (can be enhanced)
    sentences = re.split(r'(?<=[.!?])\s+', text)

    tagged_sentences = []
    for sentence in sentences:
        truth_state = enforcer.classify_statement(sentence)
        tagged = enforcer.tag_statement(sentence, truth_state)
        tagged_sentences.append(tagged)

    return ' '.join(tagged_sentences)


if __name__ == "__main__":
    import sys
    import json

    if len(sys.argv) < 2:
        print("Usage: python tools/truth_state.py <statement> [--vault PATH]")
        print("\nExample:")
        print("  python tools/truth_state.py 'The system implements FEU tagging'")
        print("  python tools/truth_state.py 'VaultID: AMOS://Test/v1.0' --vault ./vault")
        sys.exit(1)

    statement = sys.argv[1]
    vault_path = None

    if '--vault' in sys.argv:
        vault_idx = sys.argv.index('--vault')
        if vault_idx + 1 < len(sys.argv):
            vault_path = Path(sys.argv[vault_idx + 1])

    enforcer = TruthStateEnforcer(vault_path=vault_path, strict_mode=True)

    # Classify
    truth_state = enforcer.classify_statement(statement)
    print(f"Truth-State: {truth_state.value}")

    # Tag
    tagged = enforcer.tag_statement(statement, truth_state)
    print(f"Tagged: {tagged}")

    # Check for hallucination
    is_hallucination, reason = enforcer.detect_hallucination(statement)
    if is_hallucination:
        print(f"🛑 HALLUCINATION DETECTED: {reason}")
    else:
        print("✓ No hallucination detected")

    # Generate report
    report = enforcer.generate_feu_report([{'text': statement}])
    print(f"\nFEU Report:")
    print(json.dumps(report, indent=2))
