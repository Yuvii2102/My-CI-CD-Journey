# Jenkins Shared Libraries – Complete Theory

## 1. Introduction to Jenkins Shared Libraries

Before understanding Shared Libraries, let's understand a problem that DevOps Engineers face when managing multiple Jenkins pipelines.

Imagine we are working in a large company like Amazon. The company has hundreds of microservices such as:

- Login Service
- Payment Service
- User Service
- Transaction Service
- Notification Service

Each microservice is an independent application. It needs its own CI/CD pipeline to build, test and deploy the application.

If we use Jenkins, we need to create a separate Jenkins pipeline for each microservice.

For example:

- 200 microservices
- 200 Jenkins pipelines
- 200 Jenkinsfiles

### What is the problem?

Most Jenkins pipelines perform similar tasks:

1. Checkout source code from GitHub.
2. Build the application using Maven.
3. Run test cases.
4. Perform code quality analysis using SonarQube.
5. Build a Docker image.
6. Deploy the application to Kubernetes.

The steps are almost the same for every application. Only a few things like repository URLs, application names and configurations change.

Normally, a DevOps Engineer creates one Jenkinsfile and copies it into other projects. Then they modify the required details.

This approach works initially, but creates maintenance problems when the number of pipelines increases.

## 2. Problems with Duplicating Jenkins Pipelines

Let's take an example.

Suppose we have 200 Jenkins pipelines and all of them use the following Maven command:

```bash
mvn clean package
```

After some time, the team decides to change the command to:

```bash
mvn clean install
```

Now we have to open all 200 Jenkinsfiles and manually update the command.

This creates several problems:

- **Code Duplication:** The same code is written repeatedly in multiple Jenkinsfiles.
- **Difficult Maintenance:** We need to update multiple pipelines whenever a common change is required.
- **More Chances of Errors:** We might forget to update some pipelines.
- **Security Risks:** If a security issue exists in common code, we need to fix it everywhere.
- **Difficult Onboarding:** New team members need to understand and maintain multiple pipeline implementations.

To solve these problems, Jenkins provides a concept called **Shared Libraries**.

## 3. What are Jenkins Shared Libraries?

A Jenkins Shared Library is a collection of reusable code that can be shared across multiple Jenkins pipelines.

In simple words, instead of writing the same code in every Jenkinsfile, we write it once in a separate Git repository and reuse it whenever required.

### Example

Suppose we have 200 Jenkins pipelines.

Instead of writing the Maven build command in all 200 Jenkinsfiles, we create a Shared Library containing the Maven build command.

Whenever a pipeline needs to build a Java application, it simply calls that Shared Library.

Jenkins loads the required code from the Shared Library and executes it.

### How Shared Libraries work

1. Create a GitHub repository for Shared Libraries.
2. Write reusable code inside the repository.
3. Configure the Shared Library in Jenkins.
4. Import the library into the Jenkinsfile.
5. Call the required function from the Jenkinsfile.
6. Jenkins loads and executes the reusable code.

**The main idea is to write common code once and reuse it across multiple Jenkins pipelines.**

### Real-world example

Think about a restaurant where multiple chefs prepare different dishes.

Without Shared Libraries, every chef has to prepare the same sauce separately.

With Shared Libraries, the restaurant prepares the sauce once and all chefs can use it whenever required.

Similarly, Shared Libraries allow multiple Jenkins pipelines to reuse the same code.

## 4. Advantages of Jenkins Shared Libraries

### 1. Code Reusability

We write common code once and reuse it in multiple Jenkins pipelines instead of writing it repeatedly.

### 2. Standardization

We can maintain a common pipeline structure across different applications and projects.

This makes pipelines consistent across the organization.

### 3. Less Code Duplication

We avoid writing the same commands and pipeline stages in multiple Jenkinsfiles.

### 4. Easy Maintenance

If we need to modify common code, we update it in the Shared Library instead of manually changing every Jenkinsfile.

### 5. Easy Onboarding

New developers and DevOps Engineers can easily use existing pipeline templates and shared functions.

They don't need to write everything from scratch.

### 6. Reduced Errors

Since we reuse tested code instead of writing the same code repeatedly, there are fewer chances of introducing errors.

