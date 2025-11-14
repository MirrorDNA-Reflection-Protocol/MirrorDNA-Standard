"""
Continuity compliance checks for MirrorDNA Standard.

Validates continuity profiles and state persistence requirements.
"""

from typing import Dict, Any, List, Tuple


def check_continuity_compliance(
    manifest: Dict[str, Any],
    profile: Dict[str, Any]
) -> Tuple[bool, List[str], List[str]]:
    """
    Check continuity compliance based on declared level.

    Args:
        manifest: Project manifest data
        profile: Continuity profile data (empty dict if not provided)

    Returns:
        Tuple of (passed, errors, warnings)
    """
    errors = []
    warnings = []
    compliance_level = manifest.get('mirrorDNA_compliance_level', '')

    # Level 1: No continuity requirements
    if compliance_level == 'level_1_basic_reflection':
        if profile:
            warnings.append("Level 1 does not require continuity profile, but one was provided (acceptable)")
        return True, errors, warnings

    # Level 2 and 3: Require continuity profile
    if compliance_level in ['level_2_continuity_aware', 'level_3_vault_backed_sovereign']:
        if not profile:
            errors.append("Level 2+ requires a continuity profile")
            return False, errors, warnings

        # Check required fields in profile
        if 'state_persistence' not in profile:
            errors.append("Continuity profile missing 'state_persistence' configuration")

        if profile.get('state_persistence', {}).get('enabled') is False:
            errors.append("State persistence must be enabled for Level 2+")

        # Level 3 specific: vault requirement
        if compliance_level == 'level_3_vault_backed_sovereign':
            mechanism = profile.get('continuity_mechanism', '')
            if mechanism != 'vault_backed':
                errors.append(
                    f"Level 3 requires continuity_mechanism='vault_backed', got '{mechanism}'"
                )

            if 'vault_configuration' not in profile:
                errors.append("Level 3 requires vault_configuration in continuity profile")
            else:
                vault_config = profile['vault_configuration']
                if 'vault_id' not in vault_config:
                    errors.append("vault_configuration must include 'vault_id'")

        # Check continuity guarantees
        if 'continuity_guarantees' in profile:
            guarantees = profile['continuity_guarantees']

            # Level 2+ should have basic guarantees
            if not guarantees.get('state_consistency'):
                warnings.append("State consistency guarantee not declared")

            if not guarantees.get('lineage_tracking'):
                warnings.append("Lineage tracking guarantee not declared")

            # Level 3 should have identity preservation
            if compliance_level == 'level_3_vault_backed_sovereign':
                if not guarantees.get('identity_preservation'):
                    errors.append("Level 3 requires identity_preservation guarantee")

                if not guarantees.get('anti_hallucination'):
                    warnings.append("Level 3 should implement anti_hallucination guarantee")

        # Check session management
        if 'session_management' in profile:
            session_mgmt = profile['session_management']

            if not session_mgmt.get('session_tracking'):
                warnings.append("Session tracking not enabled")

            if compliance_level in ['level_2_continuity_aware', 'level_3_vault_backed_sovereign']:
                if not session_mgmt.get('session_inheritance'):
                    warnings.append("Level 2+ should enable session_inheritance for continuity")

        # Check recovery capabilities
        if 'recovery' in profile:
            recovery = profile['recovery']

            if not recovery.get('rollback_enabled'):
                warnings.append("Rollback capability not enabled (recommended for Level 2+)")
        else:
            warnings.append("No recovery configuration provided (recommended for Level 2+)")

    passed = len(errors) == 0
    return passed, errors, warnings


def check_state_persistence_config(profile: Dict[str, Any]) -> Tuple[bool, List[str]]:
    """
    Check state persistence configuration in detail.

    Args:
        profile: Continuity profile data

    Returns:
        Tuple of (is_valid, issues)
    """
    issues = []

    if 'state_persistence' not in profile:
        return False, ["Missing state_persistence configuration"]

    sp = profile['state_persistence']

    if not sp.get('enabled'):
        return False, ["State persistence is not enabled"]

    if 'storage_type' not in sp:
        issues.append("Missing storage_type")

    valid_storage_types = ['file_system', 'database', 'vault', 'distributed_storage', 'memory_only']
    if sp.get('storage_type') not in valid_storage_types:
        issues.append(f"Invalid storage_type: {sp.get('storage_type')}")

    # Recommendations
    if not sp.get('encryption'):
        issues.append("Encryption not enabled (recommended for production)")

    if not sp.get('checksum_validation'):
        issues.append("Checksum validation not enabled (recommended for integrity)")

    return len(issues) == 0, issues


def check_vault_configuration(profile: Dict[str, Any]) -> Tuple[bool, List[str]]:
    """
    Check vault configuration for Level 3 compliance.

    Args:
        profile: Continuity profile data

    Returns:
        Tuple of (is_valid, issues)
    """
    issues = []

    if 'vault_configuration' not in profile:
        return False, ["Missing vault_configuration for Level 3"]

    vault = profile['vault_configuration']

    required_fields = ['vault_type', 'vault_id']
    for field in required_fields:
        if field not in vault:
            issues.append(f"Missing required field in vault_configuration: {field}")

    valid_vault_types = ['obsidian', 'custom', 'distributed', 'cloud']
    if vault.get('vault_type') not in valid_vault_types:
        issues.append(f"Invalid vault_type: {vault.get('vault_type')}")

    # Validate vault_id format
    vault_id = vault.get('vault_id', '')
    if vault_id and not vault_id.startswith('AMOS://'):
        issues.append("vault_id should follow AMOS:// URI format (recommended)")

    return len(issues) == 0, issues
