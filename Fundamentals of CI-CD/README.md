# CI/CD – Continuous Integration and Continuous Delivery

## 1. Introduction to CI/CD

CI/CD stands for:

- **CI – Continuous Integration**
- **CD – Continuous Delivery / Continuous Deployment**

CI/CD is a process used to automate the building, testing and delivery of applications.

In simple words, CI/CD helps automate the process of taking application code from a developer's laptop and delivering it to customers.

### Why Do We Need CI/CD?

Before delivering an application to customers, it needs to go through several steps:

1. Testing the application.
2. Checking code quality.
3. Identifying security vulnerabilities.
4. Performing functional testing.
5. Generating reports.
6. Deploying the application.

Performing all these activities manually every time a developer makes a code change takes a lot of time.

To solve this problem, we use CI/CD to automate the entire process.

**Main Purpose:** To deliver applications faster, more reliably and with fewer manual efforts.

---

## 2. Continuous Integration (CI)

Continuous Integration is a practice where developers frequently integrate their code changes into a shared repository.

Whenever a developer pushes new code to the repository, an automated process starts to build and test the application.

### How Does CI Work?

1. A developer writes application code.
2. The developer commits changes using Git.
3. The code is pushed to GitHub.
4. The CI pipeline gets triggered.
5. Automated tests are executed.
6. Code quality checks are performed.
7. Test results are generated.

This helps identify errors early in the development process.

**In simple words:** Continuous Integration means frequently integrating code changes into a shared repository and automatically testing them.

---

## 3. Continuous Delivery (CD)

Continuous Delivery is the process of automatically preparing an application for deployment after it successfully passes the required build and testing stages.

The application can be deployed to different environments such as Dev and Staging.

However, deploying the application to Production usually requires manual approval.

**In simple words:** Continuous Delivery makes sure that our application is always ready for deployment.

### What Is Continuous Deployment?

Continuous Deployment takes automation one step further.

After the application passes all the required tests and checks, it is automatically deployed to Production without requiring manual approval for every release.

### Continuous Delivery vs Continuous Deployment

| Continuous Delivery | Continuous Deployment |
|---|---|
| Application is automatically built and tested. | Application is automatically built and tested. |
| Application is ready for production deployment. | Application is automatically deployed to Production. |
| Manual approval is generally required before production deployment. | No manual approval is required for each production deployment. |
| Production deployment is controlled by a person. | Production deployment is fully automated. |

---

## 4. Different Stages of a CI/CD Pipeline

Before delivering an application to customers, it needs to pass through several stages.

The exact stages can change depending on the organization and application requirements.

Some common stages are:

1. Unit Testing
2. Static Code Analysis
3. Code Quality and Vulnerability Testing
4. Automation Testing
5. Reports
6. Deployment

### 4.1 Unit Testing

Unit testing means testing individual functions or small components of an application.

For example, imagine I am developing a calculator application using Python.

I have written an addition function:

```python
def addition(a, b):
    return a + b
```

Now I want to verify whether the function is working correctly.

I provide two numbers:

```python
addition(2, 3)
```

Expected output:

```text
5
```

If the output is 5, the test passes.

If the output is incorrect, the test fails.

This is called Unit Testing.

**Purpose:** To verify whether individual functions or components of an application are working correctly.

### 4.2 Static Code Analysis

Static Code Analysis means checking source code without actually executing the application.

It helps identify problems in the code.

For example:

- Unused variables.
- Poor coding practices.
- Formatting issues.
- Potential bugs.
- Code complexity.
- Coding standard violations.

Imagine I declare 20 variables but use only 5 variables in my application.

Static code analysis tools can identify unused variables and other code quality problems.

**Purpose:** To maintain code quality and identify potential problems before deployment.

One popular tool used for this purpose is **SonarQube**.

### 4.3 Code Quality and Vulnerability Testing

Before delivering an application to customers, we need to make sure that the application is secure.

For example, imagine I am developing an application and unknowingly use an outdated library that contains a security vulnerability.

