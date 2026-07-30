
# 🚀 Blue-Green Deployment Using PowerShell
## 📌 Project Overview

This project demonstrates the **Blue-Green Deployment** pattern for databases using **PowerShell** and **SQL Server Express**.

The goal is to achieve **zero-downtime deployments** by maintaining two identical tables (`sales_blue` and `sales_green`) and switching a database view (`sales`) between them.

The entire deployment is executed using **PowerShell** with the `Invoke-Sqlcmd` cmdlet.

---

## 🛠️ Tech Stack

- Windows PowerShell 5.1
- SQL Server Express
- SQLServer PowerShell Module
- Git
- GitHub

---

## 📂 Project Structure

```text
de-pipeline/
│
├── deploy.ps1
├── rollback.ps1
├── config.ps1
├── README.md
│
├── logs/
│
└── scripts/
```

---

## 🎯 Project Objectives

- Create Blue and Green deployment tables
- Create a common view (`sales`)
- Load data into the idle table
- Switch production traffic by repointing the view
- Roll back instantly if deployment fails
- Automate everything using PowerShell

---

## 🏗️ Architecture

```text
                Users / Reports
                       │
                       ▼
               SELECT * FROM sales
                       │
                +---------------+
                |   sales View  |
                +---------------+
                       │
          ┌────────────┴────────────┐
          ▼                         ▼
   sales_blue                 sales_green
(Current Production)      (Deployment Target)
```

---

## ⚙️ Environment Setup

### Check PowerShell Version

```powershell
$PSVersionTable.PSVersion
```

### Install SQL Server Module

```powershell
Install-Module SqlServer -Scope CurrentUser -AllowClobber -Force
```

### Import Module

```powershell
Import-Module SqlServer
```

### Verify Installation

```powershell
Get-Command Invoke-Sqlcmd
```

---

## 🗄️ Create Database

```powershell
Invoke-Sqlcmd `
    -ServerInstance ".\SQLEXPRESS" `
    -Query "
IF DB_ID('BlueGreenDB') IS NULL
    CREATE DATABASE BlueGreenDB;
"
```

---

## 📋 Create Tables

The deployment creates two identical tables:

- `sales_blue`
- `sales_green`

Both contain:

| Column | Type |
|---------|------|
| SaleID | INT |
| CustomerName | VARCHAR(100) |
| Amount | DECIMAL(10,2) |

---

## 👀 Create View

A common view named **sales** points to the active table.

Initially:

```sql
sales → sales_blue
```

Applications always query:

```sql
SELECT * FROM sales;
```

This allows switching the underlying table without changing application code.

---

## 📥 Load Initial Data

PowerShell loads sample data into:

```text
sales_blue
```

Example:

| SaleID | Customer | Amount |
|--------|----------|---------|
|1|Alice|500|
|2|Bob|700|
|3|Charlie|650|

---

## 🚀 Blue-Green Deployment

New data is loaded into:

```text
sales_green
```

Example:

| SaleID | Customer | Amount |
|--------|----------|---------|
|1|Alice|550|
|2|Bob|780|
|3|Charlie|670|
|4|David|900|

---

## 🔄 Switch Deployment

The deployment switches the view:

```text
Before

sales
   │
   ▼
sales_blue
```

↓

```text
After

sales
   │
   ▼
sales_green
```

No application changes are required.

No downtime occurs.

---

## 🔙 Rollback

If deployment fails:

```text
sales
   │
   ▼
sales_green
```

↓

```text
sales
   │
   ▼
sales_blue
```

Rollback takes only a few seconds.

---

## ▶️ Sample PowerShell Commands

### List Databases

```powershell
Invoke-Sqlcmd `
    -ServerInstance ".\SQLEXPRESS" `
    -Query "SELECT name FROM sys.databases"
```

### Verify Tables

```powershell
Invoke-Sqlcmd `
    -ServerInstance ".\SQLEXPRESS" `
    -Database "BlueGreenDB" `
    -Query "SELECT name FROM sys.tables"
```

### Verify View

```powershell
Invoke-Sqlcmd `
    -ServerInstance ".\SQLEXPRESS" `
    -Database "BlueGreenDB" `
    -Query "SELECT name FROM sys.views"
```

---

## 📚 Key DevOps Concepts Learned

- Blue-Green Deployment
- Zero-Downtime Deployment
- Database View Switching
- Rollback Strategy
- PowerShell Automation
- SQL Server Administration
- Git Version Control
- Infrastructure Automation

---

## 💡 Future Enhancements

- Add deployment logging
- Add error handling (`try/catch`)
- Parameterize server and database names
- Automate deployment using GitHub Actions
- Generate deployment reports
- Add validation before switching the view

---

## 👨‍💻 Author

**Thajunnisa N**

Data Engineering | DevOps | Azure | SQL | PowerShell

GitHub: https://github.com/Thaju-nisa
