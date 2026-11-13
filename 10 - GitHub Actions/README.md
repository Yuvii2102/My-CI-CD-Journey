# GitHub Actions – Theory and Concepts

## 1. Introduction to GitHub Actions

GitHub Actions is a CI/CD automation platform provided by GitHub.

It helps us automate different software development tasks such as:

- Building applications.
- Running automated tests.
- Checking code quality.
- Building Docker images.
- Pushing images to container registries.
- Deploying applications.

Whenever we push code to GitHub, GitHub Actions can automatically execute the tasks defined in our workflow.

**In simple words:** GitHub Actions helps us automate our development and deployment process instead of performing every task manually.

## 2. How GitHub Actions Works

GitHub Actions uses workflows to automate our development tasks.

The basic flow is:

1. A developer pushes code to GitHub.
2. GitHub Actions detects the change.
3. The configured workflow starts.
4. The application is built.
5. Automated tests are executed.
6. If everything is successful, the workflow can continue with Docker image creation and deployment.

This helps us automate the CI/CD process.

## 3. What is a Workflow?

A workflow is an automated process that contains instructions for GitHub Actions.

We write workflows using YAML files.

These files are stored inside the `.github/workflows/` directory of our repository.

**Folder structure:**

```text
My-Repository/
│
└── .github/
    │
    └── workflows/
        │
        └── first-workflow.yml
```

**In simple words:** A workflow tells GitHub Actions what tasks to perform and when to perform them.

## 4. Understanding the Workflow YAML File

A GitHub Actions workflow contains different keywords. Each keyword has a specific purpose.

### A. name

Defines the name of the workflow.

```yaml
name: Python CI Pipeline
```

### B. on

Defines when the workflow should execute.

```yaml
on:
  push:
```

Here, the workflow runs whenever code is pushed to the repository.

Some commonly used events are:

- `push` – Runs when code is pushed.
- `pull_request` – Runs when a pull request event occurs.
- `workflow_dispatch` – Allows us to manually trigger a workflow.

### C. jobs

A workflow contains one or more jobs.

```yaml
jobs:
  build:
```

Here, `build` is the name of the job.

### D. runs-on

Specifies which machine should execute the job.

```yaml
runs-on: ubuntu-latest
```

Here, GitHub Actions uses a GitHub-hosted Ubuntu Runner.

### E. steps

A job contains one or more steps. Each step performs a particular task.

```yaml
steps:
  - name: Print Message
    run: echo "Hello from GitHub Actions"
```

### F. uses

The `uses` keyword allows us to use an existing GitHub Action.

For example:

```yaml
- name: Checkout Repository
  uses: actions/checkout@v4
```

This action checks out our repository code into the Runner's workspace.

### G. run

The `run` keyword executes commands directly on the Runner.

For example:

```yaml
- name: Install Dependencies
  run: pip install pytest
```

This executes the shell command on the Runner.

### Quick Revision

| Keyword | Purpose |
|---|---|
| `name` | Defines the workflow name |
| `on` | Defines the workflow trigger |
| `jobs` | Defines the jobs |
| `runs-on` | Selects the Runner |
| `steps` | Defines individual tasks |
| `uses` | Uses an existing GitHub Action |
| `run` | Executes commands |

## 5. What is Checkout?

When a workflow starts, the Runner needs access to our application's source code.

For this, we use the checkout action.

```yaml
- name: Checkout Repository
  uses: actions/checkout@v4
```

This action checks out our GitHub repository into the Runner's workspace.

For example, our repository might contain:

```text
My-Python-App/
│
├── app.py
├── test_app.py
└── requirements.txt
```

After checkout, these files are available to the workflow.

**In simple words:** Checkout makes our GitHub repository code available to the Runner so that it can build and test our application.

## 6. What is Setup Python?

If we are building a Python application, we need Python available on the Runner.

We can use the setup-python action.

```yaml
- name: Setup Python
  uses: actions/setup-python@v5
  with:
    python-version: '3.9'
```

This configures the required Python version for our workflow.

We can also install the project dependencies:

```yaml
- name: Install Dependencies
  run: pip install -r requirements.txt
```

**In simple words:** Setup Python makes the required Python version available so that we can execute our Python application and tests.

