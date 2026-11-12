# End-to-End CI/CD Pipeline for a Java Application Using Jenkins, Maven, SonarQube, Docker, Argo CD, Helm and Kubernetes

## 1. Introduction

In this project, I am learning how to build an end-to-end CI/CD pipeline for a Java application.

Earlier, I learned individual DevOps tools like Git, GitHub, Docker, Jenkins, Kubernetes, Helm and Argo CD. Now I want to understand how these tools work together in a real-world project.

The main goal of this project is to automate the process of building, testing, analyzing, packaging and deploying a Java application.

Instead of manually performing every step, I will use Jenkins to automate the CI process and Argo CD to manage application deployment in Kubernetes.

## 2. What is CI/CD?

CI/CD stands for Continuous Integration and Continuous Delivery or Continuous Deployment.

It is a process that helps developers build, test and deploy applications automatically.

Without CI/CD, developers need to manually build the application, test it, create Docker images and deploy it to servers.

With CI/CD, most of these tasks can be automated through a pipeline.

### Continuous Integration (CI)

Continuous Integration is the practice of frequently adding code changes to a shared Git repository.

Whenever a developer pushes new code to GitHub, Jenkins can automatically start a pipeline.

The pipeline can:

- Download the latest source code.
- Build the application.
- Run unit tests.
- Check code quality.
- Create a Docker image.
- Push the image to Docker Hub.

The main goal of CI is to identify problems early and make sure that new code changes do not break the application.

### Continuous Delivery (CD)

Continuous Delivery is the process of preparing an application for deployment.

After the CI process is completed, the application is ready to be deployed.

The deployment process can be triggered manually after approval.

### Continuous Deployment

Continuous Deployment takes automation one step further.

Whenever new code passes all the required checks, the changes can automatically reach the production environment without manual approval.

In this project, Jenkins handles CI and Argo CD handles continuous delivery to Kubernetes.

## 3. Understanding the Tools Used in This Project

### 3.1 Git and GitHub

Git is a version control system used to track changes in source code.

GitHub is a platform where developers can store and manage their Git repositories.

In this project:

- The Java application code is stored in GitHub.
- Jenkins downloads the source code from GitHub.
- Kubernetes deployment files are also stored in GitHub.
- Argo CD continuously monitors the deployment repository for changes.

### 3.2 Jenkins

Jenkins is an open-source automation server used to automate tasks in software development.

It helps us create pipelines that perform multiple tasks automatically.

In this project, Jenkins is responsible for:

- Checking out the source code.
- Building the Java application.
- Running tests.
- Performing SonarQube analysis.
- Building Docker images.
- Pushing images to Docker Hub.
- Updating the Kubernetes deployment configuration in GitHub.

Jenkins uses a file called `Jenkinsfile` to define the pipeline stages.

### 3.3 Maven

Maven is a build automation and dependency management tool mainly used for Java projects.

It helps us manage project dependencies and build Java applications.

The main configuration file used by Maven is:

`pom.xml`

This file contains:

- Project information.
- Java version.
- Dependencies.
- Build configuration.
- Plugins.

Some commonly used Maven commands:

| Command | Purpose |
|---|---|
| `mvn clean` | Removes previous build files |
| `mvn compile` | Compiles Java source code |
| `mvn test` | Runs unit tests |
| `mvn package` | Creates the JAR or WAR package |
| `mvn clean package` | Cleans, builds and packages the application |

In this project, Maven builds the Java application and generates a JAR file.

### 3.4 SonarQube

SonarQube is a code quality and security analysis tool.

It checks source code and helps developers identify problems before deploying an application.

It can identify:

- Bugs.
- Code smells.
- Security vulnerabilities.
- Duplicated code.
- Maintainability issues.

In this project, Jenkins sends the Java source code to SonarQube for analysis.

SonarQube analyzes the code and generates a report showing its quality.

### 3.5 Docker

Docker is a containerization platform used to package applications along with their required dependencies.

It helps applications run consistently across different environments.

In this project:

1. Maven builds the Java application.
2. A JAR file is generated.
3. Docker uses the Dockerfile to create an image.
4. The image contains the Java application and the required runtime.
5. The image is pushed to Docker Hub.

The Dockerfile defines how the Docker image should be created.

### 3.6 Docker Hub

Docker Hub is a container image registry where we can store and share Docker images.

After Jenkins builds the Docker image, it pushes the image to Docker Hub.

Kubernetes can later pull this image and use it to run application containers.

For example:

`abhishekf5/ultimate-cicd:1`

Here:

- `abhishekf5` is the Docker Hub username.
- `ultimate-cicd` is the image name.
- `1` is the image tag.

### 3.7 Kubernetes

Kubernetes is a container orchestration platform.

It helps us deploy, manage and scale containerized applications.

In this project, Kubernetes is responsible for running the Java application.

Some important Kubernetes resources used in this project are:

**Deployment**

