Examples
========

This section provides comprehensive examples of using Scribe for various scenarios.

Basic Examples
--------------

Simple User Dataset
~~~~~~~~~~~~~~~~~~~

**YAML Definition** (``datasets/user.yaml``)::

   User:
     type: object
     description: "A basic user in the system"
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
       email:
         type: string
         description: "User's email address"
         owner: "backend-team@company.com"
         format: email
       is_active:
         type: boolean
         description: "Whether the user is active"
         owner: "backend-team@company.com"
         default: true

**Generated Python** (``generated/python/user.py``)::

   from dataclasses import dataclass
   from typing import Optional
   
   @dataclass
   class User:
       """A basic user in the system"""
       
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

**Generated Scala** (``generated/scala/user.scala``)::

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

**Generated Protocol Buffers** (``generated/protobuf/user.proto``)::

   syntax = "proto3";
   
   package com.company.datasets;
   
   message User {
     int32 id = 1;
     string name = 2;
     string email = 3;
     bool is_active = 4;
   }

Advanced Examples
-----------------

E-commerce Order Dataset
~~~~~~~~~~~~~~~~~~~~~~~~

**YAML Definition** (``datasets/order.yaml``)::

   Order:
     type: object
     description: "An e-commerce order"
     owner: "order-team@company.com"
     properties:
       order_id:
         type: string
         description: "Unique order identifier"
         owner: "order-team@company.com"
         pattern: "^ORD-[0-9]{4}-[0-9]{3}$"
       
       customer:
         type: object
         description: "Customer information"
         owner: "customer-team@company.com"
         properties:
           customer_id:
             type: string
             description: "Customer identifier"
             owner: "customer-team@company.com"
           name:
             type: string
             description: "Customer name"
             owner: "customer-team@company.com"
             min_length: 2
             max_length: 100
           email:
             type: string
             description: "Customer email"
             owner: "customer-team@company.com"
             format: email
       
       items:
         type: array
         description: "Order items"
         owner: "order-team@company.com"
         min_items: 1
         max_items: 50
         items:
           type: object
           description: "Order item"
           owner: "order-team@company.com"
           properties:
             product_id:
               type: string
               description: "Product identifier"
               owner: "product-team@company.com"
             quantity:
               type: integer
               description: "Quantity ordered"
               owner: "order-team@company.com"
               minimum: 1
               maximum: 100
             unit_price:
               type: number
               description: "Unit price"
               owner: "finance-team@company.com"
               minimum: 0.01
       
       status:
         type: string
         description: "Order status"
         owner: "order-team@company.com"
         enum: ["pending", "confirmed", "shipped", "delivered", "cancelled"]
       
       total_amount:
         type: number
         description: "Total order amount"
         owner: "finance-team@company.com"
         minimum: 0.01

Enum Dataset
~~~~~~~~~~~~

**YAML Definition** (``datasets/status.yaml``)::

   Status:
     type: string
     description: "Order status values"
     owner: "order-team@company.com"
     enum: ["pending", "confirmed", "shipped", "delivered", "cancelled"]

**Generated Python** (``generated/python/status.py``)::

   class Status:
       """Order status values"""
       
       PENDING = "pending"
       CONFIRMED = "confirmed"
       SHIPPED = "shipped"
       DELIVERED = "delivered"
       CANCELLED = "cancelled"

**Generated Scala** (``generated/scala/status.scala``)::

   package com.company.datasets
   
   object Status {
     val PENDING = "pending"
     val CONFIRMED = "confirmed"
     val SHIPPED = "shipped"
     val DELIVERED = "delivered"
     val CANCELLED = "cancelled"
   }

**Generated Protocol Buffers** (``generated/protobuf/status.proto``)::

   syntax = "proto3";
   
   package com.company.datasets;
   
   enum StatusEnum {
     PENDING = 0;
     CONFIRMED = 1;
     SHIPPED = 2;
     DELIVERED = 3;
     CANCELLED = 4;
   }

Configuration Examples
----------------------

Development Configuration
~~~~~~~~~~~~~~~~~~~~~~~~~

**Configuration for development** (``scribe.config.yaml``)::

   target_languages: ["python", "scala"]
   datasets_dir: "datasets"
   output_dir: "generated"
   
   languages:
     python:
       include_validation: true
       include_documentation: true
       line_length: 88
     
     scala:
       package_name: "com.dev.datasets"
       include_spark_imports: true
       include_validation: true
       line_length: 100

Production Configuration
~~~~~~~~~~~~~~~~~~~~~~~~~

**Configuration for production** (``scribe.config.yaml``)::

   target_languages: ["python", "scala", "protobuf"]
   datasets_dir: "datasets"
   output_dir: "generated"
   
   languages:
     python:
       include_validation: true
       include_documentation: true
       line_length: 100
     
     scala:
       package_name: "com.company.prod.datasets"
       include_spark_imports: true
       include_validation: true
       use_option_types: true
       line_length: 120
     
     protobuf:
       proto_version: "proto3"
       package_name: "com.company.prod.datasets"
       go_package: "github.com/company/prod/datasets"
       java_package: "com.company.prod.datasets"
       include_documentation: true
       line_length: 100

Multi-Language Project
~~~~~~~~~~~~~~~~~~~~~~~

**Project structure for multi-language project**::

   my-project/
   ├── datasets/
   │   ├── user.yaml
   │   ├── product.yaml
   │   └── order.yaml
   ├── generated/
   │   ├── python/
   │   │   ├── __init__.py
   │   │   ├── user.py
   │   │   ├── product.py
   │   │   └── order.py
   │   ├── scala/
   │   │   ├── package.scala
   │   │   ├── user.scala
   │   │   ├── product.scala
   │   │   └── order.scala
   │   └── protobuf/
   │       ├── package.proto
   │       ├── user.proto
   │       ├── product.proto
   │       └── order.proto
   └── scribe.config.yaml

**CLI commands for multi-language project**::

   # Initialize project
   scribe init
   
   # Configure languages
   scribe config set --language python --setting include_validation --value true
   scribe config set --language scala --setting package_name --value com.mycompany.datasets
   scribe config set --language protobuf --setting proto_version --value proto3
   
   # Generate code
   scribe generate
   
   # Verify configuration
   scribe config show
