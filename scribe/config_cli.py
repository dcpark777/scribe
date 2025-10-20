"""
Configuration management CLI commands for scribe.
"""

import click
from pathlib import Path

from .config import ScribeConfig, PythonConfig, ScalaConfig, ProtobufConfig


@click.group()
def config():
    """Configuration management commands."""
    pass


@config.command()
@click.option(
    "--config-path",
    type=click.Path(),
    default="scribe.config.yaml",
    help="Path to configuration file",
)
def show(config_path: str):
    """Show current configuration."""
    config_file = Path(config_path)
    if not config_file.exists():
        click.echo(f"❌ Configuration file not found: {config_path}")
        click.echo("Run 'scribe init' to create a default configuration.")
        return

    config = ScribeConfig(config_file)

    click.echo("📋 Current Scribe Configuration")
    click.echo("=" * 40)
    click.echo(f"Target Languages: {', '.join(config.target_languages)}")
    click.echo(f"Datasets Directory: {config.datasets_dir}")
    click.echo(f"Output Directory: {config.output_dir}")
    click.echo()

    # Python configuration
    click.echo("🐍 Python Configuration:")
    click.echo(f"  Include Validation: {config.languages.python.include_validation}")
    click.echo(
        f"  Include Documentation: {config.languages.python.include_documentation}"
    )
    click.echo(
        f"  Use Typing Extensions: {config.languages.python.use_typing_extensions}"
    )
    click.echo(
        f"  Add Dataclass Decorator: {config.languages.python.add_dataclass_decorator}"
    )
    click.echo(f"  Generate Init File: {config.languages.python.generate_init_file}")
    click.echo(f"  Line Length: {config.languages.python.line_length}")
    click.echo()

    # Scala configuration
    click.echo("☕ Scala Configuration:")
    click.echo(f"  Package Name: {config.languages.scala.package_name}")
    click.echo(
        f"  Include Spark Imports: {config.languages.scala.include_spark_imports}"
    )
    click.echo(f"  Include Validation: {config.languages.scala.include_validation}")
    click.echo(
        f"  Include Documentation: {config.languages.scala.include_documentation}"
    )
    click.echo(
        f"  Generate Package Object: {config.languages.scala.generate_package_object}"
    )
    click.echo(f"  Use Option Types: {config.languages.scala.use_option_types}")
    click.echo(f"  Line Length: {config.languages.scala.line_length}")
    click.echo()

    # Protobuf configuration
    click.echo("📦 Protocol Buffers Configuration:")
    click.echo(f"  Proto Version: {config.languages.protobuf.proto_version}")
    click.echo(f"  Package Name: {config.languages.protobuf.package_name}")
    click.echo(f"  Go Package: {config.languages.protobuf.go_package}")
    click.echo(f"  Java Package: {config.languages.protobuf.java_package}")
    click.echo(f"  C# Namespace: {config.languages.protobuf.csharp_namespace}")
    click.echo(
        f"  Include Documentation: {config.languages.protobuf.include_documentation}"
    )
    click.echo(
        f"  Create Package Files: {config.languages.protobuf.create_package_files}"
    )
    click.echo(
        f"  Include Google Types: {config.languages.protobuf.include_google_types}"
    )
    click.echo(f"  Use Field Numbers: {config.languages.protobuf.use_field_numbers}")
    click.echo(f"  Add Go Package: {config.languages.protobuf.add_go_package}")
    click.echo(f"  Add Java Package: {config.languages.protobuf.add_java_package}")
    click.echo(f"  Add C# Namespace: {config.languages.protobuf.add_csharp_namespace}")
    click.echo(f"  Line Length: {config.languages.protobuf.line_length}")


@config.command()
@click.option(
    "--config-path",
    type=click.Path(),
    default="scribe.config.yaml",
    help="Path to configuration file",
)
@click.option(
    "--language",
    type=click.Choice(["python", "scala", "protobuf"]),
    required=True,
    help="Language to configure",
)
@click.option("--setting", required=True, help="Setting name to change")
@click.option("--value", required=True, help="New value for the setting")
def set(config_path: str, language: str, setting: str, value: str):
    """Set a configuration value for a specific language."""
    config_file = Path(config_path)
    if not config_file.exists():
        click.echo(f"❌ Configuration file not found: {config_path}")
        click.echo("Run 'scribe init' to create a default configuration.")
        return

    config = ScribeConfig(config_file)

    # Convert value to appropriate type
    converted_value = convert_value(value)

    # Update the appropriate language configuration
    if language == "python":
        if hasattr(config.languages.python, setting):
            setattr(config.languages.python, setting, converted_value)
            click.echo(f"✅ Updated Python {setting} to {converted_value}")
        else:
            click.echo(f"❌ Invalid Python setting: {setting}")
            return
    elif language == "scala":
        if hasattr(config.languages.scala, setting):
            setattr(config.languages.scala, setting, converted_value)
            click.echo(f"✅ Updated Scala {setting} to {converted_value}")
        else:
            click.echo(f"❌ Invalid Scala setting: {setting}")
            return
    elif language == "protobuf":
        if hasattr(config.languages.protobuf, setting):
            setattr(config.languages.protobuf, setting, converted_value)
            click.echo(f"✅ Updated Protobuf {setting} to {converted_value}")
        else:
            click.echo(f"❌ Invalid Protobuf setting: {setting}")
            return

    # Save the updated configuration
    config.save_config()
    click.echo(f"💾 Configuration saved to {config_path}")


