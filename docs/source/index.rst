Scribe Documentation
=====================

Welcome to Scribe, a powerful tool for generating dataset definitions in multiple languages and formats from YAML specifications.

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   installation
   quickstart
   user_guide
   configuration
   api_reference
   examples
   contributing

What is Scribe?
---------------

Scribe is a code generation tool that allows you to:

* Define datasets in YAML format with comprehensive validation rules
* Generate equivalent definitions in Python dataclasses, Scala case classes, and Protocol Buffers
* Maintain type safety and documentation across different languages
* Configure generation settings for each target language
* Track ownership and documentation for datasets and fields

Key Features
-------------

* **Multi-Language Support**: Generate code for Python, Scala, and Protocol Buffers
* **Type Safety**: Maintain consistent types across all generated code
* **Validation**: Built-in validation rules and constraints
* **Documentation**: Automatic generation of documentation and comments
* **Configuration**: Flexible configuration system for each language
* **CLI Interface**: Easy-to-use command-line interface
* **Extensible**: Easy to add new languages and formats

Quick Start
-----------

1. Install Scribe::

   .. code-block:: bash

      pip install scribe

2. Initialize a new project::

   .. code-block:: bash

      scribe init

3. Define your dataset in YAML::

   .. literalinclude:: ../../examples/datasets/user.yaml

4. Generate code::

   .. code-block:: bash

      scribe generate

5. Configure settings::

   .. code-block:: bash

      scribe config set --language python --setting include_validation --value true

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
