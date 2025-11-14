"""
Tests for validators.loader module.
"""

import pytest
import json
import tempfile
from pathlib import Path

from validators.loader import (
    load_yaml_or_json,
    load_schema,
    validate_against_schema,
    load_and_validate_manifest,
    load_and_validate_profile,
    load_and_validate_policy
)


def test_load_json_file():
    """Test loading a valid JSON file."""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
        json.dump({"key": "value"}, f)
        f.flush()
        temp_path = f.name

    try:
        data = load_yaml_or_json(temp_path)
        assert data == {"key": "value"}
    finally:
        Path(temp_path).unlink()


def test_load_yaml_file():
    """Test loading a valid YAML file."""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
        f.write("key: value\n")
        f.flush()
        temp_path = f.name

    try:
        data = load_yaml_or_json(temp_path)
        assert data == {"key": "value"}
    finally:
        Path(temp_path).unlink()


def test_load_nonexistent_file():
    """Test loading a non-existent file raises FileNotFoundError."""
    with pytest.raises(FileNotFoundError):
        load_yaml_or_json("/nonexistent/file.yaml")


def test_load_invalid_json():
    """Test loading invalid JSON raises ValueError."""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
        f.write("{ invalid json }")
        f.flush()
        temp_path = f.name

    try:
        with pytest.raises(ValueError, match="Invalid JSON"):
            load_yaml_or_json(temp_path)
    finally:
        Path(temp_path).unlink()


def test_load_schema():
    """Test loading a schema file."""
    schema = load_schema('project_manifest.schema.json')
    assert isinstance(schema, dict)
    assert '$schema' in schema
    assert schema['title'] == 'MirrorDNA Project Manifest'


def test_validate_against_schema_valid():
    """Test validating valid data against schema."""
    schema = {
        "type": "object",
        "required": ["name"],
        "properties": {
            "name": {"type": "string"}
        }
    }
    data = {"name": "test"}

    is_valid, errors = validate_against_schema(data, schema)
    assert is_valid
    assert len(errors) == 0


def test_validate_against_schema_invalid():
    """Test validating invalid data against schema."""
    schema = {
        "type": "object",
        "required": ["name"],
        "properties": {
            "name": {"type": "string"}
        }
    }
    data = {"wrong_field": "test"}

    is_valid, errors = validate_against_schema(data, schema)
    assert not is_valid
    assert len(errors) > 0


def test_load_and_validate_manifest_valid():
    """Test loading and validating a valid manifest."""
    manifest_path = "examples/minimal_project_manifest.yaml"
    manifest, errors = load_and_validate_manifest(manifest_path)

    assert isinstance(manifest, dict)
    assert 'name' in manifest
    assert 'mirrorDNA_compliance_level' in manifest


def test_load_and_validate_profile_valid():
    """Test loading and validating a valid continuity profile."""
    profile_path = "examples/example_continuity_profile.yaml"
    profile, errors = load_and_validate_profile(profile_path)

    assert isinstance(profile, dict)
    assert 'continuity_mechanism' in profile
    assert 'state_persistence' in profile


def test_load_and_validate_policy_valid():
    """Test loading and validating a valid reflection policy."""
    policy_path = "examples/example_reflection_policy.yaml"
    policy, errors = load_and_validate_policy(policy_path)

    assert isinstance(policy, dict)
    assert 'reflection_mode' in policy
    assert 'uncertainty_handling' in policy