### 7. Better Security Maintenance

If a common security issue is found in the shared code, we can fix it in one central location and make the updated version available to the pipelines.

**The biggest advantage of Shared Libraries is centralized code maintenance.**

## 5. Jenkins Shared Library Folder Structure

A Jenkins Shared Library mainly contains three important directories:

```text
jenkins-shared-library/
│
├── vars/
│   ├── helloWorld.groovy
│   ├── mavenBuild.groovy
│   └── dockerBuild.groovy
│
├── src/
│
└── resources/
```

Let's understand each directory.

### 1. vars/

The `vars` directory contains reusable pipeline steps that can be directly called from Jenkinsfiles.

For example:

- helloWorld.groovy
- mavenBuild.groovy
- dockerBuild.groovy

Each Groovy file can contain a reusable function.

This is the main directory we focus on when starting with Shared Libraries.

### 2. src/

The `src` directory contains reusable Groovy classes and supporting code.

It is useful when we need to organize more complex logic into classes.

### 3. resources/

The `resources` directory contains external resources such as scripts, configuration files and other supporting files that can be accessed by Shared Libraries.

**For now, we mainly focus on the `vars` directory.**

## 6. What is Groovy?

Groovy is a programming language that runs on the Java platform.

Jenkins pipelines use Groovy-based syntax to define pipeline stages, steps and other operations.

We use Groovy to write reusable functions inside Jenkins Shared Libraries.

### Basic Groovy example

```groovy
def call() {
    echo 'Hello from DevOps Team'
}
```

Let's understand this code.

| Syntax | Meaning |
|---|---|
| `def` | Used to define a method or variable. |
| `call()` | Special method used to execute a Shared Library step. |
| `{ }` | Contains the code that needs to be executed. |
| `echo` | Prints a message in the Jenkins console. |

### Why do we use def call()?

When we create a reusable step inside the `vars` directory, we commonly use the `call()` method.

This allows us to call the Shared Library using the filename from our Jenkinsfile.

For example:

File name:

```text
helloWorld.groovy
```

Code inside the file:

```groovy
def call() {
    echo 'Hello from DevOps Team'
}
```

We can call this function in our Jenkinsfile using:

```groovy
helloWorld()
```

Remember:

- File name: `helloWorld.groovy`
- Method name: `call()`
- Jenkinsfile call: `helloWorld()`

We use the filename when calling the Shared Library, not the method name `call()`.

## 7. Configuring Shared Libraries in Jenkins

Before using a Shared Library, we need to tell Jenkins where the library is located.

For this, Jenkins provides a configuration called **Global Pipeline Libraries**.

### Configuration steps

1. Open the Jenkins Dashboard.
2. Go to Manage Jenkins.
3. Open System Configuration or Configure System.
4. Find Global Pipeline Libraries.
5. Click Add.
6. Provide a name for the Shared Library.
7. Select the default branch, such as `main`.
8. Under Modern SCM, select Git.
9. Provide the GitHub repository URL.
10. Save the configuration.

### Important configurations

| Configuration | Example | Purpose |
|---|---|---|
| Name | my-shared-library | Identifies the library in Jenkins. |
| Default Version | main | Specifies the default Git branch. |
| Retrieval Method | Modern SCM | Defines how Jenkins retrieves the library. |
| Repository URL | GitHub repository URL | Specifies where the library is stored. |

### Why do we configure it globally?

We configure the Shared Library globally so that multiple Jenkins pipelines can use the same library.

We don't need to configure the same GitHub repository separately in every Jenkins pipeline.

This is a one-time configuration for that Jenkins instance.

## 8. Importing Shared Libraries into Jenkinsfiles

After configuring the Shared Library, we need to import it into our Jenkinsfile.

We use the following syntax:

```groovy
@Library('my-shared-library') _
```

Let's understand each part.

| Syntax | Meaning |
|---|---|
| `@Library` | Tells Jenkins to load a Shared Library. |
| `my-shared-library` | Name configured in Global Pipeline Libraries. |
| `_` | Allows the library's global variables and steps to be available in the pipeline. |

The library name in the Jenkinsfile must match the name configured in Jenkins.

We generally place this statement at the beginning of the Jenkinsfile.

