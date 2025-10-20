"""
CLI module for scribe commands.
"""

import click
from pathlib import Path

from .init import create_project_structure, validate_project_structure
from .config_cli import config


@click.group()
@click.version_option(version="0.1.0", prog_name="scribe")
def main() -> None:
    """
    Scribe - Generate dataset definitions in multiple languages and formats.

    Define your datasets in YAML format and generate equivalent definitions
    in Python dataclasses, Scala case classes, and Protocol Buffers.
    """
    pass


@main.command()
@click.option("--path", "-p", default=".", help="Project path")
def init(path: str) -> None:
    """Initialize a new scribe project with directory structure."""
    base_path = Path(path)

    if validate_project_structure(base_path):
        click.echo("⚠️  Scribe project already exists in this directory.")
        if not click.confirm("Do you want to reinitialize?"):
            click.echo("Initialization cancelled.")
            return

    click.echo("Initializing scribe project...")
    create_project_structure(base_path)
    click.echo("✓ Scribe project initialized successfully!")


@main.command()
def generate() -> None:
    """Generate dataset definitions for configured target languages."""
    if not validate_project_structure():
        click.echo("❌ No scribe project found. Run 'scribe init' first.")
        return

    click.echo("Generating dataset definitions...")
    # TODO: Implement code generation
    click.echo("✓ Dataset definitions generated successfully!")


# Add config commands to the main group
main.add_command(config)


if __name__ == "__main__":
    main()
