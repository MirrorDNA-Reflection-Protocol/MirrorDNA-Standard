"""
Reflection policy compliance checks for MirrorDNA Standard.

Validates anti-hallucination measures and reflection protocols.
"""

from typing import Dict, Any, List, Tuple


def check_reflection_compliance(
    manifest: Dict[str, Any],
    policy: Dict[str, Any]
) -> Tuple[bool, List[str], List[str]]:
    """
    Check reflection policy compliance based on declared level.

    Args:
        manifest: Project manifest data
        policy: Reflection policy data (empty dict if not provided)

    Returns:
        Tuple of (passed, errors, warnings)
    """
    errors = []
    warnings = []
    compliance_level = manifest.get('mirrorDNA_compliance_level', '')

    # All levels require at least basic reflection policy
    if not policy:
        errors.append("All compliance levels require a reflection policy")
        return False, errors, warnings

    # Check required fields
    required_fields = ['policy_version', 'reflection_mode', 'uncertainty_handling']
    for field in required_fields:
        if field not in policy:
            errors.append(f"Reflection policy missing required field: '{field}'")

    # Check uncertainty handling (required for all levels)
    if 'uncertainty_handling' in policy:
        uh = policy['uncertainty_handling']

        # Cite or Silence is mandatory
        if 'cite_or_silence' not in uh:
            errors.append("uncertainty_handling must include 'cite_or_silence' (AHP)")
        elif not uh['cite_or_silence']:
            errors.append("cite_or_silence (AHP) must be enabled for MirrorDNA compliance")

        # Check markers
        if 'unknown_marker' not in uh:
            warnings.append("No unknown_marker specified (default: [Unknown])")

        if uh.get('speculation_allowed') and 'speculation_marker' not in uh:
            warnings.append("Speculation allowed but no speculation_marker specified")

    # Level-specific checks
    if compliance_level == 'level_1_basic_reflection':
        # Level 1: Basic anti-hallucination
        if 'anti_hallucination' not in policy:
            warnings.append("Level 1 should declare anti_hallucination measures")

    elif compliance_level == 'level_2_continuity_aware':
        # Level 2: Enhanced reflection
        if 'anti_hallucination' not in policy:
            errors.append("Level 2 requires anti_hallucination configuration")
        else:
            ah = policy['anti_hallucination']
            if not ah.get('grounding_required'):
                warnings.append("Level 2 should enable grounding_required")

            if not ah.get('source_citation'):
                warnings.append("Level 2 should enable source_citation")

        if 'reflection_protocols' not in policy:
            warnings.append("Level 2 should include reflection_protocols configuration")

    elif compliance_level == 'level_3_vault_backed_sovereign':
        # Level 3: Comprehensive reflection
        if 'anti_hallucination' not in policy:
            errors.append("Level 3 requires comprehensive anti_hallucination measures")
        else:
            ah = policy['anti_hallucination']

            required_ah = ['grounding_required', 'source_citation']
            for field in required_ah:
                if not ah.get(field):
                    errors.append(f"Level 3 requires anti_hallucination.{field}")

            if not ah.get('hallucination_detection'):
                warnings.append("Level 3 should implement hallucination_detection")

            if not ah.get('correction_protocol') or ah.get('correction_protocol') == 'none':
                warnings.append("Level 3 should have a correction_protocol")

        # Check glyph signatures
        if 'glyph_signatures' not in policy:
            errors.append("Level 3 requires glyph_signatures configuration")
        else:
            glyphs = policy['glyph_signatures']
            if not glyphs.get('enabled'):
                errors.append("Level 3 requires glyph_signatures.enabled=true")

            if 'registered_glyphs' not in glyphs or not glyphs['registered_glyphs']:
                warnings.append("Level 3 should register standard glyphs")

        # Check interaction safety
        if 'interaction_safety' not in policy:
            errors.append("Level 3 requires interaction_safety configuration")
        else:
            safety = policy['interaction_safety']

            recommended_safety = [
                'session_duration_warnings',
                'dependency_detection',
                'human_escalation'
            ]
            for field in recommended_safety:
                if not safety.get(field):
                    warnings.append(f"Level 3 should enable interaction_safety.{field}")

        # Check reflection protocols
        if 'reflection_protocols' not in policy:
            warnings.append("Level 3 should include comprehensive reflection_protocols")

    # Validate reflection mode
    valid_modes = ['constitutive', 'simulated', 'hybrid']
    if policy.get('reflection_mode') not in valid_modes:
        errors.append(f"Invalid reflection_mode: {policy.get('reflection_mode')}")

    passed = len(errors) == 0
    return passed, errors, warnings


