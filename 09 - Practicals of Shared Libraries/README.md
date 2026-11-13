# Jenkins Shared Libraries ( Practicals )

## 1. Introduction

A Jenkins Shared Library allows us to write reusable pipeline code and share it across multiple Jenkins pipelines.

Instead of writing the same pipeline steps repeatedly, we can create reusable Groovy functions in a GitHub repository and call them whenever required.

### Why do we use Shared Libraries?

- Avoid repeating pipeline code.
- Reuse functions across multiple Jenkins jobs.
- Maintain pipeline code in one central location.
- Update shared code without changing every Jenkinsfile.

### How Shared Libraries Work

1. We create Groovy files inside a GitHub repository.
2. We configure that repository in Jenkins as a Global Trusted Pipeline Library.
3. Jenkins downloads the library when a pipeline runs.
4. The Jenkinsfile imports the library using `@Library`.
5. The pipeline calls the required shared function.

---

## 2. Prerequisites

Before starting the practical, we need:

- AWS EC2 instance running Ubuntu.
- Jenkins installed and running.
- GitHub repository to store Shared Library files.
- Java 21 JDK.
- Maven.

### Step 1: Update Ubuntu

```bash
sudo apt update
sudo apt upgrade -y
```

### Step 2: Install Java 21 JDK

Install the complete JDK because it includes both Java and the Java compiler.

```bash
sudo apt install openjdk-21-jdk -y
```

Verify Java:

```bash
java -version
```

Verify the Java compiler:

```bash
javac -version
```

Both should show Java 21.

### Step 3: Install Maven

```bash
sudo apt install maven -y
```

Verify Maven:

```bash
mvn -version
```

Check that Maven is using Java 21.

### Step 4: Verify Tools for the Jenkins User

Jenkins executes pipeline commands using its own Linux user.

Run:

```bash
sudo -H -u jenkins bash -c 'cd /var/lib/jenkins && java -version && javac -version && mvn -version'
```

Verify that Java 21, javac 21 and Maven are available.

---

## 3. GitHub Repository Structure

Our GitHub repository:

**Repository:** My-CI-CD-Journey

https://github.com/Yuvii2102/My-CI-CD-Journey

The Shared Library files are stored in this folder:

`09 - Practicals of Shared Libraries`

Our folder structure:

```text
My-CI-CD-Journey/
│
└── 09 - Practicals of Shared Libraries/
    │
    └── vars/
        │
        ├── helloWorld.groovy
        │
        └── mavenBuild.groovy
```

### Understanding the vars Folder

The `vars` folder contains reusable Groovy functions.

Each Groovy file inside this folder can be called as a pipeline step using its filename.

For example:

- `helloWorld.groovy` → `helloWorld()`
- `mavenBuild.groovy` → `mavenBuild()`

---

# PROJECT 1 – HelloWorld Shared Library

## 4. Objective

Create a reusable Groovy function that prints messages in the Jenkins console.

We will store the function in GitHub and call it from a Jenkins pipeline.

### Step 1: Create helloWorld.groovy

Navigate to:

`09 - Practicals of Shared Libraries/vars/`

Create a file named:

`helloWorld.groovy`

Add the following code:

```groovy
def call() {
    echo 'Welcome to my Jenkins Shared Library!'
    echo 'This code is reused across multiple pipelines.'
}
```

### Understanding the Code

- `def` defines a function in Groovy.
- `call()` allows us to execute the function directly by using its library name.
- `echo` prints a message in the Jenkins console.

Because the file is named `helloWorld.groovy`, we can call it using:

```groovy
helloWorld()
```

### Step 2: Push the File to GitHub

Commit and push the file to the `main` branch.

Make sure the file is available at:

`09 - Practicals of Shared Libraries/vars/helloWorld.groovy`

### Step 3: Configure Global Trusted Pipeline Library

Open Jenkins.

Navigate to:

**Manage Jenkins → System → Global Trusted Pipeline Libraries**

Add a new library with these settings:

