"""
Tests for Python dataclass generator.
"""

from pathlib import Path
import tempfile
import shutil

from scribe.generators.python import PythonDataclassGenerator, PythonGeneratorConfig
from scribe.parser import DatasetDefinition, FieldDefinition


class TestPythonDataclassGenerator:
    """Test cases for PythonDataclassGenerator."""

    def setup_method(self):
        """Set up test environment."""
        self.temp_dir = tempfile.mkdtemp()
        self.temp_path = Path(self.temp_dir)
        self.generator = PythonDataclassGenerator()

    def teardown_method(self):
        """Clean up test environment."""
        shutil.rmtree(self.temp_dir)

    def test_generate_simple_dataclass(self):
        """Test generating a simple dataclass."""
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

        code = self.generator.generate_dataclass(dataset)

        # Check basic structure
        assert "from dataclasses import dataclass" in code
        assert "from typing import" in code
        assert "@dataclass" in code
        assert "class User:" in code

        # Check field definitions
        assert "id: int" in code
        assert "name: str" in code
        assert "is_active: Optional[bool] = True" in code

        # Check documentation
        assert "A simple user" in code
        assert "User ID" in code
        assert "User name" in code

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

        code = self.generator.generate_dataclass(dataset)

        # Check array type
        assert "tags: List[str]" in code

        # Check constraints in documentation
        assert "min_items: 1" in code
        assert "max_items: 10" in code

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

        code = self.generator.generate_dataclass(dataset)

        # Check nested object type
        assert "customer: Dict[str, Any]" in code

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

        code = self.generator.generate_dataclass(dataset)

        # Check enum type (should use Literal)
        assert 'Literal["pending", "approved", "rejected"]' in code

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

        code = self.generator.generate_dataclass(dataset)

        # Check optional type
        assert "email: Optional[str] = None" in code

    def test_generate_file(self):
        """Test generating a Python file."""
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

        output_path = self.temp_path / "user.py"
        self.generator.generate_file(dataset, output_path)

        # Check file was created
        assert output_path.exists()

        # Check file content
        content = output_path.read_text()
        assert "class User:" in content
        assert "id: int" in content

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
        assert (self.temp_path / "user.py").exists()
        assert (self.temp_path / "product.py").exists()
        assert (self.temp_path / "__init__.py").exists()

        # Check __init__.py content
        init_content = (self.temp_path / "__init__.py").read_text()
        assert "from .user import User" in init_content
        assert "from .product import Product" in init_content
        assert "__all__ = ['User', 'Product']" in init_content

    def test_generate_with_validation(self):
        """Test generating with validation."""
        config = PythonGeneratorConfig(include_validation=True)
        generator = PythonDataclassGenerator(config)

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

        code = generator.generate_dataclass(dataset)

        # Check validation imports
        assert "import re" in code

        # Check validation method
        assert "def _validate_email(self) -> None:" in code
        assert "len(self.email) < 5" in code
        assert "len(self.email) > 100" in code
        assert 're.match(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}$"' in code

    def test_generate_without_validation(self):
        """Test generating without validation."""
        config = PythonGeneratorConfig(include_validation=False)
        generator = PythonDataclassGenerator(config)

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

        code = generator.generate_dataclass(dataset)

        # Check no validation code
        assert "import re" not in code
        assert "def _validate_" not in code

    def test_generate_without_documentation(self):
        """Test generating without documentation."""
        config = PythonGeneratorConfig(include_documentation=False)
        generator = PythonDataclassGenerator(config)

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

        code = generator.generate_dataclass(dataset)

        # Check no docstrings
        assert '"""' not in code
        assert "A user" not in code
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

        code = self.generator.generate_dataclass(dataset)

        # Check enum values
        assert 'PENDING = "pending"' in code
        assert 'APPROVED = "approved"' in code
        assert 'REJECTED = "rejected"' in code

    def test_type_mapping(self):
        """Test type mapping for different field types."""
        test_cases = [
            ("string", "str"),
            ("integer", "int"),
            ("number", "float"),
            ("boolean", "bool"),
            ("array", "List"),
            ("object", "Dict[str, Any]"),
        ]

        for scribe_type, expected_python_type in test_cases:
            field_def = FieldDefinition(
                name="test_field",
                type=scribe_type,
                description="Test field",
                owner="test-team@company.com",
            )

            python_type = self.generator._get_python_type(field_def)
            assert expected_python_type in python_type

    def test_format_default_value(self):
        """Test default value formatting."""
        test_cases = [
            ("string", "hello", '"hello"'),
            ("boolean", True, "True"),
            ("boolean", False, "False"),
            ("integer", 42, "42"),
            ("number", 3.14, "3.14"),
            ("array", ["a", "b"], '["a", "b"]'),
            ("object", {}, "{}"),
        ]

        for field_type, value, expected in test_cases:
            result = self.generator._format_default_value(value, field_type)
            assert result == expected
