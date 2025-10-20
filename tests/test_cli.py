"""
Tests for scribe CLI functionality.
"""

from click.testing import CliRunner
from pathlib import Path
import tempfile
import shutil

from scribe.cli import main


class TestCLI:
    """Test cases for CLI commands."""

    def setup_method(self):
        """Set up test environment."""
        self.runner = CliRunner()
        self.temp_dir = tempfile.mkdtemp()
        self.temp_path = Path(self.temp_dir)

    def teardown_method(self):
        """Clean up test environment."""
        shutil.rmtree(self.temp_dir)

    def test_main_help(self):
        """Test that main command shows help."""
        result = self.runner.invoke(main, ["--help"])
        assert result.exit_code == 0
        assert "Generate dataset definitions" in result.output

    def test_init_command(self):
        """Test init command creates project structure."""
        result = self.runner.invoke(main, ["init", "--path", self.temp_dir])
        assert result.exit_code == 0
        assert "Scribe project initialized successfully!" in result.output

        # Check that directories were created
        assert (self.temp_path / "datasets").exists()
        assert (self.temp_path / "generated").exists()
        assert (self.temp_path / "generated" / "python").exists()
        assert (self.temp_path / "generated" / "scala").exists()
        assert (self.temp_path / "generated" / "protobuf").exists()

        # Check that example file was created
        assert (self.temp_path / "datasets" / "user.yaml").exists()

        # Check that config file was created
        assert (self.temp_path / "scribe.config.yaml").exists()

    def test_generate_without_init(self):
        """Test generate command fails without initialization."""
        result = self.runner.invoke(main, ["generate"])
        assert result.exit_code == 0  # CLI doesn't exit with error code
        assert "No scribe project found" in result.output
