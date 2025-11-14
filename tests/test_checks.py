"""
Tests for validators.checks modules.
"""

import pytest

from validators.checks.continuity_checks import check_continuity_compliance
from validators.checks.reflection_checks import check_reflection_compliance
from validators.checks.trustbydesign_checks import check_trustbydesign_compliance


# Level 1 test data
LEVEL1_MANIFEST = {
    'name': 'TestApp',
    'version': '1.0.0',
    'mirrorDNA_compliance_level': 'level_1_basic_reflection',
    'layers': {'mirrorDNA_protocol': True}
}

LEVEL1_POLICY = {
    'policy_version': '1.0.0',
    'reflection_mode': 'constitutive',
    'uncertainty_handling': {
        'cite_or_silence': True,
        'unknown_marker': '[Unknown]'
    },
    'anti_hallucination': {
        'source_citation': True
    }
}


# Level 2 test data
LEVEL2_MANIFEST = {
    'name': 'TestApp',
    'version': '2.0.0',
    'mirrorDNA_compliance_level': 'level_2_continuity_aware',
    'layers': {'mirrorDNA_protocol': True}
}

LEVEL2_PROFILE = {
    'profile_version': '1.0.0',
    'continuity_mechanism': 'local_state',
    'state_persistence': {
        'enabled': True,
        'storage_type': 'file_system'
    },
    'continuity_guarantees': {
        'state_consistency': True,
        'lineage_tracking': True
    }
}


# Level 3 test data
LEVEL3_MANIFEST = {
    'name': 'TestApp',
    'version': '3.0.0',
    'mirrorDNA_compliance_level': 'level_3_vault_backed_sovereign',
    'layers': {'mirrorDNA_protocol': True}
}

LEVEL3_PROFILE = {
    'profile_version': '1.0.0',
    'continuity_mechanism': 'vault_backed',
    'state_persistence': {
        'enabled': True,
        'storage_type': 'vault'
    },
    'vault_configuration': {
        'vault_type': 'obsidian',
        'vault_id': 'AMOS://Test/v1.0'
    },
    'continuity_guarantees': {
        'identity_preservation': True,
        'state_consistency': True,
        'lineage_tracking': True,
        'anti_hallucination': True
    }
}

LEVEL3_POLICY = {
    'policy_version': '1.0.0',
    'reflection_mode': 'constitutive',
    'uncertainty_handling': {
        'cite_or_silence': True,
        'unknown_marker': '[Unknown]'
    },
    'anti_hallucination': {
        'grounding_required': True,
        'source_citation': True,
        'hallucination_detection': True,
        'correction_protocol': 'immediate_correction'
    },
    'glyph_signatures': {
        'enabled': True,
        'registered_glyphs': [
            {'glyph': '⟡⟦CONTINUITY⟧', 'meaning': 'Continuity marker', 'category': 'continuity'}
        ]
    },
    'interaction_safety': {
        'session_duration_warnings': True,
        'dependency_detection': True,
        'human_escalation': True
    },
    'trust_markers': [
        {'marker': '[Unknown]', 'meaning': 'Unknown information'},
        {'marker': '⟡⟦VERIFIED⟧', 'meaning': 'Verified content'}
    ]
}


class TestContinuityChecks:
    """Tests for continuity compliance checks."""

    def test_level1_no_profile_passes(self):
        """Level 1 should pass without continuity profile."""
        passed, errors, warnings = check_continuity_compliance(LEVEL1_MANIFEST, {})
        assert passed
        assert len(errors) == 0

    def test_level2_without_profile_fails(self):
        """Level 2 should fail without continuity profile."""
        passed, errors, warnings = check_continuity_compliance(LEVEL2_MANIFEST, {})
        assert not passed
        assert len(errors) > 0

    def test_level2_with_valid_profile_passes(self):
        """Level 2 should pass with valid profile."""
        passed, errors, warnings = check_continuity_compliance(LEVEL2_MANIFEST, LEVEL2_PROFILE)
        assert passed
        assert len(errors) == 0

    def test_level3_requires_vault_backed(self):
        """Level 3 requires vault_backed mechanism."""
        invalid_profile = LEVEL3_PROFILE.copy()
        invalid_profile['continuity_mechanism'] = 'local_state'

        passed, errors, warnings = check_continuity_compliance(LEVEL3_MANIFEST, invalid_profile)
        assert not passed
        assert any('vault_backed' in e for e in errors)

    def test_level3_requires_vault_configuration(self):
        """Level 3 requires vault_configuration."""
        invalid_profile = LEVEL3_PROFILE.copy()
        del invalid_profile['vault_configuration']

        passed, errors, warnings = check_continuity_compliance(LEVEL3_MANIFEST, invalid_profile)
        assert not passed
        assert any('vault_configuration' in e for e in errors)


class TestReflectionChecks:
    """Tests for reflection compliance checks."""

    def test_no_policy_fails(self):
        """All levels should fail without reflection policy."""
        passed, errors, warnings = check_reflection_compliance(LEVEL1_MANIFEST, {})
        assert not passed
        assert len(errors) > 0

    def test_level1_with_policy_passes(self):
        """Level 1 should pass with basic policy."""
        passed, errors, warnings = check_reflection_compliance(LEVEL1_MANIFEST, LEVEL1_POLICY)
        assert passed
        assert len(errors) == 0

    def test_cite_or_silence_required(self):
        """cite_or_silence must be enabled."""
        invalid_policy = LEVEL1_POLICY.copy()
        invalid_policy['uncertainty_handling'] = {'cite_or_silence': False}

        passed, errors, warnings = check_reflection_compliance(LEVEL1_MANIFEST, invalid_policy)
        assert not passed
        assert any('cite_or_silence' in e or 'AHP' in e for e in errors)

    def test_level3_requires_glyph_signatures(self):
        """Level 3 requires glyph signatures."""
        invalid_policy = LEVEL3_POLICY.copy()
        del invalid_policy['glyph_signatures']

        passed, errors, warnings = check_reflection_compliance(LEVEL3_MANIFEST, invalid_policy)
        assert not passed
        assert any('glyph' in e for e in errors)

    def test_level3_requires_interaction_safety(self):
        """Level 3 requires interaction safety."""
        invalid_policy = LEVEL3_POLICY.copy()
        del invalid_policy['interaction_safety']

        passed, errors, warnings = check_reflection_compliance(LEVEL3_MANIFEST, invalid_policy)
        assert not passed
        assert any('interaction_safety' in e for e in errors)


class TestTrustByDesignChecks:
    """Tests for trust-by-design compliance checks."""

    def test_level1_requires_trust_marker(self):
        """Level 1 requires at least one trust marker."""
        passed, errors, warnings = check_trustbydesign_compliance(LEVEL1_MANIFEST, LEVEL1_POLICY)
        assert passed  # cite_or_silence counts as trust marker

    def test_level3_requires_comprehensive_measures(self):
        """Level 3 requires comprehensive trust measures."""
        passed, errors, warnings = check_trustbydesign_compliance(LEVEL3_MANIFEST, LEVEL3_POLICY)
        assert passed
        assert len(errors) == 0
