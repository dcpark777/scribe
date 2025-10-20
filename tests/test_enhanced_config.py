"""
Tests for enhanced configuration system.
"""

import tempfile
import shutil
from pathlib import Path
import yaml

from scribe.config import (
    ScribeConfig,
    PythonConfig,
    ScalaConfig,
    ProtobufConfig,
    LanguageConfigs,
)


class TestEnhancedConfig:
    """Test cases for enhanced configuration system."""

    def setup_method(self):
        """Set up test environment."""
        self.temp_dir = tempfile.mkdtemp()
        self.temp_path = Path(self.temp_dir)
        self.config_path = self.temp_path / "test_config.yaml"

    def teardown_method(self):
        """Clean up test environment."""
        shutil.rmtree(self.temp_dir)

    def test_default_configuration(self):
        """Test default configuration values."""
        config = ScribeConfig(self.config_path)

        # Basic settings
        assert config.target_languages == ["python", "scala", "protobuf"]
        assert config.datasets_dir == Path("datasets")
        assert config.output_dir == Path("generated")

        # Python configuration
        assert config.languages.python.include_validation is True
        assert config.languages.python.include_documentation is True
        assert config.languages.python.use_typing_extensions is False
        assert config.languages.python.add_dataclass_decorator is True
        assert config.languages.python.generate_init_file is True
        assert config.languages.python.line_length == 100

        # Scala configuration
        assert config.languages.scala.package_name == "com.company.datasets"
        assert config.languages.scala.include_spark_imports is True
        assert config.languages.scala.include_validation is True
        assert config.languages.scala.include_documentation is True
        assert config.languages.scala.generate_package_object is True
        assert config.languages.scala.use_option_types is True
        assert config.languages.scala.line_length == 100

        # Protobuf configuration
        assert config.languages.protobuf.proto_version == "proto3"
        assert config.languages.protobuf.package_name == "com.company.datasets"
        assert config.languages.protobuf.go_package == "github.com/company/datasets"
        assert config.languages.protobuf.java_package == "com.company.datasets"
        assert config.languages.protobuf.csharp_namespace == "Company.Datasets"
        assert config.languages.protobuf.include_documentation is True
        assert config.languages.protobuf.create_package_files is True
        assert config.languages.protobuf.include_google_types is True
        assert config.languages.protobuf.use_field_numbers is True
        assert config.languages.protobuf.add_go_package is True
        assert config.languages.protobuf.add_java_package is True
        assert config.languages.protobuf.add_csharp_namespace is True
        assert config.languages.protobuf.line_length == 100

    def test_load_custom_configuration(self):
        """Test loading custom configuration from file."""
        custom_config = {
            "target_languages": ["python", "protobuf"],
            "datasets_dir": "custom_datasets",
            "output_dir": "custom_generated",
            "languages": {
                "python": {
                    "include_validation": False,
                    "include_documentation": False,
                    "line_length": 120,
                },
                "protobuf": {
                    "proto_version": "proto2",
                    "package_name": "custom.package",
                    "go_package": "github.com/custom/datasets",
                    "add_go_package": False,
                },
            },
        }

        with open(self.config_path, "w") as f:
            yaml.dump(custom_config, f)

        config = ScribeConfig(self.config_path)

        # Basic settings
        assert config.target_languages == ["python", "protobuf"]
        assert config.datasets_dir == Path("custom_datasets")
        assert config.output_dir == Path("custom_generated")

        # Python configuration
        assert config.languages.python.include_validation is False
        assert config.languages.python.include_documentation is False
        assert config.languages.python.line_length == 120

        # Protobuf configuration
        assert config.languages.protobuf.proto_version == "proto2"
        assert config.languages.protobuf.package_name == "custom.package"
        assert config.languages.protobuf.go_package == "github.com/custom/datasets"
        assert config.languages.protobuf.add_go_package is False

    def test_save_configuration(self):
        """Test saving configuration to file."""
        config = ScribeConfig(self.config_path)

        # Modify some settings
        config.target_languages = ["python"]
        config.languages.python.include_validation = False
        config.languages.scala.package_name = "custom.scala"
        config.languages.protobuf.proto_version = "proto2"

        # Save configuration
        config.save_config()

        # Load and verify
        loaded_config = ScribeConfig(self.config_path)
        assert loaded_config.target_languages == ["python"]
        assert loaded_config.languages.python.include_validation is False
        assert loaded_config.languages.scala.package_name == "custom.scala"
        assert loaded_config.languages.protobuf.proto_version == "proto2"

    def test_to_dict(self):
        """Test converting configuration to dictionary."""
        config = ScribeConfig(self.config_path)
        config_dict = config.to_dict()

        # Check basic structure
        assert "target_languages" in config_dict
        assert "datasets_dir" in config_dict
        assert "output_dir" in config_dict
        assert "languages" in config_dict

        # Check languages structure
        languages = config_dict["languages"]
        assert "python" in languages
        assert "scala" in languages
        assert "protobuf" in languages

        # Check Python settings
        python_settings = languages["python"]
        assert python_settings["include_validation"] is True
        assert python_settings["include_documentation"] is True
        assert python_settings["line_length"] == 100

    def test_partial_language_config(self):
        """Test loading configuration with only some language settings."""
        partial_config = {"languages": {"python": {"include_validation": False}}}

        with open(self.config_path, "w") as f:
            yaml.dump(partial_config, f)

        config = ScribeConfig(self.config_path)

        # Python should have custom setting
        assert config.languages.python.include_validation is False

        # Other Python settings should be defaults
        assert config.languages.python.include_documentation is True
        assert config.languages.python.line_length == 100

        # Scala and Protobuf should be defaults
        assert config.languages.scala.package_name == "com.company.datasets"
        assert config.languages.protobuf.proto_version == "proto3"

    def test_config_dataclasses(self):
        """Test individual config dataclasses."""
        # Python config
        python_config = PythonConfig(include_validation=False, line_length=120)
        assert python_config.include_validation is False
        assert python_config.include_documentation is True  # default
        assert python_config.line_length == 120

        # Scala config
        scala_config = ScalaConfig(
            package_name="custom.package", include_spark_imports=False
        )
        assert scala_config.package_name == "custom.package"
        assert scala_config.include_spark_imports is False
        assert scala_config.include_validation is True  # default

        # Protobuf config
        protobuf_config = ProtobufConfig(
            proto_version="proto2", package_name="custom.package"
        )
        assert protobuf_config.proto_version == "proto2"
        assert protobuf_config.package_name == "custom.package"
        assert protobuf_config.include_documentation is True  # default

    def test_language_configs_container(self):
        """Test LanguageConfigs container."""
        configs = LanguageConfigs()

        assert isinstance(configs.python, PythonConfig)
        assert isinstance(configs.scala, ScalaConfig)
        assert isinstance(configs.protobuf, ProtobufConfig)

        # Test custom configs
        custom_python = PythonConfig(include_validation=False)
        custom_scala = ScalaConfig(package_name="custom")
        custom_protobuf = ProtobufConfig(proto_version="proto2")

        configs.python = custom_python
        configs.scala = custom_scala
        configs.protobuf = custom_protobuf

        assert configs.python.include_validation is False
        assert configs.scala.package_name == "custom"
        assert configs.protobuf.proto_version == "proto2"
