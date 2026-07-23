An end-to-end Azure Databricks Data Engineering project implementing a Medallion Architecture (Bronze, Silver, Gold) for Food Delivery Analytics using PySpark, Delta Lake, and Databricks SQL Dashboards.
Food Delivery Analytics using Databricks
Project Overview

This project demonstrates an end-to-end Data Engineering pipeline built using Azure Databricks and Delta Lake. The pipeline follows the Medallion Architecture (Bronze → Silver → Gold) to ingest, clean, transform, and analyze food delivery data.

The project also includes Databricks SQL dashboards for business reporting.

Technologies Used
Azure Databricks
PySpark
Delta Lake
Databricks SQL
Parquet
GitHub

Architecture
CSV Files
(Customers, Orders, Restaurants)

        │

        ▼

Bronze Layer
(Raw Delta Tables)

        │

        ▼

Silver Layer
(Data Cleaning & Transformations)

        │

        ▼

Gold Layer
(Fact & Dimension Tables)

        │

        ▼

Databricks Dashboard
