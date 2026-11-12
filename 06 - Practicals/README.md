# Jenkins Practical: Docker Agents and Multi-Agent Pipelines

## 1. Introduction

In this practical, I learned how to configure Jenkins with Docker and execute CI/CD pipelines using Docker containers as Jenkins Agents.

I started by installing Jenkins on an AWS EC2 instance. Then I installed Docker, configured Jenkins to access Docker and created different Jenkins pipelines.

The main topics I covered were:

1. Installing Jenkins on AWS EC2.
2. Installing and configuring Docker.
3. Connecting Jenkins with Docker.
4. Installing the Docker Pipeline Plugin.
5. Creating my first Jenkins Pipeline.
6. Running a pipeline using a Docker Agent.
7. Creating a Multi-Stage, Multi-Agent Pipeline.
8. Using different Docker images for different pipeline stages.

---

## 2. Installing Jenkins on AWS EC2

I started by launching an Ubuntu EC2 instance on AWS.

### EC2 Configuration

| Configuration | Value |
|---|---|
| Operating System | Ubuntu |
| Instance Type | t3.medium |
| Storage | 20 GB |
| Service | Jenkins |

### Step 1: Update the packages

```bash
sudo apt update
```

### Step 2: Install Java 21

Jenkins requires Java to run. I installed Java 21 using:

```bash
sudo apt install fontconfig openjdk-21-jre -y
```

Verify Java:

```bash
java -version
```

### Step 3: Add the Jenkins repository

```bash
sudo wget -O /etc/apt/keyrings/jenkins-keyring.asc \
https://pkg.jenkins.io/debian-stable/jenkins.io-2026.key
```

Add the Jenkins repository:

```bash
echo "deb [signed-by=/etc/apt/keyrings/jenkins-keyring.asc]" \
https://pkg.jenkins.io/debian-stable binary/ | \
sudo tee /etc/apt/sources.list.d/jenkins.list > /dev/null
```

Update the package list:

```bash
sudo apt update
```

### Step 4: Install Jenkins

```bash
sudo apt install jenkins -y
```

### Step 5: Start Jenkins

```bash
sudo systemctl start jenkins
sudo systemctl enable jenkins
```

Check Jenkins status:

```bash
sudo systemctl status jenkins
```

I verified that the Jenkins service was running successfully.

### Step 6: Configure the Security Group

I allowed the following inbound traffic in the EC2 Security Group:

| Port | Purpose |
|---|---|
| 22 | SSH access |
| 8080 | Jenkins web interface |

I accessed Jenkins through:

```text
http://<EC2-Public-IP>:8080
```

### Step 7: Unlock Jenkins

I retrieved the initial administrator password using:

```bash
sudo cat /var/lib/jenkins/secrets/initialAdminPassword
```

Then I completed the initial configuration:

1. Entered the administrator password.
2. Selected Install Suggested Plugins.
3. Created an administrator account.
4. Completed the Jenkins setup.

After that, Jenkins was ready to use.

---

## 3. Installing Docker on EC2

After setting up Jenkins, I installed Docker on the same EC2 instance.

Docker allows us to create and run containers that provide separate execution environments for applications.

### Step 1: Install Docker

```bash
sudo apt update
sudo apt install docker.io -y
```

### Step 2: Start Docker

```bash
sudo systemctl start docker
sudo systemctl enable docker
```

Verify Docker:

```bash
sudo systemctl status docker
```

I confirmed that the Docker service was running.

---

## 4. Configuring Jenkins to Access Docker

One important thing I learned is that Jenkins runs using a separate Linux user called `jenkins`.

By default, this user does not automatically have permission to execute Docker commands.

To allow Jenkins to communicate with the Docker daemon, I added the Jenkins user to the Docker group.

### Step 1: Add Jenkins to the Docker group

```bash
sudo usermod -aG docker jenkins
```

I also added the Ubuntu user:

```bash
sudo usermod -aG docker ubuntu
```

