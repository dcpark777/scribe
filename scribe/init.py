"""
Project initialization utilities for scribe.
"""

from pathlib import Path
import click

from .config import ScribeConfig


def create_project_structure(base_path: Path = Path(".")) -> None:
    """Create the basic scribe project directory structure."""

    # Create main directories
    directories = [
        "datasets",
        "generated",
        "generated/python",
        "generated/scala",
        "generated/protobuf",
    ]

    for directory in directories:
        dir_path = base_path / directory
        dir_path.mkdir(parents=True, exist_ok=True)
        click.echo(f"✓ Created directory: {dir_path}")

    # Create example dataset file
    example_dataset = base_path / "datasets" / "user.yaml"
    if not example_dataset.exists():
        example_content = """# User dataset demonstrating primitive types, arrays, and maps
User:
  type: object
  description: "A comprehensive user example showing primitive types, arrays, and nested objects"
  owner: "data-team@company.com"
  properties:
    # Primitive data types
    id:
      type: integer
      description: "Unique user identifier"
      owner: "backend-team@company.com"
      example: 12345
    
    username:
      type: string
      description: "User's unique username"
      owner: "backend-team@company.com"
      min_length: 3
      max_length: 50
      pattern: "^[a-zA-Z0-9_]+$"
      example: "john_doe"
    
    email:
      type: string
      format: email
      description: "User's email address"
      owner: "backend-team@company.com"
      example: "john@example.com"
    
    is_active:
      type: boolean
      description: "Whether the user account is active"
      owner: "backend-team@company.com"
      default: true
    
    score:
      type: number
      description: "User's overall score"
      owner: "analytics-team@company.com"
      minimum: 0
      maximum: 100
      example: 85.5
    
    created_at:
      type: string
      format: date-time
      description: "When the user account was created"
      owner: "backend-team@company.com"
      example: "2023-10-19T15:30:00Z"
    
    # Array examples
    tags:
      type: array
      description: "User tags for categorization"
      owner: "product-team@company.com"
      items:
        type: string
        min_length: 1
        max_length: 20
      min_items: 0
      max_items: 10
      unique_items: true
      example: ["premium", "verified", "early-adopter"]
    
    permissions:
      type: array
      description: "User permissions"
      owner: "security-team@company.com"
      items:
        type: string
        enum: ["read", "write", "delete", "admin"]
      min_items: 1
      example: ["read", "write"]
    
    # Map/Object examples
    profile:
      type: object
      description: "User profile information"
      owner: "product-team@company.com"
      properties:
        first_name:
          type: string
          description: "User's first name"
          owner: "product-team@company.com"
          min_length: 1
          max_length: 50
          example: "John"
        
        last_name:
          type: string
          description: "User's last name"
          owner: "product-team@company.com"
          min_length: 1
          max_length: 50
          example: "Doe"
        
        bio:
          type: string
          description: "User biography"
          owner: "product-team@company.com"
          max_length: 500
          example: "Software engineer passionate about clean code"
    
    preferences:
      type: object
      description: "User preferences"
      owner: "ux-team@company.com"
      properties:
        theme:
          type: string
          enum: ["light", "dark", "auto"]
          default: "auto"
          description: "UI theme preference"
          owner: "ux-team@company.com"
        
        notifications:
          type: object
          description: "Notification preferences"
          owner: "ux-team@company.com"
          properties:
            email:
              type: boolean
              default: true
              description: "Email notifications enabled"
              owner: "ux-team@company.com"
            
            push:
              type: boolean
              default: false
              description: "Push notifications enabled"
              owner: "ux-team@company.com"
        
        language:
          type: string
          pattern: "^[a-z]{2}(-[A-Z]{2})?$"
          default: "en"
          description: "Preferred language code"
          owner: "ux-team@company.com"
          example: "en-US"
"""
        example_dataset.write_text(example_content)
        click.echo(f"✓ Created example dataset: {example_dataset}")

    # Create default config file
    config_path = base_path / "scribe.config.yaml"
    if not config_path.exists():
        config = ScribeConfig(config_path)
        config.save_config()
        click.echo(f"✓ Created config file: {config_path}")


def validate_project_structure(base_path: Path = Path(".")) -> bool:
    """Validate that the project has the required structure."""
    required_dirs = ["datasets", "generated"]

    for directory in required_dirs:
        if not (base_path / directory).exists():
            return False

    return True
