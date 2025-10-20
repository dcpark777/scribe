"""
Configuration management for scribe.
"""

from typing import Any, Dict, List, Optional
import yaml  # type: ignore
from pathlib import Path
from dataclasses import dataclass, field


@dataclass
class PythonConfig:
    """Configuration for Python dataclass generation."""

    include_validation: bool = True
    include_documentation: bool = True
    use_typing_extensions: bool = False
    add_dataclass_decorator: bool = True
    generate_init_file: bool = True
    line_length: int = 100


@dataclass
class ScalaConfig:
    """Configuration for Scala case class generation."""

    package_name: str = "com.company.datasets"
    include_spark_imports: bool = True
    include_validation: bool = True
    include_documentation: bool = True
    generate_package_object: bool = True
    use_option_types: bool = True
    line_length: int = 100


@dataclass
class ProtobufConfig:
    """Configuration for Protocol Buffers generation."""

    proto_version: str = "proto3"
    package_name: str = "com.company.datasets"
    go_package: str = "github.com/company/datasets"
    java_package: str = "com.company.datasets"
    csharp_namespace: str = "Company.Datasets"
    include_documentation: bool = True
    create_package_files: bool = True
    include_google_types: bool = True
    use_field_numbers: bool = True
    add_go_package: bool = True
    add_java_package: bool = True
    add_csharp_namespace: bool = True
    line_length: int = 100


@dataclass
class LanguageConfigs:
    """Container for all language-specific configurations."""

    python: PythonConfig = field(default_factory=PythonConfig)
    scala: ScalaConfig = field(default_factory=ScalaConfig)
    protobuf: ProtobufConfig = field(default_factory=ProtobufConfig)