def convert_value(value: str):
    """Convert string value to appropriate Python type."""
    # Try boolean
    if value.lower() in ("true", "false"):
        return value.lower() == "true"

    # Try integer
    try:
        return int(value)
    except ValueError:
        pass

    # Try float
    try:
        return float(value)
    except ValueError:
        pass

    # Return as string
    return value


@config.command()
@click.option(
    "--config-path",
    type=click.Path(),
    default="scribe.config.yaml",
    help="Path to configuration file",
)
@click.option(
    "--language",
    type=click.Choice(["python", "scala", "protobuf"]),
    required=True,
    help="Language to show settings for",
)
def list_settings(config_path: str, language: str):
    """List all available settings for a language."""
    config_file = Path(config_path)
    if not config_file.exists():
        click.echo(f"❌ Configuration file not found: {config_path}")
        click.echo("Run 'scribe init' to create a default configuration.")
        return

    click.echo(f"📋 Available {language.title()} Settings:")
    click.echo("=" * 40)

    if language == "python":
        settings = [
            ("include_validation", "bool", "Include validation methods"),
            ("include_documentation", "bool", "Include docstrings"),
            ("use_typing_extensions", "bool", "Use typing_extensions imports"),
            ("add_dataclass_decorator", "bool", "Add @dataclass decorator"),
            ("generate_init_file", "bool", "Generate __init__.py files"),
            ("line_length", "int", "Maximum line length"),
        ]
    elif language == "scala":
        settings = [
            ("package_name", "string", "Package name for generated classes"),
            ("include_spark_imports", "bool", "Include Spark imports"),
            ("include_validation", "bool", "Include validation methods"),
            ("include_documentation", "bool", "Include documentation"),
            ("generate_package_object", "bool", "Generate package object"),
            ("use_option_types", "bool", "Use Option types for optional fields"),
            ("line_length", "int", "Maximum line length"),
        ]
    elif language == "protobuf":
        settings = [
            ("proto_version", "string", "Protocol Buffers version"),
            ("package_name", "string", "Package name"),
            ("go_package", "string", "Go package path"),
            ("java_package", "string", "Java package name"),
            ("csharp_namespace", "string", "C# namespace"),
            ("include_documentation", "bool", "Include documentation"),
            ("create_package_files", "bool", "Create package files"),
            ("include_google_types", "bool", "Include Google types"),
            ("use_field_numbers", "bool", "Use field numbers"),
            ("add_go_package", "bool", "Add go_package option"),
            ("add_java_package", "bool", "Add java_package option"),
            ("add_csharp_namespace", "bool", "Add csharp_namespace option"),
            ("line_length", "int", "Maximum line length"),
        ]

    for setting, type_hint, description in settings:
        click.echo(f"  {setting:<20} ({type_hint:<6}) - {description}")

    click.echo()
    click.echo(
        "Usage: scribe config set --language <lang> --setting <name> --value <value>"
    )


@config.command()
@click.option(
    "--config-path",
    type=click.Path(),
    default="scribe.config.yaml",
    help="Path to configuration file",
)
@click.option(
    "--language",
    type=click.Choice(["python", "scala", "protobuf"]),
    required=True,
    help="Language to reset",
)
def reset(config_path: str, language: str):
    """Reset language configuration to defaults."""
    config_file = Path(config_path)
    if not config_file.exists():
        click.echo(f"❌ Configuration file not found: {config_path}")
        click.echo("Run 'scribe init' to create a default configuration.")
        return

    config = ScribeConfig(config_file)

    # Reset to defaults
    if language == "python":
        config.languages.python = PythonConfig()
        click.echo("✅ Reset Python configuration to defaults")
    elif language == "scala":
        config.languages.scala = ScalaConfig()
        click.echo("✅ Reset Scala configuration to defaults")
    elif language == "protobuf":
        config.languages.protobuf = ProtobufConfig()
        click.echo("✅ Reset Protobuf configuration to defaults")

    # Save the updated configuration
    config.save_config()
    click.echo(f"💾 Configuration saved to {config_path}")
