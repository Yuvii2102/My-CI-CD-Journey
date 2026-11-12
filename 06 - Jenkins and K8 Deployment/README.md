# Jenkins Practical: Docker Agents and Kubernetes Deployment

## 1. Introduction

In this lesson, I learned how to use Jenkins for practical CI/CD implementation.

The main topics covered were:

1. Installing Jenkins on an AWS EC2 instance.
2. Configuring Docker to work with Jenkins.
3. Understanding Jenkins Controller and Agents.
4. Using Docker containers as Jenkins Agents.
5. Creating Jenkins pipelines using Pipeline as Code.
6. Running multi-stage and multi-agent pipelines.
7. Building an end-to-end CI/CD pipeline.
8. Deploying applications to Kubernetes using Argo CD.

The main goal was to understand how Jenkins can automate application builds, testing and deployments using Docker and Kubernetes.

---

## 2. Installing Jenkins on AWS EC2

The first step is to launch an AWS EC2 instance and install Jenkins on it.

Jenkins is a Java-based application. Therefore, Java (JDK) must be installed before installing Jenkins.

### Installation Flow

```text
AWS EC2 Instance
       |
       v
Install Java (JDK)
       |
       v
Install Jenkins
       |
       v
Start Jenkins Service
       |
       v
Access Jenkins Through Browser
```

### Why is Port 8080 Required?

Jenkins uses port `8080` by default for its web interface.

Even after installing Jenkins, we cannot access it externally unless the required inbound traffic is allowed.

AWS Security Groups control incoming and outgoing network traffic for EC2 instances.

To access Jenkins, we need to allow inbound traffic on port `8080`.

Some commonly used ports:

| Port | Purpose |
|---|---|
| 22 | SSH access |
| 8080 | Jenkins web interface |

After configuring the Security Group, Jenkins can be accessed using:

```text
http://<EC2-Public-IP>:8080
```

**Security Note:** In production environments, access to Jenkins should be restricted to trusted IP addresses or provided through a secure access method.

### Initial Jenkins Configuration

When Jenkins is opened for the first time:

1. Jenkins asks for an initial administrator password.
2. Retrieve the password from the EC2 instance.
3. Select Install Suggested Plugins.
4. Create an administrator username and password.
5. Complete the initial setup.

The initial password is available at:

```bash
/var/lib/jenkins/secrets/initialAdminPassword
```

The exact location depends on the Jenkins installation and configured `JENKINS_HOME`.

---

## 3. Understanding Jenkins Architecture

Jenkins uses two important components:

1. Jenkins Controller
2. Jenkins Agent

The Controller manages the Jenkins environment, while Agents execute pipeline tasks.

### A. Jenkins Controller

The Jenkins Controller is the central component of Jenkins.

Its responsibilities include:

- Managing Jenkins jobs and pipelines.
- Scheduling pipeline executions.
- Managing Jenkins Agents.
- Displaying build results.
- Coordinating pipeline execution.

Think of the Controller as a manager who assigns work to different agents.

### B. Jenkins Agent

A Jenkins Agent is a machine or execution environment where Jenkins runs pipeline tasks.

For example, an organization may have different applications:

- Java application.
- Node.js application.
- Python application.

Each application may require different tools and dependencies.

Jenkins can use different agents to execute these applications.

### Traditional Jenkins Architecture

```text
             Jenkins Controller
                     |
          +----------+----------+
          |          |          |
          v          v          v
       Agent 1    Agent 2    Agent 3
        Java      Node.js     Python
```

### Why Not Execute Everything on the Controller?

There are several problems with running all pipeline jobs on one machine.

**1. High Workload**

If multiple pipelines run simultaneously, the Controller may become overloaded.

**2. Dependency Conflicts**

Different applications may require different software versions.

For example:

- Application A requires Java 17.
- Application B requires Java 21.
- Application C requires Node.js.

Managing all these dependencies on the same machine can become difficult.

**3. Resource Wastage**

