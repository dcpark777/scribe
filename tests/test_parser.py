"""
Tests for YAML parser functionality.
"""

import pytest
from pathlib import Path
import tempfile
import yaml

from scribe.parser import YAMLParser


class TestYAMLParser:
    """Test cases for YAMLParser."""

    def setup_method(self):
        """Set up test environment."""
        self.parser = YAMLParser()
        self.temp_dir = tempfile.mkdtemp()
        self.temp_path = Path(self.temp_dir)

    def teardown_method(self):
        """Clean up test environment."""
        import shutil

        shutil.rmtree(self.temp_dir)

    def test_parse_simple_dataset(self):
        """Test parsing a simple dataset definition."""
        yaml_content = """
User:
  type: object
  description: "A simple user"
  owner: "test-team@company.com"
  properties:
    id:
      type: integer
      description: "User ID"
      owner: "backend-team@company.com"
    name:
      type: string
      description: "User name"
      owner: "backend-team@company.com"
      min_length: 1
      max_length: 100
    email:
      type: string
      format: email
      description: "User email"
      owner: "backend-team@company.com"
"""

        yaml_file = self.temp_path / "test.yaml"
        yaml_file.write_text(yaml_content)

        dataset = self.parser.parse_file(yaml_file)

        assert dataset.name == "User"
        assert dataset.type == "object"
        assert dataset.description == "A simple user"
        assert dataset.owner == "test-team@company.com"
        assert len(dataset.properties) == 3

        # Check id field
        id_field = dataset.properties["id"]
        assert id_field.name == "id"
        assert id_field.type == "integer"
        assert id_field.description == "User ID"
        assert id_field.owner == "backend-team@company.com"

        # Check name field
        name_field = dataset.properties["name"]
        assert name_field.name == "name"
        assert name_field.type == "string"
        assert name_field.min_length == 1
        assert name_field.max_length == 100

        # Check email field
        email_field = dataset.properties["email"]
        assert email_field.name == "email"
        assert email_field.type == "string"
        assert email_field.format == "email"

    def test_parse_array_field(self):
        """Test parsing array fields."""
        yaml_content = """
Product:
  type: object
  description: "A product with array fields"
  owner: "product-team@company.com"
  properties:
    tags:
      type: array
      description: "Product tags"
      owner: "product-team@company.com"
      items:
        type: string
        description: "Tag value"
        owner: "product-team@company.com"
      min_items: 1
      max_items: 10
    ratings:
      type: array
      description: "Product ratings"
      owner: "analytics-team@company.com"
      items:
        type: number
        description: "Rating value"
        owner: "analytics-team@company.com"
        minimum: 1
        maximum: 5
      min_items: 0
      max_items: 1000
"""

        yaml_file = self.temp_path / "test.yaml"
        yaml_file.write_text(yaml_content)

        dataset = self.parser.parse_file(yaml_file)
        assert dataset.name == "Product"

        # Check tags field
        tags_field = dataset.properties["tags"]
        assert tags_field.type == "array"
        assert tags_field.min_items == 1
        assert tags_field.max_items == 10
        assert tags_field.items is not None
        assert tags_field.items.type == "string"
        assert tags_field.items.description == "Tag value"
        assert tags_field.items.owner == "product-team@company.com"

        # Check ratings field
        ratings_field = dataset.properties["ratings"]
        assert ratings_field.type == "array"
        assert ratings_field.items is not None
        assert ratings_field.items.type == "number"
        assert ratings_field.items.minimum == 1
        assert ratings_field.items.maximum == 5

    def test_parse_nested_object(self):
        """Test parsing nested objects."""
        yaml_content = """
Order:
  type: object
  description: "An order with nested objects"
  owner: "order-team@company.com"
  properties:
    customer:
      type: object
      description: "Customer information"
      owner: "customer-team@company.com"
      properties:
        name:
          type: string
          description: "Customer name"
          owner: "customer-team@company.com"
        address:
          type: object
          description: "Customer address"
          owner: "customer-team@company.com"
          properties:
            street:
              type: string
              description: "Street address"
              owner: "customer-team@company.com"
            city:
              type: string
              description: "City"
              owner: "customer-team@company.com"
"""

        yaml_file = self.temp_path / "test.yaml"
        yaml_file.write_text(yaml_content)

        dataset = self.parser.parse_file(yaml_file)
        assert dataset.name == "Order"

        customer_field = dataset.properties["customer"]
        assert customer_field.type == "object"
        assert customer_field.properties is not None
        assert "name" in customer_field.properties
        assert "address" in customer_field.properties

        address_field = customer_field.properties["address"]
        assert address_field.type == "object"
        assert address_field.properties is not None
        assert "street" in address_field.properties
        assert "city" in address_field.properties

    def test_parse_enum_field(self):
        """Test parsing enum fields."""
        yaml_content = """
Status:
  type: string
  description: "Status values"
  owner: "status-team@company.com"
  enum: ["pending", "approved", "rejected"]
"""

        yaml_file = self.temp_path / "test.yaml"
        yaml_file.write_text(yaml_content)

        dataset = self.parser.parse_file(yaml_file)
        assert dataset.name == "Status"
        assert dataset.type == "string"
        assert dataset.enum == ["pending", "approved", "rejected"]
        assert dataset.description == "Status values"
        assert dataset.owner == "status-team@company.com"

    def test_parse_oneof_field(self):
        """Test parsing oneOf (union) fields."""
        yaml_content = """
ContactInfo:
  type: object
  description: "Contact information with multiple formats"
  owner: "contact-team@company.com"
  properties:
    contact_data:
      type: object
      description: "Contact data"
      owner: "contact-team@company.com"
      oneOf:
        - type: object
          description: "Email contact"
          owner: "contact-team@company.com"
          properties:
            email:
              type: string
              format: email
              description: "Email address"
              owner: "contact-team@company.com"
        - type: object
          description: "Phone contact"
          owner: "contact-team@company.com"
          properties:
            phone:
              type: string
              description: "Phone number"
              owner: "contact-team@company.com"
"""

        yaml_file = self.temp_path / "test.yaml"
        yaml_file.write_text(yaml_content)

        dataset = self.parser.parse_file(yaml_file)
        assert dataset.name == "ContactInfo"

        contact_data_field = dataset.properties["contact_data"]
        assert contact_data_field.one_of is not None
        assert len(contact_data_field.one_of) == 2

        # Check first oneOf option (email)
        email_option = contact_data_field.one_of[0]
        assert email_option.type == "object"
        assert email_option.properties is not None
        assert "email" in email_option.properties

        # Check second oneOf option (phone)
        phone_option = contact_data_field.one_of[1]
        assert phone_option.type == "object"
        assert phone_option.properties is not None
        assert "phone" in phone_option.properties

    def test_parse_multiple_datasets_error(self):
        """Test error handling for multiple datasets in one file."""
        yaml_content = """
User:
  type: object
  description: "A user"
  owner: "user-team@company.com"
  properties:
    id:
      type: integer
      description: "User ID"
      owner: "backend-team@company.com"

Product:
  type: object
  description: "A product"
  owner: "product-team@company.com"
  properties:
    name:
      type: string
      description: "Product name"
      owner: "product-team@company.com"
"""

        yaml_file = self.temp_path / "test.yaml"
        yaml_file.write_text(yaml_content)

        with pytest.raises(ValueError, match="YAML file contains multiple datasets"):
            self.parser.parse_file(yaml_file)

    def test_parse_directory(self):
        """Test parsing multiple YAML files from a directory."""
        # Create first file
        file1_content = """
User:
  type: object
  description: "A user dataset"
  owner: "user-team@company.com"
  properties:
    id:
      type: integer
      description: "User ID"
      owner: "backend-team@company.com"
"""
        file1 = self.temp_path / "users.yaml"
        file1.write_text(file1_content)

        # Create second file
        file2_content = """
Product:
  type: object
  description: "A product dataset"
  owner: "product-team@company.com"
  properties:
    name:
      type: string
      description: "Product name"
      owner: "product-team@company.com"
"""
        file2 = self.temp_path / "products.yaml"
        file2.write_text(file2_content)

        datasets = self.parser.parse_directory(self.temp_path)

        assert len(datasets) == 2
        assert "User" in datasets
        assert "Product" in datasets

        assert datasets["User"].properties["id"].type == "integer"
        assert datasets["Product"].properties["name"].type == "string"

    def test_validation_errors(self):
        """Test dataset validation."""
        yaml_content = """
InvalidDataset:
  type: object
  description: "An invalid dataset for testing"
  owner: "test-team@company.com"
  properties:
    invalid_field:
      type: invalid_type
      description: "Invalid field"
      owner: "test-team@company.com"
      minimum: 10
      maximum: 5  # Invalid: minimum > maximum
"""

        yaml_file = self.temp_path / "test.yaml"
        yaml_file.write_text(yaml_content)

        dataset = self.parser.parse_file(yaml_file)
        assert dataset.name == "InvalidDataset"

        errors = self.parser.validate_dataset(dataset)

        assert len(errors) > 0
        assert any("Unsupported type 'invalid_type'" in error for error in errors)
        assert any(
            "minimum cannot be greater than maximum" in error for error in errors
        )

    def test_file_not_found(self):
        """Test error handling for missing file."""
        with pytest.raises(FileNotFoundError):
            self.parser.parse_file(Path("nonexistent.yaml"))

    def test_invalid_yaml(self):
        """Test error handling for invalid YAML."""
        yaml_file = self.temp_path / "invalid.yaml"
        yaml_file.write_text("invalid: yaml: content: [")

        with pytest.raises(yaml.YAMLError):
            self.parser.parse_file(yaml_file)

    def test_invalid_dataset_structure(self):
        """Test error handling for invalid dataset structure."""
        yaml_file = self.temp_path / "test.yaml"
        yaml_file.write_text("User: 'not a dictionary'")

        with pytest.raises(ValueError, match="Dataset 'User' must be a dictionary"):
            self.parser.parse_file(yaml_file)

    def test_field_constraints(self):
        """Test parsing field constraints."""
        yaml_content = """
ConstrainedField:
  type: object
  description: "A field with various constraints"
  owner: "constraint-team@company.com"
  properties:
    score:
      type: number
      description: "Score value"
      owner: "analytics-team@company.com"
      minimum: 0
      maximum: 100
      exclusive_minimum: true
      multiple_of: 0.5
    name:
      type: string
      description: "Name value"
      owner: "data-team@company.com"
      min_length: 2
      max_length: 50
      pattern: "^[a-zA-Z ]+$"
    tags:
      type: array
      description: "Tags array"
      owner: "data-team@company.com"
      items:
        type: string
        description: "Tag item"
        owner: "data-team@company.com"
      min_items: 1
      max_items: 10
      unique_items: true
"""

        yaml_file = self.temp_path / "test.yaml"
        yaml_file.write_text(yaml_content)

        dataset = self.parser.parse_file(yaml_file)
        assert dataset.name == "ConstrainedField"

        score_field = dataset.properties["score"]
        assert score_field.minimum == 0
        assert score_field.maximum == 100
        assert score_field.exclusive_minimum is True
        assert score_field.multiple_of == 0.5

        name_field = dataset.properties["name"]
        assert name_field.min_length == 2
        assert name_field.max_length == 50
        assert name_field.pattern == "^[a-zA-Z ]+$"

        tags_field = dataset.properties["tags"]
        assert tags_field.min_items == 1
        assert tags_field.max_items == 10
        assert tags_field.unique_items is True

    def test_missing_description_error(self):
        """Test error handling for missing description."""
        yaml_content = """
User:
  type: object
  owner: "test-team@company.com"
  properties:
    id:
      type: integer
      description: "User ID"
      owner: "backend-team@company.com"
"""

        yaml_file = self.temp_path / "test.yaml"
        yaml_file.write_text(yaml_content)

        with pytest.raises(
            ValueError, match="Dataset 'User' must have a 'description' field"
        ):
            self.parser.parse_file(yaml_file)

    def test_missing_owner_error(self):
        """Test error handling for missing owner."""
        yaml_content = """
User:
  type: object
  description: "A user"
  properties:
    id:
      type: integer
      description: "User ID"
      owner: "backend-team@company.com"
"""

        yaml_file = self.temp_path / "test.yaml"
        yaml_file.write_text(yaml_content)

        with pytest.raises(
            ValueError, match="Dataset 'User' must have an 'owner' field"
        ):
            self.parser.parse_file(yaml_file)

    def test_missing_field_description_error(self):
        """Test error handling for missing field description."""
        yaml_content = """
User:
  type: object
  description: "A user"
  owner: "test-team@company.com"
  properties:
    id:
      type: integer
      owner: "backend-team@company.com"
"""

        yaml_file = self.temp_path / "test.yaml"
        yaml_file.write_text(yaml_content)

        with pytest.raises(
            ValueError, match="Field 'id' must have a 'description' field"
        ):
            self.parser.parse_file(yaml_file)

    def test_missing_field_owner_error(self):
        """Test error handling for missing field owner."""
        yaml_content = """
User:
  type: object
  description: "A user"
  owner: "test-team@company.com"
  properties:
    id:
      type: integer
      description: "User ID"
"""

        yaml_file = self.temp_path / "test.yaml"
        yaml_file.write_text(yaml_content)

        with pytest.raises(ValueError, match="Field 'id' must have an 'owner' field"):
            self.parser.parse_file(yaml_file)
