
# Project 2: Multi-Stage Multi-Agent Pipeline Using Jenkins and Docker ( Practicals )

## 1. Project Overview

In this project, I created a Jenkins Pipeline with two stages using different Docker agents.

- **Back-end:** Used a Maven Docker image to check the Maven version.
- **Front-end:** Used a Node.js Docker image to check the Node.js version.

The main goal was to understand how Jenkins can use different Docker environments for different stages.

## 2. Tools and Technologies

- AWS EC2
- Ubuntu Server 24.04
- Jenkins
- Docker
- Maven
- Node.js
- Groovy (Jenkins Pipeline)

## 3. Creating the Jenkins Pipeline

I opened the Jenkins dashboard and created a new job with the following details:

| Configuration | Value |
|---|---|
| Job Name | `multi-stage-multi-agent` |
| Job Type | Pipeline |
| Definition | Pipeline script |

## 4. Jenkinsfile

I used the following Jenkinsfile provided by my teacher:

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

## 5. Short Script Explanation

| Script | Explanation |
|---|---|
| `agent none` | Does not assign a global agent. |
| `stages` | Contains all pipeline stages. |
| `stage('Back-end')` | Defines the Back-end stage. |
| `docker` | Uses Docker as the execution environment. |
| `image 'maven:3.8.1-adoptopenjdk-11'` | Uses Maven with Java 11. |
| `sh 'mvn --version'` | Displays the Maven version. |
| `stage('Front-end')` | Defines the Front-end stage. |
| `image 'node:16-alpine'` | Uses the Node.js 16 image. |
| `sh 'node --version'` | Displays the Node.js version. |

## 6. Executing the Pipeline

After saving the Jenkinsfile, I clicked **Build Now** to execute the pipeline.

I opened Build History, selected Build #1 and checked the Console Output.

### Back-end Stage Output

Jenkins pulled the Maven Docker image and executed the version command.

```text
Apache Maven 3.8.1
Java version: 11.0.11
```

This confirmed that Maven and Java 11 were available inside the Maven Docker container.

### Front-end Stage Output

Jenkins used the Node.js Docker image and executed the version command.

```text
v16.20.2
```

This confirmed that Node.js 16 was available inside the Node.js Docker container.

## 7. How the Pipeline Executed

1. Jenkins started the pipeline with `agent none`.
2. It created a Docker container using the Maven image.
3. It executed `mvn --version` inside the container.
4. The Maven container was stopped and removed.
5. Jenkins created another Docker container using the Node.js image.
6. It executed `node --version` inside the container.
7. The Node.js container was stopped and removed.
8. Both stages completed successfully.

**Note:** Both stages ran sequentially, not in parallel.

## 8. Understanding the Console Output

| Console Message | Meaning |
|---|---|
| `docker pull` | Downloads the Docker image if it is not available locally. |
| `docker inspect` | Checks whether the image exists locally. |
| `withDockerContainer` | Executes pipeline commands inside a Docker container. |
| `docker stop` | Stops the container after execution. |
| `docker rm` | Removes the temporary container. |

## 9. Final Result

<badge color="success">BUILD SUCCESS</badge>

Both pipeline stages executed successfully.

| Stage | Tool | Verified Version | Status |
|---|---|---|---|
| Back-end | Maven | 3.8.1 | Success |
| Front-end | Node.js | 16.20.2 | Success |

Jenkins displayed:

```text
Finished: SUCCESS
```

## 10. Key Learnings

Through this project, I learned:

- How to create a multi-stage Jenkins Pipeline.
- How `agent none` works.
- How to configure separate Docker agents for different stages.
- How to use different Docker images in one pipeline.
- How Jenkins executes stages sequentially.
- How Jenkins creates and removes temporary Docker containers.

This practical helped me understand how Jenkins can use different execution environments within a single pipeline.
