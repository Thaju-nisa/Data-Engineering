Lab
Take the dbt CI from Session 3 and rewrite it as an Azure Pipeline.
In Github:

<img width="1895" height="869" alt="image" src="https://github.com/user-attachments/assets/c720e7fc-496b-408b-81c0-67cc8dbbed8b" />


In Azure Devops:
<img width="1908" height="849" alt="image" src="https://github.com/user-attachments/assets/4d6570be-f911-48cc-829c-0b1f82ad196b" />
<img width="1918" height="861" alt="image" src="https://github.com/user-attachments/assets/33812267-0f37-4c3f-8b2a-bce66cc74202" />






Note which concepts map 1:1 and which differ.
| GitHub Actions             | Azure DevOps                     |
| -------------------------- | -------------------------------- |
| `.github/workflows/ci.yml` | `azure-pipelines.yml`            |
| `on: push`                 | `trigger:`                       |
| `on: pull_request`         | `pr:`                            |
| `jobs:`                    | `jobs:`                          |
| `runs-on: ubuntu-latest`   | `pool: vmImage: ubuntu-latest`   |
| `actions/checkout`         | `checkout: self`                 |
| `setup-python`             | `UsePythonVersion@0`             |
| `secrets.MY_SECRET`        | Variable Group (`MY_SECRET`)     |
| GitHub Secret              | Azure Key Vault + Variable Group |
| Workflow                   | Pipeline                         |