| Setting | Value |
|---|---|
| Name | `my-shared-library` |
| Default version | `main` |
| Retrieval method | Modern SCM |
| Source Code Management | Git |
| Project Repository | `https://github.com/Yuvii2102/My-CI-CD-Journey.git` |
| Credentials | None (public repository) |
| Library Path | `09 - Practicals of Shared Libraries` |

Save the configuration.

**Important:** Configure this library only once. We will reuse the same configuration for Project 2.

### Step 4: Create a Jenkins Pipeline Job

1. Open the Jenkins dashboard.
2. Click **New Item**.
3. Enter the job name: `shared-library-demo`.
4. Select **Pipeline**.
5. Click **OK**.
6. Scroll to the Pipeline section.
7. Select **Pipeline script**.

Add this Jenkinsfile:

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

### Understanding the Jenkinsfile

- `@Library('my-shared-library') _` imports our configured Shared Library.
- `pipeline` defines the Jenkins pipeline.
- `agent any` allows Jenkins to execute the pipeline on an available agent.
- `stage` defines a stage in the pipeline.
- `helloWorld()` calls the function from `helloWorld.groovy`.

### Step 5: Execute the Pipeline

1. Click **Save**.
2. Click **Build Now**.
3. Open the latest build.
4. Click **Console Output**.

Expected output:

```text
Welcome to my Jenkins Shared Library!
This code is reused across multiple pipelines.
```

The build should finish with:

```text
Finished: SUCCESS
```

### Step 6: Test Code Reusability

Now change the message inside `helloWorld.groovy` in GitHub.

For example:

```groovy
def call() {
    echo 'Hello from DevOps Team!'
    echo 'Updated from the Jenkins Shared Library.'
}
```

Commit and push the changes.

Run the Jenkins pipeline again.

Jenkins will retrieve the updated library code and execute the new messages without changing the Jenkinsfile.

**Project 1 completed!**

---

# PROJECT 2 – Maven Build Using Shared Library

## 5. Objective

Create a reusable Maven build function inside our Jenkins Shared Library.

We will create a simple Java application, generate its Maven configuration and build it using the shared function.

### Step 1: Create mavenBuild.groovy

Navigate to:

`09 - Practicals of Shared Libraries/vars/`

Create a file named:

`mavenBuild.groovy`

Add the following code:

```groovy
def call() {
    sh 'mvn clean install'
}
```

### Understanding the Code

- `def call()` defines the reusable function.
- `sh` executes a shell command on the Jenkins agent.
- `mvn clean install` performs the Maven build.

The command has two main parts:

**clean**

Removes the previous build output, usually stored in the `target` directory.

**install**

Builds the project, runs configured tests and installs the generated artifact into the local Maven repository if the build succeeds.

### Step 2: Push the File to GitHub

Commit and push `mavenBuild.groovy` to the `main` branch.

Confirm that both files are present:

```text
vars/
│
├── helloWorld.groovy
└── mavenBuild.groovy
```

We do not need to create another Shared Library configuration. We will reuse `my-shared-library`.

### Step 3: Prepare the Maven Project

Our Jenkins pipeline will create a simple Java project.

The project structure will be:

```text
shared-library-demo/
│
├── pom.xml
│
└── src/
    └── main/
        └── java/
            └── com/
                └── example/
                    └── App.java
```

### Step 4: Update the Jenkins Pipeline Script

Open the existing Jenkins job:

`shared-library-demo`

Navigate to:

**Configure → Pipeline → Pipeline script**

Replace the previous Jenkinsfile with:

