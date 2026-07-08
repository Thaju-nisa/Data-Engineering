# 🚀 Live Search Trends Pipeline using Azure Data Factory

## 📌 Project Overview

This project demonstrates an end-to-end Azure Data Engineering pipeline that retrieves live Google Trends data using the SearchAPI.io REST API, stores raw JSON in Azure Blob Storage, transforms nested JSON using Azure Data Factory Mapping Data Flow, and loads the cleaned data into Azure SQL Database with monitoring and error handling.

---

## 🎯 Project Goal

Build an automated ETL pipeline that:

- Fetches live Google Trends data from SearchAPI.io
- Stores raw JSON files in Azure Blob Storage
- Transforms nested JSON into relational data
- Loads transformed data into Azure SQL Database
- Implements monitoring and error handling

---

## ✅ Features

### Data Ingestion
- Connected to SearchAPI.io REST API
- Retrieved live Google Trends data
- Triggered pipeline execution

### Data Storage
- Stored raw JSON in Azure Blob Storage

### Data Transformation
- Built Mapping Data Flow
- Flattened nested JSON arrays
- Selected and renamed required columns
- Converted hierarchical JSON into relational format

### Data Loading
- Loaded transformed data into Azure SQL Database
- Created the `GoogleTrends` table
- Inserted cleaned records successfully

### Error Handling
- Added Failure dependency
- Created `ErrorLog` table
- Logged pipeline failures using Stored Procedure

### Monitoring
- Monitored Pipeline Runs
- Monitored Activity Runs
- Validated success and failure scenarios

---

## 🛠 Technologies Used

- Azure Data Factory
- Azure SQL Database
- Azure Blob Storage
- REST API
- SearchAPI.io
- Mapping Data Flow
- Azure Integration Runtime
- SQL
- JSON

---

## 📊 Pipeline Flow

SearchAPI.io REST API
⬇
Copy Activity
⬇
Azure Blob Storage
⬇
Mapping Data Flow
⬇
Azure SQL Database
⬇
GoogleTrends Table

If Failure
⬇
Stored Procedure
⬇
ErrorLog Table

---

## 📷 Screens
Google trends Table:
<img width="1902" height="863" alt="GoogleTrendTable" src="https://github.com/user-attachments/assets/154b8048-59a9-496f-b81b-1c7720e559d6" />

Google trend raw data
<img width="1902" height="862" alt="GoogleTrendJsonRawData" src="https://github.com/user-attachments/assets/d83d933f-4bbe-417d-9adb-817ffcd1aa69" />

fetched Json Data
<img width="982" height="530" alt="FetchedJsonData" src="https://github.com/user-attachments/assets/0a618e13-98be-442c-bce6-bc6aea03c3c8" />

Dataflow for saving json to table
<img width="1905" height="793" alt="DataFlowForSaveJsontoTable" src="https://github.com/user-attachments/assets/0cd4f227-2f0a-468a-a52c-5b26b92b7fb6" />

Complete pipline
<img width="1912" height="841" alt="CompletedPipline" src="https://github.com/user-attachments/assets/f61fe3fc-1d8d-4b5c-91c0-1e81acdf0552" />


Complete Flow Video: 
https://youtu.be/G5DxrQpFzXk










