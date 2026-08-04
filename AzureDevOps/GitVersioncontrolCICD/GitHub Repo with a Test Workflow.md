# 🚀 GitHub Repository with a Test Workflow (CI using GitHub Actions)

## 📌 Project Overview

This project demonstrates how to implement **Continuous Integration (CI)** using **GitHub Actions** and **Pytest**.

The objective is to automate the testing process so that every code push and Pull Request is automatically validated. The project also simulates a real-world development workflow by intentionally introducing a failing test, observing the CI failure, fixing the issue, and verifying that the pipeline passes again.

---

## 🎯 Objectives

- Create a Python ETL transformation function.
- Write automated unit tests using **Pytest**.
- Configure **GitHub Actions** to execute tests automatically.
- Trigger CI on every **Push** and **Pull Request**.
- Simulate a failed build by introducing a broken test.
- Fix the issue and verify a successful CI pipeline.

---

## 🛠️ Technologies Used

- Python 3.14
- Pytest
- Git
- GitHub
- GitHub Actions
- Continuous Integration (CI)

---

## 📂 Project Structure

```text
Project1.3/
│
├── .github/
│   └── workflows/
│       └── ci.yml
│
├── etl.py
├── test_etl.py
├── .gitignore
└── README.md
```

---

## 🔄 Workflow Architecture

```text
Developer Changes Code
          │
          ▼
      Push to GitHub
          │
          ▼
 GitHub Actions Triggered
          │
          ▼
 Checkout Repository
          │
          ▼
 Setup Python
          │
          ▼
 Install Pytest
          │
          ▼
 Execute Unit Tests
          │
     ┌────┴────┐
     │         │
     ▼         ▼
 PASS ✅      FAIL ❌
     │         │
     ▼         ▼
 Merge      Fix Code
```

---

## 🐍 ETL Script

The ETL script contains a simple transformation function that doubles each value in a list.

### Example

**Input**

```python
[1, 2, 3]
```

**Output**

```python
[2, 4, 6]
```

---

## ✅ Unit Testing with Pytest

The project uses **Pytest** to verify that the transformation logic works correctly.

Example test:

```python
from etl import transform

def test_transform():
    assert transform([1,2,3]) == [2,4,6]
```

Run tests locally:

```bash
python -m pytest
```

Expected Output:

```text
1 passed
```

---

## ⚙️ GitHub Actions Workflow

The workflow automatically executes whenever code is pushed or a Pull Request is created.

### Workflow Features

- Checkout repository
- Setup Python
- Install Pytest
- Execute Unit Tests
- Display test results

Workflow file:

```text
.github/workflows/ci.yml
```

Example configuration:

```yaml
name: Python CI

on:
  push:
    branches:
      - main
  pull_request:

jobs:
  test:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v4

      - uses: actions/setup-python@v5
        with:
          python-version: '3.14'

      - name: Install pytest
        run: python -m pip install pytest

      - name: Run Tests
        run: python -m pytest
```

---

## 🔬 CI Failure Demonstration

To simulate a real development workflow:

1. Created a new feature branch.
2. Modified the unit test with an incorrect expected value.
3. Opened a Pull Request.
4. GitHub Actions automatically executed.
5. The workflow failed due to an AssertionError.
6. Corrected the test.
7. Pushed the fix.
8. GitHub Actions automatically reran and passed successfully.

This demonstrates how CI helps identify issues before code is merged.

---

## 🚀 Running the Project Locally

Clone the repository:

```bash
git clone https://github.com/Thaju-nisa/Project1.3.git
```

Navigate to the project:

```bash
cd Project1.3
```

Install dependencies:

```bash
python -m pip install pytest
```

Run the ETL script:

```bash
python etl.py
```

Run unit tests:

```bash
python -m pytest
```

---

## 📊 Project Outcome

✔ Successfully implemented Continuous Integration using GitHub Actions.

✔ Automated testing on every Push and Pull Request.

✔ Verified application behavior using Pytest.

✔ Simulated CI failure and recovery.

✔ Demonstrated a professional Git-based development workflow.

---

## 📚 Learning Outcomes

This project provided hands-on experience with:

- Git Fundamentals
- GitHub Repository Management
- Git Branching Strategy
- Pull Requests
- Unit Testing with Pytest
- GitHub Actions
- Continuous Integration (CI)
- Automated Build Validation
- Debugging Failed Pipelines
- Software Development Best Practices

---

## 🚀 Future Improvements

- Add code coverage reporting
- Integrate Flake8 or Ruff for linting
- Add Black for code formatting
- Test across multiple Python versions
- Add deployment after successful tests
- Include test badges in the README

---

## 👩‍💻 Author

**Thajunnisa N**

- GitHub: https://github.com/Thaju-nisa
- LinkedIn: https://www.linkedin.com/in/thajunnisa-n-637855ba/

---

⭐ If you found this project helpful, feel free to star the repository!
