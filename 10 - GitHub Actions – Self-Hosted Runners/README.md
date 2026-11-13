# GitHub Actions – Self-Hosted Runners

## 1. Introduction to GitHub Actions

GitHub Actions is a CI/CD automation platform provided by GitHub.

It helps us automate tasks such as:

- Building applications.
- Running tests.
- Checking code quality.
- Deploying applications.
- Automating development workflows.

Whenever we push code to a GitHub repository, GitHub Actions can automatically execute the tasks we have defined in a workflow file.

For example:

1. A developer pushes code to GitHub.
2. GitHub Actions detects the change.
3. It starts the configured workflow.
4. The application is built and tested.
5. The workflow reports whether the execution was successful or failed.

**In simple words:** GitHub Actions automates our software development tasks whenever a specific event happens in a GitHub repository.

## 2. What is a Runner?

A Runner is a machine that executes the jobs defined in a GitHub Actions workflow.

It provides the environment where our commands and application build processes run.

For example, when we create a workflow to build a Python application, the Runner executes the Python commands and tests.

In Jenkins, we commonly call this machine an **Agent** or **Worker Node**.

In GitHub Actions, we call it a **Runner**.

There are two types of Runners:

1. GitHub-Hosted Runners
2. Self-Hosted Runners

## 3. GitHub-Hosted Runners

A GitHub-Hosted Runner is a virtual machine provided and managed by GitHub to execute workflow jobs.

We don't need to create or maintain our own server. GitHub provides the machine whenever a workflow needs to run.

For example:

```yaml
jobs:
  build:
    runs-on: ubuntu-latest
```

Here, `ubuntu-latest` tells GitHub Actions to use a GitHub-hosted Ubuntu Runner.

### How it works

1. We push code to GitHub.
2. GitHub Actions starts the workflow.
3. GitHub provides a temporary Runner.
4. The Runner executes the required jobs.
5. After the job finishes, the Runner is decommissioned.

### Important points

- GitHub manages the Runner infrastructure.
- We don't need to install or maintain the server.
- Different operating system environments are available.
- Public repositories can use GitHub-hosted standard runners without charge, subject to GitHub's applicable usage policies.
- We don't have ownership or direct control over the underlying machine.

**In simple words:** GitHub gives us a machine to execute our pipeline. We use it and GitHub manages the infrastructure.

## 4. Self-Hosted Runners

A Self-Hosted Runner is a machine that we create, configure and manage ourselves to execute GitHub Actions workflows.

We can use:

- AWS EC2 instances.
- Virtual machines.
- Physical servers.
- Docker-based environments.

For our practical, we will use an Ubuntu EC2 instance on AWS.

### How it works

1. We create an EC2 instance.
2. We install and configure the GitHub Actions Runner.
3. We register the Runner with our GitHub repository.
4. GitHub Actions identifies the registered Runner.
5. We configure our workflow to use the self-hosted Runner.
6. The Runner executes the workflow jobs.

### Important points

- We have control over the machine.
- We can install the software and dependencies we need.
- We can choose the machine's CPU and RAM.
- We are responsible for maintaining and securing the machine.
- The machine can be reused for multiple workflow jobs.

**In simple words:** Instead of using a machine provided by GitHub, we use our own server to execute GitHub Actions workflows.

## 5. Difference Between GitHub-Hosted and Self-Hosted Runners

| GitHub-Hosted Runner | Self-Hosted Runner |
|---|---|
| Managed by GitHub | Managed by us |
| GitHub provides the machine | We provide the machine |
| No server setup required | We must configure the server |
| Temporary environment for jobs | Machine can be reused |
| Limited to available configurations | We can customize the environment |
| Less infrastructure maintenance | We handle maintenance and security |

## 6. Why Do We Use Self-Hosted Runners?

If GitHub already provides Runners, why should we create our own?

There are three important reasons.

### 1. Private Projects and Security

Some companies work with private repositories where the source code is confidential.