### Understanding the command

| Command | Purpose |
|---|---|
| `usermod` | Modifies a Linux user |
| `-a` | Appends the user to an additional group |
| `-G` | Specifies the group |
| `docker` | Docker group |
| `jenkins` | Jenkins Linux user |

### Step 2: Restart services

```bash
sudo systemctl restart docker
sudo systemctl restart jenkins
```

### Step 3: Verify Docker access as Jenkins

I executed:

```bash
sudo -u jenkins docker run hello-world
```

The command executed successfully and displayed:

```text
Hello from Docker!

This message shows that your installation
appears to be working correctly.
```

### What did I verify?

- Docker was installed successfully.
- The Docker daemon was running.
- The Jenkins user could communicate with Docker.
- Docker could pull an image from Docker Hub.
- A container could be created and executed successfully.

This confirmed that Docker was ready to be integrated with Jenkins.

**Security Note:** Membership in the Docker group provides highly privileged access and can effectively grant root-level permissions. This configuration was used for my learning environment.

---

## 5. Installing Docker Pipeline Plugin

To use Docker containers inside Jenkins pipelines, I installed the Docker Pipeline Plugin.

### Installation Steps

1. Opened the Jenkins Dashboard.
2. Clicked the Settings icon.
3. Opened Plugins.
4. Selected Available plugins.
5. Searched for Docker Pipeline.
6. Selected the plugin.
7. Clicked Install.

During installation, Jenkins also installed the required dependencies:

- Authentication Tokens API
- Docker Commons
- Docker Pipeline

All plugins were installed successfully.

I then restarted Jenkins to load the installed plugins.

### Why is Docker Pipeline Plugin required?

The Docker Pipeline Plugin allows Jenkins pipelines to build and use Docker containers.

It provides Docker-related functionality inside Jenkins pipeline scripts.

---

## 6. Understanding Jenkins Controller and Agents

Before creating pipelines, I understood the basic Jenkins architecture.

Jenkins mainly uses two important components.

### A. Jenkins Controller

The Controller is the central component of Jenkins.

Its responsibilities include:

- Managing Jenkins jobs and pipelines.
- Scheduling pipeline executions.
- Managing Jenkins Agents.
- Coordinating pipeline activities.
- Displaying build results.

### B. Jenkins Agent

An Agent is an execution environment where Jenkins runs pipeline tasks.

For example, different applications may require different tools:

| Application | Required Tool |
|---|---|
| Java | JDK and Maven |
| Node.js | Node.js and npm |
| Python | Python |

Instead of installing all these dependencies on one machine, Jenkins can use different agents to execute pipeline tasks.

### Traditional Jenkins Architecture

```text
              Jenkins Controller
                      |
          +-----------+-----------+
          |           |           |
          v           v           v
        Agent 1     Agent 2     Agent 3
         Java       Node.js     Python
```

### Why use Docker Agents?

Docker containers can provide temporary execution environments for Jenkins pipelines.

Instead of maintaining separate permanent worker machines for every application, Jenkins can create containers using the required Docker images.

For example:

- `node:18-alpine` for Node.js.
- `maven:3.9-eclipse-temurin-17` for Java and Maven.

This helps reduce dependency conflicts and makes pipeline environments easier to manage.

---

## 7. Practical 1 – My First Jenkins Pipeline Using Docker Agent

After configuring Docker and Jenkins, I created my first Jenkins Pipeline.

### Step 1: Create a Pipeline Job

From the Jenkins Dashboard:

1. Clicked New Item.
2. Entered the job name `first-docker-pipeline`.
3. Selected Pipeline.
4. Clicked OK.

### Step 2: Configure the Pipeline

Under the Pipeline section:

- Definition: Pipeline script
- Use Groovy Sandbox: Enabled

I added the following pipeline script.

### Jenkinsfile