def check_anti_hallucination_measures(policy: Dict[str, Any]) -> Tuple[bool, List[str]]:
    """
    Check anti-hallucination measures in detail.

    Args:
        policy: Reflection policy data

    Returns:
        Tuple of (is_complete, issues)
    """
    issues = []

    if 'anti_hallucination' not in policy:
        return False, ["Missing anti_hallucination configuration"]

    ah = policy['anti_hallucination']

    # Check key measures
    if not ah.get('grounding_required'):
        issues.append("Grounding not required (outputs may not be grounded in sources)")

    if not ah.get('source_citation'):
        issues.append("Source citation not enabled (claims may lack citations)")

    if not ah.get('hallucination_detection'):
        issues.append("Hallucination detection not enabled (recommended)")

    correction = ah.get('correction_protocol', 'none')
    if correction == 'none':
        issues.append("No correction protocol for detected hallucinations")

    return len(issues) == 0, issues


def check_glyph_signatures(policy: Dict[str, Any]) -> Tuple[bool, List[str]]:
    """
    Check glyph signature configuration.

    Args:
        policy: Reflection policy data

    Returns:
        Tuple of (is_valid, issues)
    """
    issues = []

    if 'glyph_signatures' not in policy:
        return False, ["Missing glyph_signatures configuration"]

    glyphs = policy['glyph_signatures']

    if not glyphs.get('enabled'):
        return False, ["Glyph signatures not enabled"]

    if 'registered_glyphs' not in glyphs:
        issues.append("No registered_glyphs defined")
        return False, issues

    registered = glyphs['registered_glyphs']
    if not isinstance(registered, list) or len(registered) == 0:
        issues.append("registered_glyphs should be a non-empty list")

    # Check for standard glyphs
    standard_glyphs = ['⟡⟦CONTINUITY⟧', '⟡⟦VERIFIED⟧', '⟡⟦CANONICAL⟧']
    found_glyphs = [g.get('glyph', '') for g in registered if isinstance(g, dict)]

    missing_standard = [g for g in standard_glyphs if g not in found_glyphs]
    if missing_standard:
        issues.append(f"Consider registering standard glyphs: {', '.join(missing_standard)}")

    return len(issues) == 0, issues


def check_interaction_safety(policy: Dict[str, Any]) -> Tuple[bool, List[str]]:
    """
    Check interaction safety protocols.

    Args:
        policy: Reflection policy data

    Returns:
        Tuple of (is_complete, issues)
    """
    issues = []

    if 'interaction_safety' not in policy:
        return False, ["Missing interaction_safety configuration"]

    safety = policy['interaction_safety']

    # Check key safety measures
    if not safety.get('session_duration_warnings'):
        issues.append("Session duration warnings not enabled (risk for long sessions)")

    if not safety.get('dependency_detection'):
        issues.append("Dependency detection not enabled (risk for vulnerable users)")

    if not safety.get('human_escalation'):
        issues.append("Human escalation not enabled (risk in crisis situations)")

    if not safety.get('rhythm_checks'):
        issues.append("Rhythm checks not enabled (recommended for long sessions)")

    return len(issues) == 0, issues
