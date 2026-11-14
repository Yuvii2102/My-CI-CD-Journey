# GitHub Actions – Complete Practical Guide

In this practical session, I learned how to automate application workflows using GitHub Actions.

I started with a basic workflow and gradually added Python application execution, automated testing, matrix testing and Docker image building and pushing.

**GitHub Repository:** `My-CI-CD-Journey`

**Branch:** `main`

---

# Practical 1 – Creating My First GitHub Actions Workflow

## Objective

My first practical was to understand how GitHub Actions works and how to execute a basic workflow whenever code is pushed to GitHub.

## Step 1: Create the workflow directory

Inside the repository root, create this folder structure:

```text
.github/
    workflows/
```

GitHub Actions automatically detects workflow YAML files inside `.github/workflows/`.

## Step 2: Create the workflow file

Create:

```text
.github/workflows/first-actions.yml
```

## Step 3: Add the following code

```yaml
name: My First GitHub Actions Workflow

on:
  push:

jobs:
  first-job:
    runs-on: ubuntu-latest

    steps:
      - name: Print Welcome Message
        run: echo "Hello from GitHub Actions!"

      - name: Check Python Version
        run: python3 --version

      - name: Check Current Directory
        run: pwd
```

## Step 4: Understand the code

- `name` – Defines the workflow name.
- `on: push` – Runs the workflow whenever code is pushed.
- `jobs` – Contains the jobs to execute.
- `first-job` – Name of our job.
- `runs-on: ubuntu-latest` – Runs the job on a GitHub-hosted Ubuntu runner.
- `steps` – Contains the individual tasks.
- `run` – Executes a shell command.

## Step 5: Commit the changes

I created and committed the file through the GitHub website.

The equivalent Git commands are:

```bash
git add .
git commit -m "Add first GitHub Actions workflow"
git push origin main
```

## Step 6: Verify the workflow

1. Open the GitHub repository.
2. Click the Actions tab.
3. Open My First GitHub Actions Workflow.
4. Open the latest workflow run.
5. Select `first-job`.
6. Check the output of each step.

**Expected output:**

```text
Hello from GitHub Actions!
Python 3.12.3
/home/runner/work/My-CI-CD-Journey/My-CI-CD-Journey
```

The exact Python version and working directory can vary depending on the runner.

**Result:** My first GitHub Actions workflow executed successfully.

---

# Practical 2 – Creating and Running a Python Application

## Objective

In this practical, I created a simple Python application and used GitHub Actions to execute it automatically.

## Step 1: Create app.py

Inside the repository root, create:

```text
app.py
```

Add the following code:

```python
def add(a, b):
    return a + b

print("Result:", add(10, 20))
```

### Explanation

- `def add(a, b)` defines a function.
- `return a + b` adds two numbers.
- `print()` displays the result.

## Step 2: Create the workflow

Create:

```text
.github/workflows/python-ci.yml
```

Add the following code:

```yaml
name: Python CI Pipeline

on:
  push:

jobs:
  test:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout Repository
        uses: actions/checkout@v4

      - name: Setup Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.12'

      - name: Run Python Application
        run: python app.py
```

## Step 3: Understand the workflow

- `actions/checkout@v4` downloads the repository code into the runner.
- `actions/setup-python@v5` installs and configures Python.
- `python-version: '3.12'` selects Python 3.12.
- `python app.py` executes our Python application.

## Step 4: Commit and push

```bash
git add .
git commit -m "Add Python application workflow"
git push origin main
```

## Step 5: Verify

Open GitHub → Actions → Python CI Pipeline.

Check the `Run Python Application` step.

**Expected output:**

```text
Result: 30
```

**Result:** I successfully executed my Python application using GitHub Actions.

---

# Practical 3 – Automating Python Tests Using Pytest

## Objective

In this practical, I learned how to execute automated tests whenever code is pushed to GitHub.

Instead of manually testing the application, GitHub Actions installs the required dependency and runs the tests automatically.

## Step 1: Update app.py

Use this application code:

```python
def add(a, b):
    return a + b
```

## Step 2: Create test_app.py

Create:

```text
test_app.py
```

Add:

```python
from app import add

def test_add_positive_numbers():
    assert add(10, 20) == 30

def test_add_negative_numbers():
    assert add(-5, -5) == -10

def test_add_zero():
    assert add(10, 0) == 10
```

### Explanation

- `from app import add` imports the function from our application.
- `def test_...()` defines a test case.
- `assert` checks whether the actual result matches the expected result.

We created three test cases to verify our addition function.

## Step 3: Create requirements.txt

Create:

```text
requirements.txt
```

Add:

```text
pytest
```

This file contains the Python dependency required for running our tests.

## Step 4: Create or update python-ci.yml

File location:

```text
.github/workflows/python-ci.yml
```

Add:

```yaml
name: Python CI Pipeline

on:
  push:

jobs:
  test:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout Repository
        uses: actions/checkout@v4

      - name: Setup Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.12'

      - name: Install Dependencies
        run: pip install -r requirements.txt

      - name: Run Automated Tests
        run: pytest
```