## 9. How Jenkins Executes a Shared Library

Let's understand the complete execution flow.

1. We write a Jenkinsfile.
2. We import the Shared Library using `@Library`.
3. Jenkins Controller loads the configured Shared Library from GitHub.
4. Jenkins looks for the required Groovy file inside the `vars` directory.
5. It executes the `call()` method inside that file.
6. The result appears in the Jenkins console.

### Execution flow

```text
          Jenkinsfile
               |
               |
        @Library Import
               |
               v
       Jenkins Controller
               |
               |
       Loads Shared Library
               |
               v
       GitHub Repository
               |
               |
          vars/ folder
               |
               v
       Required Groovy File
               |
               |
          call() Method
               |
               v
        Execute the Code
               |
               v
        Jenkins Console
```

The Jenkins Controller manages loading the library and coordinating its execution within the pipeline.

## 10. Using Shared Libraries – Hello World Example

Let's understand how we can replace normal Jenkins pipeline code with a Shared Library.

### Step 1: Create a GitHub repository

Create a repository for your Jenkins Shared Library.

For example:

```text
jenkins-shared-library
```

### Step 2: Create the vars directory

Inside the repository, create a folder called `vars`.

```text
jenkins-shared-library/
│
└── vars/
```

### Step 3: Create a Groovy file

Inside `vars`, create a file called:

```text
helloWorld.groovy
```

### Step 4: Write the reusable code

Inside `helloWorld.groovy`:

```groovy
def call() {
    echo 'Hello from DevOps Team'
}
```

Commit and push this code to GitHub.

### Step 5: Configure the Shared Library in Jenkins

Go to Global Pipeline Libraries and configure:

```text
Name: my-shared-library

Default Version: main

Retrieval Method: Modern SCM

Repository: Your GitHub Repository URL
```

Save the configuration.

### Step 6: Import the library into Jenkinsfile

Now create a Jenkins pipeline and use:

```groovy
@Library('my-shared-library') _

pipeline {
    agent any

    stages {
        stage('Greeting') {
            steps {
                helloWorld()
            }
        }
    }
}
```

### Step 7: Execute the pipeline

When we run the pipeline, Jenkins loads `helloWorld.groovy` from GitHub and executes the `call()` method.

Expected output:

```text
Hello from DevOps Team
```

This is our first example of using a Jenkins Shared Library.

## 11. Using Shared Libraries for Maven Builds

Now let's understand a practical DevOps example.

Suppose multiple Java applications use the same Maven build command.

```bash
mvn clean install
```

Instead of writing this command in every Jenkinsfile, we can create a reusable Maven Shared Library.

### Step 1: Create a Groovy file

Inside the `vars` directory, create:

```text
mavenBuild.groovy
```

### Step 2: Write the Maven command

Inside `mavenBuild.groovy`:

```groovy
def call() {
    sh 'mvn clean install'
}
```

Here:

- `def call()` defines the reusable function.
- `sh` executes a shell command.
- `mvn clean install` builds and installs the Java application using Maven.

### Step 3: Call the library from Jenkinsfile

```groovy
@Library('my-shared-library') _

pipeline {
    agent any

    stages {
        stage('Build') {
            steps {
                mavenBuild()
            }
        }
    }
}
```

Now Jenkins executes the Maven command from the Shared Library.

Instead of writing the same command repeatedly, we simply call:

```groovy
mavenBuild()
```

We can follow the same approach for other common operations such as:

- Git checkout
- Maven builds
- SonarQube analysis
- Docker image builds
- Kubernetes deployments

## 12. Passing Arguments to Shared Libraries

Sometimes different applications need different configurations.

Instead of creating separate Shared Libraries for every application, we can pass arguments to the reusable function.

Example:

Inside `vars/buildApplication.groovy`:

```groovy
def call(String appName) {
    echo "Building ${appName}"
}
```

Now call it from the Jenkinsfile:

```groovy
buildApplication('payment-service')
```

Output:

```text
Building payment-service
```

Here, `appName` is the argument passed to the Shared Library.

This makes our reusable functions more flexible because we can use the same function with different application names.

## 13. Updating Shared Library Code

One of the biggest advantages of Shared Libraries is that we can maintain common code from one central location.