Organizations may maintain multiple EC2 worker instances. Some instances may remain idle when there are no jobs to execute.

This increases infrastructure costs.

To solve these problems, my teacher introduced Docker containers as Jenkins Agents.

---

## 4. Using Docker Containers as Jenkins Agents

Instead of creating multiple EC2 instances as Jenkins Agents, we can use Docker containers to execute pipeline jobs.

Docker containers are lightweight compared with virtual machines and can be created and removed when required.

### How Does Docker Agent Work?

Imagine an application requires Node.js to execute its pipeline.

Instead of creating a separate EC2 worker instance, Jenkins requests Docker to create a container using a Node.js image.

The process works like this:

```text
Jenkins Controller
        |
        v
Requests Docker Container
        |
        v
Docker Engine
        |
        v
Creates Required Container
        |
        v
Jenkins Executes Pipeline
        |
        v
Pipeline Completes
        |
        v
Container Is Removed
```

For example:

| Application | Docker Image |
|---|---|
| Node.js | node:18-alpine |
| Java | Maven image |
| Python | Python image |

Each pipeline can use an image containing the dependencies it requires.

### Advantages of Docker Agents

- Containers are lightweight compared with virtual machines.
- They can be created and removed easily.
- Different applications can use different environments.
- Dependency conflicts can be reduced.
- Less maintenance is required for permanent worker machines.
- Infrastructure resources can be used more efficiently.

**Important:** Docker Agents provide temporary execution environments. The Jenkins Controller still manages and schedules pipeline jobs.

---

## 5. Installing Docker and Configuring Jenkins Access

To use Docker as a Jenkins Agent, Docker must be installed on the machine where the Docker Engine will run.

In my teacher's demonstration, Jenkins and Docker were installed on the same EC2 instance.

### Docker Engine

Docker Engine manages Docker images and containers.

It runs a background service called the Docker daemon.

The Docker daemon handles operations such as:

- Creating containers.
- Running containers.
- Stopping containers.
- Managing Docker images.

### Why Does the Jenkins User Need Docker Permissions?

Jenkins normally runs using a Linux user called `jenkins`.

This user needs permission to communicate with the Docker daemon to create and manage containers.

In the practical, the Jenkins user is added to the Docker group.

The Ubuntu user is also added in the teacher's setup.

**Security Note:** Membership in the Docker group provides powerful privileges and can effectively grant root-level access. It should be carefully restricted in production environments.

After changing group membership, the relevant services or sessions may need to be restarted or refreshed so that the new permissions take effect.

### Docker Pipeline Plugin

Installing Docker on the EC2 instance is not enough.

Jenkins also needs the Docker Pipeline Plugin to use Docker-related functionality inside pipeline definitions.

The plugin allows Jenkins pipelines to work with Docker and configure Docker agents.

We can install it through:

```text
Jenkins Dashboard
       |
       v
Manage Jenkins
       |
       v
Manage Plugins
       |
       v
Available Plugins
       |
       v
Docker Pipeline
       |
       v
Install
```

The two important components are:

| Component | Responsibility |
|---|---|
| Docker Engine | Creates and manages containers |
| Docker Pipeline Plugin | Enables Docker integration in Jenkins pipelines |

---

## 6. Understanding Jenkins Job Types

Jenkins provides different ways to create and manage jobs.

In this lesson, my teacher mainly compared:

1. Freestyle Project
2. Pipeline Project

### A. Freestyle Project

A Freestyle Project is a traditional way of creating Jenkins jobs.

We configure the job through the Jenkins web interface using different input fields.

For example, we can configure:

- Git repository URL.
- Build commands.
- Test commands.
- Shell scripts.
- Build triggers.

The main limitation is that the job configuration is maintained inside Jenkins rather than as a pipeline file in a version control system.

This makes reviewing, sharing and tracking configuration changes more difficult.

### B. Pipeline Project

A Pipeline Project allows us to define the entire CI/CD workflow using code.

Instead of configuring everything through the Jenkins interface, we write the pipeline in a file called:

