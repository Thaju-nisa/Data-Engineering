# Food Delivery Analytics using Azure Databricks

## Project Overview
This project demonstrates an end-to-end Data Engineering pipeline built using Azure Databricks and Delta Lake. The pipeline follows the Medallion Architecture (Bronze → Silver → Gold) to ingest, clean, transform, and analyze food delivery data.

The project also includes Databricks SQL dashboards for business reporting.


## Technologies Used
- Azure Databricks
- PySpark
- Delta Lake
- Databricks SQL
- CSV
- Git & GitHub

## Architecture

```text
CSV Files
(Customers, Orders, Restaurants)

        │
        ▼
Bronze Layer (Raw Delta Tables)

        │
        ▼
Silver Layer (Data Cleaning & Transformation)

        │
        ▼
Gold Layer (Fact & Dimension Tables)

        │
        ▼
Databricks Dashboard
```



## Dataset

The project uses three datasets:

- Customers
- Orders
- Restaurants

## Bronze Layer

- Read CSV files
- Created Bronze Delta tables
- Preserved raw data


## Silver Layer

- Removed duplicates
- Standardized order status
- Fixed null values
- Standardized city names
- Derived total_amount
- Converted data types



## Gold Layer

Created analytics-ready tables:

### Dimension Tables

- Customer Dimension
- Restaurant Dimension

### Fact Table

- Orders Fact



## Dashboard

Business KPIs:

- Total Revenue
- Total Orders
- Active Customers
- Revenue by City
- Revenue by Cuisine
- Order Status
- Top Restaurants
- Delivery Time Distribution
```
Datab

## Dashboard Preview

![Dashboard](screenshots/dashboard.png)ricks Dashboard