```groovy
pipeline {
    agent {
        docker {
            image 'alpine:latest'
        }
    }

    stages {
        stage('Hello') {
            steps {
                echo 'Hello from Jenkins!'
            }
        }

        stage('Check Docker Agent') {
            steps {
                sh 'echo Running inside a Docker container'
                sh 'cat /etc/os-release'
            }
        }

        stage('Complete') {
            steps {
                echo 'My first Docker Agent pipeline is successful!'
            }
        }
    }
}
```

### Understanding the Jenkinsfile

**1. Pipeline**

The `pipeline` block defines the complete Jenkins pipeline.

**2. Agent**

```groovy
agent {
    docker {
        image 'alpine:latest'
    }
}
```

This tells Jenkins to use a Docker container created from the Alpine image as the pipeline execution environment.

**3. Stages**

The `stages` block contains different activities in the pipeline.

**4. Steps**

The `steps` block contains the commands executed inside each stage.

### Understanding the Pipeline Stages

| Stage | Purpose |
|---|---|
| Hello | Prints a welcome message |
| Check Docker Agent | Checks whether commands are running inside Alpine Linux |
| Complete | Prints the completion message |

### Step 3: Execute the Pipeline

I saved the pipeline and clicked Build Now.

Jenkins executed the pipeline successfully.

### Important Console Output

Initially, Jenkins checked whether the Alpine image was available locally.

```bash
docker inspect -f . alpine:latest
```

Since the image was not available locally, Docker pulled it from Docker Hub.

```bash
docker pull alpine:latest
```

Jenkins then created a temporary container:

```bash
docker run -t -d alpine:latest cat
```

The pipeline executed the following commands:

```bash
echo 'Running inside a Docker container'
cat /etc/os-release
```

The output confirmed:

```text
NAME="Alpine Linux"
ID=alpine
VERSION_ID=3.24.4
PRETTY_NAME="Alpine Linux v3.24"
```

After the pipeline completed, Jenkins stopped and removed the temporary container.

```bash
docker stop <container-id>
docker rm -f --volumes <container-id>
```

### Final Result

```text
My first Docker Agent pipeline is successful!

Finished: SUCCESS
```

**Practical Result:** I successfully executed my first Jenkins Pipeline using an Alpine Docker container as an Agent.

---

## 8. Practical 2 – Multi-Stage, Multi-Agent Pipeline

After completing the first pipeline, I created another pipeline to understand how different stages can use different Docker containers.

For this practical, I used:

1. Node.js Docker image for the Frontend stage.
2. Maven Docker image for the Backend stage.

### Step 1: Create a New Pipeline Job

I created another Jenkins job with the name:

```text
multi-stage-multi-agent
```

I selected Pipeline and opened the Pipeline configuration page.

### Step 2: Configure the Jenkinsfile

I used `agent none` because I wanted individual stages to define their own execution environments.

### Jenkinsfile

```groovy
pipeline {
    agent none

    stages {
        stage('Frontend - Node.js') {
            agent {
                docker {
                    image 'node:18-alpine'
                }
            }

            steps {
                echo 'Running Frontend Stage'

                sh 'node --version'
                sh 'npm --version'
            }
        }

        stage('Backend - Maven') {
            agent {
                docker {
                    image 'maven:3.9-eclipse-temurin-17'
                }
            }

            steps {
                echo 'Running Backend Stage'

                sh 'mvn --version'
                sh 'java -version'
            }
        }

        stage('Pipeline Completed') {
            agent any

            steps {
                echo 'Multi-Stage Multi-Agent Pipeline Completed Successfully!'
            }
        }
    }
}
```

### Understanding `agent none`

Normally, a Jenkins pipeline can define one agent for the entire pipeline.

However:

```groovy
agent none
```

means that the pipeline does not allocate one common agent for all its stages.

Instead, each stage can define its own agent.

### Stage 1: Frontend – Node.js

```groovy
stage('Frontend - Node.js') {
    agent {
        docker {
            image 'node:18-alpine'
        }
    }
}
```

