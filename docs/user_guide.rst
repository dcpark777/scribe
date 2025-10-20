User Guide
==========

This guide covers the advanced features and usage patterns of Scribe.

Dataset Definition Format
-------------------------

Scribe uses YAML format for dataset definitions. Each dataset is defined in its own file with the following structure:

.. code-block:: yaml

   DatasetName:
     type: object                    # Root type (object, string, array, etc.)
     description: "Dataset description"
     owner: "team@company.com"       # Owner/team responsible
     properties:                      # Fields for object types
       field_name:
         type: string                 # Field type
         description: "Field description"
         owner: "team@company.com"   # Field owner
         # ... additional constraints

Supported Data Types
--------------------

**Primitive Types:**

* ``string`` - Text data
* ``integer`` - Whole numbers
* ``number`` - Decimal numbers
* ``boolean`` - True/false values

**Complex Types:**

* ``array`` - Lists of items
* ``object`` - Nested structures
* ``enum`` - Enumerated values
* ``oneOf`` - Union types

Field Constraints
-----------------

**String Constraints:**

.. code-block:: yaml

   username:
     type: string
     min_length: 3
     max_length: 50
     pattern: "^[a-zA-Z0-9_]+$"

**Numeric Constraints:**

.. code-block:: yaml

   age:
     type: integer
     minimum: 0
     maximum: 150
     multiple_of: 1

   price:
     type: number
     minimum: 0.01
     maximum: 9999.99

**Array Constraints:**

.. code-block:: yaml

   tags:
     type: array
     items:
       type: string
     min_items: 1
     max_items: 10
     unique_items: true

**Enum Values:**

.. code-block:: yaml

   status:
     type: string
     enum: ["pending", "approved", "rejected"]

**OneOf (Union Types):**

.. code-block:: yaml

   contact:
     type: object
     oneOf:
       - type: object
         properties:
           email:
             type: string
             format: email
       - type: object
         properties:
           phone:
             type: string
             pattern: "^\\+?[1-9]\\d{1,14}$"

Configuration System
--------------------

Scribe provides a comprehensive configuration system for customizing code generation.

**View Configuration:**

.. code-block:: bash

   scribe config show

**Set Configuration Values:**

.. code-block:: bash

   scribe config set --language python --setting include_validation --value true
   scribe config set --language scala --setting package_name --value com.mycompany.data
   scribe config set --language protobuf --setting proto_version --value proto2

**List Available Settings:**

.. code-block:: bash

   scribe config list-settings --language python
   scribe config list-settings --language scala
   scribe config list-settings --language protobuf

**Reset to Defaults:**

.. code-block:: bash

   scribe config reset --language python

Language-Specific Features
--------------------------

**Python Dataclass Features:**

* Type hints with ``typing`` module
* Validation methods
* Documentation strings
* Optional field handling
* Enum class generation

**Scala Case Class Features:**

* Apache Spark integration
* Schema generation
* Column extraction
* Encoder support
* Package object generation

**Protocol Buffers Features:**

* Multiple proto versions (proto2, proto3)
* Language-specific package options
* Google types integration
* Field numbering
* Enum generation

Advanced Usage Patterns
-----------------------

**Multi-Dataset Projects:**

Organize datasets by domain::

   datasets/
   ├── user.yaml
   ├── product.yaml
   ├── order.yaml
   └── payment.yaml

**Custom Validation:**

Add custom validation logic in generated code by configuring validation settings.

**Documentation Generation:**

Ensure all generated code includes comprehensive documentation by enabling documentation settings.

**Type Safety:**

Maintain type safety across languages by using consistent type mappings.

Best Practices
--------------

1. **One Dataset Per File**: Keep each dataset in its own YAML file for better maintainability.

2. **Descriptive Names**: Use clear, descriptive names for datasets and fields.

3. **Owner Tracking**: Always specify owners for datasets and fields for accountability.

4. **Constraint Validation**: Use appropriate constraints to ensure data quality.

5. **Documentation**: Provide clear descriptions for all datasets and fields.

6. **Consistent Naming**: Use consistent naming conventions across your project.

Troubleshooting
---------------

**Common Issues:**

* **Missing Description/Owner**: Ensure all datasets and fields have required description and owner fields.
* **Invalid YAML**: Check YAML syntax and indentation.
* **Type Conflicts**: Verify type mappings are consistent across languages.
* **Configuration Errors**: Use ``scribe config show`` to verify settings.

**Getting Help:**

* Check the :doc:`api_reference` for detailed API documentation
* Review :doc:`examples` for usage patterns
* Use ``scribe --help`` for CLI help
