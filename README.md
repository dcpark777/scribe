# Scribe

[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://python.org)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Build Status](https://img.shields.io/badge/build-passing-brightgreen.svg)]()

**Scribe** is a powerful tool for generating dataset definitions in multiple languages and formats from YAML specifications.

## Features

- 🐍 **Python Dataclasses** - Generate type-safe Python dataclasses with validation
- ☕ **Scala Case Classes** - Generate Scala case classes optimized for Apache Spark
- 📦 **Protocol Buffers** - Generate Protocol Buffer definitions for efficient serialization
- ⚙️ **Configurable** - Extensive configuration options for each target language
- 📚 **Documentation** - Automatic generation of documentation and comments
- 🔧 **CLI Interface** - Easy-to-use command-line interface
- 🏗️ **Type Safety** - Maintain consistent types across all generated code

## How to Use Scribe

Scribe provides a simple command-line interface for all operations:

### Core Commands

- **`scribe init`** - Initialize a new project with directory structure and example files
- **`scribe generate`** - Generate code from your YAML dataset definitions  
- **`scribe config`** - Manage configuration settings for different languages

### Configuration Commands

- **`scribe config show`** - Display current configuration
- **`scribe config set`** - Set specific configuration values
- **`scribe config list-settings`** - List available settings for a language
- **`scribe config reset`** - Reset language configuration to defaults

### Getting Help

- **`scribe --help`** - Show all available commands
- **`scribe <command> --help`** - Get help for a specific command
- **`scribe --version`** - Check Scribe version

## Understanding Scribe's Outputs

When you run `scribe generate`, Scribe creates language-specific code files in the `generated/` directory:

### Directory Structure
```
generated/
├── python/           # Python dataclasses
│   ├── __init__.py   # Package initialization
│   └── user.py       # Generated dataclass
├── scala/            # Scala case classes
│   ├── package.scala # Package object
│   └── user.scala    # Generated case class
└── protobuf/         # Protocol Buffers
    ├── package.proto # Package imports
    └── user.proto    # Generated message
```

### Python Outputs
- **Dataclasses** with type hints and validation
- **Documentation** via docstrings
- **Validation methods** for data integrity
- **Import statements** for required modules

### Scala Outputs
- **Case classes** optimized for Spark
- **Schema definitions** for DataFrame operations
- **Column extraction** utilities
- **Package objects** for easy access

### Protocol Buffers Outputs
- **Message definitions** with proper field numbering
- **Enum types** for constrained values
- **Package declarations** with language options
- **Import statements** for Google types

## Configuring Scribe's Outputs

Scribe allows you to customize how code is generated for each language:

### Configuration Commands
```bash
# View current configuration
scribe config show

# Set specific values
scribe config set --language python --setting include_validation --value true

# List available settings
scribe config list-settings --language scala

# Reset to defaults
scribe config reset --language protobuf
```

### Python Configuration Options
- `include_validation` - Generate validation methods (default: true)
- `include_documentation` - Include docstrings (default: true)
- `use_typing_extensions` - Use typing_extensions imports (default: false)
- `add_dataclass_decorator` - Add @dataclass decorator (default: true)
- `generate_init_file` - Generate __init__.py files (default: true)
- `line_length` - Maximum line length (default: 100)

### Scala Configuration Options
- `package_name` - Package name for generated classes (default: com.company.datasets)
- `include_spark_imports` - Include Spark imports (default: true)
- `include_validation` - Generate validation methods (default: true)
- `include_documentation` - Include Scaladoc comments (default: true)
- `generate_package_object` - Generate package.scala object (default: true)
- `use_option_types` - Use Option[T] for optional fields (default: true)
- `line_length` - Maximum line length (default: 100)

### Protocol Buffers Configuration Options
- `proto_version` - Protocol Buffers version (default: proto3)
- `package_name` - Package name (default: com.company.datasets)
- `go_package` - Go package path (default: github.com/company/datasets)
- `java_package` - Java package name (default: com.company.datasets)
- `csharp_namespace` - C# namespace (default: Company.Datasets)
- `include_documentation` - Include comments (default: true)
- `create_package_files` - Create package.proto files (default: true)
- `include_google_types` - Include Google types (default: true)
- `use_field_numbers` - Use field numbers (default: true)
- `add_go_package` - Add go_package option (default: true)
- `add_java_package` - Add java_package option (default: true)
- `add_csharp_namespace` - Add csharp_namespace option (default: true)
- `line_length` - Maximum line length (default: 100)

## Quick Start

1. **Install Scribe:**
   ```bash
   pip install scribe
   ```

2. **Initialize a new project:**
   ```bash
   scribe init
   ```

3. **Define your dataset in YAML:**
   ```yaml
   # datasets/user.yaml
   User:
     type: object
     description: "A user in the system"
     owner: "backend-team@company.com"
     properties:
       id:
         type: integer
         description: "Unique user identifier"
         owner: "backend-team@company.com"
       name:
         type: string
         description: "User's full name"
         owner: "backend-team@company.com"
         min_length: 2
         max_length: 100
   ```

4. **Generate code:**
   ```bash
   scribe generate
   ```

5. **Configure settings:**
   ```bash
   scribe config set --language python --setting include_validation --value true
   ```

## Generated Code Examples

### Python Dataclass
```python
from dataclasses import dataclass
from typing import Optional

@dataclass
class User:
    """A user in the system"""
    
    id: int
    name: str
    email: str
    is_active: Optional[bool] = True
    
    def validate(self) -> None:
        """Validate the user data."""
        if len(self.name) < 2:
            raise ValueError("name must be at least 2 characters long")
        if len(self.name) > 100:
            raise ValueError("name must be at most 100 characters long")
```

### Scala Case Class
```scala
package com.company.datasets

import org.apache.spark.sql.types._
import org.apache.spark.sql.{DataFrame, Dataset}

case class User(
  id: Int,
  name: String,
  email: String,
  isActive: Option[Boolean] = Some(true)
) {
  def validate(): Unit = {
    if (name.length < 2) throw new IllegalArgumentException("name must be at least 2 characters long")
    if (name.length > 100) throw new IllegalArgumentException("name must be at most 100 characters long")
  }
}

object User {
  val schema: StructType = StructType(Seq(
    StructField("id", IntegerType, nullable = false),
    StructField("name", StringType, nullable = false),
    StructField("email", StringType, nullable = false),
    StructField("isActive", BooleanType, nullable = true)
  ))
}
```

### Protocol Buffers
```protobuf
syntax = "proto3";

package com.company.datasets;

message User {
  int32 id = 1;
  string name = 2;
  string email = 3;
  bool is_active = 4;
}
```

## Configuration

Scribe provides extensive configuration options for each target language:

```bash
# View current configuration
scribe config show

# Configure Python generation
scribe config set --language python --setting include_validation --value true

# Configure Scala generation
scribe config set --language scala --setting package_name --value com.mycompany.datasets

# Configure Protocol Buffers
scribe config set --language protobuf --setting proto_version --value proto3
```

## Documentation

- 📖 [Installation Guide](docs/source/installation.rst)
- 🚀 [Quick Start Guide](docs/source/quickstart.rst)
- 📚 [User Guide](docs/source/user_guide.rst)
- ⚙️ [Configuration Reference](docs/source/configuration.rst)
- 🔧 [API Reference](docs/source/api_reference.rst)
- 💡 [Examples](docs/source/examples.rst)
- 🤝 [Contributing](docs/source/contributing.rst)

## Development

```bash
# Clone the repository
git clone https://github.com/your-org/scribe.git
cd scribe

# Install dependencies
poetry install

# Run tests
make test

# Build documentation
make docs

# Run all quality checks
make check
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contributing

Contributions are welcome! Please see our [Contributing Guide](docs/source/contributing.rst) for details.

## Support

- 📧 Email: support@scribe.dev
- 🐛 Issues: [GitHub Issues](https://github.com/your-org/scribe/issues)
- 💬 Discussions: [GitHub Discussions](https://github.com/your-org/scribe/discussions)