A Deployment manages application Pods.

It makes sure that the required number of application replicas are running.

For example:

```yaml
replicas: 2
```

This tells Kubernetes to maintain two application Pods.

**Pod**

A Pod is the smallest deployable unit in Kubernetes. It runs one or more containers.

In this project, our Java application runs inside a container within a Pod.

**Service**

A Service provides a stable way to access application Pods.

It helps other applications or users communicate with the application.

We use a NodePort Service in this project to expose the application through a port on the Kubernetes nodes.

### 3.8 Helm

Helm is a package manager for Kubernetes.

Instead of managing many Kubernetes YAML files separately, Helm allows us to organize them into a package called a Helm Chart.

A Helm Chart can contain:

- Deployment templates.
- Service templates.
- ConfigMaps.
- Secrets.
- Values files.

The `values.yaml` file contains configurable values such as the Docker image, replica count and service type.

Helm makes it easier to install, upgrade and manage Kubernetes applications.

### 3.9 Argo CD

Argo CD is a GitOps-based continuous delivery tool for Kubernetes.

It continuously monitors a Git repository containing Kubernetes deployment configurations.

Argo CD compares the configuration stored in Git with the actual state of the Kubernetes cluster.

If there is a difference, Argo CD can synchronize the cluster with the desired configuration.

For example:

- Jenkins builds a new Docker image.
- Jenkins pushes it to Docker Hub.
- Jenkins updates the image tag in the GitHub deployment repository.
- Argo CD detects the Git change.
- Argo CD synchronizes the changes with Kubernetes.
- Kubernetes deploys the updated application.

This approach is called GitOps.

## 4. Understanding the Complete CI/CD Architecture

The complete workflow contains two main parts.

### Part 1: Continuous Integration Using Jenkins

1. A developer pushes Java application code to GitHub.
2. GitHub sends a webhook notification to Jenkins.
3. Jenkins starts the pipeline.
4. Jenkins checks out the source code.
5. Maven builds the Java application.
6. Unit tests are executed.
7. SonarQube performs code quality analysis.
8. Jenkins builds a Docker image.
9. Jenkins pushes the image to Docker Hub.

### Part 2: Continuous Delivery Using Argo CD

10. Jenkins updates the Docker image tag in the Kubernetes manifests repository.
11. Argo CD detects the changes in GitHub.
12. Argo CD synchronizes the updated configuration with Kubernetes.
13. Kubernetes pulls the latest Docker image.
14. Kubernetes creates or updates the application Pods.
15. The updated Java application becomes available to users.

## 5. What is a Jenkins Pipeline?

A Jenkins Pipeline is a collection of automated steps used to build, test and deploy an application.

These steps are called stages.

A pipeline is generally written inside a file called `Jenkinsfile`.

A Jenkinsfile uses Groovy-based Pipeline syntax.

Some important Jenkins Pipeline terms:

**Pipeline:** The complete automation process.

**Agent:** Specifies where the pipeline or its stages will execute.

**Stage:** Represents a major step in the pipeline.

**Steps:** Contains the commands or operations performed inside a stage.

**Environment:** Defines environment variables and credentials used by the pipeline.

**Post:** Defines actions that should run after the pipeline or a stage completes.

Example:

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
                echo 'Running tests'
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

This is a simple example of a declarative Jenkins pipeline.

## 6. Understanding Docker Image Versioning

Whenever Jenkins builds a new Docker image, we need to give it a unique tag.

For example:

```text
ultimate-cicd:1
ultimate-cicd:2
ultimate-cicd:3
```

In this project, Jenkins uses the `BUILD_NUMBER` environment variable to generate image tags.

For example:

```groovy
DOCKER_IMAGE = "abhishekf5/ultimate-cicd:${BUILD_NUMBER}"
```

If the Jenkins build number is 5, the image will be:

```text
abhishekf5/ultimate-cicd:5
```

This helps us identify different versions of the application.

It also makes it easier to roll back to an older image when needed.

## 7. Understanding GitOps

GitOps is an approach where Git acts as the source of truth for the desired state of an application.

Instead of manually changing resources inside Kubernetes, we update the configuration stored in Git.

Argo CD monitors the Git repository and makes sure that the Kubernetes cluster matches the configuration stored there.

For example:

Suppose the GitHub deployment file contains:

```yaml
replicas: 2
```

But someone manually changes the Kubernetes deployment to three replicas.

Argo CD can detect this difference.

Depending on its synchronization and self-healing configuration, Argo CD can bring the cluster back to the desired state of two replicas.

This helps maintain consistency between Git and Kubernetes.

## 8. Understanding the Important Project Files

The reference repository contains the following structure:

```text
java-maven-sonar-argocd-helm-k8s/
│
├── Argo CD/
│   └── argocd-basic.yaml
│
├── spring-boot-app-manifests/
│   ├── deployment.yml
│   └── service.yml
│
├── spring-boot-app/
│   ├── src/
│   ├── Dockerfile
│   ├── JenkinsFile
│   ├── pom.xml
│   └── README.md
│
└── README.md
```

