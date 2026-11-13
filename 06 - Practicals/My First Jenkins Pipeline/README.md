# Project 1: My First Jenkins Pipeline

## 1. Introduction

In this project, I created my first Jenkins pipeline using a Declarative Pipeline.

The main purpose of this project is to verify whether Jenkins can use Docker as an agent and execute commands inside a Docker container.

For this, I used the Node.js 16 Alpine Docker image and executed a simple command to check the Node.js version.

## 2. What is Jenkins Pipeline?

A Jenkins Pipeline is a set of instructions that tells Jenkins how to perform a task.

It helps automate different stages of the software development process such as building, testing and deploying applications.

We define these instructions inside a file called `Jenkinsfile`.

## 3. What is a Jenkinsfile?

A Jenkinsfile is a text file that contains the pipeline instructions written using Groovy-based Pipeline syntax.

It defines:
- Where the pipeline should run.
- What stages should be executed.
- Which commands should be performed.

In this project, I used a Declarative Jenkinsfile.

## 4. What is a Docker Agent?

A Docker Agent allows Jenkins to execute pipeline steps inside a Docker container.

Instead of installing every required tool directly on the Jenkins server, we can use a Docker image that already contains the required environment.

In this project, I used:

`node:16-alpine`

This image provides Node.js 16 in a lightweight Alpine Linux environment.

## 5. Understanding the Pipeline

My Jenkinsfile contains the following main sections:

### Pipeline
Defines the complete Jenkins pipeline.

### Agent
Specifies where the pipeline should execute.

### Docker
Tells Jenkins to use a Docker container as the execution environment.

### Image
Specifies which Docker image should be used.

### Stages
Contains the different stages of the pipeline.

### Stage
Represents one particular task. In this project, the stage is named `Test`.

### Steps
Contains the commands that Jenkins needs to execute.

### Shell Command
The command `node --version` checks the installed Node.js version inside the Docker container.

## 6. Project Workflow

1. Jenkins starts the pipeline.
2. Jenkins requests a Docker agent.
3. Docker pulls the `node:16-alpine` image if it is not already available.
4. Jenkins executes the pipeline inside the container.
5. The `Test` stage runs.
6. The command `node --version` displays the Node.js version.
7. Jenkins marks the pipeline as successful if the command executes successfully.

## 7. Tools and Technologies

- Jenkins – Pipeline automation.
- Docker – Container platform.
- Node.js 16 – JavaScript runtime.
- Alpine Linux – Lightweight Linux distribution.
- Jenkinsfile – Pipeline instructions.

## 8. Expected Output

The pipeline should display a Node.js version similar to:

`v16.x.x`

The Jenkins build should show **SUCCESS**.

## 9. What I Learned

- How to create a basic Jenkins Declarative Pipeline.
- How to write and use a Jenkinsfile.
- How to configure Docker as a Jenkins agent.
- How Jenkins executes commands inside a Docker container.
- How to verify the execution environment using a shell command.

## 10. Conclusion

Through this project, I learned how Jenkins can use Docker containers as agents to execute pipeline tasks.

This is my first step towards understanding Jenkins automation and building more advanced CI/CD pipelines.
