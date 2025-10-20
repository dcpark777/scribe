Quick Start Guide
=================

This guide will walk you through creating your first Scribe project and generating code for multiple languages.

Creating Your First Project
---------------------------

1. **Initialize a new Scribe project**::

   scribe init

   This creates the following directory structure::

   .
   ├── datasets/           # YAML dataset definitions
   │   └── user.yaml      # Example dataset
   ├── generated/         # Generated code output
   │   ├── python/       # Python dataclasses
   │   ├── scala/        # Scala case classes
   │   └── protobuf/     # Protocol Buffers
   └── scribe.config.yaml # Configuration file

2. **Examine the example dataset**::

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

   scribe generate

2. **Check the generated files**::

   ls generated/python/    # Python dataclasses
   ls generated/scala/      # Scala case classes
   ls generated/protobuf/   # Protocol Buffers

Configuring Generation
----------------------

1. **View current configuration**::

   scribe config show

2. **Configure Python generation**::

   scribe config set --language python --setting include_validation --value true
   scribe config set --language python --setting include_documentation --value true

3. **Configure Scala generation**::

   scribe config set --language scala --setting package_name --value com.mycompany.datasets
   scribe config set --language scala --setting include_spark_imports --value true

4. **Configure Protocol Buffers**::

   scribe config set --language protobuf --setting proto_version --value proto3
   scribe config set --language protobuf --setting package_name --value com.mycompany.datasets

Example Generated Code
----------------------

**Python Dataclass** (generated/python/product.py)::

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
* Explore advanced features in the :doc:`user_guide`
* Check out more :doc:`examples`
* Read the :doc:`api_reference` for detailed API documentation
