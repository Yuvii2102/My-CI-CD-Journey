# Practical : Setting Up GitHub Actions Self-Hosted Runner on AWS EC2

## 1. Goal of the Practical

The goal of this practical was to understand how GitHub Actions self-hosted runners work and how to configure our own machine to execute GitHub Actions workflows.

Instead of using GitHub-hosted runners, I wanted to use my own AWS EC2 Ubuntu instance to run the workflow jobs.

By completing this practical, I learned how to connect an EC2 instance with a GitHub repository, configure a self-hosted runner and execute a GitHub Actions workflow on my own machine.

## 2. What is a Self-Hosted Runner?

A self-hosted runner is a machine that we provide and manage ourselves to execute GitHub Actions workflows.

It can be a physical machine, virtual machine or cloud server such as an AWS EC2 instance.

In this practical, I used my AWS EC2 Ubuntu instance as a self-hosted runner.

### GitHub-Hosted vs Self-Hosted Runner

| GitHub-Hosted Runner | Self-Hosted Runner |
|---|---|
| GitHub provides the machine. | We provide our own machine. |
| GitHub manages the environment. | We manage the environment. |
| Uses GitHub-hosted infrastructure. | Uses our own infrastructure. |
| Example: `ubuntu-latest` | Example: `self-hosted` |

**Simple example:**

- GitHub-hosted runner: GitHub provides a machine to execute our workflow.
- Self-hosted runner: We use our own AWS EC2 instance to execute our workflow.

## 3. Prepare the AWS EC2 Instance

I used my existing AWS EC2 instance named `Jenkins-DevOps-Projects`.

Instance details:

- **Operating System:** Ubuntu
- **Instance Type:** t2.2xlarge
- **Connection Method:** AWS EC2 Instance Connect

I also configured the security group rules as taught in the practical.

### Inbound Rules

| Type | Port | Source |
|---|---|---|
| HTTP | 80 | Anywhere IPv4 |
| HTTPS | 443 | Anywhere IPv4 |

### Outbound Rules

| Type | Port | Destination |
|---|---|---|
| HTTP | 80 | Anywhere IPv4 |
| HTTPS | 443 | Anywhere IPv4 |

## 4. Open GitHub Self-Hosted Runners

First, I opened my GitHub repository:

`My-CI-CD-Journey`

Then I followed these steps:

1. Opened the **Settings** tab.
2. Selected **Actions**.
3. Clicked **Runners**.
4. Clicked **New self-hosted runner**.

This opened the page where GitHub provides the instructions to configure a self-hosted runner.

## 5. Select Runner Image and Architecture

After clicking **New self-hosted runner**, GitHub displayed the runner setup page.

Before downloading the runner package, I selected the correct runner image and architecture.

- **Runner Image:** Linux
- **Architecture:** x64

Since my EC2 instance was running Ubuntu with x64 architecture, I selected Linux and x64.

**Important:** After selecting the runner image and architecture, GitHub automatically provides all the commands required to download, configure and start the runner.

We do not need to create these commands ourselves. We simply copy the commands provided on the GitHub setup page and execute them in our EC2 instance.

## 6. Download and Extract the Runner

I connected to my EC2 instance using AWS EC2 Instance Connect.

Under the **Download** section, GitHub provided the following instructions.

### Step 1: Create a Folder

First, I created a folder to store the GitHub Actions runner files.

```bash
mkdir actions-runner && cd actions-runner
```

### Step 2: Download the Runner Package

Next, I copied the download command provided by GitHub.

```bash
curl -o actions-runner-linux-x64-2.338.2.tar.gz -L https://github.com/actions/runner/releases/download/v2.338.2/actions-runner-linux-x64-2.338.2.tar.gz
```

This downloaded the GitHub Actions runner package into my EC2 instance.

### Step 3: Validate the Download (Optional)

GitHub also provided a command to verify the downloaded package using its checksum.

```bash
echo "baebf204307bac6193480852732f0aba2ae97b6c5597c244f4d5558390147c40  actions-runner-linux-x64-2.338.2.tar.gz" | shasum -a 256 -c
```

The output was:

```text
actions-runner-linux-x64-2.338.2.tar.gz: OK
```

This confirmed that the downloaded package matched the expected checksum.

### Step 4: Extract the Runner Package

After downloading and verifying the package, I extracted it using:

```bash
tar xzf ./actions-runner-linux-x64-2.338.2.tar.gz
```

This extracted the runner files, including `config.sh` and `run.sh`.

## 7. Configure the Self-Hosted Runner

After extracting the package, I went back to the GitHub runner setup page.

Under the **Configure** section, GitHub provided the configuration command.

I copied the command from GitHub and executed it in my EC2 instance.

The command format was:

