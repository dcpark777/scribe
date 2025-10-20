"""
YAML dataset definition parser for scribe.

This module provides functionality to parse YAML files containing dataset definitions
and convert them into structured data that can be used for code generation.
"""

from typing import Any, Dict, List, Optional, Union
from pathlib import Path
import yaml  # type: ignore
from dataclasses import dataclass, field


@dataclass
class FieldDefinition:
    """Represents a field definition in a dataset."""

    name: str
    type: str
    description: str
    owner: str
    required: bool = True
    default: Optional[Any] = None
    example: Optional[Any] = None

    # String constraints
    min_length: Optional[int] = None
    max_length: Optional[int] = None
    pattern: Optional[str] = None
    format: Optional[str] = None

    # Numeric constraints
    minimum: Optional[Union[int, float]] = None
    maximum: Optional[Union[int, float]] = None
    exclusive_minimum: bool = False
    exclusive_maximum: bool = False
    multiple_of: Optional[Union[int, float]] = None

    # Array constraints
    min_items: Optional[int] = None
    max_items: Optional[int] = None
    unique_items: bool = False

    # Enum values
    enum: Optional[List[Any]] = None

    # Nested properties for objects
    properties: Optional[Dict[str, "FieldDefinition"]] = None

    # Array item definition
    items: Optional["FieldDefinition"] = None

    # Union types (oneOf)
    one_of: Optional[List["FieldDefinition"]] = None

    # Additional properties for objects
    additional_properties: Optional[bool] = None


@dataclass
class DatasetDefinition:
    """Represents a complete dataset definition."""

    name: str
    type: str
    description: str
    owner: str
    properties: Dict[str, FieldDefinition] = field(default_factory=dict)

    # Additional metadata
    examples: List[Any] = field(default_factory=list)
    tags: List[str] = field(default_factory=list)
    enum: Optional[List[Any]] = None


