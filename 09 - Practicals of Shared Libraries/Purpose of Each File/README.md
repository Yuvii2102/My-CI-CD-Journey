# Purpose of Each File – Jenkins Shared Libraries

In this practical, I worked with Jenkins Shared Libraries using Groovy. I also created a simple Java application and built it using Maven.

Each file has a different purpose in our projects. Here is what I learned about each file and where I used it.

## 1. helloWorld.groovy

**Language:** Groovy

**Purpose:** This file contains a reusable function that prints messages in the Jenkins console.

**Code:**

```groovy
def call() {
    echo 'Welcome to my Jenkins Shared Library!'
    echo 'This code is reused across multiple pipelines.'
}
```

**How it works:**

- `def call()` defines a reusable function.
- `echo` prints messages in the Jenkins console.
- We can execute this function by calling `helloWorld()` in the Jenkinsfile.

**Where I used it:**

I used this file in Project 1 – HelloWorld Shared Library.

First, I created the function and executed it through Jenkins. Then I modified the messages in GitHub and ran the pipeline again. Jenkins picked up the updated code without requiring any changes to the Jenkinsfile.

**What I learned:** We can update shared code in one place and reuse it across Jenkins pipelines.

## 2. mavenBuild.groovy

**Language:** Groovy

**Purpose:** This file contains a reusable function that executes the Maven build command.

**Code:**

```groovy
def call() {
    sh 'mvn clean install'
}
```

**How it works:**

- `def call()` defines a reusable function.
- `sh` executes a shell command.
- `mvn clean install` cleans previous build files, builds the Java application and installs the generated artifact into the local Maven repository.

**Where I used it:**

I used this file in Project 2 – Maven Build Using Shared Library.

Instead of writing the Maven command directly in the Jenkinsfile, I created a separate function and called it using `mavenBuild()`.

**What I learned:** We can store commonly used build commands in Shared Libraries and reuse them whenever required.

## 3. Jenkinsfile

**Language:** Groovy-based Jenkins Pipeline syntax

**Purpose:** The Jenkinsfile defines the stages and steps that Jenkins needs to execute.

**Example:**

```groovy
@Library('my-shared-library') _

pipeline {
    agent any

    stages {
        stage('Hello World') {
            steps {
                helloWorld()
            }
        }
    }
}
```

**How it works:**

- `@Library` imports our configured Shared Library.
- `pipeline` defines the Jenkins pipeline.
- `agent any` allows Jenkins to select an available agent.
- `stages` contains the different stages of execution.
- `helloWorld()` calls the function from `helloWorld.groovy`.

**Where I used it:**

I used the Jenkinsfile in both projects.

- In Project 1, I called `helloWorld()` to print messages.
- In Project 2, I created the Maven project and called `mavenBuild()` to build the Java application.

**What I learned:** The Jenkinsfile controls the pipeline execution and tells Jenkins which functions to execute and in what order.

## 4. App.java

**Language:** Java

**Purpose:** This file contains the Java application that Maven builds.

**Code:**

```java
package com.example;

public class App {
    public static void main(String[] args) {
        System.out.println("Hello from Maven Shared Library!");
    }
}
```

**How it works:**

- `package` defines the Java package.
- `public class App` defines the Java class.
- `main()` is the entry point of the Java application.
- `System.out.println()` prints a message.

**Where I used it:**

I used this file in Project 2 – Maven Build Using Shared Library.

Our Jenkinsfile created `App.java` inside the Jenkins workspace. Maven then compiled the Java source code and packaged the application into a JAR file.

**What I learned:** This file contains the actual Java application that we build using Maven.

## 5. pom.xml

**Language:** XML

**Purpose:** This file contains the Maven project configuration.

It defines the following information:

- `groupId` – Identifies the project group.
- `artifactId` – Defines the project name.
- `version` – Specifies the project version.
- `maven.compiler.release` – Specifies the Java version used for compilation.
- `maven-compiler-plugin` – Configures Java compilation.

**Where I used it:**

I used this file in Project 2 – Maven Build Using Shared Library.

I did not create `pom.xml` manually in GitHub. Instead, I created it automatically through the Jenkinsfile using the `writeFile` step inside the `Create Maven Project` stage.

After creating the file, Jenkins called `mavenBuild()`. Maven read `pom.xml` to understand the project configuration and build the Java application.

**What I learned:** Maven uses `pom.xml` to understand the project structure and configuration before building the application.

---

## 6. Quick Revision

| File | Language | Where I used it |
|---|---|---|
| `helloWorld.groovy` | Groovy | Project 1 – HelloWorld |
| `mavenBuild.groovy` | Groovy | Project 2 – Maven Build |
| `Jenkinsfile` | Groovy-based Pipeline | Both projects |
| `App.java` | Java | Project 2 – Maven Build |
| `pom.xml` | XML | Project 2 – Maven Build |

## 7. How Everything Works Together

### Project 1 – HelloWorld Shared Library

1. The Jenkinsfile imports the Shared Library.
2. It calls the `helloWorld()` function.
3. The `helloWorld.groovy` file executes the function.
4. Jenkins prints the messages in the console.

### Project 2 – Maven Build Using Shared Library

1. The Jenkinsfile creates the Maven project.
2. It generates `pom.xml` and `App.java` inside the Jenkins workspace.
3. The Jenkinsfile calls `mavenBuild()`.
4. The `mavenBuild.groovy` file executes `mvn clean install`.
5. Maven reads `pom.xml` and compiles `App.java`.
6. Maven packages the application into a JAR file.

## 8. Final Understanding

From this practical, I understood that every file has a separate responsibility.

- **Groovy:** Used to create reusable Jenkins Shared Library functions.
- **Jenkinsfile:** Defines and controls pipeline execution.
- **Java:** Used to write the application code.
- **XML:** Used to configure the Maven project.
- **Maven:** Used to compile, build and package the Java application.

**Key takeaway:** I learned how to create reusable Jenkins functions using Groovy and use them to automate a Java application build with Maven.
