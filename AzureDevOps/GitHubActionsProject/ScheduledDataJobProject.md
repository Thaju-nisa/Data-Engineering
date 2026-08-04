
# 🚀 Scheduled Data Job using GitHub Actions

## 📌 Project Overview

This project demonstrates how to automate a recurring data pipeline using **Python** and **GitHub Actions**.

The workflow fetches data from a public REST API, stores the response as a JSON file, and uploads the generated file as a GitHub Actions artifact. It can be triggered manually or scheduled to run automatically using a cron expression.

---

## 🎯 Objective

- Fetch data from a public API.
- Save the API response as a JSON file.
- Automate execution using GitHub Actions.
- Schedule the workflow to run daily.
- Upload the generated JSON as a workflow artifact.

---

## 🛠️ Technologies Used

- Python 3.14
- Git
- GitHub
- GitHub Actions
- Requests Library
- JSON
- REST API

---

## 📂 Project Structure

```
Project2.2/
│
├── .github/
│   └── workflows/
│       └── scheduled-job.yml
│
├── fetch_data.py
├── output.json
├── .gitignore
└── README.md
```

---

## ⚙️ Workflow

```text
GitHub Actions Trigger
        │
        ▼
Checkout Repository
        │
        ▼
Setup Python
        │
        ▼
Install Dependencies
        │
        ▼
Execute Python Script
        │
        ▼
Fetch Data from Public API
        │
        ▼
Generate output.json
        │
        ▼
Upload Artifact
```

---

## 🌐 Public API Used

The project uses the free JSONPlaceholder API.

```
https://jsonplaceholder.typicode.com/posts
```

---

## 🐍 Python Script

The script performs the following tasks:

- Sends an HTTP GET request to the API.
- Parses the JSON response.
- Saves the response to `output.json`.
- Displays a success message after completion.

---

## 🔄 GitHub Actions Workflow

The workflow includes:

- Manual execution (`workflow_dispatch`)
- Scheduled execution (`cron`)
- Python environment setup
- Dependency installation
- Python script execution
- Artifact upload

Example schedule:

```yaml
schedule:
  - cron: '0 0 * * *'
```

This runs the workflow every day at **00:00 UTC**.

---

## 📦 Generated Artifact

After every successful workflow execution, GitHub uploads:

```
output.json
```

The artifact can be downloaded directly from the GitHub Actions run.

---

## ▶️ How to Run Locally

Clone the repository:

```bash
git clone https://github.com/Thaju-nisa/Project2.2.git
```

Navigate to the project:

```bash
cd Project2.2
```

Install dependencies:

```bash
python -m pip install requests
```

Run the script:

```bash
python fetch_data.py
```

---

## 📈 Learning Outcomes

Through this project, I gained hands-on experience with:

- REST API integration
- Python automation
- JSON data handling
- Git & GitHub
- GitHub Actions
- CI/CD concepts
- Scheduled workflows using Cron
- Workflow artifacts

---

## 📸 Workflow Execution

Successful GitHub Actions execution:

- ✅ Repository checkout
- ✅ Python setup
- ✅ Dependency installation
- ✅ API execution
- ✅ JSON generation
- ✅ Artifact upload

---

## 🚀 Future Enhancements

- Store JSON in Azure Blob Storage
- Load data into Azure SQL Database
- Push data to Azure Data Lake Storage (ADLS Gen2)
- Add logging and error handling
- Send workflow notifications
- Build dashboards using Power BI

---

## 👩‍💻 Author

**Thajunnisa N**

- GitHub: https://github.com/Thaju-nisa
- LinkedIn: https://www.linkedin.com/in/thajunnisa-n-637855ba/

---
⭐ If you found this project useful, feel free to star the repository!
