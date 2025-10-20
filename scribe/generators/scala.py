"""
Scala case class generator for scribe.

This module generates Scala case classes from parsed dataset definitions,
optimized for Apache Spark DataFrame operations and type safety.
"""

from typing import Any, Dict, List, Optional
from pathlib import Path
from dataclasses import dataclass

from ..parser import DatasetDefinition, FieldDefinition
from ..config import ScalaConfig


@dataclass
class ScalaGeneratorConfig:
    """Configuration for Scala case class generation."""

    # Output settings
    output_dir: Path = Path("generated/scala")
    create_package_files: bool = True
    include_validation: bool = True
    include_documentation: bool = True

    # Code style settings
    line_length: int = 100
    use_field_defaults: bool = True
    add_apply_method: bool = True
    add_copy_method: bool = True

    # Spark integration settings
    include_spark_imports: bool = True
    include_encoders: bool = True
    include_schema_generation: bool = True
    include_column_extraction: bool = True

    # Package settings
    package_name: str = "com.company.datasets"
    scala_version: str = "2.13"


class ScalaCaseClassGenerator:
    """Generator for Scala case classes from dataset definitions."""

    def __init__(
        self,
        config: Optional[ScalaGeneratorConfig] = None,
        scala_config: Optional[ScalaConfig] = None,
    ):
        self.config = config or ScalaGeneratorConfig()
        self.scala_config = scala_config or ScalaConfig()

        # Type mapping from scribe types to Scala types
        self.type_mapping = {
            "string": "String",
            "integer": "Int",
            "number": "Double",
            "boolean": "Boolean",
            "array": "Seq",
            "object": "Map[String, Any]",
        }

        # Format mappings for string types
        self.format_mapping = {
            "email": "String",  # Could be enhanced with custom types
            "uri": "String",
            "date": "String",  # Could be enhanced with java.time.LocalDate
            "time": "String",
            "date-time": "String",  # Could be enhanced with java.time.LocalDateTime
            "uuid": "String",
        }

        # Spark-specific type mappings
        self.spark_type_mapping = {
            "string": "StringType",
            "integer": "IntegerType",
            "number": "DoubleType",
            "boolean": "BooleanType",
            "array": "ArrayType",
            "object": "MapType",
        }

    def generate_case_class(self, dataset: DatasetDefinition) -> str:
        """
        Generate a Scala case class from a dataset definition.

        Args:
            dataset: DatasetDefinition to convert

        Returns:
            Generated Scala code as string
        """
        lines = []

        # Add package declaration
        if self.config.create_package_files:
            lines.append(f"package {self.config.package_name}")
            lines.append("")

        # Add imports
        lines.extend(self._generate_imports())
        lines.append("")

        # Add class documentation
        if self.config.include_documentation:
            lines.extend(self._generate_class_docstring(dataset))

        # Add case class definition
        lines.append(f"case class {dataset.name}(")

        # Add fields
        if dataset.properties:
            field_lines = self._generate_fields(dataset.properties)
            lines.extend(field_lines)
        else:
            # Handle enum datasets
            if dataset.enum:
                lines.extend(self._generate_enum_class(dataset))
                return "\n".join(lines)
            else:
                lines.append("  // Empty case class")

        lines.append(") {")

        # Add companion object with Spark integration
        if self.config.include_spark_imports:
            lines.append("")
            lines.extend(self._generate_companion_object(dataset))

        lines.append("}")

        return "\n".join(lines)

    def _generate_imports(self) -> List[str]:
        """Generate import statements."""
        imports = []

        # Basic Scala imports
        imports.append("import scala.collection.immutable.Seq")
        imports.append("import scala.collection.immutable.Map")

        # Spark imports
        if self.config.include_spark_imports:
            imports.append(
                "import org.apache.spark.sql.{DataFrame, Dataset, SparkSession}"
            )
            imports.append("import org.apache.spark.sql.types._")
            imports.append("import org.apache.spark.sql.functions._")

            if self.config.include_encoders:
                imports.append("import org.apache.spark.sql.Encoders")

        # Validation imports
        if self.config.include_validation:
            imports.append("import scala.util.{Try, Success, Failure}")
            imports.append("import java.util.regex.Pattern")

        return imports

    def _generate_class_docstring(self, dataset: DatasetDefinition) -> List[str]:
        """Generate class docstring."""
        lines = ["/**"]

        # Add description
        if dataset.description:
            lines.append(f" * {dataset.description}")
            lines.append(" *")

        # Add owner information
        if dataset.owner:
            lines.append(f" * @owner {dataset.owner}")
            lines.append(" *")

        # Add field documentation
        if dataset.properties:
            lines.append(" * @param fields:")
            for field_name, field_def in dataset.properties.items():
                field_desc = field_def.description or "No description"
                lines.append(f" *   - {field_name}: {field_desc}")

        lines.append(" */")
        return lines

    def _generate_fields(self, properties: Dict[str, FieldDefinition]) -> List[str]:
        """Generate field definitions."""
        lines = []
        field_count = len(properties)

        for i, (field_name, field_def) in enumerate(properties.items()):
            # Field documentation
            if self.config.include_documentation:
                doc_lines = self._generate_field_docstring(field_def)
                lines.extend(doc_lines)

            # Field definition
            scala_type = self._get_scala_type(field_def)
            field_line = f"  {field_name}: {scala_type}"

            # Add default value if present
            if field_def.default is not None:
                default_value = self._format_default_value(
                    field_def.default, field_def.type
                )
                # For Option types, wrap in Some()
                if not field_def.required or "Option[" in scala_type:
                    field_line += f" = Some({default_value})"
                else:
                    field_line += f" = {default_value}"
            elif not field_def.required:
                field_line += f" = None"

            # Add comma if not last field
            if i < field_count - 1:
                field_line += ","

            lines.append(field_line)

            # Add validation if enabled
            if self.config.include_validation and self._has_constraints(field_def):
                lines.append("")
                lines.extend(self._generate_field_validation(field_def))

        return lines

    def _generate_field_docstring(self, field_def: FieldDefinition) -> List[str]:
        """Generate field docstring."""
        lines = ["  /**"]

        # Description
        if field_def.description:
            lines.append(f"   * {field_def.description}")

        # Owner
        if field_def.owner:
            lines.append(f"   * @owner {field_def.owner}")

        # Example
        if field_def.example is not None:
            lines.append(f"   * @example {field_def.example}")

        # Constraints
        constraints = self._get_field_constraints(field_def)
        if constraints:
            lines.append("   * @constraints")
            for constraint in constraints:
                lines.append(f"   *   - {constraint}")

        lines.append("   */")
        return lines

    def _get_scala_type(self, field_def: FieldDefinition) -> str:
        """Convert scribe field type to Scala type."""
        base_type = self.type_mapping.get(field_def.type, "Any")

        # Handle format-specific types
        if field_def.format and field_def.format in self.format_mapping:
            base_type = self.format_mapping[field_def.format]

        # Handle arrays
        if field_def.type == "array" and field_def.items:
            item_type = self._get_scala_type(field_def.items)
            base_type = f"Seq[{item_type}]"

        # Handle optional fields
        if not field_def.required or field_def.default is not None:
            base_type = f"Option[{base_type}]"

        # Handle enum fields
        if field_def.enum:
            enum_values = ", ".join(
                f'"{v}"' if isinstance(v, str) else str(v) for v in field_def.enum
            )
            base_type = f"String"  # Scala doesn't have Literal like Python, use String with validation

        # Handle oneOf (union types)
        if field_def.one_of:
            union_types = [
                self._get_scala_type(one_of_field) for one_of_field in field_def.one_of
            ]
            base_type = f"Any"  # Scala union types are complex, use Any for now

        return base_type

    def _format_default_value(self, value: Any, field_type: str) -> str:
        """Format default value for Scala."""
        if field_type == "string":
            return f'"{value}"'
        elif field_type == "boolean":
            return "true" if value else "false"
        elif field_type == "array":
            if isinstance(value, list):
                formatted_items = [
                    self._format_default_value(item, "string") for item in value
                ]
                return f"Seq({', '.join(formatted_items)})"
            return "Seq.empty"
        elif field_type == "object":
            return "Map.empty"
        else:
            return str(value)

    def _get_default_value(self, field_type: str) -> str:
        """Get default value for optional fields."""
        defaults = {
            "string": "None",
            "integer": "None",
            "number": "None",
            "boolean": "None",
            "array": "None",
            "object": "None",
        }
        return defaults.get(field_type, "None")

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

    def _generate_field_validation(self, field_def: FieldDefinition) -> List[str]:
        """Generate field validation code."""
        lines = []

        # Add validation method
        method_name = f"validate{field_def.name.capitalize()}"
        lines.append(f"  def {method_name}(): Try[Unit] = {{")

        validation_checks = []

        # String validations
        if field_def.type == "string":
            if field_def.min_length is not None:
                validation_checks.append(
                    f"    if ({field_def.name}.length < {field_def.min_length})"
                )
                validation_checks.append(
                    f'      return Failure(new IllegalArgumentException("{field_def.name} must be at least {field_def.min_length} characters"))'
                )

            if field_def.max_length is not None:
                validation_checks.append(
                    f"    if ({field_def.name}.length > {field_def.max_length})"
                )
                validation_checks.append(
                    f'      return Failure(new IllegalArgumentException("{field_def.name} must be at most {field_def.max_length} characters"))'
                )

            if field_def.pattern is not None:
                # Escape backslashes for Scala string literals
                escaped_pattern = field_def.pattern.replace("\\", "\\\\")
                validation_checks.append(
                    f'    val pattern = Pattern.compile("{escaped_pattern}")'
                )
                validation_checks.append(
                    f"    if (!pattern.matcher({field_def.name}).matches())"
                )
                validation_checks.append(
                    f'      return Failure(new IllegalArgumentException("{field_def.name} does not match required pattern"))'
                )

        # Numeric validations
        elif field_def.type in ["integer", "number"]:
            if field_def.minimum is not None:
                validation_checks.append(
                    f"    if ({field_def.name} < {field_def.minimum})"
                )
                validation_checks.append(
                    f'      return Failure(new IllegalArgumentException("{field_def.name} must be at least {field_def.minimum}"))'
                )

            if field_def.maximum is not None:
                validation_checks.append(
                    f"    if ({field_def.name} > {field_def.maximum})"
                )
                validation_checks.append(
                    f'      return Failure(new IllegalArgumentException("{field_def.name} must be at most {field_def.maximum}"))'
                )

        # Array validations
        elif field_def.type == "array":
            if field_def.min_items is not None and field_def.min_items > 0:
                validation_checks.append(
                    f"    if ({field_def.name}.length < {field_def.min_items})"
                )
                validation_checks.append(
                    f'      return Failure(new IllegalArgumentException("{field_def.name} must have at least {field_def.min_items} items"))'
                )

            if field_def.max_items is not None:
                validation_checks.append(
                    f"    if ({field_def.name}.length > {field_def.max_items})"
                )
                validation_checks.append(
                    f'      return Failure(new IllegalArgumentException("{field_def.name} must have at most {field_def.max_items} items"))'
                )

            if field_def.unique_items:
                validation_checks.append(
                    f"    if ({field_def.name}.distinct.length != {field_def.name}.length)"
                )
                validation_checks.append(
                    f'      return Failure(new IllegalArgumentException("{field_def.name} must contain unique items"))'
                )

        if validation_checks:
            lines.extend(validation_checks)
            lines.append("    Success(())")
        else:
            lines.append("    Success(())")

        lines.append("  }")

        return lines

    def _generate_companion_object(self, dataset: DatasetDefinition) -> List[str]:
        """Generate companion object with Spark integration."""
        lines = []

        lines.append("}")
        lines.append("")
        lines.append(f"object {dataset.name} {{")

        # Add schema generation
        if self.config.include_schema_generation:
            lines.extend(self._generate_schema_method(dataset))

        # Add column extraction
        if self.config.include_column_extraction:
            lines.extend(self._generate_column_methods(dataset))

        # Add DataFrame conversion methods
        lines.extend(self._generate_dataframe_methods(dataset))

        # Add validation methods
        if self.config.include_validation:
            lines.extend(self._generate_validation_methods(dataset))

        lines.append("}")

        return lines

    def _generate_schema_method(self, dataset: DatasetDefinition) -> List[str]:
        """Generate Spark schema method."""
        lines = []

        lines.append("  /**")
        lines.append("   * Generate Spark SQL schema for this dataset")
        lines.append("   * @return StructType schema")
        lines.append("   */")
        lines.append("  def schema: StructType = StructType(Seq(")

        if dataset.properties:
            field_schemas = []
            for field_name, field_def in dataset.properties.items():
                spark_type = self._get_spark_type(field_def)
                nullable = "true" if not field_def.required else "false"
                field_schema = (
                    f'    StructField("{field_name}", {spark_type}, {nullable})'
                )
                field_schemas.append(field_schema)

            lines.append(",\n".join(field_schemas))

        lines.append("  ))")
        lines.append("")

        return lines

    def _get_spark_type(self, field_def: FieldDefinition) -> str:
        """Convert scribe field type to Spark SQL type."""
        base_type = self.spark_type_mapping.get(field_def.type, "StringType")

        # Handle arrays
        if field_def.type == "array" and field_def.items:
            item_type = self._get_spark_type(field_def.items)
            base_type = f"ArrayType({item_type})"

        # Handle objects
        if field_def.type == "object":
            base_type = "MapType(StringType, StringType)"

        return base_type

    def _generate_column_methods(self, dataset: DatasetDefinition) -> List[str]:
        """Generate column extraction methods."""
        lines = []

        lines.append("  /**")
        lines.append("   * Get all column names for this dataset")
        lines.append("   * @return Seq of column names")
        lines.append("   */")
        lines.append("  def columns: Seq[String] = Seq(")

        if dataset.properties:
            column_names = [
                f'"{field_name}"' for field_name in dataset.properties.keys()
            ]
            lines.append("    " + ",\n    ".join(column_names))

        lines.append("  )")
        lines.append("")

        # Add individual column methods
        if dataset.properties:
            lines.append("  /**")
            lines.append("   * Get column names as individual methods")
            lines.append("   */")
            for field_name in dataset.properties.keys():
                lines.append(f'  def {field_name}Column: String = "{field_name}"')
            lines.append("")

        return lines

    def _generate_dataframe_methods(self, dataset: DatasetDefinition) -> List[str]:
        """Generate DataFrame conversion methods."""
        lines = []

        lines.append("  /**")
        lines.append("   * Convert DataFrame to Dataset of this type")
        lines.append("   * @param df DataFrame to convert")
        lines.append("   * @return Dataset of this type")
        lines.append("   */")
        lines.append("  def fromDataFrame(df: DataFrame): Dataset[User] = {")
        lines.append("    df.as[User]")
        lines.append("  }")
        lines.append("")

        lines.append("  /**")
        lines.append("   * Convert Dataset to DataFrame")
        lines.append("   * @param ds Dataset to convert")
        lines.append("   * @return DataFrame")
        lines.append("   */")
        lines.append("  def toDataFrame(ds: Dataset[User]): DataFrame = {")
        lines.append("    ds.toDF()")
        lines.append("  }")
        lines.append("")

        return lines

    def _generate_validation_methods(self, dataset: DatasetDefinition) -> List[str]:
        """Generate validation methods."""
        lines = []

        lines.append("  /**")
        lines.append("   * Validate all fields of this dataset")
        lines.append("   * @param instance Instance to validate")
        lines.append("   * @return Try[Unit] indicating success or failure")
        lines.append("   */")
        lines.append("  def validate(instance: User): Try[Unit] = {")

        if dataset.properties:
            validation_calls = []
            for field_name, field_def in dataset.properties.items():
                if self._has_constraints(field_def):
                    validation_calls.append(
                        f"    instance.validate{field_name.capitalize()}()"
                    )

            if validation_calls:
                lines.extend(validation_calls)
                lines.append("    Success(())")
            else:
                lines.append("    Success(())")
        else:
            lines.append("    Success(())")

        lines.append("  }")
        lines.append("")

        return lines

    def _generate_enum_class(self, dataset: DatasetDefinition) -> List[str]:
        """Generate enum class for simple enum datasets."""
        lines = []

        if not dataset.enum:
            return lines

        lines.append("  // Enum values")
        for enum_value in dataset.enum:
            if isinstance(enum_value, str):
                lines.append(f'  val {enum_value.upper()} = "{enum_value}"')
            else:
                lines.append(f"  val VALUE_{enum_value} = {enum_value}")

        return lines

    def generate_file(self, dataset: DatasetDefinition, output_path: Path) -> None:
        """
        Generate a Scala file for a dataset.

        Args:
            dataset: DatasetDefinition to generate
            output_path: Path where to write the generated file
        """
        # Ensure output directory exists
        output_path.parent.mkdir(parents=True, exist_ok=True)

        # Generate the case class code
        code = self.generate_case_class(dataset)

        # Write to file
        with open(output_path, "w") as f:
            f.write(code)

    def generate_directory(
        self, datasets: Dict[str, DatasetDefinition], base_path: Path
    ) -> None:
        """
        Generate Scala files for multiple datasets.

        Args:
            datasets: Dictionary of dataset definitions
            base_path: Base path for generated files
        """
        for dataset_name, dataset in datasets.items():
            # Create file path based on dataset name
            file_path = base_path / f"{dataset_name}.scala"

            # Generate the file
            self.generate_file(dataset, file_path)

        # Create package object if requested
        if self.config.create_package_files:
            self._generate_package_object(datasets, base_path)

    def _generate_package_object(
        self, datasets: Dict[str, DatasetDefinition], base_path: Path
    ) -> None:
        """Generate package object for the package."""
        lines = []

        # Add package declaration
        lines.append(f"package {self.config.package_name}")
        lines.append("")

        # Add package object
        lines.append("/**")
        lines.append(" * Package object for generated dataset definitions")
        lines.append(" */")
        lines.append("package object datasets {")
        lines.append("")

        # Add imports
        lines.append("  import org.apache.spark.sql.{DataFrame, Dataset}")
        lines.append("  import org.apache.spark.sql.types.StructType")
        lines.append("")

        # Add dataset references
        for dataset_name in datasets.keys():
            lines.append(f"  // {dataset_name} dataset")
            lines.append(
                f"  // Use {dataset_name}.schema, {dataset_name}.columns, etc."
            )

        lines.append("}")

        # Write package object
        package_path = base_path / "package.scala"
        with open(package_path, "w") as f:
            f.write("\n".join(lines))