## Step 5: Understand the new steps

**Install Dependencies**

```yaml
- name: Install Dependencies
  run: pip install -r requirements.txt
```

Installs the packages listed in requirements.txt.

**Run Automated Tests**

```yaml
- name: Run Automated Tests
  run: pytest
```

Executes all the test files discovered by pytest.

## Step 6: Run tests locally (optional)

To install pytest on a local Ubuntu system:

```bash
python3 -m pip install pytest
```

Run the tests:

```bash
python3 -m pytest test_app.py
```

## Step 7: Commit and push

```bash
git add .
git commit -m "Add Python application test cases"
git push origin main
```

## Step 8: Verify

Open GitHub → Actions → Python CI Pipeline.

Open the `Run Automated Tests` step.

**Expected output:**

```text
collected 3 items

test_app.py ...                 [100%]

3 passed
```

Our actual successful workflow showed:

```text
3 passed in 0.03s
```

**Result:** I successfully automated Python application testing using Pytest and GitHub Actions.

---

# Practical 4 – Matrix Testing with Multiple Python Versions

## Objective

In this practical, I learned how to test the same Python application using multiple Python versions through GitHub Actions Matrix Strategy.

Instead of creating separate jobs for every Python version, I used a matrix to execute the same job with different versions.

## Step 1: Update python-ci.yml

File location:

```text
.github/workflows/python-ci.yml
```

Replace the previous workflow with:

```yaml
name: Python CI Pipeline

on:
  push:

jobs:
  test:
    runs-on: ubuntu-latest

    strategy:
      matrix:
        python-version: ['3.10', '3.11', '3.12']

    steps:
      - name: Checkout Repository
        uses: actions/checkout@v4

      - name: Setup Python
        uses: actions/setup-python@v5
        with:
          python-version: ${{ matrix.python-version }}

      - name: Install Dependencies
        run: pip install -r requirements.txt

      - name: Run Automated Tests
        run: pytest
```

## Step 2: Understand Matrix Strategy

```yaml
strategy:
  matrix:
    python-version: ['3.10', '3.11', '3.12']
```

This tells GitHub Actions to execute the same job using three Python versions.

GitHub Actions creates three separate jobs:

- Python 3.10
- Python 3.11
- Python 3.12

The following expression selects the Python version for each job:

```yaml
python-version: ${{ matrix.python-version }}
```

## Step 3: Commit and push

```bash
git add .
git commit -m "Add Python matrix testing"
git push origin main
```

## Step 4: Verify

Open GitHub → Actions → Python CI Pipeline.

Open the latest workflow run.

You should see three jobs:

```text
test (3.10)
test (3.11)
test (3.12)
```

All three jobs should complete successfully.

**Our actual practical result:**

- Python 3.10 – Passed
- Python 3.11 – Passed
- Python 3.12 – Passed

All three versions successfully executed the automated tests.

**Result:** I successfully implemented matrix testing using multiple Python versions.

---

# Practical 5 – Building and Pushing a Docker Image Using GitHub Actions

## Objective

In this practical, I extended my existing Python CI pipeline to build a Docker image and push it automatically to Docker Hub.

First, GitHub Actions runs the Python tests. If the tests pass, the Docker build and push job executes.

## Step 1: Create a Dockerfile

Inside the repository root, create:

```text
Dockerfile
```

Add:

```dockerfile
FROM python:3.12-slim

WORKDIR /app

COPY app.py .

CMD ["python", "app.py"]
```

## Step 2: Understand the Dockerfile

- `FROM python:3.12-slim` – Uses a lightweight Python 3.12 base image.
- `WORKDIR /app` – Sets `/app` as the working directory inside the container.
- `COPY app.py .` – Copies the Python application into the container.
- `CMD` – Runs the Python application when the container starts.

## Step 3: Create a Docker Hub repository

1. Log in to Docker Hub.
2. Open Repositories.
3. Click Create Repository.
4. Repository name: `my-python-app`.
5. Select Public.
6. Add this description:

   A Python application built and tested using GitHub Actions. The workflow automatically runs tests across multiple Python versions, builds a Docker image and pushes it to Docker Hub.

7. Create the repository.

Our Docker Hub repository:

```text
yuvi2102/my-python-app
```

## Step 4: Generate a Docker Hub Access Token

1. Open Docker Hub account settings.
2. Select Personal access tokens.
3. Create a new token.
4. Name it `github-actions`.
5. Give it Read & Write permissions.
6. Generate and copy the token.

The token is used instead of the normal Docker Hub password.

Keep it private.

## Step 5: Add GitHub Repository Secrets

Open:

```text
GitHub Repository
    → Settings
    → Secrets and variables
    → Actions
```

Create these two repository secrets:

| Secret name | Value |
|---|---|
| `DOCKER_USERNAME` | `yuvi2102` |
| `DOCKER_PASSWORD` | Docker Hub access token |

These secrets allow GitHub Actions to authenticate with Docker Hub without exposing credentials in the workflow file.

## Step 6: Update python-ci.yml

