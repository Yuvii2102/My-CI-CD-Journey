Jenkins Shared Libraries ( Practicals )

## Project 1 – HelloWorld Shared Library

### Objective

Create a reusable Groovy function, execute it through Jenkins, modify the function and verify that Jenkins uses the updated code.

### Step 1: Create the Initial Shared Library File

Navigate to the GitHub repository:

`My-CI-CD-Journey/09 - Practicals of Shared Libraries/vars/`

Create a file named:

`helloWorld.groovy`

**Initial code – Version 1**

```groovy
def call() {
    echo 'Hello from DevOps Team'
}
```

Commit and push this file to the `main` branch.

### Step 2: Configure the Shared Library in Jenkins

Navigate to:

**Manage Jenkins → System → Global Trusted Pipeline Libraries**

Configure the following settings:

| Setting | Value |
|---|---|
| Name | `my-shared-library` |
| Default version | `main` |
| Retrieval method | Modern SCM |
| Source Code Management | Git |
| Repository URL | `https://github.com/Yuvii2102/My-CI-CD-Journey.git` |
| Credentials | None (public repository) |
| Library Path | `09 - Practicals of Shared Libraries` |

Save the configuration.

### Step 3: Create a Jenkins Pipeline Job

1. Open the Jenkins dashboard.
2. Click **New Item**.
3. Enter the name `shared-library-demo`.
4. Select **Pipeline**.
5. Click **OK**.
6. Scroll down to the Pipeline section.
7. Select **Pipeline script**.

Add the following Jenkinsfile:

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

### Step 4: Execute the First Build

1. Click **Save**.
2. Click **Build Now**.
3. Open the latest build.
4. Click **Console Output**.

**Expected output:**

```text
Hello from DevOps Team
```

The build should finish with:

```text
Finished: SUCCESS
```

At this point, we have successfully executed our first Shared Library function.

### Step 5: Modify the Shared Library Code

Now go back to GitHub and open:

`09 - Practicals of Shared Libraries/vars/helloWorld.groovy`

Initially, our function printed only one message. Now we will modify it to print two messages.

**Updated code – Version 2**

```groovy
def call() {
    echo 'Welcome to my Jenkins Shared Library!'
    echo 'This code is reused across multiple pipelines.'
}
```

Commit and push the updated code to the `main` branch.

### Step 6: Execute the Pipeline Again

We do not need to modify our Jenkinsfile.

1. Open the `shared-library-demo` job.
2. Click **Build Now**.
3. Open the latest build.
4. Click **Console Output**.

**Expected output:**

```text
Welcome to my Jenkins Shared Library!
This code is reused across multiple pipelines.
```

The build should finish with:

```text
Finished: SUCCESS
```

### Step 7: Understand What Happened

In this practical, we executed the same Jenkins pipeline twice.

| First Build | Second Build |
|---|---|
| Used the original code | Used the updated code |
| Printed `Hello from DevOps Team` | Printed two updated messages |
| Jenkinsfile called `helloWorld()` | Jenkinsfile still called `helloWorld()` |

**Important learning:**

We changed the code inside the Shared Library without changing the Jenkinsfile.

Jenkins fetched the updated Shared Library code from GitHub during the next build and executed it.

This demonstrates the main advantage of Shared Libraries: we can maintain reusable code centrally and use it across multiple Jenkins pipelines.

**Project 1 completed!**

---

## Project 2 – Maven Build Using Shared Library

### Objective

Create another reusable Groovy function that executes a Maven build command and use it to build a Java application through Jenkins.

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

Commit and push the file to GitHub.

Our `vars` folder should now contain:

```text
vars/
│
├── helloWorld.groovy
└── mavenBuild.groovy
```

### Step 2: Verify Java and Maven

Install Java 21 JDK and Maven on Ubuntu if they are not already installed.

```bash
sudo apt update
sudo apt install openjdk-21-jdk -y
sudo apt install maven -y
```

Verify the installations:

```bash
java -version
javac -version
mvn -version
```

Verify that the Jenkins user can access all three tools:

```bash
sudo -H -u jenkins bash -c 'cd /var/lib/jenkins && java -version && javac -version && mvn -version'
```

### Step 3: Update the Jenkins Pipeline

Open the existing `shared-library-demo` job.

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

### Step 4: Understand the Pipeline

**Stage 1 – Create Maven Project**

- Creates the Java source directory.
- Creates `pom.xml` with Maven project configuration.
- Creates `App.java` containing our Java application.

**Stage 2 – Maven Build**

Calls:

```groovy
mavenBuild()
```

This executes the function stored in `mavenBuild.groovy`:

```groovy
sh 'mvn clean install'
```

### Step 5: Execute the Pipeline

1. Save the Jenkinsfile.
2. Open the `shared-library-demo` job.
3. Click **Build Now**.
4. Open the latest build.
5. Click **Console Output**.

Maven will clean previous build files, compile the Java application, run configured tests, package the application and install the generated artifact into its local repository.

**Expected output:**

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

## Final Outcome

In this practical, I created and executed two Jenkins Shared Library projects.

1. **HelloWorld Shared Library:** Created a reusable Groovy function, executed its original version, modified the code in GitHub and verified the updated output without changing the Jenkinsfile.

2. **Maven Build Shared Library:** Created a reusable Maven build function and used it to compile and package a Java application through Jenkins.

I learned how Shared Libraries help us avoid code duplication, reuse pipeline functions and maintain Jenkins pipeline code centrally.