Let's understand with an example.

Initially, our `helloWorld.groovy` contains:

```groovy
def call() {
    echo 'Hello from DevOps Team'
}
```

Now suppose our team wants to change the message.

We update the code in GitHub:

```groovy
def call() {
    echo 'Welcome to our CI/CD Pipeline'
}
```

After committing the changes, Jenkins can load the updated library when the pipeline retrieves the new version.

Now multiple Jenkins pipelines can use the updated code without manually editing every Jenkinsfile.

This is called centralized code maintenance.

**Note:** Jenkins must retrieve the updated library version. If a pipeline is pinned to an older version or commit, it will continue using that version until the reference is changed.

## 14. Important Points to Remember

| Concept | Explanation |
|---|---|
| Jenkins Shared Library | Reusable code shared across multiple Jenkins pipelines. |
| Groovy | Programming language used for Jenkins pipeline scripting. |
| vars/ | Contains reusable pipeline steps. |
| src/ | Contains reusable Groovy classes. |
| resources/ | Contains external resources. |
| def call() | Defines the callable method for a shared library step. |
| @Library | Used to import a Shared Library. |
| Global Pipeline Libraries | Used to configure Shared Libraries globally in Jenkins. |
| Modern SCM | Used to retrieve the Shared Library from a source control repository. |
| Jenkins Controller | Loads and coordinates the Shared Library execution. |

## 15. Interview Questions and Answers

### Q1. What are Jenkins Shared Libraries?

Jenkins Shared Libraries are collections of reusable code that can be shared across multiple Jenkins pipelines. They help reduce code duplication and make pipeline maintenance easier.

### Q2. Why do we use Shared Libraries?

We use Shared Libraries to reuse common pipeline code, standardize pipelines, reduce duplication, simplify maintenance and reduce errors.

### Q3. What is the purpose of the vars directory?

The `vars` directory contains reusable pipeline steps that can be directly called from Jenkinsfiles.

### Q4. What is the purpose of def call()?

The `call()` method allows us to execute a Shared Library step by using its filename from the Jenkinsfile.

### Q5. How do we configure a Shared Library in Jenkins?

We go to Manage Jenkins, open System Configuration, find Global Pipeline Libraries and configure the library name, default branch and Git repository URL.

### Q6. How do we import a Shared Library?

We use the `@Library` annotation.

```groovy
@Library('my-shared-library') _
```

### Q7. What is the purpose of Global Pipeline Libraries?

It allows us to configure Shared Libraries centrally so that multiple Jenkins pipelines can use the same library.

### Q8. What is the biggest advantage of Shared Libraries?

Centralized maintenance. We can update common code in one location instead of manually modifying multiple Jenkins pipelines.

### Q9. Can we pass arguments to Shared Libraries?

Yes. We can pass arguments to reusable functions to make them flexible and use them with different applications or configurations.

### Q10. What happens when we update Shared Library code?

When Jenkins retrieves the updated library version, pipelines using that version can execute the updated code without manually changing every Jenkinsfile.

---

## 16. Final Understanding

Before learning Shared Libraries, I used to write the same code in different Jenkins pipelines.

Now I understand that Shared Libraries help us avoid this problem by allowing us to write reusable code once and use it across multiple pipelines.

The main things I learned are:

1. Why we need Shared Libraries.
2. Problems with duplicating Jenkinsfiles.
3. Advantages of Shared Libraries.
4. Shared Library folder structure.
5. Basics of Groovy.
6. How to create reusable functions using `def call()`.
7. How to configure Shared Libraries in Jenkins.
8. How to import libraries using `@Library`.
9. How Jenkins loads and executes shared code.
10. How to use Shared Libraries for Maven builds.
11. How to pass arguments to reusable functions.
12. How centralized code maintenance works.

**My key takeaway:** Instead of writing the same code in multiple Jenkins pipelines, I can create a Shared Library, store the reusable code in GitHub and call it whenever required. This makes CI/CD pipelines cleaner, reusable, consistent and easier to maintain.

---

**Next Topic:** Practical Implementation of Jenkins Shared Libraries – Creating a GitHub repository, configuring it in Jenkins and executing reusable functions in a Jenkins pipeline.
