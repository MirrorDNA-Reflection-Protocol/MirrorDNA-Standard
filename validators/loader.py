"""
Loader module for MirrorDNA manifests and profiles.

Handles loading and schema validation of YAML/JSON configuration files.
"""

import json
from pathlib import Path
from typing import Dict, Any, List, Tuple
import jsonschema


def load_yaml_or_json(file_path: str) -> Dict[str, Any]:
    """
    Load a YAML or JSON file.

    Args:
        file_path: Path to the file

    Returns:
        Parsed dictionary

    Raises:
        FileNotFoundError: If file doesn't exist
        ValueError: If file cannot be parsed
    """
    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")

    content = path.read_text(encoding='utf-8')

    # Try JSON first
    if file_path.endswith('.json'):
        try:
            return json.loads(content)
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON in {file_path}: {e}")

    # Try YAML
    try:
        import yaml
        data = yaml.safe_load(content)
        if not isinstance(data, dict):
            raise ValueError(f"Expected dictionary at root of {file_path}")
        return data
    except ImportError:
        raise ValueError("PyYAML not installed. Install with: pip install pyyaml")
    except yaml.YAMLError as e:
        raise ValueError(f"Invalid YAML in {file_path}: {e}")


def load_schema(schema_name: str) -> Dict[str, Any]:
    """
    Load a JSON schema from the schema directory.

    Args:
        schema_name: Name of the schema file (e.g., 'project_manifest.schema.json')

    Returns:
        Schema dictionary

    Raises:
        FileNotFoundError: If schema doesn't exist
    """
    # Find schema directory relative to this file
    validators_dir = Path(__file__).parent
    repo_root = validators_dir.parent
    schema_dir = repo_root / 'schema'
    schema_path = schema_dir / schema_name

    if not schema_path.exists():
        raise FileNotFoundError(f"Schema not found: {schema_path}")

    return json.loads(schema_path.read_text(encoding='utf-8'))


def validate_against_schema(data: Dict[str, Any], schema: Dict[str, Any]) -> Tuple[bool, List[str]]:
    """
    Validate data against a JSON schema.

    Args:
        data: Data to validate
        schema: JSON schema

    Returns:
        Tuple of (is_valid, error_messages)
    """
    try:
        jsonschema.validate(instance=data, schema=schema)
        return True, []
    except jsonschema.ValidationError as e:
        return False, [str(e)]
    except jsonschema.SchemaError as e:
        return False, [f"Invalid schema: {e}"]


def load_and_validate_manifest(manifest_path: str) -> Tuple[Dict[str, Any], List[str]]:
    """
    Load and validate a project manifest.

    Args:
        manifest_path: Path to manifest file

    Returns:
        Tuple of (manifest_data, error_messages)
    """
    errors = []

    try:
        manifest = load_yaml_or_json(manifest_path)
    except (FileNotFoundError, ValueError) as e:
        return {}, [str(e)]

    try:
        schema = load_schema('project_manifest.schema.json')
        is_valid, schema_errors = validate_against_schema(manifest, schema)
        if not is_valid:
            errors.extend(schema_errors)
    except FileNotFoundError as e:
        errors.append(str(e))

    return manifest, errors


def load_and_validate_profile(profile_path: str) -> Tuple[Dict[str, Any], List[str]]:
    """
    Load and validate a continuity profile.

    Args:
        profile_path: Path to profile file

    Returns:
        Tuple of (profile_data, error_messages)
    """
    errors = []

    try:
        profile = load_yaml_or_json(profile_path)
    except (FileNotFoundError, ValueError) as e:
        return {}, [str(e)]

    try:
        schema = load_schema('continuity_profile.schema.json')
        is_valid, schema_errors = validate_against_schema(profile, schema)
        if not is_valid:
            errors.extend(schema_errors)
    except FileNotFoundError as e:
        errors.append(str(e))

    return profile, errors


def load_and_validate_policy(policy_path: str) -> Tuple[Dict[str, Any], List[str]]:
    """
    Load and validate a reflection policy.

    Args:
        policy_path: Path to policy file

    Returns:
        Tuple of (policy_data, error_messages)
    """
    errors = []

    try:
        policy = load_yaml_or_json(policy_path)
    except (FileNotFoundError, ValueError) as e:
        return {}, [str(e)]

    try:
        schema = load_schema('reflection_policy.schema.json')
        is_valid, schema_errors = validate_against_schema(policy, schema)
        if not is_valid:
            errors.extend(schema_errors)
    except FileNotFoundError as e:
        errors.append(str(e))

    return policy, errors
