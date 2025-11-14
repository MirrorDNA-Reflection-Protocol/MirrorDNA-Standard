"""
Trust-by-Design compliance checks for MirrorDNA Standard.

Validates trust markers, checksums, and verification protocols.
"""

from typing import Dict, Any, List, Tuple


def check_trustbydesign_compliance(
    manifest: Dict[str, Any],
    policy: Dict[str, Any]
) -> Tuple[bool, List[str], List[str]]:
    """
    Check Trust-by-Design compliance.

    Args:
        manifest: Project manifest data
        policy: Reflection policy data

    Returns:
        Tuple of (passed, errors, warnings)
    """
    errors = []
    warnings = []
    compliance_level = manifest.get('mirrorDNA_compliance_level', '')

    # Level 1: At least one trust marker
    if compliance_level == 'level_1_basic_reflection':
        if not policy:
            errors.append("Cannot verify trust markers without reflection policy")
            return False, errors, warnings

        # Check for at least one trust mechanism
        has_trust_marker = False

        if policy.get('uncertainty_handling', {}).get('cite_or_silence'):
            has_trust_marker = True

        if 'trust_markers' in policy and policy['trust_markers']:
            has_trust_marker = True

        if 'anti_hallucination' in policy:
            ah = policy['anti_hallucination']
            if ah.get('source_citation') or ah.get('grounding_required'):
                has_trust_marker = True

        if not has_trust_marker:
            errors.append("Level 1 requires at least one trust marker (cite_or_silence, trust_markers, etc.)")

    # Level 2: Multiple trust markers
    elif compliance_level == 'level_2_continuity_aware':
        trust_marker_count = 0

        # Count trust markers
        if policy.get('uncertainty_handling', {}).get('cite_or_silence'):
            trust_marker_count += 1

        if policy.get('anti_hallucination', {}).get('source_citation'):
            trust_marker_count += 1

        if policy.get('anti_hallucination', {}).get('grounding_required'):
            trust_marker_count += 1

        if 'trust_markers' in policy and policy['trust_markers']:
            trust_marker_count += len(policy['trust_markers'])

        if trust_marker_count < 2:
            warnings.append(f"Level 2 should have multiple trust markers (found {trust_marker_count})")

        # Check for checksum validation (in continuity, but we check here for trust)
        # This would ideally check the continuity profile, but we only have policy here
        # The continuity checks handle this, so just warn
        warnings.append("Ensure checksum validation is enabled in continuity profile")

    # Level 3: Comprehensive trust system
    elif compliance_level == 'level_3_vault_backed_sovereign':
        # Must have trust markers documented
        if 'trust_markers' not in policy or not policy['trust_markers']:
            errors.append("Level 3 requires documented trust_markers in reflection policy")

        # Must have comprehensive anti-hallucination
        if 'anti_hallucination' not in policy:
            errors.append("Level 3 requires comprehensive anti_hallucination measures")
        else:
            ah = policy['anti_hallucination']
            required = ['grounding_required', 'source_citation', 'hallucination_detection']
            for field in required:
                if not ah.get(field):
                    errors.append(f"Level 3 requires anti_hallucination.{field}")

        # Must have glyph signatures (trust markers)
        if 'glyph_signatures' not in policy or not policy['glyph_signatures'].get('enabled'):
            errors.append("Level 3 requires glyph_signatures for trust marking")

        # Should have interaction safety (part of trust)
        if 'interaction_safety' not in policy:
            warnings.append("Level 3 should include interaction_safety for complete trust framework")

    # Validate trust markers format
    if 'trust_markers' in policy:
        markers = policy['trust_markers']
        if not isinstance(markers, list):
            errors.append("trust_markers must be a list")
        else:
            for i, marker in enumerate(markers):
                if not isinstance(marker, dict):
                    errors.append(f"trust_markers[{i}] must be an object with 'marker' and 'meaning'")
                elif 'marker' not in marker or 'meaning' not in marker:
                    errors.append(f"trust_markers[{i}] must have 'marker' and 'meaning' fields")

    passed = len(errors) == 0
    return passed, errors, warnings


def check_trust_markers(policy: Dict[str, Any]) -> Tuple[bool, List[str]]:
    """
    Check trust markers configuration.

    Args:
        policy: Reflection policy data

    Returns:
        Tuple of (is_valid, issues)
    """
    issues = []

    if 'trust_markers' not in policy:
        return False, ["No trust_markers defined"]

    markers = policy['trust_markers']

    if not isinstance(markers, list) or len(markers) == 0:
        return False, ["trust_markers should be a non-empty list"]

    # Check standard trust markers
    standard_markers = ['[Unknown]', '[Speculation]', '[Unverified]']
    found_markers = [m.get('marker', '') for m in markers if isinstance(m, dict)]

    for std_marker in standard_markers:
        if std_marker not in found_markers:
            issues.append(f"Consider adding standard trust marker: {std_marker}")

    # Validate format
    for i, marker in enumerate(markers):
        if not isinstance(marker, dict):
            issues.append(f"trust_markers[{i}] is not an object")
            continue

        if 'marker' not in marker:
            issues.append(f"trust_markers[{i}] missing 'marker' field")

        if 'meaning' not in marker:
            issues.append(f"trust_markers[{i}] missing 'meaning' field")

    return len(issues) == 0, issues


def check_verification_protocols(
    manifest: Dict[str, Any],
    policy: Dict[str, Any]
) -> Tuple[bool, List[str]]:
    """
    Check verification and transparency protocols.

    Args:
        manifest: Project manifest data
        policy: Reflection policy data

    Returns:
        Tuple of (is_complete, recommendations)
    """
    recommendations = []
    compliance_level = manifest.get('mirrorDNA_compliance_level', '')

    # Check cite-or-silence
    if not policy.get('uncertainty_handling', {}).get('cite_or_silence'):
        recommendations.append("Enable cite_or_silence (AHP) for transparent uncertainty")

    # Check source citation
    if not policy.get('anti_hallucination', {}).get('source_citation'):
        recommendations.append("Enable source_citation for verifiable outputs")

    # Check grounding
    if not policy.get('anti_hallucination', {}).get('grounding_required'):
        recommendations.append("Enable grounding_required to ensure outputs are grounded in sources")

    # Level 2+ specific
    if compliance_level in ['level_2_continuity_aware', 'level_3_vault_backed_sovereign']:
        if not policy.get('anti_hallucination', {}).get('fact_checking'):
            recommendations.append("Consider enabling fact_checking for Level 2+")

    # Level 3 specific
    if compliance_level == 'level_3_vault_backed_sovereign':
        if not policy.get('reflection_protocols', {}).get('meta_commentary'):
            recommendations.append("Enable meta_commentary for transparent reasoning (Level 3)")

        if not policy.get('reflection_protocols', {}).get('chain_of_thought'):
            recommendations.append("Enable chain_of_thought for transparent decision-making (Level 3)")

    is_complete = len(recommendations) == 0
    return is_complete, recommendations
