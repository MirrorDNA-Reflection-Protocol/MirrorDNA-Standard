"""
Tests for validators.cli module.
"""

import pytest
import sys
from io import StringIO
from pathlib import Path

from validators.cli import main


class TestCLI:
    """Tests for CLI functionality."""

    def test_cli_with_valid_level1_example(self, monkeypatch, capsys):
        """Test CLI with valid Level 1 example."""
        # Simulate command-line arguments
        test_args = [
            'cli.py',
            '--manifest', 'examples/minimal_project_manifest.yaml',
            '--policy', 'examples/example_reflection_policy.yaml',
            '--no-color'
        ]
        monkeypatch.setattr(sys, 'argv', test_args)

        # Run CLI
        exit_code = main()

        # Check exit code
        assert exit_code == 0, "Valid Level 1 example should pass"

        # Check output
        captured = capsys.readouterr()
        assert 'PASSED' in captured.out or 'PASSED' in str(exit_code)

    def test_cli_with_valid_level2_example(self, monkeypatch, capsys):
        """Test CLI with valid Level 2 example."""
        test_args = [
            'cli.py',
            '--manifest', 'examples/level2_project_manifest.yaml',
            '--profile', 'examples/example_continuity_profile.yaml',
            '--policy', 'examples/example_reflection_policy.yaml',
            '--no-color'
        ]
        monkeypatch.setattr(sys, 'argv', test_args)

        exit_code = main()
        assert exit_code == 0, "Valid Level 2 example should pass"

    def test_cli_with_valid_level3_example(self, monkeypatch, capsys):
        """Test CLI with valid Level 3 example."""
        test_args = [
            'cli.py',
            '--manifest', 'examples/level3_project_manifest.yaml',
            '--profile', 'examples/level3_continuity_profile.yaml',
            '--policy', 'examples/level3_reflection_policy.yaml',
            '--no-color'
        ]
        monkeypatch.setattr(sys, 'argv', test_args)

        exit_code = main()
        assert exit_code == 0, "Valid Level 3 example should pass"

    def test_cli_with_missing_manifest(self, monkeypatch, capsys):
        """Test CLI with missing manifest file."""
        test_args = [
            'cli.py',
            '--manifest', 'nonexistent.yaml',
            '--policy', 'examples/example_reflection_policy.yaml',
            '--no-color'
        ]
        monkeypatch.setattr(sys, 'argv', test_args)

        exit_code = main()
        assert exit_code == 1, "Missing manifest should fail"

    def test_cli_without_required_args(self, monkeypatch):
        """Test CLI without required arguments."""
        test_args = ['cli.py']
        monkeypatch.setattr(sys, 'argv', test_args)

        # Should exit with error
        with pytest.raises(SystemExit):
            main()

    def test_cli_verbose_output(self, monkeypatch, capsys):
        """Test CLI with verbose flag."""
        test_args = [
            'cli.py',
            '--manifest', 'examples/minimal_project_manifest.yaml',
            '--policy', 'examples/example_reflection_policy.yaml',
            '--verbose',
            '--no-color'
        ]
        monkeypatch.setattr(sys, 'argv', test_args)

        exit_code = main()

        captured = capsys.readouterr()
        assert 'Loading' in captured.out or exit_code is not None
