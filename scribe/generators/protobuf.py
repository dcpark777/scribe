"""
Protocol Buffers generator for scribe.

This module generates Protocol Buffer (.proto) files from parsed dataset definitions,
enabling efficient serialization and cross-language data contracts.
"""

from typing import Any, Dict, List, Optional
from pathlib import Path
from dataclasses import dataclass

from ..parser import DatasetDefinition, FieldDefinition
from ..config import ProtobufConfig


@dataclass
class ProtobufGeneratorConfig:
    """Configuration for Protocol Buffers generation."""

    # Output settings
    output_dir: Path = Path("generated/protobuf")
    create_package_files: bool = True
    include_documentation: bool = True

    # Code style settings
    line_length: int = 100
    use_field_numbers: bool = True
    add_go_package: bool = True

    # Protocol Buffers settings
    proto_version: str = "proto3"
    package_name: str = "com.company.datasets"
    go_package: str = "github.com/company/datasets"

    # Import settings
    include_google_types: bool = True
    include_common_imports: bool = True


class ProtobufGenerator:
    """Generator for Protocol Buffer files from dataset definitions."""

    def __init__(
        self,
        config: Optional[ProtobufGeneratorConfig] = None,
        protobuf_config: Optional[ProtobufConfig] = None,
    ):
        self.config = config or ProtobufGeneratorConfig()
        self.protobuf_config = protobuf_config or ProtobufConfig()

        # Type mapping from scribe types to Protocol Buffers types
        self.type_mapping = {
            "string": "string",
            "integer": "int32",
            "number": "double",
            "boolean": "bool",
            "array": "repeated",
            "object": "map<string, string>",  # Simplified for protobuf
        }

        # Format mappings for string types
        self.format_mapping = {
            "email": "string",
            "uri": "string",
            "date": "string",
            "time": "string",
            "date-time": "string",
            "uuid": "string",
        }

        # Field number counter for automatic numbering
        self.field_number = 1

    def generate_proto_file(self, dataset: DatasetDefinition) -> str:
        """
        Generate a Protocol Buffer file from a dataset definition.

        Args:
            dataset: DatasetDefinition to convert

        Returns:
            Generated Protocol Buffer code as string
        """
        lines = []

        # Add syntax declaration
        lines.append(f'syntax = "{self.config.proto_version}";')
        lines.append("")

        # Add package declaration
        lines.append(f"package {self.config.package_name};")
        lines.append("")

        # Add imports
        lines.extend(self._generate_imports())
        lines.append("")

        # Add message documentation
        if self.config.include_documentation:
            lines.extend(self._generate_message_docstring(dataset))

        # Add message definition
        lines.append(f"message {dataset.name} {{")

        # Add fields
        if dataset.properties:
            field_lines = self._generate_fields(dataset.properties)
            lines.extend(field_lines)

            # Add enum definitions for fields that have enums
            enum_definitions = self._generate_field_enums(dataset.properties)
            if enum_definitions:
                lines.extend(enum_definitions)
        else:
            # Handle enum datasets
            if dataset.enum:
                lines.extend(self._generate_enum_message(dataset))
            else:
                lines.append("  // Empty message")

        lines.append("}")

        return "\n".join(lines)

    def _generate_imports(self) -> List[str]:
        """Generate import statements."""
        imports = []

        # Google types imports
        if self.config.include_google_types:
            imports.append('import "google/protobuf/timestamp.proto";')
            imports.append('import "google/protobuf/struct.proto";')

        # Common imports
        if self.config.include_common_imports:
            imports.append('import "google/protobuf/any.proto";')

        return imports

    def _generate_message_docstring(self, dataset: DatasetDefinition) -> List[str]:
        """Generate message docstring."""
        lines = ["  //"]

        # Add description
        if dataset.description:
            lines.append(f"  // {dataset.description}")
            lines.append("  //")

        # Add owner information
        if dataset.owner:
            lines.append(f"  // Owner: {dataset.owner}")
            lines.append("  //")

        # Add field documentation
        if dataset.properties:
            lines.append("  // Fields:")
            for field_name, field_def in dataset.properties.items():
                field_desc = field_def.description or "No description"
                lines.append(f"  //   - {field_name}: {field_desc}")

        return lines

    def _generate_fields(self, properties: Dict[str, FieldDefinition]) -> List[str]:
        """Generate field definitions."""
        lines = []
        self.field_number = 1  # Reset field number counter

        for field_name, field_def in properties.items():
            # Field documentation
            if self.config.include_documentation:
                doc_lines = self._generate_field_docstring(field_def)
                lines.extend(doc_lines)

            # Field definition
            proto_type = self._get_protobuf_type(field_def)
            field_line = f"  {proto_type} {field_name} = {self.field_number}"

            # Add field options
            options = self._get_field_options(field_def)
            if options:
                field_line += f" [{options}]"

            field_line += ";"
            lines.append(field_line)

            self.field_number += 1

        return lines

    def _generate_field_docstring(self, field_def: FieldDefinition) -> List[str]:
        """Generate field docstring."""
        lines = ["  //"]

        # Description
        if field_def.description:
            lines.append(f"  // {field_def.description}")

        # Owner
        if field_def.owner:
            lines.append(f"  // Owner: {field_def.owner}")

        # Example
        if field_def.example is not None:
            lines.append(f"  // Example: {field_def.example}")

        # Constraints
        constraints = self._get_field_constraints(field_def)
        if constraints:
            lines.append("  // Constraints:")
            for constraint in constraints:
                lines.append(f"  //   - {constraint}")

        return lines

    def _generate_field_enums(
        self, properties: Dict[str, FieldDefinition]
    ) -> List[str]:
        """Generate enum definitions for fields that have enums."""
        lines = []

        for field_name, field_def in properties.items():
            if field_def.enum:
                enum_name = f"{field_name.capitalize()}Enum"
                lines.append("")
                lines.append(f"  enum {enum_name} {{")

                # Add enum values
                for i, enum_value in enumerate(field_def.enum):
                    if isinstance(enum_value, str):
                        enum_constant = (
                            enum_value.upper().replace("-", "_").replace(" ", "_")
                        )
                        lines.append(f"    {enum_constant} = {i};")
                    else:
                        lines.append(f"    VALUE_{i} = {enum_value};")

                lines.append("  }")

        return lines

    def _get_protobuf_type(self, field_def: FieldDefinition) -> str:
        """Convert scribe field type to Protocol Buffers type."""
        base_type = self.type_mapping.get(field_def.type, "string")

        # Handle format-specific types
        if field_def.format and field_def.format in self.format_mapping:
            base_type = self.format_mapping[field_def.format]

        # Handle arrays
        if field_def.type == "array" and field_def.items:
            item_type = self._get_protobuf_type(field_def.items)
            base_type = f"repeated {item_type}"

        # Handle optional fields (proto3 doesn't have optional by default)
        if not field_def.required or field_def.default is not None:
            # In proto3, all fields are optional by default
            # We can use wrapper types for explicit optionality if needed
            pass

        # Handle enum fields
        if field_def.enum:
            # Create enum type name based on field name
            enum_name = f"{field_def.name.capitalize()}Enum"
            base_type = enum_name

        # Handle oneOf (union types) - not directly supported in protobuf
        if field_def.one_of:
            base_type = "google.protobuf.Any"  # Use Any type for unions

        return base_type

    def _get_field_options(self, field_def: FieldDefinition) -> str:
        """Get field options for Protocol Buffers."""
        options = []

        # Add validation options if available
        if field_def.min_length is not None:
            options.append(f"min_length: {field_def.min_length}")

        if field_def.max_length is not None:
            options.append(f"max_length: {field_def.max_length}")

        if field_def.pattern is not None:
            options.append(f'pattern: "{field_def.pattern}"')

        if field_def.minimum is not None:
            options.append(f"minimum: {field_def.minimum}")

        if field_def.maximum is not None:
            options.append(f"maximum: {field_def.maximum}")

        # Add default value
        if field_def.default is not None:
            default_value = self._format_default_value(
                field_def.default, field_def.type
            )
            options.append(f"default: {default_value}")

        return ", ".join(options) if options else ""

    def _format_default_value(self, value: Any, field_type: str) -> str:
        """Format default value for Protocol Buffers."""
        if field_type == "string":
            return f'"{value}"'
        elif field_type == "boolean":
            return "true" if value else "false"
        elif field_type == "integer":
            return str(value)
        elif field_type == "number":
            return str(value)
        elif field_type == "array":
            return "[]"  # Empty array
        elif field_type == "object":
            return "{}"  # Empty object
        else:
            return str(value)

    def _get_field_constraints(self, field_def: FieldDefinition) -> List[str]:
        """Get list of field constraints for documentation."""
        constraints = []

        if field_def.min_length is not None:
            constraints.append(f"minLength: {field_def.min_length}")
        if field_def.max_length is not None:
            constraints.append(f"maxLength: {field_def.max_length}")
        if field_def.pattern is not None:
            constraints.append(f"pattern: {field_def.pattern}")
        if field_def.minimum is not None:
            constraints.append(f"minimum: {field_def.minimum}")
        if field_def.maximum is not None:
            constraints.append(f"maximum: {field_def.maximum}")
        if field_def.min_items is not None:
            constraints.append(f"minItems: {field_def.min_items}")
        if field_def.max_items is not None:
            constraints.append(f"maxItems: {field_def.max_items}")
        if field_def.unique_items:
            constraints.append("uniqueItems: true")

        return constraints

    def _generate_enum_message(self, dataset: DatasetDefinition) -> List[str]:
        """Generate enum message for simple enum datasets."""
        lines = []

        if not dataset.enum:
            return lines

        # Generate enum definition
        enum_name = f"{dataset.name}Enum"
        lines.append(f"  enum {enum_name} {{")

        # Add enum values
        for i, enum_value in enumerate(dataset.enum):
            if isinstance(enum_value, str):
                enum_constant = enum_value.upper().replace("-", "_").replace(" ", "_")
                lines.append(f"    {enum_constant} = {i};")
            else:
                lines.append(f"    VALUE_{i} = {enum_value};")

        lines.append("  }")

        return lines

    def generate_file(self, dataset: DatasetDefinition, output_path: Path) -> None:
        """
        Generate a Protocol Buffer file for a dataset.

        Args:
            dataset: DatasetDefinition to generate
            output_path: Path where to write the generated file
        """
        # Ensure output directory exists
        output_path.parent.mkdir(parents=True, exist_ok=True)

        # Generate the proto code
        code = self.generate_proto_file(dataset)

        # Write to file
        with open(output_path, "w") as f:
            f.write(code)

    def generate_directory(
        self, datasets: Dict[str, DatasetDefinition], base_path: Path
    ) -> None:
        """
        Generate Protocol Buffer files for multiple datasets.

        Args:
            datasets: Dictionary of dataset definitions
            base_path: Base path for generated files
        """
        for dataset_name, dataset in datasets.items():
            # Create file path based on dataset name
            file_path = base_path / f"{dataset_name.lower()}.proto"

            # Generate the file
            self.generate_file(dataset, file_path)

        # Create package file if requested
        if self.config.create_package_files:
            self._generate_package_file(datasets, base_path)

    def _generate_package_file(
        self, datasets: Dict[str, DatasetDefinition], base_path: Path
    ) -> None:
        """Generate package file for the Protocol Buffers."""
        lines = []

        # Add syntax declaration
        lines.append(f'syntax = "{self.config.proto_version}";')
        lines.append("")

        # Add package declaration
        lines.append(f"package {self.config.package_name};")
        lines.append("")

        # Add imports
        lines.append('import "google/protobuf/timestamp.proto";')
        lines.append('import "google/protobuf/struct.proto";')
        lines.append("")

        # Add package documentation
        lines.append("// Package containing all dataset definitions")
        lines.append("// Generated by scribe - Dataset Definition to Code Generator")
        lines.append("")

        # Add dataset references
        for dataset_name in datasets.keys():
            lines.append(f"// {dataset_name} dataset")
            lines.append(f"// Use {dataset_name.lower()}.proto for the full definition")

        # Write package file
        package_path = base_path / "package.proto"
        with open(package_path, "w") as f:
            f.write("\n".join(lines))

    def generate_go_package_option(self, dataset: DatasetDefinition) -> str:
        """Generate go_package option for Go language support."""
        if not self.config.add_go_package:
            return ""

        go_package_name = dataset.name.lower()
        return f'option go_package = "{self.config.go_package}/{go_package_name}";'

    def generate_java_package_option(self, dataset: DatasetDefinition) -> str:
        """Generate java_package option for Java language support."""
        java_package = self.config.package_name.replace(".", "_")
        return f'option java_package = "{java_package}";'

    def generate_csharp_package_option(self, dataset: DatasetDefinition) -> str:
        """Generate csharp_namespace option for C# language support."""
        csharp_namespace = self.config.package_name.replace(".", ".")
        return f'option csharp_namespace = "{csharp_namespace}";'
