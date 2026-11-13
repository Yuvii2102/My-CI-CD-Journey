# Project 1: My First Jenkins Pipeline Using Docker ( Practicals )

## 1. Project Overview

In this project, I set up Jenkins on an AWS EC2 instance and created my first Jenkins Pipeline using Docker as the agent.

The main goal was to understand how Jenkins executes pipeline instructions inside a Docker container.

## 2. Tools and Technologies

- AWS EC2
- Ubuntu Server 24.04
- Jenkins
- Docker
- Java 21
- Node.js 16 (Docker image)
- MobaXterm

## 3. Launching the EC2 Instance

I created a new EC2 instance on AWS with the following configuration:

| Configuration | Value |
|---|---|
| Instance Name | Jenkins-DevOps-Projects |
| AMI | Ubuntu Server 24.04 LTS |
| Instance Type | t3.large |
| Storage | 30 GB |
| SSH Port | 22 |
| Jenkins Port | 8080 |

I configured the security group to allow SSH and Jenkins access from my IP address.

After launching the instance, I connected to it using MobaXterm and my downloaded `.pem` key.

## 4. Updating the System

First, I updated Ubuntu and installed some basic tools.

```bash
sudo apt update && sudo apt upgrade -y
sudo apt install -y git curl wget unzip
```

These tools are useful for downloading files, managing repositories and working with the system.

## 5. Installing Docker

I installed Docker because Jenkins needs it to execute pipeline steps inside containers.

```bash
sudo apt install -y docker.io
```

Started and enabled the Docker service:

```bash
sudo systemctl enable --now docker
```

Added my Ubuntu user to the Docker group:

```bash
sudo usermod -aG docker $USER
newgrp docker
```

Verified Docker:

```bash
docker --version
docker run hello-world
```

The `Hello from Docker!` message confirmed that Docker was working.

## 6. Installing Java 21

Jenkins requires Java to run. I installed Java 21 using:

```bash
sudo apt install -y fontconfig openjdk-21-jre
```

Verified the installation:

```bash
java -version
```

## 7. Installing Jenkins

First, I added the Jenkins repository signing key:

```bash
sudo wget -O /etc/apt/keyrings/jenkins-keyring.asc \
https://pkg.jenkins.io/debian-stable/jenkins.io-2026.key
```

Added the Jenkins repository:

```bash
echo "deb [signed-by=/etc/apt/keyrings/jenkins-keyring.asc] https://pkg.jenkins.io/debian-stable binary/" | sudo tee /etc/apt/sources.list.d/jenkins.list > /dev/null
```

Updated the package list and installed Jenkins:

```bash
sudo apt update
sudo apt install -y jenkins
```

Started Jenkins and enabled it on system startup:

```bash
sudo systemctl enable --now jenkins
```

Checked the Jenkins service:

```bash
sudo systemctl status jenkins
```

The service showed `active (running)`.

## 8. Giving Jenkins Permission to Use Docker

Since our pipeline uses Docker as an agent, Jenkins needs permission to communicate with Docker.

I added the Jenkins user to the Docker group:

```bash
sudo usermod -aG docker jenkins
```

Restarted Jenkins:

```bash
sudo systemctl restart jenkins
```

Verified Docker access for Jenkins:

```bash
sudo -u jenkins docker run hello-world
```

I received the `Hello from Docker!` message, confirming that Jenkins could access Docker successfully.

## 9. Initial Jenkins Configuration

I opened Jenkins using my EC2 public IP address:

```text
http://<EC2-PUBLIC-IP>:8080
```

Retrieved the initial administrator password:

```bash
sudo cat /var/lib/jenkins/secrets/initialAdminPassword
```

I copied the password into the Jenkins setup page and completed the initial configuration.

I selected **Install suggested plugins** and created my Jenkins administrator account.

## 10. Installing Docker Pipeline Plugin

I installed the Docker Pipeline plugin because our Jenkinsfile uses Docker as its pipeline agent.

Steps followed:

1. Opened Manage Jenkins.
2. Selected Plugins.
3. Opened Available plugins.
4. Searched for Docker Pipeline.
5. Installed the plugin.

## 11. Creating the First Jenkins Pipeline

I created a new Jenkins job with the following details:

- **Item Name:** `my-first-pipeline`
- **Job Type:** Pipeline
- **Definition:** Pipeline script

I pasted the following Jenkinsfile into the Pipeline script section.

### Jenkinsfile

```groovy
pipeline {
    agent {
        docker {
            image 'node:16-alpine'
        }
    }

    stages {
        stage('Test') {
            steps {
                sh 'node --version'
            }
        }
    }
}
```

### Short Explanation of the Script

| Script | Explanation |
|---|---|
| `pipeline` | Defines the Jenkins pipeline. |
| `agent` | Specifies where the pipeline runs. |
| `docker` | Tells Jenkins to use Docker as the agent. |
| `image 'node:16-alpine'` | Uses the Node.js 16 Alpine Docker image. |
| `stages` | Contains the stages of the pipeline. |
| `stage('Test')` | Creates a stage named Test. |
| `steps` | Contains the commands to execute. |
| `sh 'node --version'` | Runs a shell command to display the Node.js version. |

## 12. Executing the Pipeline

After saving the Jenkins job, I clicked **Build Now** to execute the pipeline.

I opened Build History, selected Build #1 and checked the Console Output.

### Expected Output

```text
+ node --version
v16.20.2

Finished: SUCCESS
```

### What Happened During Execution?

1. Jenkins started the pipeline.
2. Jenkins requested Docker to start a container using `node:16-alpine`.
3. The container provided the Node.js environment.
4. Jenkins executed `node --version` inside the container.
5. Node.js displayed version `v16.20.2`.
6. After execution, Jenkins stopped and removed the temporary container.

<End of Project 1>

## 13. Final Result

<badge>SUCCESS</badge>

My first Jenkins Pipeline executed successfully.

Through this practical, I learned how to install Jenkins on an AWS EC2 instance, configure Docker integration and execute a simple pipeline using a Docker agent.

## 14. Key Learnings

- Installed and configured Jenkins on AWS EC2.
- Understood how Jenkins works with Docker.
- Learned how to create a Jenkins Pipeline job.
- Understood the basic structure of a Jenkinsfile.
- Executed shell commands inside a Docker container.
- Verified pipeline execution using Console Output.
