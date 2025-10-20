Configuration Reference
========================

Scribe provides extensive configuration options for customizing code generation for each target language.

Configuration File
------------------

Scribe uses a YAML configuration file (``scribe.config.yaml``) to store settings::

   # Basic settings
   target_languages: ["python", "scala", "protobuf"]
   datasets_dir: "datasets"
   output_dir: "generated"

   # Language-specific configurations
   languages:
     python: { ... }
     scala: { ... }
     protobuf: { ... }

Python Configuration
--------------------

**Settings:**

* ``include_validation`` (bool): Generate validation methods
* ``include_documentation`` (bool): Include docstrings
* ``use_typing_extensions`` (bool): Use typing_extensions imports
* ``add_dataclass_decorator`` (bool): Add @dataclass decorator
* ``generate_init_file`` (bool): Generate __init__.py files
* ``line_length`` (int): Maximum line length

**Example Configuration:**

.. code-block:: yaml

   languages:
     python:
       include_validation: true
       include_documentation: true
       use_typing_extensions: false
       add_dataclass_decorator: true
       generate_init_file: true
       line_length: 100

Scala Configuration
-------------------

**Settings:**

* ``package_name`` (string): Package name for generated classes
* ``include_spark_imports`` (bool): Include Spark imports
* ``include_validation`` (bool): Generate validation methods
* ``include_documentation`` (bool): Include documentation
* ``generate_package_object`` (bool): Generate package object
* ``use_option_types`` (bool): Use Option types for optional fields
* ``line_length`` (int): Maximum line length

**Example Configuration:**

.. code-block:: yaml

   languages:
     scala:
       package_name: "com.company.datasets"
       include_spark_imports: true
       include_validation: true
       include_documentation: true
       generate_package_object: true
       use_option_types: true
       line_length: 100

Protocol Buffers Configuration
-----------------------------

**Settings:**

* ``proto_version`` (string): Protocol Buffers version (proto2, proto3)
* ``package_name`` (string): Package name
* ``go_package`` (string): Go package path
* ``java_package`` (string): Java package name
* ``csharp_namespace`` (string): C# namespace
* ``include_documentation`` (bool): Include documentation
* ``create_package_files`` (bool): Create package files
* ``include_google_types`` (bool): Include Google types
* ``use_field_numbers`` (bool): Use field numbers
* ``add_go_package`` (bool): Add go_package option
* ``add_java_package`` (bool): Add java_package option
* ``add_csharp_namespace`` (bool): Add csharp_namespace option
* ``line_length`` (int): Maximum line length

**Example Configuration:**

.. code-block:: yaml

   languages:
     protobuf:
       proto_version: "proto3"
       package_name: "com.company.datasets"
       go_package: "github.com/company/datasets"
       java_package: "com.company.datasets"
       csharp_namespace: "Company.Datasets"
       include_documentation: true
       create_package_files: true
       include_google_types: true
       use_field_numbers: true
       add_go_package: true
       add_java_package: true
       add_csharp_namespace: true
       line_length: 100

CLI Configuration Commands
--------------------------

**Show Current Configuration:**

.. code-block:: bash

   scribe config show

**Set Configuration Values:**

.. code-block:: bash

   scribe config set --language <lang> --setting <name> --value <value>

**List Available Settings:**

.. code-block:: bash

   scribe config list-settings --language <lang>

**Reset to Defaults:**

.. code-block:: bash

   scribe config reset --language <lang>

Configuration Examples
----------------------

**Minimal Python Configuration:**

.. code-block:: bash

   scribe config set --language python --setting include_validation --value false
   scribe config set --language python --setting include_documentation --value false

**Production Scala Configuration:**

.. code-block:: bash

   scribe config set --language scala --setting package_name --value com.mycompany.prod
   scribe config set --language scala --setting include_spark_imports --value true
   scribe config set --language scala --setting use_option_types --value true

**Multi-Language Protobuf Configuration:**

.. code-block:: bash

   scribe config set --language protobuf --setting proto_version --value proto3
   scribe config set --language protobuf --setting go_package --value github.com/mycompany/datasets
   scribe config set --language protobuf --setting java_package --value com.mycompany.datasets
   scribe config set --language protobuf --setting csharp_namespace --value MyCompany.Datasets

Configuration Validation
------------------------

Scribe validates configuration values when they are set:

* **Boolean values**: ``true``, ``false``
* **String values**: Any valid string
* **Integer values**: Valid integers
* **Path values**: Valid file system paths

Invalid values will result in an error message and the configuration will not be updated.