For this stage, Jenkins used the Node.js Docker image.

It executed:

```bash
node --version
npm --version
```

Console Output:

```text
v18.20.8
10.8.2
```

This confirmed that Node.js and npm were available inside the Docker container.

After completing the stage, Jenkins stopped and removed the temporary container.

### Stage 2: Backend – Maven

```groovy
stage('Backend - Maven') {
    agent {
        docker {
            image 'maven:3.9-eclipse-temurin-17'
        }
    }
}
```

For this stage, Jenkins used a Maven Docker image containing Java 17.

It executed:

```bash
mvn --version
java -version
```

Console Output:

```text
Apache Maven 3.9.16

Java version: 17.0.20.1
```

This confirmed that Maven and Java were available inside the Maven Docker container.

After completing the stage, Jenkins also stopped and removed this temporary container.

### Stage 3: Pipeline Completed

The final stage used:

```groovy
agent any
```

This allowed Jenkins to execute the final stage on any available Jenkins agent.

The command executed:

```groovy
echo 'Multi-Stage Multi-Agent Pipeline Completed Successfully!'
```

### Final Result

```text
Multi-Stage Multi-Agent Pipeline Completed Successfully!

Finished: SUCCESS
```

**Practical Result:** I successfully created and executed a Multi-Stage, Multi-Agent Jenkins Pipeline using separate Docker containers for Node.js and Maven.

---

## 9. Understanding the Complete Multi-Agent Architecture

The practical helped me understand how Jenkins can use different Docker containers for different pipeline stages.

```text
             Jenkins Controller
                     |
                     |
             Jenkins Pipeline
                     |
             agent none
                     |
          +----------+----------+
          |                     |
          v                     v
    Frontend Stage         Backend Stage
          |                     |
          v                     v
    Node.js Container      Maven Container
          |                     |
          v                     v
     Node.js Check          Maven Check
     npm Check              Java Check
          |                     |
          v                     v
     Container Removed    Container Removed
          |                     |
          +----------+----------+
                     |
                     v
             Pipeline Completed
                     |
                     v
              Finished: SUCCESS
```

### Tools and Technologies Used

| Tool | Purpose |
|---|---|
| AWS EC2 | Hosted Jenkins |
| Ubuntu | Operating system |
| Java 21 | Runtime for Jenkins |
| Jenkins | CI/CD automation |
| Docker | Containerization |
| Docker Hub | Docker image registry |
| Docker Pipeline Plugin | Docker integration with Jenkins |
| Alpine Linux | First Docker Agent environment |
| Node.js | Frontend execution environment |
| Maven | Java build environment |

---

## 10. What I Learned

Through these practicals, I learned:

1. How to install Jenkins on an AWS EC2 instance.
2. How to install and configure Docker on Ubuntu.
3. How to give Jenkins permission to access Docker.
4. How to install the Docker Pipeline Plugin.
5. How Jenkins Controllers and Agents work.
6. How to create Jenkins Pipeline jobs.
7. How to write a basic Jenkinsfile.
8. How to use Docker containers as Jenkins Agents.
9. How to execute pipeline commands inside Docker containers.
10. How to use `agent none` in a Declarative Pipeline.
11. How to configure different Docker images for different stages.
12. How Jenkins automatically stops and removes temporary Docker containers after execution.

## 11. Final Summary

In this practical, I started by installing Jenkins on an AWS EC2 instance and configuring Docker to work with Jenkins.

I successfully executed my first Jenkins Pipeline using an Alpine Docker container.

After that, I created a Multi-Stage, Multi-Agent Pipeline using Node.js and Maven Docker images.

I verified that each stage used its own Docker execution environment and that Jenkins automatically cleaned up the containers after execution.

These practicals helped me understand how Docker Agents work in Jenkins and how different applications can use different environments within the same CI/CD pipeline.

**Next Practical:** Building Java and Node.js applications using Jenkins Multi-Stage, Multi-Agent Pipelines.
