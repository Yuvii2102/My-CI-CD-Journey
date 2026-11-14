---

# Official Documentation & References

I used the following official documentation to understand the commands, configure the workflows and complete these practicals.

## 1. GitHub Actions – Basic Workflow

| What I used | Official documentation |
|---|---|
| Workflow YAML syntax (`name`, `on`, `jobs`, `steps`) | [GitHub Actions Workflow Syntax](https://docs.github.com/en/actions/writing-workflows/workflow-syntax-for-github-actions) |
| Push event trigger | [Events that Trigger Workflows](https://docs.github.com/en/actions/writing-workflows/choosing-when-your-workflow-runs/events-that-trigger-workflows) |
| Ubuntu hosted runner (`ubuntu-latest`) | [GitHub-hosted Runners](https://docs.github.com/en/actions/using-github-hosted-runners/about-github-hosted-runners) |
| Running shell commands using `run` | [Workflow Syntax – Steps](https://docs.github.com/en/actions/writing-workflows/workflow-syntax-for-github-actions#jobsjob_idsteps) |

## 2. Checking Out Code and Setting Up Python

| What I used | Official documentation |
|---|---|
| `actions/checkout@v4` | [Checkout Action](https://github.com/actions/checkout) |
| `actions/setup-python@v5` | [Setup Python Action](https://github.com/actions/setup-python) |
| Selecting Python versions | [Setup Python – Usage](https://github.com/actions/setup-python#usage) |
| Python installation and usage | [Official Python Documentation](https://docs.python.org/3/) |

## 3. Python Application and Pytest

| What I used | Official documentation |
|---|---|
| Python functions and return statements | [Python Tutorial – Defining Functions](https://docs.python.org/3/tutorial/controlflow.html#defining-functions) |
| Installing Python packages using pip | [Pip Documentation](https://pip.pypa.io/en/stable/) |
| `requirements.txt` | [Requirements File Format](https://pip.pypa.io/en/stable/reference/requirements-file-format/) |
| Installing and using pytest | [Pytest – Getting Started](https://pytest.org/en/stable/getting-started.html) |
| Running tests using `pytest` | [Pytest – How to Invoke](https://pytest.org/en/stable/how-to/usage.html) |
| Writing test cases using `assert` | [Pytest – Assertions](https://docs.pytest.org/en/stable/how-to/assert.html) |

## 4. Matrix Testing

| What I used | Official documentation |
|---|---|
| `strategy` | [GitHub Actions – Workflow Syntax](https://docs.github.com/en/actions/writing-workflows/workflow-syntax-for-github-actions#jobsjob_idstrategy) |
| `matrix` | [GitHub Actions – Running Variations of Jobs](https://docs.github.com/en/actions/how-tos/writing-workflows/choosing-what-your-workflow-does/running-variations-of-jobs-in-a-workflow) |
| `${{ matrix.python-version }}` | [GitHub Actions – Matrix Context](https://docs.github.com/en/actions/reference/workflows-and-actions/contexts#matrix-context) |

## 5. Dockerfile

| What I used | Official documentation |
|---|---|
| `FROM` | [Dockerfile Reference](https://docs.docker.com/reference/dockerfile/#from) |
| `WORKDIR` | [Dockerfile Reference](https://docs.docker.com/reference/dockerfile/#workdir) |
| `COPY` | [Dockerfile Reference](https://docs.docker.com/reference/dockerfile/#copy) |
| `CMD` | [Dockerfile Reference](https://docs.docker.com/reference/dockerfile/#cmd) |
| Building Docker images | [Docker Build Documentation](https://docs.docker.com/build/) |

## 6. Docker Hub Authentication and GitHub Secrets

| What I used | Official documentation |
|---|---|
| Creating Docker Hub access tokens | [Docker Hub – Access Tokens](https://docs.docker.com/security/access-tokens/) |
| Storing credentials in GitHub | [GitHub – Using Secrets in Actions](https://docs.github.com/en/actions/security-for-github-actions/security-guides/using-secrets-in-github-actions) |
| Repository secrets | [GitHub – Secrets and Variables](https://docs.github.com/en/actions/concepts/security/secrets) |
| Docker login action | [Docker Login Action](https://github.com/docker/login-action) |

## 7. Docker Build and Push Actions

| What I used | Official documentation |
|---|---|
| `docker/setup-buildx-action@v3` | [Docker Setup Buildx Action](https://github.com/docker/setup-buildx-action) |
| `docker/build-push-action@v6` | [Docker Build and Push Action](https://github.com/docker/build-push-action) |
| `context` | [Build and Push Action – Inputs](https://github.com/docker/build-push-action#inputs) |
| `push: true` | [Build and Push Action – Inputs](https://github.com/docker/build-push-action#inputs) |
| Docker image tags | [Docker Image Tags](https://docs.docker.com/reference/cli/docker/image/tag/) |
| Pushing images to Docker Hub | [Docker Hub – Push Images](https://docs.docker.com/docker-hub/repos/manage/hub-images/push/) |

## 8. Git Commands

| Command | Official documentation |
|---|---|
| `git status` | [Git Status](https://git-scm.com/docs/git-status) |
| `git add .` | [Git Add](https://git-scm.com/docs/git-add) |
| `git commit -m` | [Git Commit](https://git-scm.com/docs/git-commit) |
| `git push origin main` | [Git Push](https://git-scm.com/docs/git-push) |

---

**Note:** These links are the official references I can use to understand and revise the concepts. The practical code above is the version I used in my project, with the action versions we selected during our hands-on session.