```bash
./config.sh --url REPOSITORY_URL --token YOUR_TEMPORARY_TOKEN
```

I replaced the placeholders with my actual GitHub repository URL and the temporary registration token provided by GitHub.

### Configuration Options

During the configuration process, I selected the following options:

| Option | Selection |
|---|---|
| Runner Group | Default |
| Runner Name | Default |
| Additional Labels | Pressed Enter to skip |
| Work Folder | `_work` |

After completing the configuration, I received the following messages:

```text
Runner successfully added
Settings Saved.
```

This confirmed that my AWS EC2 instance was successfully registered as a self-hosted runner in GitHub.

**Note:** The registration token is temporary and sensitive. It should never be shared or added to documentation.

## 8. Start the Self-Hosted Runner

After completing the configuration, GitHub provided the final command to start the runner.

I copied and executed:

```bash
./run.sh
```

This started the runner and connected my EC2 instance to GitHub.

The terminal displayed:

```text
Connected to GitHub

Current runner version: '2.338.2'

Listening for Jobs
```

This means my EC2 instance was successfully connected to GitHub and was waiting for workflow jobs.

I kept the EC2 terminal session open while testing the workflow.

## 9. Update the GitHub Actions Workflow

After starting the runner, I went to my GitHub repository.

I opened the following file:

`.github/workflows/first-actions.yml`

Initially, the workflow was configured to use a GitHub-hosted runner.

```yaml
runs-on: ubuntu-latest
```

I changed it to:

```yaml
runs-on: self-hosted
```

This tells GitHub to execute the workflow using my registered self-hosted runner instead of a GitHub-hosted machine.

After making the change, I committed the updated workflow directly to the `main` branch.

**Commit Message:**

`Use self-hosted runner`

## 10. Verify the Runner Status in GitHub

After committing the workflow changes, I opened:

**Settings → Actions → Runners**

I could see my registered EC2 runner.

The details were:

| Property | Value |
|---|---|
| Runner Name | `ip-172-31-40-145` |
| Runner Type | Self-hosted |
| Operating System | Linux |
| Architecture | x64 |
| Status | Idle |

The green **Idle** status confirmed that my runner was online and waiting for workflow jobs.

## 11. Execute and Verify the Workflow

Next, I opened the **Actions** tab in my GitHub repository.

I selected the workflow named **My First GitHub Actions Workflow** and opened the latest workflow run.

The workflow completed successfully.

### Verify the Runner Details

Inside the job logs, I found the following information:

```text
Current runner version: '2.338.2'

Runner name: 'ip-172-31-40-145'

Runner group name: 'Default'

Machine name: 'ip-172-31-40-145'
```

This confirmed that GitHub executed the workflow on my AWS EC2 instance.

### Workflow Steps

The workflow successfully executed the following steps:

1. Printed a welcome message.
2. Checked the Python version.
3. Checked the current working directory.

**Python Version:**

```text
Python 3.14.4
```

**Working Directory:**

```text
/home/ubuntu/actions-runner/actions-runner/_work/My-CI-CD-Journey/My-CI-CD-Journey
```

The workflow completed successfully in approximately 5 seconds.

This proved that my self-hosted runner was working correctly.

## 12. What I Learned

Through this practical, I learned:

1. What GitHub Actions runners are and why they are needed.
2. The difference between GitHub-hosted and self-hosted runners.
3. How to use an AWS EC2 Ubuntu instance as a self-hosted runner.
4. How to select the correct runner image and architecture.
5. How to download, verify and extract the GitHub Actions runner package.
6. How to register an EC2 instance with a GitHub repository.
7. How to configure and start a self-hosted runner.
8. How to use `runs-on: self-hosted` in a GitHub Actions workflow.
9. How to check runner status and verify workflow execution through GitHub Actions logs.

## 13. What We Achieved

By completing this practical, I successfully:

- Configured my AWS EC2 Ubuntu instance as a GitHub Actions self-hosted runner.
- Connected my EC2 instance to my GitHub repository.
- Registered the runner successfully.
- Changed my workflow from a GitHub-hosted runner to a self-hosted runner.
- Executed the GitHub Actions workflow on my own EC2 instance.
- Verified the runner name, machine name and successful job execution through GitHub Actions logs.

## 14. Conclusion

In this practical, I learned how to set up and use a GitHub Actions self-hosted runner on AWS EC2.

I used my own EC2 Ubuntu instance instead of relying on GitHub-hosted runners. I registered the instance with my GitHub repository, updated the workflow configuration and successfully executed the workflow on my own machine.

This practical helped me understand how we can use our own infrastructure to run GitHub Actions workflows.

**Tools and Technologies Used:** AWS EC2, Ubuntu, GitHub Actions, GitHub Self-Hosted Runner, YAML and Linux Shell Commands.