## 7. What is Automated Testing?

Automated testing means running tests automatically to check whether our application works correctly.

For example, suppose we have a Python application that performs addition.

**app.py**

```python
def add(a, b):
    return a + b
```

**test_app.py**

```python
from app import add

def test_add():
    assert add(10, 20) == 30
```

We can execute the test using:

```bash
pytest
```

In GitHub Actions, we can add:

```yaml
- name: Run Tests
  run: pytest
```

Whenever we push code, GitHub Actions can automatically execute these tests.

If the tests pass, the workflow continues. If they fail, the job reports failure.

**In simple words:** Automated testing helps us identify problems in our application before deployment.

## 8. What is Matrix Testing?

Matrix testing allows us to execute the same job using multiple configurations.

For example, suppose we want to check whether our Python application works with Python 3.8 and Python 3.9.

Instead of creating separate jobs manually, we can use a matrix.

```yaml
strategy:
  matrix:
    python-version: ['3.8', '3.9']
```

We can use the selected version in our setup-python step:

```yaml
- name: Setup Python
  uses: actions/setup-python@v5
  with:
    python-version: ${{ matrix.python-version }}
```

GitHub Actions creates separate job runs for each Python version.

**Example:**

| Job | Python Version |
|---|---|
| Job 1 | Python 3.8 |
| Job 2 | Python 3.9 |

Both jobs execute the same application tests.

**In simple words:** Matrix testing helps us check whether our application works with different versions or configurations.

## 9. Why Do We Use Docker in CI/CD?

Docker and GitHub Actions have different responsibilities.

- GitHub Actions automates the CI/CD pipeline.
- Docker packages our application and its dependencies into a container image.

Let's understand this with an example.

Suppose we develop a Python application and successfully build and test it using GitHub Actions.

Now we want to deploy this application on an AWS EC2 instance.

Without Docker, we may need to install Python, libraries and other dependencies separately on the server. We must also make sure that the environment is configured correctly.

With Docker, we can package our application and its required dependencies into an image.

We can then use that same image in different environments that support Docker.

### Why Docker is useful

1. **Consistency:** Helps our application run in a consistent environment.
2. **Portability:** Allows us to run the same image in different environments.
3. **Dependency management:** Packages the required application dependencies.
4. **Easy deployment:** We can distribute and deploy the same image.
5. **Isolation:** Containers provide isolated application environments.

**In simple words:** Docker helps us package our application so that we can deploy it without manually setting up all its dependencies on every server.

## 10. Dockerfile, Docker Image and Docker Container

These three concepts are important when working with Docker.

### Dockerfile

A Dockerfile contains instructions to build a Docker image.

Example:

```dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

CMD ["python", "app.py"]
```

### Docker Image

A Docker image is a packaged version of our application along with its required dependencies.

### Docker Container

A Docker container is a running instance of a Docker image.

**Quick Revision:**

| Component | Purpose |
|---|---|
| Dockerfile | Contains instructions to build an image |
| Docker Image | Contains the packaged application |
| Docker Container | Runs the application |

## 11. How GitHub Actions and Docker Work Together

GitHub Actions can automate the entire Docker build and deployment process.

The flow is:

1. A developer pushes code to GitHub.
2. GitHub Actions starts the workflow.
3. The Runner checks out the repository.
4. The application is built and tested.
5. Docker builds an image using the Dockerfile.
6. The image is pushed to a container registry.
7. The image is deployed to a server or Kubernetes.

### What is a Container Registry?

A container registry is a place where we store and manage Docker images.

Some commonly used registries are:

- Docker Hub.
- Amazon Elastic Container Registry (ECR).
- GitHub Container Registry (GHCR).

**In simple words:** GitHub Actions automates the process, while Docker packages our application. The registry stores the image so that we can use it during deployment.

## 12. GitHub Secrets and Variables

Sometimes our workflows require sensitive information such as:

- Docker Hub username.
- Docker Hub access token.
- AWS credentials.
- API tokens.

We should not directly write these values inside our workflow files.

GitHub provides Secrets and Variables to store this information.

We can configure them under:

**Repository → Settings → Secrets and variables → Actions**

### Secrets