For sensitive applications, companies may prefer to execute workflows on infrastructure that they control.

For example, a banking application may have strict security requirements. The company may want its build environment to remain within its own infrastructure.

### 2. Resource Requirements

Sometimes the GitHub-hosted Runner configurations may not meet our application requirements.

For example:

- Our application needs more RAM.
- Our tests require higher CPU resources.
- We need a specific machine configuration.

In these situations, we can create a self-hosted Runner with the required resources.

### 3. Custom Software and Dependencies

Sometimes our application requires specific software, tools or dependencies that are not available in the default Runner environment.

With a self-hosted Runner, we can install the required packages and configure the environment according to our project needs.

**In simple words:** We use self-hosted Runners when we need more control, customized resources, specific dependencies or an environment that meets our security requirements.

## 7. How Does GitHub Communicate With a Self-Hosted Runner?

This is an important concept from our teacher's explanation.

In Jenkins, the Jenkins Controller communicates with Jenkins Agents. In this practical, we will see how GitHub Actions works with our EC2 instance.

Our EC2 instance runs the GitHub Actions Runner software.

After registration, the Runner connects to GitHub and listens for available jobs.

When a matching job is assigned:

1. The Runner receives the job.
2. It executes the workflow steps on the EC2 instance.
3. It sends the execution result back to GitHub.
4. GitHub displays the workflow status.

### Network Configuration

In our teacher's demonstration, the EC2 security group was configured with HTTP and HTTPS rules.

| Port | Protocol | Purpose |
|---|---|---|
| 80 | HTTP | HTTP communication |
| 443 | HTTPS | Secure HTTPS communication |

The teacher demonstrated configuring these rules in both inbound and outbound traffic settings.

**Important:** In a real environment, security group rules should follow the actual communication requirements. GitHub Actions self-hosted Runners normally initiate outbound connections to GitHub. We should not open unnecessary inbound ports or expose the Runner to the internet.

## 8. How Do We Register a Self-Hosted Runner?

We register our machine with GitHub so that GitHub Actions can identify and assign jobs to it.

The general process is:

1. Open the GitHub repository.
2. Navigate to Settings.
3. Open Actions.
4. Select Runners.
5. Click New self-hosted runner.
6. Select the operating system.
7. Select the machine architecture.
8. Follow the installation and configuration commands provided by GitHub.
9. Register the Runner with the repository.
10. Start the Runner using the provided script.

After successful configuration, the Runner becomes available to execute jobs.

### Important Security Point

During Runner registration, GitHub provides a temporary registration token.

We must never share this token with anyone or upload it to GitHub.

It should be treated as sensitive information.

## 9. How Do We Use a Self-Hosted Runner in a Workflow?

GitHub Actions workflows are stored inside the repository.

The standard directory structure is:

```text
My-Repository/
│
└── .github/
    │
    └── workflows/
        │
        └── first-actions.yml
```

Inside the workflow file, we specify which Runner should execute the job.

### GitHub-Hosted Runner

```yaml
jobs:
  build:
    runs-on: ubuntu-latest
```

### Self-Hosted Runner

```yaml
jobs:
  build:
    runs-on: self-hosted
```

The `runs-on` keyword specifies the type of Runner required for the job.

When we use `self-hosted`, GitHub Actions selects an available self-hosted Runner that matches the job's requirements.

**In simple words:** We change the Runner label in our workflow to tell GitHub whether to use its own machine or our machine.

## 10. How Does the Workflow Get Triggered?

GitHub Actions uses events to decide when a workflow should run.

For example:

```yaml
on:
  push:
```

Here, `push` means the workflow runs when changes are pushed to the repository.

Other commonly used events include:

- `pull_request` – Runs when a pull request event occurs.
- `push` – Runs when code is pushed.
- `workflow_dispatch` – Allows us to manually start a workflow.

In our teacher's practical, the workflow was triggered whenever code was pushed to GitHub.