```text
Jenkinsfile
```

The Jenkinsfile can be stored in a GitHub repository.

### Advantages of Pipeline as Code

- Pipeline configuration can be stored in GitHub.
- Team members can review pipeline changes.
- Previous versions can be tracked.
- Pipeline code can be shared with other developers.
- Changes can go through pull requests and peer reviews.
- Pipeline configuration can be maintained along with application code.

**Remember:** Pipeline as Code means defining and maintaining the CI/CD pipeline through code instead of configuring every step manually through the Jenkins interface.

---

## 7. Understanding Jenkinsfile Structure

A Jenkinsfile defines the stages and steps that Jenkins should execute.

A Declarative Pipeline generally contains three important components:

1. Agent
2. Stages
3. Steps

### A. Agent

The `agent` defines where Jenkins should execute the pipeline.

Example:

```groovy
agent any
```

This tells Jenkins that the pipeline can run on any available agent.

We can also configure a Docker Agent:

```groovy
agent {
    docker {
        image 'node:18-alpine'
    }
}
```

This tells Jenkins to use a Docker container created from the specified Node.js image.

### B. Stages

`stages` contains the different stages of the pipeline.

Example:

```groovy
stages {
    stage('Build') {
        steps {
            echo 'Building application'
        }
    }

    stage('Test') {
        steps {
            echo 'Testing application'
        }
    }
}
```

Here, the pipeline contains two stages:

- Build
- Test

### C. Steps

`steps` contains the actual commands that Jenkins executes inside a stage.

Example:

```groovy
stage('Test') {
    steps {
        sh 'node --version'
    }
}
```

Here:

- `stage('Test')` defines the stage.
- `steps` contains the commands.
- `sh` executes a shell command.
- `node --version` checks the Node.js version.

### Complete Jenkinsfile Example

```groovy
pipeline {
    agent any

    stages {
        stage('Build') {
            steps {
                echo 'Building application'
            }
        }

        stage('Test') {
            steps {
                echo 'Testing application'
            }
        }

        stage('Deploy') {
            steps {
                echo 'Deploying application'
            }
        }
    }
}
```

### Jenkinsfile Structure

```text
Jenkinsfile
    |
    v
  Agent
    |
    v
  Stages
    |
    +---- Build Stage
    |         |
    |         v
    |       Steps
    |
    +---- Test Stage
    |         |
    |         v
    |       Steps
    |
    +---- Deploy Stage
              |
              v
            Steps
```

---

## 8. What Is Pipeline Syntax in Jenkins?

Jenkins provides a useful feature called Pipeline Syntax.

Imagine we want to check out source code from GitHub but do not know the exact Jenkins pipeline syntax.

Instead of writing everything manually, we can use the Pipeline Syntax generator.

### How It Helps

1. Open a Jenkins Pipeline job.
2. Navigate to Pipeline Syntax.
3. Select the operation we want.
4. Enter the required details.
5. Generate the pipeline script.
6. Copy the generated code into the Jenkinsfile.

It can help generate syntax for operations such as:

- Git checkout.
- Shell commands.
- Other supported Jenkins pipeline operations.

**Purpose:** Pipeline Syntax helps developers generate Jenkins pipeline code without memorizing every syntax.

---

## 9. Multi-Stage and Multi-Agent Pipelines

My teacher next explained how different application components can use different Docker containers.

Imagine an application has three components:

1. Frontend
2. Backend
3. Database

Each component may require a different environment.

| Component | Required Environment |
|---|---|
| Frontend | Node.js |
| Backend | Java and Maven |
| Database | MySQL |

Instead of installing every dependency on one machine, we can use separate Docker containers.

### Example Pipeline

```groovy
pipeline {
    agent none

    stages {
        stage('Frontend') {
            agent {
                docker {
                    image 'node:18-alpine'
                }
            }

            steps {
                sh 'node --version'
            }
        }

        stage('Backend') {
            agent {
                docker {
                    image 'maven:3.9-eclipse-temurin-17'
                }
            }

            steps {
                sh 'mvn --version'
            }
        }
    }
}
```

