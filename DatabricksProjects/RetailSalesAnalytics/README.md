
# 🛍️ Retail Sales Analytics using Azure Data Engineering

An end-to-end Azure Data Engineering project that demonstrates how retail sales data can be ingested, transformed, and analyzed using the Azure ecosystem. This project follows the **Medallion Architecture (Bronze → Silver → Gold)** and delivers interactive business insights through a Power BI dashboard.

---

## 📌 Project Overview

This project simulates a real-world retail analytics solution by integrating data from multiple sources, processing it using Azure Databricks, and building an executive dashboard in Power BI.

The pipeline automates data ingestion, performs data cleaning and transformations, creates analytics-ready Gold tables, and enables business users to monitor key performance indicators through interactive visualizations.

---

## 🏗️ Solution Architecture

```
GitHub (Customer JSON)
          │
          ▼
Azure SQL Database (Products, Stores, Transactions)
          │
          ▼
Azure Data Factory
          │
          ▼
Azure Data Lake Storage Gen2
          │
          ▼
Azure Databricks
Bronze → Silver → Gold
          │
          ▼
Power BI Dashboard
```
<img width="940" height="226" alt="image" src="https://github.com/user-attachments/assets/7e703a21-2ba3-42da-9fa4-36935043cb1b" />

---

## 🛠️ Technologies Used

- Microsoft Azure
- Azure Data Factory
- Azure Data Lake Storage Gen2
- Azure Databricks
- PySpark
- Delta Lake
- Azure SQL Database
- Power BI
- Git & GitHub

---

## 📂 Dataset

The project uses multiple datasets:

- Customers (JSON from GitHub)
- Products (Azure SQL Database)
- Stores (Azure SQL Database)
- Transactions (Azure SQL Database)

---

## ⚙️ Project Workflow

### 🔹 Data Ingestion

- Extracted customer data from GitHub.
- Extracted product, store, and transaction data from Azure SQL Database.
- Automated ingestion using Azure Data Factory.
- Stored raw data in Azure Data Lake Storage Gen2.

---

### 🥉 Bronze Layer

- Loaded raw datasets into Delta tables.
- Preserved original data without transformations.

---

### 🥈 Silver Layer

Performed data cleaning and transformation using PySpark:

- Removed duplicate records
- Standardized text values
- Converted data types
- Handled null values
- Created calculated columns
- Joined multiple datasets into a unified sales table

---

### 🥇 Gold Layer

Created business-ready aggregated tables for reporting:

- Store Sales
- Product Sales
- Category Sales
- Customer Sales
- Monthly Sales

These Gold tables were optimized for Power BI reporting.

---

# 📊 Power BI Dashboard

## Executive KPIs

- 💰 Total Revenue
- 🛒 Total Orders
- 👥 Total Customers
- 📦 Total Products
- 🏬 Total Stores
- 💳 Average Order Value

---

## Dashboard Features

- Monthly Revenue Trend
- Revenue by Category
- Store Performance
- Sales by City
- Product Performance
- Interactive Filters
  - Year
  - Month
  - Category
  - Store
  - City

---

## 📈 Key Business Insights

- Track monthly sales performance
- Compare revenue across product categories
- Identify top-performing stores
- Analyze city-wise sales distribution
- Monitor customer purchasing trends
- Support data-driven business decisions

---

## 📁 Repository Structure

```
Retail-Sales-Analytics-Azure-Data-Engineering
│
├── Architecture
├── Azure Data Factory
├── Databricks
│   ├── Bronze
│   ├── Silver
│   └── Gold
├── Dataset
├── Power BI
├── Images
└── README.md
```

---

## 🚀 Skills Demonstrated

- Azure Data Factory Pipelines
- Azure Databricks
- PySpark
- Delta Lake
- Data Cleaning & Transformation
- Medallion Architecture
- Data Modeling
- ETL Pipeline Development
- Power BI Dashboard Development
- Azure Cloud Services

---

## 📷 Dashboard Preview

> **Retail Sales Analytics Dashboard**


<img width="1313" height="738" alt="image" src="https://github.com/user-attachments/assets/b01cf1e2-950f-4de0-881f-e3802d92c643" />


<img width="1305" height="736" alt="image" src="https://github.com/user-attachments/assets/86fff0ac-0567-4f2b-83f3-dee10f836e4d" />



```markdown
![Retail Sales Dashboard](Images/Dashboard.png)
```

---

## 🎯 Learning Outcomes

Through this project, I gained hands-on experience in:

- Designing end-to-end ETL pipelines
- Building scalable data pipelines using Azure services
- Implementing the Medallion Architecture
- Performing data transformations with PySpark
- Creating analytics-ready Gold tables
- Developing interactive Power BI dashboards
- Applying cloud-based data engineering best practices

---

## 🔮 Future Enhancements

- Incremental Data Loading
- Slowly Changing Dimensions (SCD Type 2)
- CI/CD using Azure DevOps
- Data Quality Validation
- Pipeline Monitoring & Alerts
- Real-Time Data Streaming with Azure Event Hubs

---

## 👩‍💻 Author

**Thajunnisa N**

Aspiring Azure Data Engineer

- 💼 LinkedIn: https://www.linkedin.com/in/thajunnisa-n-637855ba/
- 💻 GitHub: https://github.com/Thaju-nisa

---

⭐ If you found this project useful, consider giving it a **Star** on GitHub!