Hackers might exploit that vulnerability to attack my application.

To avoid such problems, we perform security checks.

These checks help identify:

- Security vulnerabilities.
- Vulnerable dependencies.
- Insecure coding practices.
- Known security issues.

**Purpose:** To identify security weaknesses and improve application security before deployment.

### 4.4 Automation Testing (Functional and End-to-End Testing)

Unit testing checks whether individual functions are working correctly.

But sometimes, one function might work correctly while affecting another function.

Let's take the calculator example again.

My calculator has four operations:

1. Addition.
2. Subtraction.
3. Multiplication.
4. Division.

Now imagine I develop a new addition feature.

Unit testing confirms that addition is working correctly.

But I also need to verify whether subtraction, multiplication and division are still working.

This is where functional testing and end-to-end testing help.

They verify whether different parts of the application work together correctly.

**Purpose:** To make sure that new changes do not break existing application functionalities.

### 4.5 Reports

After completing the testing stages, we need reports to understand the results.

For example:

| Testing Stage | Result |
|---|---|
| Unit Testing | Passed |
| Code Quality | Passed |
| Security Testing | Passed |
| Functional Testing | Passed |
| Code Coverage | 85% |

Code coverage tells us how much of our application code is covered by automated tests.

Reports help developers and DevOps engineers understand whether the application is ready for deployment.

**Purpose:** To track test results, code quality and application health.

### 4.6 Deployment

Deployment is the final stage of the CI/CD pipeline.

After successfully completing the required checks, we deploy the application to a platform where customers can access it.

Some examples are:

- AWS EC2.
- Docker Containers.
- Kubernetes Clusters.
- Cloud Platforms.

**Purpose:** To make the application available to customers.

---

## 5. Version Control System (VCS)

Before understanding Jenkins, I need to understand Version Control Systems.

Imagine I am developing an application.

I don't write the entire application in one day. I continuously make changes to the application.

For example:

- Version 1: Created the initial application.
- Version 2: Added login functionality.
- Version 3: Added registration functionality.
- Version 4: Fixed bugs.
- Version 5: Improved application performance.

I need a place to store and manage all these code changes.

This is where a Version Control System comes into the picture.

**VCS (Version Control System)** is a system that helps developers track, manage and maintain changes made to their source code.

### Popular Version Control Tools and Platforms

| Tool | Description |
|---|---|
| Git | A distributed version control system. |
| GitHub | A platform used to host and manage Git repositories. |
| GitLab | A platform that provides Git repository management and DevOps features. |
| Bitbucket | A platform used for hosting and managing Git repositories. |

### How Does CI/CD Get Triggered?

Imagine I am a developer.

1. I write code on my local machine.
2. I commit my changes using Git.
3. I push my changes to GitHub.
4. The CI/CD pipeline gets triggered.
5. The pipeline starts executing the required tasks.

This is where Jenkins comes into the picture.

---

## 6. Jenkins

Jenkins is an open-source automation server used to build, test and deploy applications.

In simple words, Jenkins automates different stages of a CI/CD pipeline.

### How Does Jenkins Work?

Imagine I have a GitHub repository containing my application code.

I configure Jenkins to monitor that GitHub repository.

I tell Jenkins:

> Whenever a developer pushes new code to this repository, automatically execute my CI/CD pipeline.

Now imagine a developer pushes new code.

The following activities take place:

1. Jenkins detects the new code changes.
2. Jenkins starts the pipeline.
3. Jenkins runs unit tests.
4. Jenkins performs code quality checks.
5. Jenkins performs security checks.
6. Jenkins builds the application.
7. Jenkins deploys the application.

All these tasks happen automatically based on the pipeline configuration.

### Jenkins Workflow

```text
       Developer
           |
           v
         GitHub
           |
           v
         Jenkins
           |
           v
      Unit Testing
           |
           v
      Code Analysis
           |
           v
     Security Testing
           |
           v
     Build Application
           |
           v
        Deployment
           |
           v
         Customer
```