This is an illustrative example of a multi-stage and multi-agent pipeline.

### What Is `agent none`?

When we use:

```groovy
agent none
```

The pipeline does not allocate one common agent for all stages.

Instead, individual stages can define their own agents.

### How Does It Work?

- The Frontend stage uses a Node.js container.
- The Backend stage uses a Maven container.
- Each stage executes commands in its own environment.

**Purpose:** Multi-stage and multi-agent pipelines allow different application components to use the tools and dependencies they require.

---

## 10. End-to-End CI/CD Using Jenkins, Docker and Kubernetes

The final major topic in this lesson is implementing an end-to-end CI/CD workflow.

My teacher uses an existing Python To-Do application as an example.

The goal is to automate the process from checking out application code to deploying the application to Kubernetes.

### Complete Architecture

```text
          GitHub Repository
          Python Application
                  |
                  v
            Jenkins Pipeline
                  |
          +-------+-------+
          |       |       |
          v       v       v
       Checkout  Build   Push Image
                 Docker  to Docker Hub
                  |
                  v
          Update Kubernetes
          Deployment Manifest
                  |
                  v
          Push Updated Manifest
             to GitHub
                  |
                  v
               Argo CD
                  |
                  v
          Kubernetes Cluster
                  |
                  v
          Application Deployed
```

Let's understand the pipeline stages.

### Stage 1: Checkout Application Code

Jenkins checks out the Python application source code from the GitHub repository.

This provides Jenkins with the application files required for the build.

### Stage 2: Build Docker Image

Jenkins uses the application's Dockerfile to build a Docker image.

Example:

```bash
docker build -t username/todo-app:v1 .
```

This creates a Docker image containing the application and its required environment.

### Stage 3: Push Docker Image

After building the image, Jenkins pushes it to Docker Hub.

```bash
docker push username/todo-app:v1
```

Docker Hub stores the image so that Kubernetes can pull and run it.

### Stage 4: Update Kubernetes Deployment Manifest

Kubernetes uses deployment YAML files to understand which Docker image should run.

For example:

```yaml
containers:
  - name: todo-app
    image: username/todo-app:v1
```

Suppose Jenkins builds a new image with version `v2`.

The deployment manifest is updated:

```yaml
containers:
  - name: todo-app
    image: username/todo-app:v2
```

Jenkins then commits and pushes the updated manifest to GitHub.

### Stage 5: Argo CD Detects the Change

Argo CD continuously monitors the configured Git repository.

When it detects a change in the Kubernetes deployment manifest, it can synchronize the new configuration with the Kubernetes cluster.

### Stage 6: Kubernetes Deploys the Application

Kubernetes pulls the new Docker image and updates the running application according to the deployment configuration.

### Responsibilities of Each Tool

| Tool | Responsibility |
|---|---|
| GitHub | Stores application code and Kubernetes manifests |
| Jenkins | Automates build, testing and image creation |
| Docker | Builds application images |
| Docker Hub | Stores Docker images |
| Argo CD | Synchronizes Git configuration with Kubernetes |
| Kubernetes | Runs the deployed application |

**Important:** Jenkins builds and pushes the image, then updates the Kubernetes manifest in GitHub. Argo CD detects the manifest change and deploys the desired configuration to Kubernetes.

This is an example of GitOps-based Continuous Delivery.

---

## 11. Jenkins and Argo CD – Difference

Both Jenkins and Argo CD are used in the CI/CD process, but they have different responsibilities.

| Jenkins | Argo CD |
|---|---|
| Automates Continuous Integration | Automates Kubernetes delivery |
| Builds applications | Deploys application configurations |
| Runs tests | Monitors Git and cluster state |
| Builds Docker images | Synchronizes Kubernetes resources |
| Pushes images to a registry | Helps maintain the desired state in Kubernetes |

**Simple Understanding:**

Jenkins prepares the application, while Argo CD delivers the application configuration to Kubernetes.

