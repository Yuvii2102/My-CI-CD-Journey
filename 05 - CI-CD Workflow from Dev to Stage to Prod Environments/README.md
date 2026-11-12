# How Does an Application Move From Development to Production?

## 1. Introduction

In a company, multiple developers work on the same application. Each developer may work on a different feature, such as:

- Login page
- Payment system
- Shopping cart
- Bug fixes
- User interface improvements

If every developer directly modifies the live application, their changes might affect other features or introduce bugs.

To avoid these problems, companies follow a structured process using:

1. Git branches
2. Different environments
3. CI/CD pipelines
4. Testing and approvals

The main goal is to move application code safely from development to production.

---

## 2. Understanding the Four Git Branches

Git branches allow developers to work on different parts of an application without directly affecting other developers' work.

There are four important branches covered in this lesson:

1. Feature Branch
2. Main Branch
3. Release Branch
4. Hotfix Branch

### A. Feature Branch

A Feature Branch is created when a developer starts working on a new feature.

For example, if a developer is building a login page, they can create a separate branch:

```bash
git checkout -b feature/login-page
```

Other developers can create their own branches:

```bash
git checkout -b feature/payment-system
git checkout -b feature/shopping-cart
```

Each developer works independently on their assigned feature.

**Purpose:** To develop individual features without directly modifying the Main branch.

### B. Main Branch

Once developers complete their features, their changes are reviewed and merged into the Main branch.

For example:

```text
feature/login-page --------\
feature/payment-system -----+----> Main Branch
feature/shopping-cart ------/
```

The Main branch contains the integrated application code. Development continues as different approved changes are merged into it.

**Purpose:** To bring different developers' changes together into one application.

### C. Release Branch

When the required features are completed and the company is preparing a new application version, a Release Branch is created from Main.

```text
Main Branch
     |
     v
Release Branch
     |
     v
Prepare Application v1.0
```

The team uses this branch for final testing and release-related bug fixes.

This allows the team to prepare a stable version without interrupting ongoing development in Main.

**Purpose:** To prepare a particular application version for release.

### D. Hotfix Branch

A Hotfix Branch is used to fix critical problems in an application that is already running in Production.

For example, imagine the payment system stops working in the live application. The company cannot wait for the next regular release.

A Hotfix Branch can be created from the affected production release branch.

```text
Release v1.0
     |
     v
Hotfix Branch
     |
     v
Fix Payment Bug
     |
     v
Test and Merge Fix
```

After fixing and testing the issue, the changes are merged into the affected release branch and Main. Other relevant branches may also need the fix.

**Purpose:** To fix critical production issues quickly.

### Branches Summary

| Branch | Purpose |
|---|---|
| Feature | Develop individual features |
| Main | Integrate development changes |
| Release | Prepare a particular application version |
| Hotfix | Fix critical production issues |

These are common branching approaches. Some organizations may also use additional branches such as `develop` or `integration`.

---

## 3. Understanding the Four Environments

An environment is a separate place where an application is deployed and tested for a particular purpose.

Companies do not directly deploy every code change to the live application. They move the application through different environments before releasing it to customers.

The four environments covered in this lesson are:

1. Development
2. Staging / QA
3. Pre-Production / UAT
4. Production

### A. Development Environment

The Development Environment is where developers test the features they are building.

For example, a developer completes a new login feature and pushes the code to a Feature Branch in GitHub.

The process looks like this:

```text
Developer
    |
    v
Feature Branch (GitHub)
    |
    v
GitHub Webhook
    |
    v
Jenkins Pipeline
    |
    v
Build and Testing
    |
    v
Docker Image Creation and Push
    |
    v
Argo CD
    |
    v
Development Kubernetes Cluster
    |
    v
Developer Tests the Feature
```

The Jenkins pipeline can perform:

- Code checkout
- Application build
- Unit testing
- Code quality analysis
- Docker image creation
- Image scanning
- Image push to a container registry

Argo CD helps deploy the application to the Development Kubernetes cluster using the configuration stored in Git.

**Purpose:** To allow developers to test the features they are building.

### B. Staging / QA Environment

Once different developers complete their features, the changes are reviewed and merged into the Main branch.

Now the application contains multiple integrated features.

The integrated application is deployed to the Staging environment.

