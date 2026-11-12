# Top 5 CI/CD Interview Questions and Answers

## 1. Introduction

In this lesson, I learned five important CI/CD interview questions based on real-world scenarios.

The main focus was understanding how CI/CD works in an organization, how secrets are managed, different deployment strategies and how Jenkins infrastructure is backed up and scaled.

The five topics covered are:

1. Explain your current CI/CD setup.
2. How do you handle secrets?
3. What are the different deployment strategies?
4. What do you do if a deployed application is faulty?
5. How do you back up and scale Jenkins?

## 2. Explain Your Current CI/CD Setup

This is one of the most common CI/CD interview questions.

The interviewer wants to understand how application code moves from development to production and which tools are used at each stage.

Let's take a Java application as an example.

### Real-Time CI/CD Workflow

1. Developers write application code and push it to GitHub.
2. A GitHub Webhook triggers the Jenkins pipeline.
3. Jenkins checks out the latest source code.
4. Maven builds the Java application.
5. JUnit executes unit tests.
6. SonarQube performs static code analysis.
7. AppScan performs application security testing.
8. Docker builds the container image.
9. The image is pushed to a container registry.
10. Kubernetes manifest files are updated with the new image tag.
11. Argo CD monitors the manifest repository and synchronizes changes with Kubernetes.
12. The updated application runs in the Kubernetes cluster.

### Tools Used

| Tool | Purpose |
|---|---|
| GitHub | Stores application code |
| Jenkins | CI/CD pipeline orchestration |
| Maven | Builds Java applications |
| JUnit | Unit testing |
| SonarQube | Code quality analysis |
| AppScan | Application security testing |
| Docker | Container image creation |
| Docker Hub / ECR | Container image storage |
| Helm | Kubernetes application packaging |
| Argo CD | GitOps-based continuous delivery |
| Kubernetes | Container orchestration |

If an organization does not use Kubernetes, Jenkins can also deploy applications directly to EC2 instances using shell scripts, Ansible or other deployment tools.

**Interview tip:** Explain the complete pipeline and the responsibility of each tool instead of just listing tool names.

## 3. How Do You Handle Secrets?

Secrets are sensitive information used by applications and CI/CD pipelines.

Examples include:

- SSH keys
- AWS credentials
- API keys
- Database passwords
- Kubernetes authentication credentials

We should never hardcode secrets inside pipeline files because this can expose sensitive information.

### Different Ways to Manage Secrets

| Platform | Secret Management |
|---|---|
| GitHub Actions | GitHub Actions Secrets |
| GitLab CI/CD | CI/CD Variables |
| AWS | AWS Systems Manager Parameter Store |
| Azure | Azure Key Vault |
| Multiple environments | HashiCorp Vault |

### Example Using HashiCorp Vault

HashiCorp Vault is a secrets management tool used to securely store and manage sensitive information.

Jenkins can integrate with Vault and retrieve the required secrets when a pipeline runs.

Example workflow:

```text
Jenkins Pipeline
       |
       v
Request Secret
       |
       v
HashiCorp Vault
       |
       v
Return Required Credential
       |
       v
Execute Pipeline
```

### Important Security Practices

- Never hardcode passwords or access keys.
- Avoid printing secrets in build logs.
- Restrict access to credentials.
- Use minimum required permissions.
- Rotate credentials when necessary.

**Remember:** Store secrets securely and retrieve them only when required.

## 4. What Are Deployment Strategies?

Deployment strategies define how a new application version is released to customers.

Imagine our application is currently running version 34.

Now developers have created version 35.

We need to deploy the new version without unnecessarily affecting customers.

Two popular deployment strategies covered in this lesson are:

1. Blue-Green Deployment
2. Canary Deployment

### 4.1 Blue-Green Deployment

Blue-Green Deployment uses two separate environments.

- Blue Environment: Runs the old application version.
- Green Environment: Runs the new application version.

Let's say:

- Blue runs v34.
- Green will run v35.

### How Does It Work?

1. Customers are currently using the Blue environment.
2. Deploy the new application version to the Green environment.
3. Test the Green environment.
4. If everything works correctly, switch the load balancer to Green.
5. New customer traffic goes to v35.
6. Allow existing traffic to finish during the required grace period.
7. Remove the old Blue environment when it is safe.

### Example

Before deployment:

```text
Load Balancer
      |
      v
Blue Environment (v34)
      |
      v
Customers
```

After successful deployment:

```text
Load Balancer
      |
      v
Green Environment (v35)
      |
      v
Customers
```

### What Is a Load Balancer?

A load balancer distributes incoming application traffic across servers or application instances.

In Blue-Green Deployment, we use it to switch traffic from the old environment to the new environment.

### Advantages

- Reduces deployment downtime.
- Allows testing before switching traffic.
- Makes rollback easier.
- Keeps the previous version available temporarily.

**Simple meaning:** Deploy the new version in a separate environment, test it and then switch customer traffic to it.

### 4.2 Canary Deployment

Canary Deployment is a strategy where we gradually send traffic to a new application version.

Instead of sending all customers to the new version immediately, we initially send only a small percentage of traffic.

### How Does It Work?

1. Deploy the old and new application versions.
2. Initially send 10% of traffic to the new version.
3. Send the remaining 90% to the old version.
4. Monitor the new version for errors and performance.
5. If everything works correctly, gradually increase traffic to the new version.
6. Eventually, send all traffic to the new version.

### Example

Initial traffic:

```text
Old Version (v34) → 90% Traffic
New Version (v35) → 10% Traffic
```

Later:

```text
Old Version (v34) → 50% Traffic
New Version (v35) → 50% Traffic
```

Final:

```text
New Version (v35) → 100% Traffic
```