Replace the previous workflow with the following final version:

```yaml
name: Python CI Pipeline

on:
  push:

jobs:
  test:
    runs-on: ubuntu-latest

    strategy:
      matrix:
        python-version: ['3.10', '3.11', '3.12']

    steps:
      - name: Checkout Repository
        uses: actions/checkout@v4

      - name: Setup Python
        uses: actions/setup-python@v5
        with:
          python-version: ${{ matrix.python-version }}

      - name: Install Dependencies
        run: pip install -r requirements.txt

      - name: Run Automated Tests
        run: pytest

  docker-build:
    runs-on: ubuntu-latest
    needs: test

    steps:
      - name: Checkout Repository
        uses: actions/checkout@v4

      - name: Setup Docker Buildx
        uses: docker/setup-buildx-action@v3

      - name: Login to Docker Hub
        uses: docker/login-action@v3
        with:
          username: ${{ secrets.DOCKER_USERNAME }}
          password: ${{ secrets.DOCKER_PASSWORD }}

      - name: Build and Push Docker Image
        uses: docker/build-push-action@v6
        with:
          context: .
          push: true
          tags: yuvi2102/my-python-app:latest
```

## Step 7: Understand the Docker workflow

**1. needs: test**

```yaml
needs: test
```

The Docker job waits for the Python testing job to finish successfully.

**2. Setup Docker Buildx**

```yaml
uses: docker/setup-buildx-action@v3
```

Sets up Docker Buildx for building Docker images.

**3. Login to Docker Hub**

```yaml
uses: docker/login-action@v3
```

Authenticates with Docker Hub using our GitHub Secrets.

**4. Build and Push Docker Image**

```yaml
uses: docker/build-push-action@v6
```

Builds the Docker image and pushes it to Docker Hub.

**5. Image tag**

```yaml
tags: yuvi2102/my-python-app:latest
```

Defines the Docker image name and tag.

## Step 8: Commit and push

```bash
git add .
git commit -m "Add Docker Hub login and image push"
git push origin main
```

If you are updating an existing workflow, use a suitable commit message describing the change.

## Step 9: Verify GitHub Actions

Open:

```text
GitHub Repository → Actions → Python CI Pipeline
```

The workflow should show:

```text
test (3.10)       Success
test (3.11)       Success
test (3.12)       Success
docker-build      Success
```

## Step 10: Verify Docker Hub

Open:

```text
https://hub.docker.com/r/yuvi2102/my-python-app
```

Go to the Tags section.

You should see:

```text
latest
```

Our actual image was pushed successfully with:

- Repository: `yuvi2102/my-python-app`
- Tag: `latest`
- Platform: `linux/amd64`
- Image size: approximately 41.26 MB

**Result:** I successfully automated Docker image building and pushing using GitHub Actions.

---

# Complete Project Structure

After completing the practicals, my repository structure looks like this:

```text
My-CI-CD-Journey/
│
├── .github/
│   └── workflows/
│       ├── first-actions.yml
│       └── python-ci.yml
│
├── app.py
├── test_app.py
├── requirements.txt
├── Dockerfile
│
└── 10 - GitHub Actions Theory Concepts/
    └── README.md
```

---

# Commands Used – Quick Revision

These are the main commands used or documented for repeating the practicals.

## 1. Check Python version

```bash
python3 --version
```

## 2. Run the Python application

```bash
python3 app.py
```

## 3. Install pytest

```bash
python3 -m pip install pytest
```

## 4. Run automated tests

```bash
python3 -m pytest test_app.py
```

## 5. Install dependencies from requirements.txt

```bash
pip install -r requirements.txt
```

## 6. Run pytest

```bash
pytest
```

## 7. Check current directory

```bash
pwd
```

## 8. Git commands

```bash
git status
git add .
git commit -m "Your commit message"
git push origin main
```

---

# Complete Workflow Understanding

```text
Developer pushes code to GitHub
             |
             v
      GitHub Actions
             |
             v
      Python CI Pipeline
             |
             v
       Matrix Testing
       /      |      \
    3.10     3.11     3.12
       \      |      /
             |
             v
       All Tests Pass
             |
             v
       Docker Buildx
             |
             v
      Docker Hub Login
             |
             v
      Build Docker Image
             |
             v
       Push Docker Image
             |
             v
          Docker Hub
```

# Final Learning

Through these practicals, I learned:

1. How to create a GitHub Actions workflow.
2. How to use GitHub-hosted Ubuntu runners.
3. How to checkout repository code.
4. How to configure Python versions.
5. How to execute Python applications.
6. How to install dependencies using requirements.txt.
7. How to automate tests using Pytest.
8. How to use Matrix Strategy for multiple Python versions.
9. How to create a Dockerfile.
10. How to configure Docker Hub authentication.
11. How to store sensitive credentials using GitHub Secrets.
12. How to build and push Docker images automatically.

**My main learning:** GitHub Actions helps automate the complete process from checking out source code and running tests to building and pushing Docker images. This reduces manual work and makes the CI process easier to repeat.