---

## 7. Jenkins Pipeline

A Jenkins Pipeline is a collection of automated steps that define how an application should be built, tested and deployed.

Instead of manually performing every task, we define all the required steps inside a Jenkins Pipeline.

For example:

- Pull source code from GitHub.
- Build the application using Maven.
- Run unit tests using JUnit.
- Perform code quality analysis using SonarQube.
- Build a Docker image.
- Deploy the application to Kubernetes.

Jenkins executes these stages based on the pipeline configuration.

### What Is an Orchestrator?

An orchestrator is a tool that coordinates and manages different tools and processes to complete a workflow.

Jenkins acts as an orchestrator because it integrates and coordinates different tools within a CI/CD pipeline.

### Tools Integrated with Jenkins

| Tool | Purpose |
|---|---|
| GitHub | Source code management. |
| Maven | Building Java applications. |
| JUnit | Unit testing. |
| SonarQube | Code quality analysis. |
| Docker | Containerization. |
| Kubernetes | Container orchestration. |
| AWS EC2 | Application hosting. |

**Important:** Jenkins does not replace these tools. It coordinates them and triggers their activities through the pipeline.

This is why Jenkins is called an Orchestrator.

---

## 8. Different Application Environments

In real-world organizations, applications are generally not deployed directly to customers whenever developers make changes.

Instead, applications pass through different environments.

The three commonly used environments are:

1. Development (Dev).
2. Staging.
3. Production (Prod).

### 8.1 Development Environment

The Development environment is where developers initially deploy their applications and test new changes.

For example, imagine I develop a new login feature.

Before making it available to customers, the application is deployed to the Dev environment.

Developers and testers verify whether the new feature works correctly.

The Dev environment is generally used for initial development and testing.

### 8.2 Staging Environment

After the application passes initial testing in Dev, it moves to the Staging environment.

Staging is designed to closely resemble the Production environment.

Here, the team performs additional testing before releasing the application to customers.

Some activities include:

- Integration Testing.
- Performance Testing.
- Final Application Verification.
- User Acceptance Testing.

The main purpose is to identify problems before deploying the application to Production.

### 8.3 Production Environment

Production is the actual environment where customers use the application.

For example, when I open Amazon and purchase something, I am interacting with its Production environment.

This environment needs to be stable, secure and reliable.

Production environments generally have more resources and infrastructure depending on application requirements.

### Why Do We Need Different Environments?

Imagine directly deploying new code to Production without testing it.

What if the application crashes?

Thousands of customers might be affected.

Instead, we first test the application in Dev and Staging.

Once everything is working correctly, we deploy it to Production.

This reduces the risk of failures affecting customers.

---

## 9. Application Promotion Using Jenkins

Jenkins can automate the process of moving an application from one environment to another.

This process is called Environment Promotion.

Let's understand with an example.

Imagine a developer pushes new code to GitHub.

The Jenkins pipeline starts executing.

### Step 1: Deploy to Dev

- Jenkins deploys the application to the Dev environment.
- Developers and testers verify the application.
- Initial testing is performed.

### Step 2: Promote to Staging

After successful testing in Dev, the application moves to Staging.

- Additional testing is performed.
- QA engineers verify the application.
- Performance and integration testing can be performed.

### Step 3: Promote to Production

After successful testing in Staging, the application is ready for Production.

Depending on the organization's process, Jenkins can wait for manual approval or automatically promote the application.

Finally, the application is deployed to Production where customers can access it.

### Complete Environment Promotion Workflow

```text
        Developer
            |
            v
          GitHub
            |
            v
          Jenkins
            |
            v
       Build & Test
            |
            v
      Dev Environment
            |
            v
       Initial Testing
            |
            v
    Staging Environment
            |
            v
        Final Testing
            |
            v
      Manual Approval
            |
            v
   Production Environment
            |
            v
         Customers
```

### Why Are Dev and Staging Environments Different from Production?