```text
Main Branch (GitHub)
        |
        v
   Jenkins Pipeline
        |
        v
      Argo CD
        |
        v
 Staging Kubernetes Cluster
        |
        v
      QA Team
```

The QA team (Quality Assurance team) tests whether the application works correctly.

For example:

- Does the login page work?
- Can customers add products to the cart?
- Does the payment system work?
- Are there any bugs?
- Do the different features work together?

The QA team may perform different types of testing:

**Functional Testing:** Checks whether the application features work as expected.

**Regression Testing:** Checks whether new changes have broken features that were already working.

**Performance Testing:** Checks how well the application performs under different workloads.

**Penetration Testing:** Checks for security weaknesses by testing the application for possible attacks.

After completing the required testing, the QA team provides approval. This is called **QA Sign-off**.

**Purpose:** To test the integrated application before preparing a release.

### C. Pre-Production / UAT Environment

After the QA team approves the application, the company prepares a release.

A Release Branch is created from Main, and the release pipeline deploys that version to the Pre-Production environment.

```text
Main Branch
    |
    v
Release Branch
    |
    v
Jenkins Release Pipeline
    |
    v
Argo CD
    |
    v
Pre-Production Environment
    |
    v
Final Testing and Approval
```

**What is Pre-Production?**

Pre-Production is an environment designed to closely resemble the Production environment.

It tries to use similar:

- Application configuration
- Infrastructure
- Networking
- Deployment settings

This helps the team identify problems before deploying the application to real customers.

**What is UAT?**

UAT stands for User Acceptance Testing.

In this stage, business users or designated users check whether the application meets their requirements.

For example, they may verify:

- Can users log in?
- Can customers purchase products?
- Does the payment system work correctly?
- Are the business requirements satisfied?

The team performs final validation and obtains the required approval before production deployment.

**Purpose:** To perform final testing and validation before releasing the application to customers.

### D. Production Environment

Production is the live environment where real customers use the application.

Once the application passes the required testing and approvals, it is deployed to Production.

```text
Release Branch
      |
      v
Release Pipeline
      |
      v
Final Approval
      |
      v
Production Environment
      |
      v
Real Customers Use the Application
```

For an online shopping application, customers use Production to:

- Log in
- Browse products
- Add products to their cart
- Make payments
- Place orders

Production requires stricter access controls because it handles the live application and real customer activity.

Not every developer or QA engineer should have direct access to the Production cluster.

**Purpose:** To make the application available to real customers.

---

## 4. Connecting Git Branches and Environments

This is the most important part of the lesson.

The branches and environments work together to move application code safely from development to production.

```text
       FEATURE BRANCH
              |
              v
       DEVELOPMENT
              |
       Feature Testing
              |
              v
         MAIN BRANCH
              |
              v
        STAGING / QA
              |
          QA Sign-off
              |
              v
        RELEASE BRANCH
              |
              v
      PRE-PRODUCTION
              |
       Final Validation
              |
              v
          PRODUCTION
              |
              v
       Live Application
```

Each stage has a different purpose:

| Stage | What Happens |
|---|---|
| Feature Branch | Developers build individual features |
| Development | Developers test their features |
| Main Branch | Approved changes are integrated |
| Staging / QA | QA team tests the integrated application |
| Release Branch | A stable application version is prepared |
| Pre-Production | Final testing and approval take place |
| Production | The application is released to customers |

The application does not move directly from a developer's laptop to customers. It passes through different stages of testing and approval.

---

## 5. Why Do We Need Different Kubernetes Clusters?

In this lesson, the teacher explained that organizations can use separate Kubernetes clusters for different environments.

For example:

```text
Dev Cluster
    |
    v
Development Environment

Staging Cluster
    |
    v
QA Testing

Pre-Prod Cluster
    |
    v
Final Validation

Prod Cluster
    |
    v
Live Customers
```

Why use separate clusters?

- Different teams need different access permissions.
- Development changes should not affect Production.
- Production requires stronger security.
- Each environment can have its own resources and configuration.
- It provides better isolation between environments.

It is also technically possible to use separate Kubernetes namespaces within the same cluster for different environments.

However, separate clusters provide stronger isolation, especially between Pre-Production and Production.