## 11. GitHub Actions Secrets and Variables

Sometimes our workflows require sensitive information such as passwords, access tokens and credentials.

We should never directly write these values inside workflow files.

GitHub provides **Secrets and Variables** to store this information.

We can configure them through:

**Repository Settings → Secrets and variables → Actions**

- **Secrets:** Used for sensitive information such as passwords and access tokens.
- **Variables:** Used for configuration values that are not sensitive.

This helps us avoid exposing sensitive information in our source code.

## 12. GitHub Actions vs Jenkins

Both GitHub Actions and Jenkins are used to automate CI/CD pipelines.

However, they work differently.

| GitHub Actions | Jenkins |
|---|---|
| CI/CD platform provided by GitHub | Open-source automation server |
| Workflows are stored in `.github/workflows/` | Pipelines are commonly defined in a Jenkinsfile |
| Uses Runners | Uses Agents or Worker Nodes |
| Integrated with GitHub | Integrates with many source control platforms |
| GitHub provides hosted Runners | We generally manage Jenkins infrastructure and agents |
| Uses YAML for workflow configuration | Uses Groovy-based Pipeline syntax |
| Provides GitHub Actions marketplace | Provides a large plugin ecosystem |

### When Should We Use GitHub Actions?

GitHub Actions is especially useful when our source code and development workflow are already managed on GitHub.

For public open-source projects, GitHub-hosted Runners are a convenient option.

### When Should We Use Jenkins?

Jenkins is useful when we need extensive customization, plugin integrations, control over infrastructure and complex automation workflows.

**Important:** The best choice depends on the project requirements, infrastructure, security and maintenance needs. Neither tool is always better than the other.

## 13. Interview Questions

### Q1. What is GitHub Actions?

GitHub Actions is a CI/CD automation platform provided by GitHub. It helps automate tasks such as building, testing and deploying applications.

### Q2. What is a Runner?

A Runner is a machine that executes the jobs defined in a GitHub Actions workflow.

### Q3. What are the two types of Runners?

1. GitHub-Hosted Runners.
2. Self-Hosted Runners.

### Q4. What is a GitHub-Hosted Runner?

A GitHub-Hosted Runner is a virtual machine provided and managed by GitHub to execute workflow jobs.

### Q5. What is a Self-Hosted Runner?

A Self-Hosted Runner is a machine that we configure and manage ourselves to execute GitHub Actions workflows.

### Q6. Why do we use Self-Hosted Runners?

We use them when we need customized resources, specific dependencies, infrastructure control or additional security requirements.

### Q7. What is the difference between a Jenkins Agent and a GitHub Actions Runner?

Both execute pipeline jobs. Jenkins calls it an Agent or Worker Node, whereas GitHub Actions calls it a Runner.

### Q8. Where are GitHub Actions workflow files stored?

They are stored inside the `.github/workflows/` directory of the repository.

### Q9. What is the purpose of `runs-on`?

The `runs-on` keyword specifies which type of Runner should execute a workflow job.

### Q10. How do we protect sensitive information in GitHub Actions?

We use GitHub Secrets to securely store sensitive information instead of writing credentials directly into workflow files.

---

## 14. Final Understanding

From this topic, I learned:

- What GitHub Actions is and how it automates CI/CD.
- What a Runner is and why it is required.
- The difference between GitHub-Hosted and Self-Hosted Runners.
- Why companies use Self-Hosted Runners.
- How GitHub communicates with a Self-Hosted Runner.
- How an EC2 instance can be configured as a Runner.
- How to register a Runner with a GitHub repository.
- How to select a Runner using `runs-on`.
- How GitHub Actions workflows are triggered.
- How to store sensitive information using GitHub Secrets.
- The differences between GitHub Actions and Jenkins.

**Key takeaway:** GitHub Actions automates our CI/CD workflows, and Self-Hosted Runners allow us to execute those workflows on our own infrastructure with control over the machine, resources and dependencies.
