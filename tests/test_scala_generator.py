"""
Tests for Scala case class generator.
"""

from pathlib import Path
import tempfile
import shutil

from scribe.generators.scala import ScalaCaseClassGenerator, ScalaGeneratorConfig
from scribe.parser import DatasetDefinition, FieldDefinition


class TestScalaCaseClassGenerator:
    """Test cases for ScalaCaseClassGenerator."""

    def setup_method(self):
        """Set up test environment."""
        self.temp_dir = tempfile.mkdtemp()
        self.temp_path = Path(self.temp_dir)
        self.generator = ScalaCaseClassGenerator()

    def teardown_method(self):
        """Clean up test environment."""
        shutil.rmtree(self.temp_dir)

    def test_generate_simple_case_class(self):
        """Test generating a simple case class."""
        dataset = DatasetDefinition(
            name="User",
            type="object",
            description="A simple user",
            owner="test-team@company.com",
            properties={
                "id": FieldDefinition(
                    name="id",
                    type="integer",
                    description="User ID",
                    owner="backend-team@company.com",
                ),
                "name": FieldDefinition(
                    name="name",
                    type="string",
                    description="User name",
                    owner="backend-team@company.com",
                ),
                "is_active": FieldDefinition(
                    name="is_active",
                    type="boolean",
                    description="Whether user is active",
                    owner="backend-team@company.com",
                    default=True,
                ),
            },
        )

        code = self.generator.generate_case_class(dataset)

        # Check basic structure
        assert "package com.company.datasets" in code
        assert "import org.apache.spark.sql" in code
        assert "case class User(" in code

        # Check field definitions
        assert "id: Int" in code
        assert "name: String" in code
        assert "is_active: Option[Boolean] = Some(true)" in code

        # Check Spark integration
        assert "object User" in code
        assert "def schema: StructType" in code
        assert "def columns: Seq[String]" in code
        assert "def fromDataFrame(df: DataFrame): Dataset[User]" in code

    def test_generate_array_field(self):
        """Test generating array fields."""
        dataset = DatasetDefinition(
            name="Product",
            type="object",
            description="A product with tags",
            owner="product-team@company.com",
            properties={
                "tags": FieldDefinition(
                    name="tags",
                    type="array",
                    description="Product tags",
                    owner="product-team@company.com",
                    items=FieldDefinition(
                        name="items",
                        type="string",
                        description="Tag value",
                        owner="product-team@company.com",
                    ),
                    min_items=1,
                    max_items=10,
                )
            },
        )

        code = self.generator.generate_case_class(dataset)

        # Check array type
        assert "tags: Seq[String]" in code

        # Check Spark schema
        assert "ArrayType(StringType)" in code

    def test_generate_nested_object(self):
        """Test generating nested objects."""
        dataset = DatasetDefinition(
            name="Order",
            type="object",
            description="An order",
            owner="order-team@company.com",
            properties={
                "customer": FieldDefinition(
                    name="customer",
                    type="object",
                    description="Customer info",
                    owner="customer-team@company.com",
                    properties={
                        "name": FieldDefinition(
                            name="name",
                            type="string",
                            description="Customer name",
                            owner="customer-team@company.com",
                        )
                    },
                )
            },
        )

        code = self.generator.generate_case_class(dataset)

        # Check nested object type
        assert "customer: Map[String, Any]" in code

        # Check Spark schema
        assert "MapType(StringType, StringType)" in code

    def test_generate_enum_field(self):
        """Test generating enum fields."""
        dataset = DatasetDefinition(
            name="Status",
            type="object",
            description="Status with enum",
            owner="status-team@company.com",
            properties={
                "status": FieldDefinition(
                    name="status",
                    type="string",
                    description="Status value",
                    owner="status-team@company.com",
                    enum=["pending", "approved", "rejected"],
                )
            },
        )

        code = self.generator.generate_case_class(dataset)

        # Check enum type (should use String with validation)
        assert "status: String" in code

    def test_generate_optional_field(self):
        """Test generating optional fields."""
        dataset = DatasetDefinition(
            name="User",
            type="object",
            description="User with optional field",
            owner="user-team@company.com",
            properties={
                "email": FieldDefinition(
                    name="email",
                    type="string",
                    description="User email",
                    owner="user-team@company.com",
                    required=False,
                )
            },
        )

        code = self.generator.generate_case_class(dataset)

        # Check optional type
        assert "email: Option[String] = None" in code

    def test_generate_file(self):
        """Test generating a Scala file."""
        dataset = DatasetDefinition(
            name="User",
            type="object",
            description="A user",
            owner="user-team@company.com",
            properties={
                "id": FieldDefinition(
                    name="id",
                    type="integer",
                    description="User ID",
                    owner="backend-team@company.com",
                )
            },
        )

        output_path = self.temp_path / "User.scala"
        self.generator.generate_file(dataset, output_path)

        # Check file was created
        assert output_path.exists()

        # Check file content
        content = output_path.read_text()
        assert "case class User(" in content
        assert "id: Int" in content

    def test_generate_directory(self):
        """Test generating multiple files in a directory."""
        datasets = {
            "User": DatasetDefinition(
                name="User",
                type="object",
                description="A user",
                owner="user-team@company.com",
                properties={
                    "id": FieldDefinition(
                        name="id",
                        type="integer",
                        description="User ID",
                        owner="backend-team@company.com",
                    )
                },
            ),
            "Product": DatasetDefinition(
                name="Product",
                type="object",
                description="A product",
                owner="product-team@company.com",
                properties={
                    "name": FieldDefinition(
                        name="name",
                        type="string",
                        description="Product name",
                        owner="product-team@company.com",
                    )
                },
            ),
        }

        self.generator.generate_directory(datasets, self.temp_path)

        # Check files were created
        assert (self.temp_path / "User.scala").exists()
        assert (self.temp_path / "Product.scala").exists()

    def test_generate_with_validation(self):
        """Test generating with validation."""
        config = ScalaGeneratorConfig(include_validation=True)
        generator = ScalaCaseClassGenerator(config)

        dataset = DatasetDefinition(
            name="User",
            type="object",
            description="A user with validation",
            owner="user-team@company.com",
            properties={
                "email": FieldDefinition(
                    name="email",
                    type="string",
                    description="User email",
                    owner="user-team@company.com",
                    min_length=5,
                    max_length=100,
                    pattern="^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}$",
                )
            },
        )

        code = generator.generate_case_class(dataset)

        # Check validation imports
        assert "import scala.util.{Try, Success, Failure}" in code
        assert "import java.util.regex.Pattern" in code

        # Check validation method
        assert "def validateEmail(): Try[Unit]" in code
        assert "email.length < 5" in code
        assert "email.length > 100" in code
        assert (
            'Pattern.compile("^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\\\.[a-zA-Z]{2,}$")'
            in code
        )

    def test_generate_without_validation(self):
        """Test generating without validation."""
        config = ScalaGeneratorConfig(include_validation=False)
        generator = ScalaCaseClassGenerator(config)

        dataset = DatasetDefinition(
            name="User",
            type="object",
            description="A user",
            owner="user-team@company.com",
            properties={
                "email": FieldDefinition(
                    name="email",
                    type="string",
                    description="User email",
                    owner="user-team@company.com",
                    min_length=5,
                )
            },
        )

        code = generator.generate_case_class(dataset)

        # Check no validation code
        assert "import scala.util" not in code
        assert "def validate" not in code

    def test_generate_without_documentation(self):
        """Test generating without documentation."""
        config = ScalaGeneratorConfig(include_documentation=False)
        generator = ScalaCaseClassGenerator(config)

        dataset = DatasetDefinition(
            name="User",
            type="object",
            description="A user",
            owner="user-team@company.com",
            properties={
                "id": FieldDefinition(
                    name="id",
                    type="integer",
                    description="User ID",
                    owner="backend-team@company.com",
                )
            },
        )

        code = generator.generate_case_class(dataset)

        # Check no class docstrings (but Spark imports may have some)
        assert "A simple user" not in code
        assert "User ID" not in code

    def test_generate_enum_dataset(self):
        """Test generating enum datasets."""
        dataset = DatasetDefinition(
            name="Status",
            type="string",
            description="Status values",
            owner="status-team@company.com",
            enum=["pending", "approved", "rejected"],
        )

        code = self.generator.generate_case_class(dataset)

        # Check enum values
        assert 'PENDING = "pending"' in code
        assert 'APPROVED = "approved"' in code
        assert 'REJECTED = "rejected"' in code

    def test_type_mapping(self):
        """Test type mapping for different field types."""
        test_cases = [
            ("string", "String"),
            ("integer", "Int"),
            ("number", "Double"),
            ("boolean", "Boolean"),
            ("array", "Seq"),
            ("object", "Map[String, Any]"),
        ]

        for scribe_type, expected_scala_type in test_cases:
            field_def = FieldDefinition(
                name="test_field",
                type=scribe_type,
                description="Test field",
                owner="test-team@company.com",
            )

            scala_type = self.generator._get_scala_type(field_def)
            assert expected_scala_type in scala_type

    def test_format_default_value(self):
        """Test default value formatting."""
        test_cases = [
            ("string", "hello", '"hello"'),
            ("boolean", True, "true"),
            ("boolean", False, "false"),
            ("integer", 42, "42"),
            ("number", 3.14, "3.14"),
            ("array", ["a", "b"], 'Seq("a", "b")'),
            ("object", {}, "Map.empty"),
        ]

        for field_type, value, expected in test_cases:
            result = self.generator._format_default_value(value, field_type)
            assert result == expected

    def test_spark_schema_generation(self):
        """Test Spark schema generation."""
        dataset = DatasetDefinition(
            name="User",
            type="object",
            description="A user",
            owner="user-team@company.com",
            properties={
                "id": FieldDefinition(
                    name="id",
                    type="integer",
                    description="User ID",
                    owner="backend-team@company.com",
                ),
                "tags": FieldDefinition(
                    name="tags",
                    type="array",
                    description="User tags",
                    owner="user-team@company.com",
                    items=FieldDefinition(
                        name="items",
                        type="string",
                        description="Tag value",
                        owner="user-team@company.com",
                    ),
                ),
            },
        )

        code = self.generator.generate_case_class(dataset)

        # Check schema generation
        assert "def schema: StructType" in code
        assert 'StructField("id", IntegerType' in code
        assert 'StructField("tags", ArrayType(StringType)' in code

    def test_column_extraction(self):
        """Test column extraction methods."""
        dataset = DatasetDefinition(
            name="User",
            type="object",
            description="A user",
            owner="user-team@company.com",
            properties={
                "id": FieldDefinition(
                    name="id",
                    type="integer",
                    description="User ID",
                    owner="backend-team@company.com",
                ),
                "name": FieldDefinition(
                    name="name",
                    type="string",
                    description="User name",
                    owner="backend-team@company.com",
                ),
            },
        )

        code = self.generator.generate_case_class(dataset)

        # Check column methods
        assert "def columns: Seq[String]" in code
        assert '"id"' in code
        assert '"name"' in code
        assert "def idColumn: String" in code
        assert "def nameColumn: String" in code
