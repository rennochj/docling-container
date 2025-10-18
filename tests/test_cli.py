"""Tests for the CLI module."""

import pytest
from click.testing import CliRunner
from docling_container.main import cli, INPUT_FORMATS, OUTPUT_FORMATS


class TestCLI:
    """Test cases for CLI interface."""

    def setup_method(self):
        """Set up test fixtures."""
        self.runner = CliRunner()

    def test_cli_help(self):
        """Test CLI help command."""
        result = self.runner.invoke(cli, ['--help'])
        assert result.exit_code == 0
        assert 'Docling Container' in result.output

    def test_cli_version(self):
        """Test CLI version command."""
        result = self.runner.invoke(cli, ['--version'])
        assert result.exit_code == 0
        assert '0.1.0' in result.output

    def test_convert_help(self):
        """Test convert command help."""
        result = self.runner.invoke(cli, ['convert', '--help'])
        assert result.exit_code == 0
        assert 'INPUT_PATH' in result.output
        assert 'OUTPUT_DIR' in result.output

    def test_formats_command(self):
        """Test formats listing command."""
        result = self.runner.invoke(cli, ['formats'])
        assert result.exit_code == 0
        assert 'Supported Input Formats' in result.output
        assert 'Supported Output Formats' in result.output

    def test_formats_lists_correct_formats(self):
        """Test that formats command lists all supported formats."""
        result = self.runner.invoke(cli, ['formats'])
        assert result.exit_code == 0

        # Check some input formats are listed
        assert 'pdf' in result.output
        assert 'docx' in result.output
        assert 'html' in result.output

        # Check output formats are listed
        assert 'markdown' in result.output.lower()
        assert 'json' in result.output.lower()

    def test_input_formats_complete(self):
        """Test that INPUT_FORMATS constant contains expected formats."""
        expected = ['pdf', 'docx', 'pptx', 'html', 'markdown', 'png', 'jpg']
        for fmt in expected:
            assert fmt in INPUT_FORMATS

    def test_output_formats_complete(self):
        """Test that OUTPUT_FORMATS constant contains expected formats."""
        expected = ['markdown', 'html', 'json', 'text', 'doctags']
        for fmt in expected:
            assert fmt in OUTPUT_FORMATS

    def test_convert_missing_arguments(self):
        """Test convert command with missing arguments."""
        result = self.runner.invoke(cli, ['convert'])
        assert result.exit_code != 0
        assert 'Error' in result.output or 'Missing' in result.output

    def test_convert_nonexistent_input(self):
        """Test convert command with non-existent input file."""
        result = self.runner.invoke(cli, [
            'convert',
            '/nonexistent/file.pdf',
            '/tmp/output'
        ])
        assert result.exit_code != 0
