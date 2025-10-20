"""
Python dataclass generator for scribe.

This module generates Python dataclasses from parsed dataset definitions,
including proper type hints, validation, and documentation.
"""

from typing import Any, Dict, List, Optional
from pathlib import Path
from dataclasses import dataclass

from ..parser import DatasetDefinition, FieldDefinition
from ..config import PythonConfig


@dataclass
class PythonGeneratorConfig:
    """Configuration for Python dataclass generation."""

    # Output settings
    output_dir: Path = Path("generated/python")
    create_init_files: bool = True
    include_validation: bool = True
    include_documentation: bool = True

    # Code style settings
    line_length: int = 88
    use_field_defaults: bool = True
    add_repr: bool = True
    add_eq: bool = True

    # Import settings
    import_dataclasses: bool = True
    import_typing: bool = True
    import_validation: bool = True


class PythonDataclassGenerator:
    """Generator for Python dataclasses from dataset definitions."""

    def __init__(
        self,
        config: Optional[PythonGeneratorConfig] = None,
        python_config: Optional[PythonConfig] = None,
    ):
        self.config = config or PythonGeneratorConfig()
        self.python_config = python_config or PythonConfig()

        # Type mapping from scribe types to Python types
        self.type_mapping = {
            "string": "str",
            "integer": "int",
            "number": "float",
            "boolean": "bool",
            "array": "List",
            "object": "Dict[str, Any]",
        }

        # Format mappings for string types
        self.format_mapping = {
            "email": "str",  # Could be enhanced with email validation
            "uri": "str",
            "date": "str",  # Could be enhanced with date types
            "time": "str",
            "date-time": "str",
            "uuid": "str",
        }

    def generate_dataclass(self, dataset: DatasetDefinition) -> str:
        """
        Generate a Python dataclass from a dataset definition.

        Args:
            dataset: DatasetDefinition to convert

        Returns:
            Generated Python code as string
        """
        lines = []

        # Add imports
        lines.extend(self._generate_imports())
        lines.append("")

        # Add class documentation
        if self.config.include_documentation:
            lines.extend(self._generate_class_docstring(dataset))

        # Add dataclass decorator
        decorator_args = []
        if self.config.add_repr:
            decorator_args.append("repr=True")
        if self.config.add_eq:
            decorator_args.append("eq=True")

        decorator = "@dataclass"
        if decorator_args:
            decorator += f"({', '.join(decorator_args)})"
        lines.append(decorator)

        # Add class definition
        lines.append(f"class {dataset.name}:")
        lines.append("")

        # Add fields
        if dataset.properties:
            for field_name, field_def in dataset.properties.items():
                field_lines = self._generate_field(field_def)
                lines.extend(field_lines)
                lines.append("")
        else:
            # Handle enum datasets
            if dataset.enum:
                lines.extend(self._generate_enum_class(dataset))
            else:
                lines.append("    pass")

        return "\n".join(lines)

    def _generate_imports(self) -> List[str]:
        """Generate import statements."""
        imports = []

        if self.config.import_dataclasses:
            imports.append("from dataclasses import dataclass")

        if self.config.import_typing:
            imports.append(
                "from typing import Any, Dict, List, Optional, Union, Literal"
            )

        if self.config.include_validation and self.config.import_validation:
            imports.append("from typing import get_type_hints")
            imports.append("import re")

        return imports

    def _generate_class_docstring(self, dataset: DatasetDefinition) -> List[str]:
        """Generate class docstring."""
        lines = ['    """']

        # Add description
        if dataset.description:
            lines.append(f"    {dataset.description}")
            lines.append("")

        # Add owner information
        if dataset.owner:
            lines.append(f"    Owner: {dataset.owner}")
            lines.append("")

        # Add field documentation
        if dataset.properties:
            lines.append("    Attributes:")
            for field_name, field_def in dataset.properties.items():
                field_desc = field_def.description or "No description"
                lines.append(f"        {field_name}: {field_desc}")

        lines.append('    """')
        return lines

    def _generate_field(self, field_def: FieldDefinition) -> List[str]:
        """Generate a field definition."""
        lines = []

        # Field documentation
        if self.config.include_documentation:
            doc_lines = self._generate_field_docstring(field_def)
            lines.extend(doc_lines)

        # Field definition
        field_line = f"    {field_def.name}: {self._get_python_type(field_def)}"

        # Add default value if present
        if field_def.default is not None:
            default_value = self._format_default_value(
                field_def.default, field_def.type
            )
            field_line += f" = {default_value}"
        elif not field_def.required:
            field_line += " = None"

        lines.append(field_line)

        # Add field metadata for validation
        if self.config.include_validation and self._has_constraints(field_def):
            lines.append("")
            lines.extend(self._generate_field_validation(field_def))

        return lines

    def _generate_field_docstring(self, field_def: FieldDefinition) -> List[str]:
        """Generate field docstring."""
        lines = ['    """']

        # Description
        if field_def.description:
            lines.append(f"    {field_def.description}")

        # Owner
        if field_def.owner:
            lines.append(f"    Owner: {field_def.owner}")

        # Example
        if field_def.example is not None:
            lines.append(f"    Example: {field_def.example}")

        # Constraints
        constraints = self._get_field_constraints(field_def)
        if constraints:
            lines.append("    Constraints:")
            for constraint in constraints:
                lines.append(f"        {constraint}")

        lines.append('    """')
        return lines

    def _get_python_type(self, field_def: FieldDefinition) -> str:
        """Convert scribe field type to Python type."""
        base_type = self.type_mapping.get(field_def.type, "Any")

        # Handle format-specific types
        if field_def.format and field_def.format in self.format_mapping:
            base_type = self.format_mapping[field_def.format]

        # Handle arrays
        if field_def.type == "array" and field_def.items:
            item_type = self._get_python_type(field_def.items)
            base_type = f"List[{item_type}]"

        # Handle optional fields
        if not field_def.required or field_def.default is not None:
            base_type = f"Optional[{base_type}]"

        # Handle enum fields
        if field_def.enum:
            enum_values = ", ".join(
                f'"{v}"' if isinstance(v, str) else str(v) for v in field_def.enum
            )
            base_type = f"Literal[{enum_values}]"

        # Handle oneOf (union types)
        if field_def.one_of:
            union_types = [
                self._get_python_type(one_of_field) for one_of_field in field_def.one_of
            ]
            base_type = f"Union[{', '.join(union_types)}]"

        return base_type

    def _format_default_value(self, value: Any, field_type: str) -> str:
        """Format default value for Python."""
        if field_type == "string":
            return f'"{value}"'
        elif field_type == "boolean":
            return "True" if value else "False"
        elif field_type == "array":
            if isinstance(value, list):
                formatted_items = [
                    self._format_default_value(item, "string") for item in value
                ]
                return f"[{', '.join(formatted_items)}]"
            return "[]"
        elif field_type == "object":
            return "{}"
        else:
            return str(value)

    def _has_constraints(self, field_def: FieldDefinition) -> bool:
        """Check if field has validation constraints."""
        return any(
            [
                field_def.min_length is not None,
                field_def.max_length is not None,
                field_def.pattern is not None,
                field_def.minimum is not None,
                field_def.maximum is not None,
                field_def.min_items is not None,
                field_def.max_items is not None,
                field_def.unique_items,
            ]
        )

    def _get_field_constraints(self, field_def: FieldDefinition) -> List[str]:
        """Get list of field constraints for documentation."""
        constraints = []

        if field_def.min_length is not None:
            constraints.append(f"min_length: {field_def.min_length}")
        if field_def.max_length is not None:
            constraints.append(f"max_length: {field_def.max_length}")
        if field_def.pattern is not None:
            constraints.append(f"pattern: {field_def.pattern}")
        if field_def.minimum is not None:
            constraints.append(f"minimum: {field_def.minimum}")
        if field_def.maximum is not None:
            constraints.append(f"maximum: {field_def.maximum}")
        if field_def.min_items is not None:
            constraints.append(f"min_items: {field_def.min_items}")
        if field_def.max_items is not None:
            constraints.append(f"max_items: {field_def.max_items}")
        if field_def.unique_items:
            constraints.append("unique_items: True")

        return constraints

    def _generate_field_validation(self, field_def: FieldDefinition) -> List[str]:
        """Generate field validation code."""
        lines = []

        # Add validation method
        method_name = f"_validate_{field_def.name}"
        lines.append(f"    def {method_name}(self) -> None:")
        lines.append('        """Validate field constraints."""')

        validation_checks = []

        # String validations
        if field_def.type == "string":
            if field_def.min_length is not None:
                validation_checks.append(
                    f"        if len(self.{field_def.name}) < {field_def.min_length}:"
                )
                validation_checks.append(
                    f'            raise ValueError("{field_def.name} must be at least {field_def.min_length} characters")'
                )

            if field_def.max_length is not None:
                validation_checks.append(
                    f"        if len(self.{field_def.name}) > {field_def.max_length}:"
                )
                validation_checks.append(
                    f'            raise ValueError("{field_def.name} must be at most {field_def.max_length} characters")'
                )

            if field_def.pattern is not None:
                validation_checks.append(
                    f'        if not re.match(r"{field_def.pattern}", self.{field_def.name}):'
                )
                validation_checks.append(
                    f'            raise ValueError("{field_def.name} does not match required pattern")'
                )

        # Numeric validations
        elif field_def.type in ["integer", "number"]:
            if field_def.minimum is not None:
                validation_checks.append(
                    f"        if self.{field_def.name} < {field_def.minimum}:"
                )
                validation_checks.append(
                    f'            raise ValueError("{field_def.name} must be at least {field_def.minimum}")'
                )

            if field_def.maximum is not None:
                validation_checks.append(
                    f"        if self.{field_def.name} > {field_def.maximum}:"
                )
                validation_checks.append(
                    f'            raise ValueError("{field_def.name} must be at most {field_def.maximum}")'
                )

        # Array validations
        elif field_def.type == "array":
            if field_def.min_items is not None and field_def.min_items > 0:
                validation_checks.append(
                    f"        if len(self.{field_def.name}) < {field_def.min_items}:"
                )
                validation_checks.append(
                    f'            raise ValueError("{field_def.name} must have at least {field_def.min_items} items")'
                )

            if field_def.max_items is not None:
                validation_checks.append(
                    f"        if len(self.{field_def.name}) > {field_def.max_items}:"
                )
                validation_checks.append(
                    f'            raise ValueError("{field_def.name} must have at most {field_def.max_items} items")'
                )

            if field_def.unique_items:
                validation_checks.append(
                    f"        if len(set(self.{field_def.name})) != len(self.{field_def.name}):"
                )
                validation_checks.append(
                    f'            raise ValueError("{field_def.name} must contain unique items")'
                )

        if validation_checks:
            lines.extend(validation_checks)
        else:
            lines.append("        pass")

        return lines

    def _generate_enum_class(self, dataset: DatasetDefinition) -> List[str]:
        """Generate enum class for simple enum datasets."""
        lines = []

        if not dataset.enum:
            return lines

        lines.append("    # Enum values")
        for i, enum_value in enumerate(dataset.enum):
            if isinstance(enum_value, str):
                lines.append(f'    {enum_value.upper()} = "{enum_value}"')
            else:
                lines.append(f"    VALUE_{i} = {enum_value}")

        return lines

    def generate_file(self, dataset: DatasetDefinition, output_path: Path) -> None:
        """
        Generate a Python file for a dataset.

        Args:
            dataset: DatasetDefinition to generate
            output_path: Path where to write the generated file
        """
        # Ensure output directory exists
        output_path.parent.mkdir(parents=True, exist_ok=True)

        # Generate the dataclass code
        code = self.generate_dataclass(dataset)

        # Write to file
        with open(output_path, "w") as f:
            f.write(code)

    def generate_directory(
        self, datasets: Dict[str, DatasetDefinition], base_path: Path
    ) -> None:
        """
        Generate Python files for multiple datasets.

        Args:
            datasets: Dictionary of dataset definitions
            base_path: Base path for generated files
        """
        for dataset_name, dataset in datasets.items():
            # Create file path based on dataset name
            file_path = base_path / f"{dataset_name.lower()}.py"

            # Generate the file
            self.generate_file(dataset, file_path)

        # Create __init__.py if requested
        if self.config.create_init_files:
            self._generate_init_file(datasets, base_path)

    def _generate_init_file(
        self, datasets: Dict[str, DatasetDefinition], base_path: Path
    ) -> None:
        """Generate __init__.py file for the package."""
        lines = []

        # Add package docstring
        lines.append('"""Generated dataset definitions."""')
        lines.append("")

        # Add imports
        for dataset_name in datasets.keys():
            lines.append(f"from .{dataset_name.lower()} import {dataset_name}")

        lines.append("")

        # Add __all__
        all_names = list(datasets.keys())
        lines.append(f"__all__ = {all_names}")

        # Write __init__.py
        init_path = base_path / "__init__.py"
        with open(init_path, "w") as f:
            f.write("\n".join(lines))
