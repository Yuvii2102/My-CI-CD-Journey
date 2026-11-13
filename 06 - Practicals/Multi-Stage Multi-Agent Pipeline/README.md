# Project 2: Multi-Stage Multi-Agent Pipeline Using Jenkins and Docker ( Theory )

## 1. Project Overview

In this project, I created a Jenkins Pipeline with multiple stages and different Docker agents.

The pipeline contains two stages:

- **Back-end:** Uses a Maven Docker image to display the Maven version.
- **Front-end:** Uses a Node.js Docker image to display the Node.js version.

The main goal was to understand how Jenkins can use different Docker environments for different pipeline stages.

## 2. Tools and Technologies

- AWS EC2
- Ubuntu Server
- Jenkins
- Docker
- Maven
- Node.js
- Groovy (Jenkins Pipeline syntax)

## 3. Concepts Used

### Multi-Stage Pipeline

A multi-stage pipeline divides the CI/CD process into different stages. Each stage performs a specific task.

For example, a pipeline can have Back-end, Front-end, Testing and Deployment stages.

### Multi-Agent Pipeline

An agent defines the environment where Jenkins executes pipeline tasks.

In this project, I used a separate Docker agent for each stage.

| Stage | Docker Image | Purpose |
|---|---|---|
| Back-end | `maven:3.8.1-adoptopenjdk-11` | Provides Maven and Java 11 |
| Front-end | `node:16-alpine` | Provides Node.js 16 |

### Understanding `agent none`

I used `agent none` at the pipeline level.

It means Jenkins does not allocate a global agent for the entire pipeline. Instead, each stage defines its own agent.

This is useful when different stages require different tools and environments.

## 4. Jenkinsfile

I created the following Jenkins Pipeline script:

```groovy
pipeline {
    agent none

    stages {
        stage('Back-end') {
            agent {
                docker {
                    image 'maven:3.8.1-adoptopenjdk-11'
                }
            }

            steps {
                sh 'mvn --version'
            }
        }

        stage('Front-end') {
            agent {
                docker {
                    image 'node:16-alpine'
                }
            }

            steps {
                sh 'node --version'
            }
        }
    }
}
```

## 5. Script Explanation

| Script | Explanation |
|---|---|
| `pipeline` | Defines the Jenkins pipeline. |
| `agent none` | Does not assign a global agent. |
| `stages` | Contains all pipeline stages. |
| `stage('Back-end')` | Creates the Back-end stage. |
| `agent` | Defines the execution environment for the stage. |
| `docker` | Uses Docker as the agent. |
| `image 'maven:3.8.1-adoptopenjdk-11'` | Uses a Maven image with Java 11. |
| `sh 'mvn --version'` | Displays the Maven version. |
| `stage('Front-end')` | Creates the Front-end stage. |
| `image 'node:16-alpine'` | Uses a Node.js 16 Docker image. |
| `sh 'node --version'` | Displays the Node.js version. |

## 6. Execution Flow

The pipeline executes in the following order:

1. Jenkins starts the pipeline without allocating a global agent.
2. Jenkins starts the Back-end stage using the Maven Docker image.
3. It executes `mvn --version` inside the Maven container.
4. After the Back-end stage completes, Jenkins starts the Front-end stage.
5. It uses the Node.js Docker image and executes `node --version`.
6. If both stages execute successfully, the pipeline finishes with a successful build status.

**Note:** Both stages execute sequentially. They do not run in parallel.

## 7. Project 1 vs Project 2

| Feature | Project 1 | Project 2 |
|---|---|---|
| Pipeline stages | One | Two |
| Global agent | Docker | None |
| Stage-level agents | No | Yes |
| Docker images | One | Two |
| Main concept | Docker agent | Multiple agents |

## 8. Expected Output

The Console Output should display the Maven and Node.js versions.

Example:

```text
[Pipeline] stage
[Pipeline] { (Back-end)
+ mvn --version
Apache Maven 3.8.1
...

[Pipeline] stage
[Pipeline] { (Front-end)
+ node --version
v16.20.2
...

Finished: SUCCESS
```

The exact Maven output may contain additional information depending on the Docker image.

## 9. Key Learnings

Through this project, I learned:

- How to create a multi-stage Jenkins Pipeline.
- How `agent none` works.
- How to configure different agents for different stages.
- How to use different Docker images in one pipeline.
- How Jenkins executes stages sequentially.
- How to run Maven and Node.js commands inside Docker containers.

## 10. Final Result

After completing the practical, I verified that Jenkins could execute both stages using their respective Docker environments.

This helped me understand how multiple stages and stage-level Docker agents work in Jenkins Pipelines.
