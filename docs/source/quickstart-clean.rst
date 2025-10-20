Quick Start Guide
=================

This guide will walk you through creating your first Scribe project and generating code for multiple languages. You'll learn how to interact with Scribe, understand its outputs, and configure the generated code.

How to Interact with Scribe
---------------------------

Scribe provides a simple command-line interface with three main commands:

**Core Commands:**

- ``scribe init`` - Initialize a new project with directory structure and example files
- ``scribe generate`` - Generate code from your YAML dataset definitions
- ``scribe config`` - Manage configuration settings for different languages

**Configuration Commands:**

- ``scribe config show`` - Display current configuration
- ``scribe config set`` - Set specific configuration values
- ``scribe config list-settings`` - List available settings for a language
- ``scribe config reset`` - Reset language configuration to defaults

**Getting Help:**

- ``scribe --help`` - Show all available commands
- ``scribe <command> --help`` - Get help for a specific command
- ``scribe --version`` - Check Scribe version

Creating Your First Project
---------------------------

1. **Initialize a new Scribe project**::

   .. code-block:: bash

      scribe init

   This creates the following directory structure::

   .. code-block:: text

      .
      ├── datasets/           # YAML dataset definitions
      │   └── user.yaml      # Example dataset
      ├── generated/         # Generated code output
      │   ├── python/       # Python dataclasses
      │   ├── scala/        # Scala case classes
      │   └── protobuf/     # Protocol Buffers
      └── scribe.config.yaml # Configuration file

2. **Examine the example dataset**::

   .. code-block:: yaml

      # datasets/user.yaml
      User:
        type: object
        description: "A comprehensive user example showing primitive types, arrays, and nested objects"
        owner: "data-team@company.com"
        properties:
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

Defining Your Own Dataset
-------------------------

Let's create a simple Product dataset::

   .. code-block:: yaml

      # datasets/product.yaml
      Product:
        type: object
        description: "A product in the catalog"
        owner: "product-team@company.com"
        properties:
          product_id:
            type: string
            description: "Unique product identifier"
            owner: "product-team@company.com"
            example: "PROD-001"
          
          name:
            type: string
            description: "Product name"
            owner: "product-team@company.com"
            min_length: 2
            max_length: 100
          
          price:
            type: number
            description: "Product price"
            owner: "finance-team@company.com"
            minimum: 0.01
          
          category:
            type: string
            description: "Product category"
            owner: "product-team@company.com"
            enum: ["electronics", "books", "clothing", "home"]

Generating Code
---------------

1. **Generate code for all configured languages**::

   .. code-block:: bash

      scribe generate

2. **Check the generated files**::

   .. code-block:: bash

      ls generated/python/    # Python dataclasses
      ls generated/scala/      # Scala case classes
      ls generated/protobuf/   # Protocol Buffers

Understanding Scribe's Outputs
------------------------------

When you run ``scribe generate``, Scribe creates language-specific code files in the ``generated/`` directory:

**Directory Structure:**
::

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

**Python Outputs:**
- **Dataclasses** with type hints and validation
- **Documentation** via docstrings
- **Validation methods** for data integrity
- **Import statements** for required modules

**Scala Outputs:**
- **Case classes** optimized for Spark
- **Schema definitions** for DataFrame operations
- **Column extraction** utilities
- **Package objects** for easy access

**Protocol Buffers Outputs:**
- **Message definitions** with proper field numbering
- **Enum types** for constrained values
- **Package declarations** with language options
- **Import statements** for Google types

Configuring Generation
----------------------

Scribe allows you to customize how code is generated for each language. All configuration is stored in ``scribe.config.yaml`` and can be managed via CLI commands.

**Configuration Commands:**

- ``scribe config show`` - Display current configuration
- ``scribe config set`` - Set specific configuration values
- ``scribe config list-settings`` - List available settings for a language
- ``scribe config reset`` - Reset language configuration to defaults

**Python Configuration Options:**

- ``include_validation`` - Generate validation methods (default: true)
- ``include_documentation`` - Include docstrings (default: true)
- ``use_typing_extensions`` - Use typing_extensions imports (default: false)
- ``add_dataclass_decorator`` - Add @dataclass decorator (default: true)
- ``generate_init_file`` - Generate __init__.py files (default: true)
- ``line_length`` - Maximum line length (default: 100)