These percentages are examples. Actual traffic distribution depends on the deployment strategy.

### Advantages

- Tests the new version with a small group first.
- Reduces the impact of a faulty release.
- Helps identify problems before sending all traffic to the new version.

**Simple meaning:** Send a small percentage of traffic to the new version first, monitor it and gradually increase the traffic.

### 4.3 Blue-Green vs Canary Deployment

| Blue-Green | Canary |
|---|---|
| Uses two separate environments | Gradually shifts traffic between versions |
| Switches traffic after testing | Starts with a small percentage of traffic |
| Makes switching back easier | Allows traffic to the new version to be reduced |
| Useful for quick environment switching | Useful for gradual application releases |

## 5. What If the Deployed Application Is Faulty?

Imagine we deployed a new application version.

But after deployment:

- The application crashes.
- Customers cannot log in.
- Some features are not working.
- Errors are appearing.

What should we do?

We need to perform a **Rollback**.

### What Is Rollback?

Rollback means returning to a previous working version of an application.

For example:

- Old version: v34
- New version: v35
- Problem: v35 is not working correctly.

If we use Blue-Green Deployment, we can switch the load balancer back to the Blue environment running v34.

### Rollback Workflow

```text
New Version v35
       |
       v
Application Has Problems
       |
       v
Switch Load Balancer Back
       |
       v
Previous Version v34
       |
       v
Application Works Again
```

Your teacher also mentioned maintaining a separate rollback pipeline or rollback strategy.

### Advantages

- Helps recover from faulty deployments.
- Reduces the impact on customers.
- Allows the previous working version to serve traffic again.

**Remember:** If the new application version has problems, return traffic to the previous working version.

## 6. How Do You Back Up Jenkins?

Jenkins stores important information such as:

- Pipeline configurations.
- Job information.
- Plugins.
- Build history.
- Build logs.
- Other Jenkins configurations.

If the Jenkins server crashes, we need backups to restore this information.

### What Is the Jenkins Home Directory?

Jenkins stores its important information inside a directory called `JENKINS_HOME`.

Depending on the installation, common locations include:

```text
/var/lib/jenkins
```

or:

```text
~/.jenkins
```

The actual location depends on the Jenkins installation and configuration.

### How to Back Up Jenkins

Your teacher explained backing up the `.jenkins` directory periodically.

We can use the Linux `rsync` command.

Example:

```bash
rsync -av ~/.jenkins/ /backup/jenkins/
```

Understanding the command:

- `rsync` – Synchronizes files and directories.
- `-a` – Preserves important file attributes and copies directories recursively.
- `-v` – Displays the files being processed.
- `~/.jenkins/` – Example source directory.
- `/backup/jenkins/` – Backup destination.

We can schedule this backup using a Linux cron job.

### What Is a Cron Job?

A cron job is a scheduled task in Linux.

For example, we can configure Jenkins backups to run every day at midnight.

**Remember:** Back up the configured Jenkins home directory regularly so that important Jenkins data can be restored if something goes wrong.

## 7. How Do You Scale Jenkins?

Imagine a company receives 10 Jenkins build requests today.

Tomorrow, it receives 100 build requests.

A small number of worker nodes might not be enough to handle the increased workload.

We need additional worker capacity.

This is where Auto Scaling becomes useful.

### What Is Auto Scaling?

Auto Scaling automatically increases or decreases computing resources based on configured conditions.

Your teacher explained using AWS EC2 Auto Scaling Groups.

### How Does It Work?

1. Jenkins is hosted on AWS.
2. Jenkins uses EC2 instances as worker nodes.
3. When workload increases, AWS Auto Scaling can launch additional EC2 instances.
4. Jenkins connects to the newly created worker nodes using SSH in the setup described.
5. The new workers execute pipeline tasks.
6. When workload decreases, unnecessary worker capacity can be removed.

### What Is Predictive Scaling?

Predictive Scaling uses historical workload patterns to estimate future resource requirements.

For example, if the organization usually receives more build requests during working hours, AWS can prepare additional capacity before the expected increase.

### Advantages

- Handles increasing workloads.
- Provides additional build capacity.
- Reduces unnecessary infrastructure costs.
- Avoids maintaining unused worker nodes.

**Remember:** Auto Scaling helps Jenkins handle changing workloads by adjusting the available worker capacity.

## 8. Quick Interview Revision

| Interview Question | Important Concept |
|---|---|
| Explain your current CI/CD setup | Complete CI/CD workflow |
| How do you handle secrets? | Secrets management |
| What is Blue-Green Deployment? | Two separate environments |
| What is Canary Deployment? | Gradual traffic shifting |
| What if a deployment fails? | Rollback |
| How do you back up Jenkins? | Jenkins home directory and rsync |
| How do you scale Jenkins? | AWS EC2 Auto Scaling Groups |
| What is Predictive Scaling? | Predicting future resource demand |

## 9. Key Takeaways

In this lesson, I learned:

- How to explain a real-time CI/CD setup in an organization.
- How to manage secrets using different platforms.
- The difference between Blue-Green and Canary Deployment.
- How load balancers help switch application traffic.
- What rollback means and how it helps recover from faulty deployments.
- How to back up Jenkins using rsync.
- How cron jobs automate regular backups.
- How AWS EC2 Auto Scaling Groups help scale Jenkins worker capacity.
- How Predictive Scaling prepares for expected workload increases.

## Conclusion

In this lesson, I learned that CI/CD is not only about building and deploying applications.

We also need to understand security, deployment strategies, rollback procedures, backups and infrastructure scaling.

These concepts are important when working with CI/CD pipelines in real-world organizations and preparing for DevOps interviews.
