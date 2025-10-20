"""
Tests for Protocol Buffers generator.
"""

from pathlib import Path
import tempfile
import shutil

from scribe.generators.protobuf import ProtobufGenerator, ProtobufGeneratorConfig
from scribe.parser import DatasetDefinition, FieldDefinition


class TestProtobufGenerator:
    """Test cases for ProtobufGenerator."""

    def setup_method(self):
        """Set up test environment."""
        self.temp_dir = tempfile.mkdtemp()
        self.temp_path = Path(self.temp_dir)
        self.generator = ProtobufGenerator()

    def teardown_method(self):
        """Clean up test environment."""
        shutil.rmtree(self.temp_dir)

    def test_generate_simple_proto(self):
        """Test generating a simple Protocol Buffer message."""
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

        code = self.generator.generate_proto_file(dataset)

        # Check basic structure
        assert 'syntax = "proto3"' in code
        assert "package com.company.datasets" in code
        assert "message User {" in code

        # Check field definitions
        assert "int32 id = 1" in code
        assert "string name = 2" in code
        assert "bool is_active = 3" in code

        # Check documentation
        assert "// A simple user" in code
        assert "// User ID" in code
        assert "// User name" in code

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

        code = self.generator.generate_proto_file(dataset)

        # Check array type
        assert "repeated string tags = 1" in code

        # Check constraints in documentation
        assert "minItems: 1" in code
        assert "maxItems: 10" in code

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

        code = self.generator.generate_proto_file(dataset)

        # Check nested object type (simplified to map in protobuf)
        assert "map<string, string> customer = 1" in code

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

        code = self.generator.generate_proto_file(dataset)

        # Check enum type
        assert "StatusEnum status = 1" in code
        assert "enum StatusEnum {" in code
        assert "PENDING = 0" in code
        assert "APPROVED = 1" in code
        assert "REJECTED = 2" in code

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

        code = self.generator.generate_proto_file(dataset)

        # Check optional type (proto3 doesn't have explicit optional)
        assert "string email = 1" in code

    def test_generate_file(self):
        """Test generating a Protocol Buffer file."""
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

        output_path = self.temp_path / "user.proto"
        self.generator.generate_file(dataset, output_path)

        # Check file was created
        assert output_path.exists()

        # Check file content
        content = output_path.read_text()
        assert "message User {" in content
        assert "int32 id = 1" in content

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
        assert (self.temp_path / "user.proto").exists()
        assert (self.temp_path / "product.proto").exists()
        assert (self.temp_path / "package.proto").exists()

    def test_generate_without_documentation(self):
        """Test generating without documentation."""
        config = ProtobufGeneratorConfig(include_documentation=False)
        generator = ProtobufGenerator(config)

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

        code = generator.generate_proto_file(dataset)

        # Check no docstrings
        assert "// A user" not in code
        assert "// User ID" not in code

    def test_generate_enum_dataset(self):
        """Test generating enum datasets."""
        dataset = DatasetDefinition(
            name="Status",
            type="string",
            description="Status values",
            owner="status-team@company.com",
            enum=["pending", "approved", "rejected"],
        )

        code = self.generator.generate_proto_file(dataset)

        # Check enum values
        assert "enum StatusEnum {" in code
        assert "PENDING = 0" in code
        assert "APPROVED = 1" in code
        assert "REJECTED = 2" in code

    def test_type_mapping(self):
        """Test type mapping for different field types."""
        test_cases = [
            ("string", "string"),
            ("integer", "int32"),
            ("number", "double"),
            ("boolean", "bool"),
            ("array", "repeated"),
            ("object", "map<string, string>"),
        ]

        for scribe_type, expected_proto_type in test_cases:
            field_def = FieldDefinition(
                name="test_field",
                type=scribe_type,
                description="Test field",
                owner="test-team@company.com",
            )

            proto_type = self.generator._get_protobuf_type(field_def)
            assert expected_proto_type in proto_type

    def test_format_default_value(self):
        """Test default value formatting."""
        test_cases = [
            ("string", "hello", '"hello"'),
            ("boolean", True, "true"),
            ("boolean", False, "false"),
            ("integer", 42, "42"),
            ("number", 3.14, "3.14"),
            ("array", ["a", "b"], "[]"),
            ("object", {}, "{}"),
        ]

        for field_type, value, expected in test_cases:
            result = self.generator._format_default_value(value, field_type)
            assert result == expected

    def test_field_numbering(self):
        """Test automatic field numbering."""
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
                "email": FieldDefinition(
                    name="email",
                    type="string",
                    description="User email",
                    owner="backend-team@company.com",
                ),
            },
        )

        code = self.generator.generate_proto_file(dataset)

        # Check field numbering
        assert "int32 id = 1" in code
        assert "string name = 2" in code
        assert "string email = 3" in code

    def test_google_imports(self):
        """Test Google Protocol Buffers imports."""
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

        code = self.generator.generate_proto_file(dataset)

        # Check Google imports
        assert 'import "google/protobuf/timestamp.proto"' in code
        assert 'import "google/protobuf/struct.proto"' in code

    def test_package_generation(self):
        """Test package file generation."""
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
            )
        }

        self.generator.generate_directory(datasets, self.temp_path)

        # Check package file
        package_path = self.temp_path / "package.proto"
        assert package_path.exists()

        content = package_path.read_text()
        assert 'syntax = "proto3"' in content
        assert "package com.company.datasets" in content
        assert "// User dataset" in content