---

## 12. Jenkins Interview Questions

My teacher also discussed common Jenkins interview questions.

### 1. Explain Your CI/CD Workflow

Explain the complete process:

```text
GitHub
   |
   v
Jenkins
   |
   v
Build
   |
   v
Testing and Code Scanning
   |
   v
Docker Image
   |
   v
Container Registry
   |
   v
Kubernetes Deployment
```

Mention Argo CD if the organization uses GitOps for deployment.

The exact stages may change depending on the application and technologies used.

### 2. How Do You Handle Jenkins Worker Node Failures?

We can explain how we:

- Check the worker node's health.
- Inspect CPU and memory usage.
- Check logs and connectivity.
- Investigate why the agent is unavailable.
- Configure monitoring and alerts.
- Use suitable scaling and recovery mechanisms.

Docker Agents can also reduce the need to maintain many permanent worker virtual machines.

### 3. How Do You Install and Expose Jenkins?

Explain the following steps:

1. Launch an EC2 instance.
2. Install Java.
3. Install Jenkins.
4. Start the Jenkins service.
5. Configure the Security Group.
6. Allow the required inbound port.
7. Access Jenkins through a browser.

### 4. Why Use Docker Agents Instead of EC2 Worker Nodes?

Docker Agents provide lightweight and temporary execution environments.

They help:

- Reduce dependency conflicts.
- Avoid maintaining many permanent worker machines.
- Create environments when required.
- Remove containers after execution.
- Use infrastructure resources more efficiently.

---

## 13. Complete Lesson Summary

| Topic | What I Learned |
|---|---|
| Jenkins Controller | Manages and schedules pipeline jobs |
| Jenkins Agent | Executes pipeline tasks |
| Docker Agent | Runs pipeline tasks inside containers |
| Docker Engine | Creates and manages Docker containers |
| Docker Pipeline Plugin | Enables Docker integration in Jenkins pipelines |
| Freestyle Project | Configures jobs through the Jenkins interface |
| Pipeline Project | Defines jobs using pipeline code |
| Jenkinsfile | Stores the pipeline definition |
| Agent | Defines where a pipeline or stage executes |
| Stages | Divides a pipeline into different activities |
| Steps | Contains commands executed inside a stage |
| Multi-Agent Pipeline | Uses different agents for different stages |
| Pipeline Syntax | Helps generate pipeline code |
| Docker Hub | Stores Docker images |
| Argo CD | Synchronizes Git configuration with Kubernetes |
| Kubernetes | Runs the deployed application |

---

## 14. Key Takeaways

- Jenkins can be installed on an AWS EC2 instance.
- Port 8080 is used by default to access the Jenkins web interface.
- Jenkins uses Controllers and Agents to manage and execute jobs.
- Docker containers can be used as temporary Jenkins Agents.
- Docker agents help reduce dependency conflicts and worker maintenance.
- Pipeline as Code is preferred for managing pipeline configurations.
- A Jenkinsfile defines agents, stages and steps.
- Multi-agent pipelines allow different stages to use different environments.
- Jenkins can build Docker images and push them to Docker Hub.
- Jenkins can update Kubernetes manifests stored in GitHub.
- Argo CD can detect Git changes and synchronize the configuration with Kubernetes.

## 15. Final Understanding

In this lesson, I learned how to install Jenkins on an AWS EC2 instance and access it through a browser.

I understood how Jenkins Controllers and Agents work together to execute pipeline jobs.

I also learned how Docker containers can be used as temporary Jenkins Agents instead of maintaining multiple EC2 worker nodes.

I explored Pipeline as Code, Jenkinsfiles, multi-stage pipelines and multi-agent pipelines.

Finally, I understood how Jenkins can build a Docker image, push it to Docker Hub, update Kubernetes manifests in GitHub and work with Argo CD to deploy an application to Kubernetes.

This lesson helped me understand how Jenkins, Docker, GitHub, Argo CD and Kubernetes work together in a real-world CI/CD workflow.
