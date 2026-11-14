# GitHub Actions – Self-Hosted Runners

## 1. What is a Runner?

A runner is a machine that executes the jobs inside a GitHub Actions workflow.

Whenever we push code to GitHub, our workflow gets triggered. GitHub Actions assigns the job to a runner, and that runner executes the commands mentioned in our YAML file.

For example:

```yaml
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - name: Print Message
        run: echo "Hello from GitHub Actions!"
```

Here, `ubuntu-latest` tells GitHub Actions to use an Ubuntu runner to execute the job.

There are two types of runners:

1. GitHub-hosted runners
2. Self-hosted runners

## 2. GitHub-Hosted Runners

GitHub-hosted runners are machines provided and managed by GitHub.

We don't need to create a server or install the runner software ourselves. GitHub provides the machine whenever our workflow needs to run.

### How it works

1. We push code to GitHub.
2. GitHub Actions triggers the workflow.
3. GitHub provides a runner machine.
4. The runner executes our workflow steps.
5. The job finishes and the hosted machine is managed by GitHub.

Example:

```yaml
jobs:
  build:
    runs-on: ubuntu-latest
```

In this example, GitHub provides an Ubuntu machine to execute our job.

### Key points

- GitHub provides the machine.
- No manual runner installation is required.
- GitHub manages the runner environment.
- We have limited control over the machine.
- Usage and billing depend on our GitHub plan.

## 3. Self-Hosted Runners

A self-hosted runner is a machine that we provide and manage ourselves to execute GitHub Actions workflows.

Instead of using a machine provided by GitHub, we can use our own machine.

It can be:

- An AWS EC2 instance
- A local computer
- A physical server
- A virtual machine

For our practical, we are going to use an Ubuntu EC2 instance as our self-hosted runner.

### How it works

1. We create or use an Ubuntu EC2 instance.
2. We download the GitHub Actions runner software.
3. We configure the runner with our GitHub repository.
4. We start the runner on our EC2 instance.
5. We update our workflow YAML file to use the self-hosted runner.
6. When we push code, GitHub Actions sends the job to our EC2 instance.
7. Our EC2 instance executes the workflow.

Example:

```yaml
jobs:
  build:
    runs-on: self-hosted
```

Here, `self-hosted` tells GitHub Actions to use an available self-hosted runner instead of a GitHub-hosted runner.

### Key points

- We provide the machine.
- We install and configure the runner ourselves.
- We manage the operating system and installed software.
- We have more control over the environment.
- We are responsible for maintenance and security.
- We pay for the infrastructure we use, such as our EC2 instance.

## 4. Difference Between GitHub-Hosted and Self-Hosted Runners

| Feature | GitHub-Hosted Runner | Self-Hosted Runner |
|---|---|---|
| Machine | Provided by GitHub | Provided by us |
| Setup | No manual installation | Manual installation required |
| Maintenance | Managed by GitHub | Managed by us |
| Control | Limited control | More control |
| Software | GitHub provides the runner environment | We install required software |
| Infrastructure | GitHub's infrastructure | Our own infrastructure |
| Cost | Depends on GitHub plan and usage | Infrastructure cost is ours |

## 5. Understanding the Architecture

### GitHub-Hosted Runner

```text
Developer
    |
    | Push Code
    v
GitHub Repository
    |
    v
GitHub Actions Workflow
    |
    v
GitHub-Hosted Runner
    |
    v
Execute Workflow Steps
    |
    v
Job Completed
```

### Self-Hosted Runner

```text
Developer
    |
    | Push Code
    v
GitHub Repository
    |
    v
GitHub Actions Workflow
    |
    v
Self-Hosted Runner
    |
    v
Our AWS EC2 Instance
    |
    v
Execute Workflow Steps
    |
    v
Job Completed
```

## 6. Why Do We Use Self-Hosted Runners?

Self-hosted runners are useful when we need more control over the machine that executes our workflows.

Some reasons are:

- We need specific software or tools installed.
- We need a customized operating system environment.
- We want to use our own infrastructure.
- We need access to internal systems or private networks.
- We want to reuse a machine that we manage.

However, we are responsible for keeping our runner secure, updated and available.

## 7. Our Practical – Setting Up a Self-Hosted Runner on AWS EC2

In this practical, I am going to configure an Ubuntu EC2 instance as a self-hosted runner for my GitHub repository.

### Tools and Technologies

- GitHub Actions
- AWS EC2
- Ubuntu Linux
- GitHub Self-Hosted Runner

### Practical Steps

1. Create or use an Ubuntu EC2 instance.
2. Open the GitHub repository.
3. Navigate to Settings → Actions → Runners.
4. Click New self-hosted runner.
5. Select Linux as the operating system.
6. Follow GitHub's instructions to download and configure the runner.
7. Start the runner on the EC2 instance.
8. Update the GitHub Actions workflow to use `runs-on: self-hosted`.
9. Push changes to GitHub.
10. Verify that the workflow executes on our EC2 instance.

### Expected Result

Our GitHub Actions workflow should execute on our own AWS EC2 instance instead of a GitHub-hosted machine.

## 8. Official Documentation

These are the official documentation links I can refer to while learning and performing this practical.

1. [GitHub Actions Documentation](https://docs.github.com/en/actions)
2. [GitHub-Hosted Runners](https://docs.github.com/en/actions/using-github-hosted-runners/about-github-hosted-runners)
3. [Self-Hosted Runners](https://docs.github.com/en/actions/hosting-your-own-runners/about-self-hosted-runners)
4. [Adding a Self-Hosted Runner](https://docs.github.com/en/actions/how-tos/manage-runners/self-hosted-runners/add-runners)

## 9. What I Learned

I understood that a runner is the machine responsible for executing GitHub Actions workflow jobs.

GitHub-hosted runners are provided and managed by GitHub, whereas self-hosted runners use our own infrastructure.

For this practical, I will configure an AWS EC2 Ubuntu instance as a self-hosted runner and execute a GitHub Actions workflow on it.