```groovy
@Library('my-shared-library') _

pipeline {
    agent any

    stages {

        stage('Create Maven Project') {
            steps {

                sh 'mkdir -p src/main/java/com/example'

                writeFile file: 'pom.xml', text: '''\
<project xmlns="http://maven.apache.org/POM/4.0.0"
         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 https://maven.apache.org/xsd/maven-4.0.0.xsd">

    <modelVersion>4.0.0</modelVersion>

    <groupId>com.example</groupId>
    <artifactId>shared-library-demo</artifactId>
    <version>1.0-SNAPSHOT</version>

    <properties>
        <maven.compiler.release>21</maven.compiler.release>
        <project.build.sourceEncoding>UTF-8</project.build.sourceEncoding>
    </properties>

    <build>
        <plugins>
            <plugin>
                <groupId>org.apache.maven.plugins</groupId>
                <artifactId>maven-compiler-plugin</artifactId>
                <version>3.13.0</version>
            </plugin>
        </plugins>
    </build>
</project>
'''

                writeFile file: 'src/main/java/com/example/App.java', text: '''\
package com.example;

public class App {
    public static void main(String[] args) {
        System.out.println("Hello from Maven Shared Library!");
    }
}
'''
            }
        }

        stage('Maven Build') {
            steps {
                mavenBuild()
            }
        }
    }
}
```

### Step 5: Understand the Jenkinsfile

**Stage 1 – Create Maven Project**

```groovy
sh 'mkdir -p src/main/java/com/example'
```

Creates the required Java source directory.

```groovy
writeFile file: 'pom.xml', text: '''...'''
```

Creates the Maven configuration file.

The `pom.xml` contains:

- Group ID
- Artifact ID
- Version
- Java compiler release
- Maven compiler plugin

```groovy
writeFile file: 'src/main/java/com/example/App.java', text: '''...'''
```

Creates our Java application.

The application prints:

```text
Hello from Maven Shared Library!
```

**Stage 2 – Maven Build**

```groovy
mavenBuild()
```

Calls the reusable function from:

`09 - Practicals of Shared Libraries/vars/mavenBuild.groovy`

That function executes:

```bash
mvn clean install
```

### Step 6: Execute the Pipeline

1. Save the Jenkinsfile.
2. Open the `shared-library-demo` job.
3. Click **Build Now**.
4. Open the latest build.
5. Click **Console Output**.

### Expected Build Process

Maven performs the following operations:

1. Reads the `pom.xml` file.
2. Downloads the required Maven plugins and dependencies.
3. Cleans previous build output.
4. Compiles the Java source file.
5. Runs configured tests.
6. Packages the application into a JAR file.
7. Installs the artifact into the local Maven repository.

### Expected Output

```text
BUILD SUCCESS

Finished: SUCCESS
```

The generated JAR file will be available at:

```text
/var/lib/jenkins/workspace/shared-library-demo/target/shared-library-demo-1.0-SNAPSHOT.jar
```

**Project 2 completed!**

---

# 6. Final Project Comparison

| Feature | Project 1 | Project 2 |
|---|---|---|
| Shared Library file | `helloWorld.groovy` | `mavenBuild.groovy` |
| Function | `helloWorld()` | `mavenBuild()` |
| Main purpose | Print messages | Build Java application |
| Jenkins operation | `echo` | `sh` |
| Tool used | Jenkins Pipeline | Maven and Java |
| Result | Console messages | Generated JAR file |

# 7. Important Concepts to Remember

**What is a Jenkins Shared Library?**

A collection of reusable Groovy code that can be shared across Jenkins pipelines.

**Why do we use the vars folder?**

It stores reusable pipeline functions that can be called directly from a Jenkinsfile.

**What is call() in a Shared Library?**

It defines the function that Jenkins executes when we call the library file by its name.

**What is @Library?**

It imports a configured Shared Library into our Jenkins pipeline.

**What is a Global Trusted Pipeline Library?**

It is a Jenkins configuration that makes a shared library available to pipeline jobs.

**What is Maven?**

Maven is a build automation tool used to compile Java code, manage dependencies, run tests and package applications.

**What is pom.xml?**

It is the Project Object Model file that contains Maven project configuration and dependencies.

# 8. Final Outcome

In this practical, I created two Jenkins Shared Library projects.

1. Created a reusable HelloWorld function and executed it through a Jenkins pipeline.
2. Created a reusable Maven build function and used it to build a Java application.

I also learned how to configure a Global Trusted Pipeline Library, import it using `@Library` and execute reusable functions from Jenkinsfiles.

**Key takeaway:** Shared Libraries help us write cleaner, reusable and maintainable Jenkins pipelines.