**Scala Configuration Options:**

- ``package_name`` - Package name for generated classes (default: com.company.datasets)
- ``include_spark_imports`` - Include Spark imports (default: true)
- ``include_validation`` - Generate validation methods (default: true)
- ``include_documentation`` - Include Scaladoc comments (default: true)
- ``generate_package_object`` - Generate package.scala object (default: true)
- ``use_option_types`` - Use Option[T] for optional fields (default: true)
- ``line_length`` - Maximum line length (default: 100)

**Protocol Buffers Configuration Options:**

- ``proto_version`` - Protocol Buffers version (default: proto3)
- ``package_name`` - Package name (default: com.company.datasets)
- ``go_package`` - Go package path (default: github.com/company/datasets)
- ``java_package`` - Java package name (default: com.company.datasets)
- ``csharp_namespace`` - C# namespace (default: Company.Datasets)
- ``include_documentation`` - Include comments (default: true)
- ``create_package_files`` - Create package.proto files (default: true)
- ``include_google_types`` - Include Google types (default: true)
- ``use_field_numbers`` - Use field numbers (default: true)
- ``add_go_package`` - Add go_package option (default: true)
- ``add_java_package`` - Add java_package option (default: true)
- ``add_csharp_namespace`` - Add csharp_namespace option (default: true)
- ``line_length`` - Maximum line length (default: 100)

**Example Configuration Commands:**

1. **View current configuration**::

   .. code-block:: bash

      scribe config show

2. **Configure Python generation**::

   .. code-block:: bash

      scribe config set --language python --setting include_validation --value true
      scribe config set --language python --setting include_documentation --value true

3. **Configure Scala generation**::

   .. code-block:: bash

      scribe config set --language scala --setting package_name --value com.mycompany.datasets
      scribe config set --language scala --setting include_spark_imports --value true

4. **Configure Protocol Buffers**::

   .. code-block:: bash

      scribe config set --language protobuf --setting proto_version --value proto3
      scribe config set --language protobuf --setting package_name --value com.mycompany.datasets

Example Generated Code
----------------------

**Python Dataclass** (generated/python/product.py)::

   .. code-block:: python

      from dataclasses import dataclass
      from typing import Optional
      
      @dataclass
      class Product:
          """A product in the catalog"""
          
          product_id: str
          name: str
          price: float
          category: str
          
          def validate(self) -> None:
              """Validate the product data."""
              if len(self.name) < 2:
                  raise ValueError("name must be at least 2 characters long")
              if len(self.name) > 100:
                  raise ValueError("name must be at most 100 characters long")
              if self.price < 0.01:
                  raise ValueError("price must be at least 0.01")

**Scala Case Class** (generated/scala/product.scala)::

   .. code-block:: scala

      package com.mycompany.datasets
      
      import org.apache.spark.sql.types._
      import org.apache.spark.sql.{DataFrame, Dataset}
      
      case class Product(
        productId: String,
        name: String,
        price: Double,
        category: String
      ) {
        def validate(): Unit = {
          if (name.length < 2) throw new IllegalArgumentException("name must be at least 2 characters long")
          if (name.length > 100) throw new IllegalArgumentException("name must be at most 100 characters long")
          if (price < 0.01) throw new IllegalArgumentException("price must be at least 0.01")
        }
      }
      
      object Product {
        val schema: StructType = StructType(Seq(
          StructField("productId", StringType, nullable = false),
          StructField("name", StringType, nullable = false),
          StructField("price", DoubleType, nullable = false),
          StructField("category", StringType, nullable = false)
        ))
      }

**Protocol Buffers** (generated/protobuf/product.proto)::

   .. code-block:: protobuf

      syntax = "proto3";
      
      package com.mycompany.datasets;
      
      message Product {
        string product_id = 1;
        string name = 2;
        double price = 3;
        string category = 4;
      }

Next Steps
----------

* Learn more about :doc:`configuration` options
* Explore :doc:`examples` for advanced usage patterns
* Read the :doc:`user_guide` for detailed features
* Check the :doc:`api_reference` for complete API documentation