class YAMLParser:
    """Parser for YAML dataset definitions."""

    def __init__(self):
        self.supported_types = {
            "string",
            "integer",
            "number",
            "boolean",
            "array",
            "object",
        }
        self.supported_formats = {"email", "uri", "date", "time", "date-time", "uuid"}

    def parse_file(self, file_path: Path) -> DatasetDefinition:
        """
        Parse a YAML file containing a single dataset definition.

        Args:
            file_path: Path to the YAML file

        Returns:
            DatasetDefinition object

        Raises:
            FileNotFoundError: If the file doesn't exist
            yaml.YAMLError: If the YAML is malformed
            ValueError: If the dataset definition is invalid
        """
        if not file_path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")

        with open(file_path, "r") as f:
            data = yaml.safe_load(f)

        if not isinstance(data, dict):
            raise ValueError("YAML file must contain a dictionary")

        # Check if file contains exactly one dataset definition
        if len(data) == 0:
            raise ValueError("YAML file is empty")
        elif len(data) > 1:
            dataset_names = list(data.keys())
            raise ValueError(
                f"YAML file contains multiple datasets ({dataset_names}). "
                f"Please create one dataset per file for better maintainability."
            )

        # Get the single dataset definition
        dataset_name, definition = next(iter(data.items()))

        if not isinstance(definition, dict):
            raise ValueError(f"Dataset '{dataset_name}' must be a dictionary")

        return self._parse_dataset(dataset_name, definition)

    def parse_directory(self, directory_path: Path) -> Dict[str, DatasetDefinition]:
        """
        Parse all YAML files in a directory (one dataset per file).

        Args:
            directory_path: Path to directory containing YAML files

        Returns:
            Dictionary mapping dataset names to DatasetDefinition objects
        """
        if not directory_path.exists() or not directory_path.is_dir():
            raise ValueError(f"Directory not found: {directory_path}")

        all_datasets = {}
        yaml_files = list(directory_path.glob("*.yaml")) + list(
            directory_path.glob("*.yml")
        )

        for yaml_file in yaml_files:
            try:
                dataset = self.parse_file(yaml_file)
                # Check for duplicate dataset names
                if dataset.name in all_datasets:
                    raise ValueError(
                        f"Duplicate dataset name '{dataset.name}' found in {yaml_file}. "
                        f"Each dataset must have a unique name across all files."
                    )
                all_datasets[dataset.name] = dataset
            except Exception as e:
                raise ValueError(f"Error parsing {yaml_file}: {e}")

        return all_datasets

    def _parse_dataset(
        self, name: str, definition: Dict[str, Any]
    ) -> DatasetDefinition:
        """Parse a single dataset definition."""
        dataset_type = definition.get("type", "object")

        if dataset_type not in self.supported_types:
            raise ValueError(f"Unsupported type '{dataset_type}' for dataset '{name}'")

        # Require description and owner
        description = definition.get("description")
        if not description:
            raise ValueError(f"Dataset '{name}' must have a 'description' field")

        owner = definition.get("owner")
        if not owner:
            raise ValueError(f"Dataset '{name}' must have an 'owner' field")

        properties = {}
        if "properties" in definition:
            properties = self._parse_properties(definition["properties"])

        # Handle enum at dataset level (for simple enum datasets)
        enum_values = None
        if "enum" in definition:
            enum_values = definition["enum"]

        dataset = DatasetDefinition(
            name=name,
            type=dataset_type,
            description=description,
            owner=owner,
            properties=properties,
            examples=definition.get("examples", []),
            tags=definition.get("tags", []),
        )

        # Add enum to the dataset if it exists
        if enum_values:
            dataset.enum = enum_values

        return dataset

    def _parse_properties(
        self, properties: Dict[str, Any]
    ) -> Dict[str, FieldDefinition]:
        """Parse properties dictionary into FieldDefinition objects."""
        field_definitions = {}

        for field_name, field_def in properties.items():
            if not isinstance(field_def, dict):
                raise ValueError(f"Field '{field_name}' must be a dictionary")

            field_definitions[field_name] = self._parse_field(field_name, field_def)

        return field_definitions

    def _parse_field(self, name: str, definition: Dict[str, Any]) -> FieldDefinition:
        """Parse a single field definition."""
        field_type = definition.get("type", "string")

        # Require description and owner for fields
        description = definition.get("description")
        if not description:
            raise ValueError(f"Field '{name}' must have a 'description' field")

        owner = definition.get("owner")
        if not owner:
            raise ValueError(f"Field '{name}' must have an 'owner' field")

        # Don't raise error here - let validation handle it
        # if field_type not in self.supported_types:
        #     raise ValueError(f"Unsupported field type '{field_type}' for field '{name}'")

        # Parse nested properties for objects
        properties = None
        if field_type == "object" and "properties" in definition:
            properties = self._parse_properties(definition["properties"])

        # Parse array items
        items = None
        if field_type == "array" and "items" in definition:
            items_def = definition["items"]
            if isinstance(items_def, dict):
                # Add default description and owner if missing
                if "description" not in items_def:
                    items_def["description"] = f"Array item for {name}"
                if "owner" not in items_def:
                    items_def["owner"] = "system"
                items = self._parse_field("items", items_def)
            else:
                # Simple type definition - create a minimal field definition
                items = FieldDefinition(
                    name="items",
                    type=items_def if isinstance(items_def, str) else "string",
                    description=f"Array item for {name}",
                    owner="system",
                )

        # Parse oneOf (union types)
        one_of = None
        if "oneOf" in definition:
            one_of_defs = definition["oneOf"]
            if isinstance(one_of_defs, list):
                one_of = []
                for i, one_of_def in enumerate(one_of_defs):
                    if isinstance(one_of_def, dict):
                        one_of.append(self._parse_field(f"oneOf_{i}", one_of_def))

        # Parse enum values
        enum_values = None
        if "enum" in definition:
            enum_values = definition["enum"]
            if not isinstance(enum_values, list):
                raise ValueError(f"Enum values must be a list for field '{name}'")

        # Validate format
        format_value = definition.get("format")
        if format_value and format_value not in self.supported_formats:
            # Allow custom formats but warn
            pass

        return FieldDefinition(
            name=name,
            type=field_type,
            description=description,
            owner=owner,
            required=definition.get("required", True),
            default=definition.get("default"),
            example=definition.get("example"),
            # String constraints
            min_length=definition.get("min_length"),
            max_length=definition.get("max_length"),
            pattern=definition.get("pattern"),
            format=format_value,
            # Numeric constraints
            minimum=definition.get("minimum"),
            maximum=definition.get("maximum"),
            exclusive_minimum=definition.get("exclusive_minimum", False),
            exclusive_maximum=definition.get("exclusive_maximum", False),
            multiple_of=definition.get("multiple_of"),
            # Array constraints
            min_items=definition.get("min_items"),
            max_items=definition.get("max_items"),
            unique_items=definition.get("unique_items", False),
            # Enum and union types
            enum=enum_values,
            one_of=one_of,
            # Nested structures
            properties=properties,
            items=items,
            # Additional properties
            additional_properties=definition.get("additional_properties"),
        )

    def validate_dataset(self, dataset: DatasetDefinition) -> List[str]:
        """
        Validate a dataset definition and return list of validation errors.

        Args:
            dataset: DatasetDefinition to validate

        Returns:
            List of validation error messages (empty if valid)
        """
        errors = []

        # Validate required fields
        if not dataset.description:
            errors.append(f"Dataset '{dataset.name}' must have a description")

        if not dataset.owner:
            errors.append(f"Dataset '{dataset.name}' must have an owner")

        # Validate dataset type
        if dataset.type not in self.supported_types:
            errors.append(
                f"Dataset '{dataset.name}' has unsupported type '{dataset.type}'"
            )

        # Validate properties
        for field_name, field_def in dataset.properties.items():
            field_errors = self._validate_field(field_def)
            for error in field_errors:
                errors.append(f"Field '{field_name}': {error}")

        return errors

    def _validate_field(self, field: FieldDefinition) -> List[str]:
        """Validate a field definition."""
        errors = []

        # Validate required fields
        if not field.description:
            errors.append("Field must have a description")

        if not field.owner:
            errors.append("Field must have an owner")

        # Validate field type
        if field.type not in self.supported_types:
            errors.append(f"Unsupported type '{field.type}'")

        # Validate format
        if field.format and field.format not in self.supported_formats:
            # Allow custom formats but could add warning
            pass

        # Validate constraints
        if field.minimum is not None and field.maximum is not None:
            if field.minimum > field.maximum:
                errors.append("minimum cannot be greater than maximum")

        if field.min_length is not None and field.max_length is not None:
            if field.min_length > field.max_length:
                errors.append("min_length cannot be greater than max_length")

        if field.min_items is not None and field.max_items is not None:
            if field.min_items > field.max_items:
                errors.append("min_items cannot be greater than max_items")

        # Validate nested properties
        if field.properties:
            for nested_field_name, nested_field in field.properties.items():
                nested_errors = self._validate_field(nested_field)
                for error in nested_errors:
                    errors.append(f"Nested field '{nested_field_name}': {error}")

        # Validate array items
        if field.items:
            item_errors = self._validate_field(field.items)
            for error in item_errors:
                errors.append(f"Array item: {error}")

        # Validate oneOf options
        if field.one_of:
            for i, one_of_field in enumerate(field.one_of):
                one_of_errors = self._validate_field(one_of_field)
                for error in one_of_errors:
                    errors.append(f"oneOf option {i}: {error}")

        return errors