**Important:** The exact architecture depends on the organization. Some companies use separate clusters, while others use namespaces for certain environments.

---

## 6. Jenkins Pipelines Across Different Environments

Jenkins automates the application build, testing and deployment process.

The pipeline stages are generally similar across environments, but additional testing and approvals may be added as the application moves closer to Production.

Common pipeline stages include:

1. Checkout code from GitHub.
2. Build the application.
3. Run unit tests.
4. Perform code quality analysis.
5. Build the Docker image.
6. Scan the Docker image.
7. Push the image to a container registry.
8. Deploy the application.

Different environments may have additional activities:

| Environment | Activities |
|---|---|
| Development | Basic build and testing |
| Staging | Functional and regression testing |
| Pre-Production | Final validation, performance and security testing |
| Production | Final approvals and controlled deployment |

The same pipeline can be configured with different stages and conditions, or organizations can maintain separate pipelines for different environments.

### What is a Jenkins Multibranch Pipeline?

A Jenkins Multibranch Pipeline automatically discovers different branches in a Git repository and runs the Jenkinsfile found in each branch.

For example:

```text
GitHub Repository
       |
       |-- feature/login
       |
       |-- feature/payment
       |
       |-- main
       |
       |-- release/v1.0
       |
       |-- hotfix/payment-bug
```

Instead of manually creating a separate Jenkins job for every branch, Jenkins can discover these branches and manage their pipelines.

**Purpose:** To manage CI/CD pipelines for multiple Git branches more easily.

---

## 7. Can One Argo CD Instance Manage All Environments?

Yes. There are two approaches explained in this lesson.

### Approach 1: Separate Argo CD Instances

Organizations can maintain separate Argo CD installations for different environments.

For example:

- One Argo CD instance for Development.
- One for Staging.
- One for Pre-Production.
- One for Production.

### Approach 2: One Argo CD Instance

A single Argo CD instance can also manage multiple applications and Kubernetes clusters, provided it has the required configuration and permissions.

For example, a Git repository can contain separate folders for each environment:

```text
kubernetes-manifests/
│
├── dev/
│   └── values.yaml
│
├── staging/
│   └── values.yaml
│
├── preprod/
│   └── values.yaml
│
└── prod/
    └── values.yaml
```

Each folder contains the configuration for its respective environment.

Argo CD Applications can be configured to watch these folders and deploy the required configuration to the corresponding Kubernetes clusters.

```text
             Git Repository
                    |
                    v
              Argo CD
                    |
       +------------+------------+
       |            |            |
       v            v            v
      Dev         Staging      Pre-Prod
       |            |            |
       v            v            v
   Dev Cluster  QA Cluster  Pre-Prod Cluster

                    |
                    v
               Prod Cluster
```

**Purpose:** Argo CD helps keep Kubernetes environments synchronized with the configuration stored in Git.

---

## 8. Complete Lesson Summary

| Topic | What I Learned |
|---|---|
| Feature Branch | Developers work on individual features |
| Main Branch | Integrates approved development changes |
| Release Branch | Prepares a particular application version |
| Hotfix Branch | Fixes critical production issues |
| Development | Developers test new features |
| Staging / QA | QA team tests integrated changes |
| Pre-Production / UAT | Final testing and validation before production |
| Production | Live environment used by customers |
| Kubernetes Clusters | Provide separate environments and isolation |
| Jenkins Pipeline | Automates application build, testing and deployment |
| Multibranch Pipeline | Manages pipelines across multiple Git branches |
| Argo CD | Synchronizes Git configurations with Kubernetes |

## 9. Key Takeaways

- Git branches help developers work independently.
- Different environments help test applications before release.
- Jenkins automates the CI/CD process.
- QA teams test integrated application changes in Staging.
- Release branches help prepare stable application versions.
- Pre-Production is used for final validation before Production.
- Production requires stricter access controls.
- Separate Kubernetes clusters provide stronger environment isolation.
- Jenkins Multibranch Pipeline manages pipelines across multiple branches.
- Argo CD can manage deployments across multiple environments and clusters.

**Final Understanding:**

An application moves from Development to Production through a controlled process. Developers build features in separate branches, changes are integrated into Main, QA tests the application, a Release Branch is prepared, and the application passes through Pre-Production before reaching real customers in Production.