One important point explained by my teacher is that Production environments can be expensive.

For example, imagine a Kubernetes setup.

**Dev Environment:**

- 1 Master Node.
- 1 Worker Node.

**Staging Environment:**

- 3 Master Nodes.
- 5 Worker Nodes.

**Production Environment:**

- 3 Master Nodes.
- 30 Worker Nodes.

These are only example configurations, not fixed requirements.

Production generally requires more resources because it handles actual customer traffic.

Maintaining the same large infrastructure in every environment can be expensive.

Therefore, organizations use different infrastructure sizes depending on their testing and production requirements.

---

## 10. Complete CI/CD Workflow

Now let's connect all the concepts I learned.

Imagine I am developing an application.

1. I write application code on my local machine.
2. I use Git to track my code changes.
3. I push the code to GitHub.
4. Jenkins detects the new changes.
5. Jenkins starts the CI/CD pipeline.
6. Maven builds the application.
7. JUnit performs unit testing.
8. SonarQube performs code quality analysis.
9. Security checks are performed.
10. Reports are generated.
11. The application is deployed to the Dev environment.
12. After successful testing, it moves to Staging.
13. After final verification and required approval, it moves to Production.
14. Customers can access the application.

### Complete CI/CD Architecture

```text
       Application Developer
                |
                v
            Write Code
                |
                v
                Git
                |
                v
              GitHub
                |
                v
              Jenkins
                |
                v
       +-------------------+
       |   CI/CD Pipeline  |
       +-------------------+
                |
       +--------+---------+
       |        |         |
       v        v         v
     Maven    JUnit   SonarQube
       |        |         |
       +--------+---------+
                |
                v
        Security Testing
                |
                v
          Build Artifact
                |
                v
         Dev Environment
                |
                v
       Staging Environment
                |
                v
      Production Environment
                |
                v
             Customers
```

---

## 11. Important CI/CD Terminologies

| Term | Meaning |
|---|---|
| CI | Continuous Integration. |
| CD | Continuous Delivery or Continuous Deployment. |
| VCS | Version Control System. |
| Git | Distributed version control tool. |
| GitHub | Platform for hosting Git repositories. |
| Jenkins | Automation server used for CI/CD. |
| Pipeline | Collection of automated steps. |
| Orchestrator | Coordinates different tools and processes. |
| Unit Testing | Testing individual functions. |
| Static Code Analysis | Checking source code without executing it. |
| Vulnerability Testing | Identifying security weaknesses. |
| Functional Testing | Checking whether application features work correctly. |
| Code Coverage | Percentage of code covered by automated tests. |
| Deployment | Making an application available in an environment. |
| Dev | Development environment. |
| Staging | Environment used for final testing before Production. |
| Production | Environment used by actual customers. |
| Environment Promotion | Moving an application from one environment to another. |

---

## 12. Key Learnings

From this session, I understood the following concepts:

1. CI/CD automates the process of building, testing and delivering applications.
2. Continuous Integration involves frequently integrating code changes into a shared repository.
3. Continuous Delivery prepares applications for deployment.
4. Continuous Deployment automatically deploys successful changes to Production.
5. Unit testing verifies individual functions.
6. Static Code Analysis checks source code without executing it.
7. Security testing helps identify vulnerabilities.
8. Functional testing verifies whether different application features work together.
9. Git and GitHub help developers manage and store source code.
10. Jenkins automates the different stages of a CI/CD pipeline.
11. Jenkins acts as an orchestrator by coordinating different tools.
12. Jenkins Pipelines define the steps involved in building, testing and deploying applications.
13. Applications generally move through Dev, Staging and Production environments.
14. Environment promotion helps organizations deploy applications safely.
15. Manual and automatic approvals can be used before Production deployment.

---

## Final Understanding

CI/CD is an important part of DevOps because it automates the process of building, testing and delivering applications.

Instead of performing every activity manually, we use tools like Jenkins to coordinate different tools and automate the complete application delivery process.