Secrets are used to store sensitive information such as passwords, access tokens and credentials.

Example:

```yaml
${{ secrets.DOCKER_USERNAME }}
${{ secrets.DOCKER_PASSWORD }}
```

### Variables

Variables are used to store configuration values that are not sensitive.

**In simple words:** We use GitHub Secrets to protect sensitive information and avoid exposing credentials in our workflow files.

## 13. GitHub Actions vs Jenkins

My teacher also compared GitHub Actions with Jenkins.

Both tools help us automate CI/CD pipelines, but they have different architectures and configurations.

| GitHub Actions | Jenkins |
|---|---|
| CI/CD platform integrated with GitHub | Open-source automation server |
| Uses YAML workflow files | Uses Groovy-based Jenkinsfiles |
| Uses Runners | Uses Agents or Worker Nodes |
| Provides GitHub-hosted Runners | We generally manage Jenkins infrastructure and agents |
| Uses GitHub Actions for integrations | Uses Jenkins plugins |
| Workflows are stored in `.github/workflows/` | Pipeline code is commonly stored in a Jenkinsfile |

### When Can We Use GitHub Actions?

GitHub Actions is useful when our source code and development workflow are already managed in GitHub.

It is especially convenient for public open-source projects because GitHub provides hosted Runner usage under its applicable free usage policies.

### When Can We Use Jenkins?

Jenkins is useful when we need extensive customization, a large plugin ecosystem, complex automation and more control over our CI/CD infrastructure.

**My understanding:** Both tools help us automate CI/CD. The choice depends on our project requirements, infrastructure, security and integrations.

## 14. Complete GitHub Actions CI/CD Flow

Let's connect all the concepts we learned.

Suppose we are developing a Python application.

1. A developer pushes code to GitHub.
2. GitHub Actions detects the push event.
3. The workflow starts.
4. The Runner checks out the repository.
5. Python is configured.
6. Dependencies are installed.
7. Automated tests are executed.
8. Docker builds an image of the application.
9. The image is pushed to a container registry.
10. The application is deployed to the target environment.

This is how we can automate the complete CI/CD process using GitHub Actions and Docker.

## 15. Important Interview Questions

**Q1. What is GitHub Actions?**

GitHub Actions is a CI/CD automation platform provided by GitHub. It helps us automate building, testing and deploying applications.

**Q2. What is a workflow?**

A workflow is an automated process defined using a YAML file inside the `.github/workflows/` directory.

**Q3. What is a Runner?**

A Runner is a machine that executes GitHub Actions jobs.

**Q4. What is the purpose of actions/checkout?**

It checks out the repository code into the Runner's workspace.

**Q5. What is the difference between uses and run?**

`uses` allows us to use an existing GitHub Action, whereas `run` executes shell commands.

**Q6. What is matrix testing?**

Matrix testing executes the same job using multiple configurations, such as different Python versions.

**Q7. Why do we use Docker with GitHub Actions?**

GitHub Actions automates Docker operations, while Docker packages our application and its dependencies into an image for consistent deployment.

**Q8. What is the difference between a Docker image and a container?**

A Docker image is the packaged application template, whereas a container is a running instance of that image.

**Q9. Why do we use GitHub Secrets?**

We use GitHub Secrets to securely store sensitive information such as passwords, tokens and credentials.

**Q10. What is the difference between Jenkins and GitHub Actions?**

Jenkins is an automation server that uses agents and plugins. GitHub Actions is a CI/CD platform integrated with GitHub that uses workflows and runners.

## 16. Final Understanding

From this GitHub Actions session, I learned:

- What GitHub Actions is and how it automates CI/CD.
- How workflows and YAML files work.
- The purpose of triggers, jobs and steps.
- How checkout and setup-python work.
- How automated testing works using pytest.
- How matrix testing works.
- Why Docker is used in CI/CD.
- How GitHub Actions and Docker work together.
- How Docker images are stored in container registries.
- How GitHub Secrets protect sensitive information.
- The differences between GitHub Actions and Jenkins.

### Key Takeaway

I learned how GitHub Actions automates our CI/CD workflow and how Docker helps us package applications into images for consistent deployment. I also understood how both tools work together to automate the application delivery process.