class ScribeConfig:
    """Configuration class for scribe settings."""

    def __init__(self, config_path: Optional[Path] = None):
        self.config_path = config_path or Path("scribe.config.yaml")
        self.target_languages: List[str] = ["python", "scala", "protobuf"]
        self.datasets_dir: Path = Path("datasets")
        self.output_dir: Path = Path("generated")
        self.languages: LanguageConfigs = LanguageConfigs()
        self._load_config()

    def _load_config(self) -> None:
        """Load configuration from file if it exists."""
        if self.config_path.exists():
            with open(self.config_path, "r") as f:
                config_data = yaml.safe_load(f)
                if config_data:
                    # Load basic settings
                    self.target_languages = config_data.get(
                        "target_languages", self.target_languages
                    )
                    self.datasets_dir = Path(
                        config_data.get("datasets_dir", self.datasets_dir)
                    )
                    self.output_dir = Path(
                        config_data.get("output_dir", self.output_dir)
                    )

                    # Load language-specific configurations
                    languages_config = config_data.get("languages", {})
                    self._load_language_configs(languages_config)

    def _load_language_configs(self, languages_config: Dict[str, Any]) -> None:
        """Load language-specific configurations."""
        # Python configuration
        python_config = languages_config.get("python", {})
        if python_config:
            self.languages.python = PythonConfig(
                include_validation=python_config.get("include_validation", True),
                include_documentation=python_config.get("include_documentation", True),
                use_typing_extensions=python_config.get("use_typing_extensions", False),
                add_dataclass_decorator=python_config.get(
                    "add_dataclass_decorator", True
                ),
                generate_init_file=python_config.get("generate_init_file", True),
                line_length=python_config.get("line_length", 100),
            )

        # Scala configuration
        scala_config = languages_config.get("scala", {})
        if scala_config:
            self.languages.scala = ScalaConfig(
                package_name=scala_config.get("package_name", "com.company.datasets"),
                include_spark_imports=scala_config.get("include_spark_imports", True),
                include_validation=scala_config.get("include_validation", True),
                include_documentation=scala_config.get("include_documentation", True),
                generate_package_object=scala_config.get(
                    "generate_package_object", True
                ),
                use_option_types=scala_config.get("use_option_types", True),
                line_length=scala_config.get("line_length", 100),
            )

        # Protobuf configuration
        protobuf_config = languages_config.get("protobuf", {})
        if protobuf_config:
            self.languages.protobuf = ProtobufConfig(
                proto_version=protobuf_config.get("proto_version", "proto3"),
                package_name=protobuf_config.get(
                    "package_name", "com.company.datasets"
                ),
                go_package=protobuf_config.get(
                    "go_package", "github.com/company/datasets"
                ),
                java_package=protobuf_config.get(
                    "java_package", "com.company.datasets"
                ),
                csharp_namespace=protobuf_config.get(
                    "csharp_namespace", "Company.Datasets"
                ),
                include_documentation=protobuf_config.get(
                    "include_documentation", True
                ),
                create_package_files=protobuf_config.get("create_package_files", True),
                include_google_types=protobuf_config.get("include_google_types", True),
                use_field_numbers=protobuf_config.get("use_field_numbers", True),
                add_go_package=protobuf_config.get("add_go_package", True),
                add_java_package=protobuf_config.get("add_java_package", True),
                add_csharp_namespace=protobuf_config.get("add_csharp_namespace", True),
                line_length=protobuf_config.get("line_length", 100),
            )

    def save_config(self) -> None:
        """Save current configuration to file."""
        config_data = {
            "target_languages": self.target_languages,
            "datasets_dir": str(self.datasets_dir),
            "output_dir": str(self.output_dir),
            "languages": {
                "python": {
                    "include_validation": self.languages.python.include_validation,
                    "include_documentation": self.languages.python.include_documentation,
                    "use_typing_extensions": self.languages.python.use_typing_extensions,
                    "add_dataclass_decorator": self.languages.python.add_dataclass_decorator,
                    "generate_init_file": self.languages.python.generate_init_file,
                    "line_length": self.languages.python.line_length,
                },
                "scala": {
                    "package_name": self.languages.scala.package_name,
                    "include_spark_imports": self.languages.scala.include_spark_imports,
                    "include_validation": self.languages.scala.include_validation,
                    "include_documentation": self.languages.scala.include_documentation,
                    "generate_package_object": self.languages.scala.generate_package_object,
                    "use_option_types": self.languages.scala.use_option_types,
                    "line_length": self.languages.scala.line_length,
                },
                "protobuf": {
                    "proto_version": self.languages.protobuf.proto_version,
                    "package_name": self.languages.protobuf.package_name,
                    "go_package": self.languages.protobuf.go_package,
                    "java_package": self.languages.protobuf.java_package,
                    "csharp_namespace": self.languages.protobuf.csharp_namespace,
                    "include_documentation": self.languages.protobuf.include_documentation,
                    "create_package_files": self.languages.protobuf.create_package_files,
                    "include_google_types": self.languages.protobuf.include_google_types,
                    "use_field_numbers": self.languages.protobuf.use_field_numbers,
                    "add_go_package": self.languages.protobuf.add_go_package,
                    "add_java_package": self.languages.protobuf.add_java_package,
                    "add_csharp_namespace": self.languages.protobuf.add_csharp_namespace,
                    "line_length": self.languages.protobuf.line_length,
                },
            },
        }
        with open(self.config_path, "w") as f:
            yaml.dump(config_data, f, default_flow_style=False)

    def to_dict(self) -> Dict[str, Any]:
        """Convert configuration to dictionary."""
        return {
            "target_languages": self.target_languages,
            "datasets_dir": str(self.datasets_dir),
            "output_dir": str(self.output_dir),
            "languages": {
                "python": {
                    "include_validation": self.languages.python.include_validation,
                    "include_documentation": self.languages.python.include_documentation,
                    "use_typing_extensions": self.languages.python.use_typing_extensions,
                    "add_dataclass_decorator": self.languages.python.add_dataclass_decorator,
                    "generate_init_file": self.languages.python.generate_init_file,
                    "line_length": self.languages.python.line_length,
                },
                "scala": {
                    "package_name": self.languages.scala.package_name,
                    "include_spark_imports": self.languages.scala.include_spark_imports,
                    "include_validation": self.languages.scala.include_validation,
                    "include_documentation": self.languages.scala.include_documentation,
                    "generate_package_object": self.languages.scala.generate_package_object,
                    "use_option_types": self.languages.scala.use_option_types,
                    "line_length": self.languages.scala.line_length,
                },
                "protobuf": {
                    "proto_version": self.languages.protobuf.proto_version,
                    "package_name": self.languages.protobuf.package_name,
                    "go_package": self.languages.protobuf.go_package,
                    "java_package": self.languages.protobuf.java_package,
                    "csharp_namespace": self.languages.protobuf.csharp_namespace,
                    "include_documentation": self.languages.protobuf.include_documentation,
                    "create_package_files": self.languages.protobuf.create_package_files,
                    "include_google_types": self.languages.protobuf.include_google_types,
                    "use_field_numbers": self.languages.protobuf.use_field_numbers,
                    "add_go_package": self.languages.protobuf.add_go_package,
                    "add_java_package": self.languages.protobuf.add_java_package,
                    "add_csharp_namespace": self.languages.protobuf.add_csharp_namespace,
                    "line_length": self.languages.protobuf.line_length,
                },
            },
        }