### spring-boot-app

This directory contains the Java application.

| File or Directory | Purpose |
|---|---|
| `src/` | Contains Java source code |
| `pom.xml` | Maven project configuration |
| `Dockerfile` | Instructions to build Docker image |
| `JenkinsFile` | Defines the Jenkins pipeline |
| `README.md` | Application documentation |

### spring-boot-app-manifests

This directory contains Kubernetes deployment configurations.

**deployment.yml**

Defines how the Java application should run inside Kubernetes.

It specifies the Docker image, number of replicas, container name and container port.

**service.yml**

Defines how users or other services can access the Java application.

### Argo CD

The reference repository contains `argocd-basic.yaml`.

This file defines an Argo CD custom resource for installations using the Argo CD Operator.

It is not the same as an Argo CD Application manifest.

An Argo CD Application manifest is used to connect Argo CD with a Git repository and Kubernetes destination.

We will understand and configure this during the practical.

## 9. Understanding Webhooks

A webhook is a mechanism used by one application to notify another application when an event occurs.

In this project, GitHub sends a webhook notification to Jenkins whenever a developer pushes new code.

The notification tells Jenkins that new changes are available.

Jenkins can then automatically trigger the pipeline.

Without a webhook, we may need to manually start the pipeline or configure periodic polling.

## 10. Understanding Jenkins Credentials

During CI/CD, Jenkins needs to access external services such as GitHub, Docker Hub and SonarQube.

We should not directly write passwords or access tokens inside the Jenkinsfile.

Instead, Jenkins provides a Credentials Manager where we can securely store these details.

Examples:

| Credential | Purpose |
|---|---|
| GitHub Token | Allows Jenkins to push deployment file changes |
| Docker Hub Credentials | Allows Jenkins to push Docker images |
| SonarQube Token | Allows Jenkins to authenticate with SonarQube |
| Argo CD Credentials | Used when Jenkins needs to interact with Argo CD APIs |

Credentials are accessed inside the pipeline when required.

## 11. What is a Quality Gate?

A Quality Gate is a set of conditions used to decide whether the analyzed code meets the required quality standards.

SonarQube checks the code against these conditions.

For example, the Quality Gate may check:

- Code coverage.
- Bugs.
- Vulnerabilities.
- Code smells.
- Duplicated code.

If the Quality Gate fails, the pipeline can be configured to stop before creating or deploying the Docker image.

This helps prevent poor-quality code from moving further into the deployment process.

## 12. Difference Between Jenkins and Argo CD

Both Jenkins and Argo CD are important in this project, but they have different responsibilities.

| Jenkins | Argo CD |
|---|---|
| Automation server | GitOps continuous delivery tool |
| Builds applications | Synchronizes applications with Kubernetes |
| Runs tests | Monitors deployment configuration |
| Performs code analysis through SonarQube integration | Detects differences between Git and cluster state |
| Builds Docker images | Applies desired configuration to Kubernetes |
| Pushes images to Docker Hub | Helps Kubernetes deploy the updated image |

In simple words:

**Jenkins builds the application and prepares it for deployment. Argo CD makes sure the application is deployed according to the configuration stored in Git.**

## 13. What I Will Build in This Project

By completing this project, I will understand how different DevOps tools work together in a real-world CI/CD workflow.

I will work on:

1. Cloning and understanding a Java Spring Boot application.
2. Building the application using Maven.
3. Installing and configuring SonarQube.
4. Performing code quality analysis.
5. Creating a Docker image.
6. Pushing the image to Docker Hub.
7. Creating a Jenkins pipeline using Jenkinsfile.
8. Configuring GitHub webhooks.
9. Configuring Jenkins credentials.
10. Preparing Kubernetes deployment and service configurations.
11. Understanding Helm Charts and deploying applications using Helm.
12. Installing and configuring Argo CD.
13. Connecting Argo CD with a GitHub repository.
14. Automating application deployment using GitOps.
15. Testing the complete CI/CD workflow.

## 14. Final Understanding

Before starting this project, I had learned Jenkins, Docker, Kubernetes, Helm and Argo CD separately.

Now I want to understand how these tools work together to automate the complete application delivery process.

The most important thing I learned from this architecture is that each tool has a specific responsibility.

- GitHub stores the source code and deployment configurations.
- Jenkins automates the build and testing process.
- Maven builds the Java application.
- SonarQube checks code quality.
- Docker packages the application.
- Docker Hub stores the Docker images.
- Kubernetes runs the application.
- Helm manages Kubernetes application packages.
- Argo CD follows GitOps and synchronizes deployments.

By connecting all these tools, we can create an automated CI/CD pipeline that reduces manual work and makes application deployment easier and more reliable.

**My next step is to start the practical implementation and understand each stage by doing it myself.**
