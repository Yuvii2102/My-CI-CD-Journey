# End-to-End CI/CD Pipeline for a Dockerized Django To-Do Application Using Python, Jenkins, Docker Hub, GitHub, Argo CD and Kubernetes on AWS EC2

## Complete End-to-End CI/CD Project: From Scratch to Deployment

### Technology Stack

- AWS EC2
- Linux
- Git
- GitHub
- Docker
- Docker Hub
- Jenkins
- Kubernetes
- Minikube
- Argo CD
- YAML
- socat

## Project Workflow

1. Developer commits code to GitHub.
2. Jenkins checks out the code and builds a Docker image.
3. Docker Hub stores the new image.
4. Jenkins updates the Kubernetes manifest in GitHub.
5. Argo CD detects the changes and synchronizes them.
6. Kubernetes deploys the updated application.

## Project overview

### What am I building?

I am building a CI/CD pipeline for a Django To-Do application.

The project has two major parts:

**Part 1 – Dockerized Application Deployment**
- Get the Django application from the teacher's source repository.
- Clone the application to an AWS EC2 instance.
- Understand and configure its Dockerfile.
- Build a Docker image.
- Run the application inside a Docker container.
- Access the application through the EC2 public IP.

**Part 2 – End-to-End CI/CD Pipeline**
- Push the application source code to my GitHub repository.
- Configure Jenkins.
- Build and push Docker images automatically.
- Update Kubernetes deployment manifests through Jenkins.
- Create a Kubernetes cluster using Minikube.
- Install Argo CD.
- Connect Argo CD to GitHub.
- Enable automatic synchronization.
- Test the complete CI/CD workflow.

---

# PART 1: Dockerized Django Application Deployment on AWS EC2

## 1. Understand the application

The application is a Django-based To-Do application.

Django is a Python web framework used to build web applications.

The application allows users to:
- Open the To-Do page.
- Add tasks.
- View tasks.
- Manage their To-Do list.

The application runs on port `8000`.

## 2. Create an AWS EC2 instance

I created an EC2 instance to host the application and later use it for Jenkins and Kubernetes.

### Instance configuration

| Configuration | Value |
|---|---|
| Operating System | Ubuntu |
| Instance Type | Suitable instance with enough RAM and CPU for Jenkins and Minikube |
| Storage | Enough disk space for Docker images and Kubernetes |
| Access | SSH / EC2 Instance Connect |

I connected to the instance using AWS EC2 Instance Connect.

## 3. Install Docker

First, I updated the package information.

```bash
sudo apt update
```

I installed Docker using the official Docker Engine installation instructions for Ubuntu.

Official documentation:

https://docs.docker.com/engine/install/ubuntu/

After installation, I checked Docker:

```bash
docker --version
```

I also checked whether Docker was running:

```bash
sudo systemctl status docker
```

I added the Ubuntu user to the Docker group:

```bash
sudo usermod -aG docker $USER
```

I refreshed the group membership by reconnecting to the terminal.

Then I verified Docker access:

```bash
docker ps
```

## 4. Clone the teacher's application repository

I cloned the original repository containing the Django application.

```bash
git clone <TEACHER-REPOSITORY-URL>
```

I entered the project directory and located the Django application folder.

The application folder used in this project was:

```text
07 - Dockerized Django To-Do Application Deployment on AWS EC2
```

I checked the files:

```bash
ls
```

Important application files included:

```text
Dockerfile
manage.py
db.sqlite3
todoApp/
todos/
```

## 5. Understand and configure the Dockerfile

The Dockerfile defines how Docker builds the Django application image.

For this project, I used Python 3.10 because the Django 3.2 application was compatible with that version.

Example Dockerfile:

```dockerfile
FROM python:3.10

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

RUN python manage.py collectstatic --noinput

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
```

The exact Dockerfile should match the application's existing requirements and configuration.

### Understanding the instructions

| Instruction | Purpose |
|---|---|
| `FROM` | Selects the base image |
| `WORKDIR` | Sets the working directory |
| `COPY` | Copies application files into the image |
| `RUN` | Executes commands during image creation |
| `EXPOSE` | Documents the application port |
| `CMD` | Defines the default container startup command |

## 6. Build the Docker image

I navigated into the application folder:

```bash
cd "07 - Dockerized Django To-Do Application Deployment on AWS EC2"
```

I built the Docker image:

```bash
docker build -t django-todo .
```

I checked the created image:

```bash
docker images
```

The image name was:

```text
django-todo
```

## 7. Run the Docker container

I started the Django application inside a Docker container:

```bash
docker run -d -p 8000:8000 --name django-todo django-todo
```

### Understanding the command

| Option | Purpose |
|---|---|
| `-d` | Runs the container in the background |
| `-p 8000:8000` | Maps host port 8000 to container port 8000 |
| `--name` | Assigns a container name |
| `django-todo` | Image used to create the container |

I checked the running container:

```bash
docker ps
```

## 8. Configure the AWS Security Group

I added an inbound rule to allow access to the Django application.

| Type | Port | Source |
|---|---:|---|
| Custom TCP | 8000 | My IP |

For public testing, access can be configured according to the required security policy.

## 9. Access the application

I opened the application in my browser:

```text
http://<EC2-PUBLIC-IP>:8000/todos/
```

I verified that the Django To-Do application was running successfully.

I also customized the page title to:

```text
Todo List - Yuvraj
```

**Part 1 was completed successfully.**

---

# PART 2: End-to-End CI/CD Pipeline

## 10. Create my GitHub repository

After completing the Docker deployment, I created my own repository:

https://github.com/Yuvii2102/My-CI-CD-Journey

I used one repository for:
- Django application source code.
- Dockerfile.
- Jenkinsfile.
- Kubernetes deployment manifest.
- Kubernetes service manifest.

I did not use a separate manifests repository.

### Final repository structure

```text
My-CI-CD-Journey/
│
└── 07 - Dockerized Django To-Do Application Deployment on AWS EC2/
    │
    ├── Dockerfile
    ├── manage.py
    ├── db.sqlite3
    ├── Jenkinsfile
    ├── docker-compose.yml
    │
    ├── todoApp/
    ├── todos/
    ├── staticfiles/
    │
    └── deploy/
        ├── deploy.yaml
        ├── service.yaml
        └── pod.yaml
```

I copied the application files from the original project into my own repository and committed them to GitHub.

The important point is that Jenkins and Argo CD both use this same repository.

## 11. Push the Docker image to Docker Hub

I created a public Docker Hub repository:

https://hub.docker.com/r/yuvi2102/django-todo

I logged in:

```bash
docker login
```

I tagged the local image:

```bash
docker tag django-todo:latest yuvi2102/django-todo:latest
```

I pushed it:

```bash
docker push yuvi2102/django-todo:latest
```

I verified that the image could be downloaded:

```bash
docker pull yuvi2102/django-todo:latest
```

Now Docker Hub contained the Django application image.

## 12. Configure Jenkins

I installed and configured Jenkins on the EC2 instance.

I accessed the Jenkins dashboard:

```text
http://<EC2-PUBLIC-IP>:8080
```

I created a Pipeline job named:

```text
django-todo-cicd
```

### 12.1 Configure Docker Hub credentials

I generated a Docker Hub Personal Access Token.

In Jenkins, I navigated to:

Manage Jenkins → Credentials → System → Global credentials → Add Credentials.

I configured:

| Field | Value |
|---|---|
| Kind | Username with password |
| Username | yuvi2102 |
| Password | Docker Hub Personal Access Token |
| ID | dockerhub-credentials |
| Description | Docker Hub Credentials |

### 12.2 Configure GitHub credentials

I generated a GitHub Personal Access Token with access to my repository.

The token required permission to read and write repository contents.

I added it in Jenkins:

| Field | Value |
|---|---|
| Kind | Username with password |
| Username | Yuvii2102 |
| Password | GitHub Personal Access Token |
| ID | github-credentials |
| Description | GitHub Repository Credentials |

These credential IDs were referenced in the Jenkinsfile.

**I never place actual passwords or access tokens directly in the Jenkinsfile.**

## 13. Create the Jenkinsfile

I created a file named:

```text
Jenkinsfile
```

This file defines the stages of the CI pipeline.

The pipeline contains four stages.

### Stage 1: Checkout

Jenkins downloads the latest code from GitHub.

### Stage 2: Build Docker Image

Jenkins builds a Docker image and tags it using the Jenkins build number.

For example:

```text
yuvi2102/django-todo:1
yuvi2102/django-todo:2
yuvi2102/django-todo:3
```

### Stage 3: Push to Docker Hub

Jenkins logs in to Docker Hub and pushes the newly built image.

### Stage 4: Update Kubernetes Manifest

Jenkins updates the image reference in `deploy.yaml` and pushes the modified manifest to GitHub.

### Final Jenkinsfile used in the project

```groovy
pipeline {
    agent any

    environment {
        IMAGE_NAME = 'yuvi2102/django-todo'
        APP_DIR = '07 - Dockerized Django To-Do Application Deployment on AWS EC2'
    }

    stages {

        stage('Checkout') {
            steps {
                git branch: 'main',
                    url: 'https://github.com/Yuvii2102/My-CI-CD-Journey.git'
            }
        }

        stage('Build Docker Image') {
            steps {
                dir("${APP_DIR}") {
                    sh 'docker build -t $IMAGE_NAME:$BUILD_NUMBER .'
                    sh 'docker tag $IMAGE_NAME:$BUILD_NUMBER $IMAGE_NAME:latest'
                }
            }
        }

        stage('Push to Docker Hub') {
            steps {
                withCredentials([
                    usernamePassword(
                        credentialsId: 'dockerhub-credentials',
                        usernameVariable: 'DOCKER_USER',
                        passwordVariable: 'DOCKER_PASSWORD'
                    )
                ]) {
                    sh '''
                        echo "$DOCKER_PASSWORD" | docker login \
                            -u "$DOCKER_USER" --password-stdin

                        docker push $IMAGE_NAME:$BUILD_NUMBER
                        docker push $IMAGE_NAME:latest

                        docker logout
                    '''
                }
            }
        }

        stage('Update Kubernetes Manifest') {
            steps {
                withCredentials([
                    usernamePassword(
                        credentialsId: 'github-credentials',
                        usernameVariable: 'GIT_USER',
                        passwordVariable: 'GIT_TOKEN'
                    )
                ]) {
                    sh '''
                        git config user.name "Jenkins"
                        git config user.email "jenkins@example.com"

                        sed -i "s|image: .*|image: ${IMAGE_NAME}:${BUILD_NUMBER}|" \
                        "${APP_DIR}/deploy/deploy.yaml"

                        git add "${APP_DIR}/deploy/deploy.yaml"

                        git commit -m "Update Django image to build ${BUILD_NUMBER}" || true

                        git push https://${GIT_USER}:${GIT_TOKEN}@github.com/Yuvii2102/My-CI-CD-Journey.git HEAD:main
                    '''
                }
            }
        }
    }
}
```

### Important Jenkins configuration

I configured the Jenkins job to use Pipeline script from SCM or the appropriate pipeline configuration used for the repository.

The pipeline uses:
- GitHub repository URL.
- `main` branch.
- Jenkinsfile from the repository.

I saved the job configuration and triggered the first build.

I verified the four stages in Console Output.

**Note:** In our actual project, I triggered Jenkins manually using Build Now after committing the code to GitHub. A GitHub webhook was not configured.

---

## 14. Install and configure Minikube

Minikube provides a Kubernetes cluster that runs on a local machine or server.

I used Minikube with Docker as its driver on my EC2 instance.

### Step 1: Verify kubectl

```bash
kubectl version --client
```

### Step 2: Verify Minikube

```bash
minikube version
```

### Step 3: Start Minikube

```bash
minikube start --driver=docker
```

### Step 4: Check the Kubernetes node

```bash
kubectl get nodes
```

Expected result:

```text
NAME       STATUS   ROLES           AGE   VERSION
minikube   Ready    control-plane   ...   ...
```

### Step 5: Check Kubernetes system pods

```bash
kubectl get pods -A
```

I verified that the Kubernetes system components were running.

---

## 15. Create Kubernetes manifests

I created a `deploy` directory inside the Django application folder.

```bash
mkdir -p deploy
```

### 15.1 Deployment manifest

File:

```text
deploy/deploy.yaml
```

Content:

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: django-todo
  labels:
    app: django-todo
spec:
  replicas: 2
  selector:
    matchLabels:
      app: django-todo
  template:
    metadata:
      labels:
        app: django-todo
    spec:
      containers:
        - name: django-todo
          image: yuvi2102/django-todo:latest
          ports:
            - containerPort: 8000
```

### Understanding the Deployment

- `replicas: 2` means Kubernetes maintains two application pods.
- `selector` identifies the pods managed by the Deployment.
- `image` identifies the Docker image to run.
- `containerPort: 8000` identifies the Django application port inside the container.

Jenkins later replaces the image tag with the current build number.

### 15.2 Service manifest

File:

```text
deploy/service.yaml
```

Content:

```yaml
apiVersion: v1
kind: Service
metadata:
  name: django-todo-service
spec:
  type: NodePort
  selector:
    app: django-todo
  ports:
    - protocol: TCP
      port: 80
      targetPort: 8000
      nodePort: 31000
```

### Understanding the Service

- `type: NodePort` exposes the service through a port on the Kubernetes node.
- `port: 80` is the Service port.
- `targetPort: 8000` forwards traffic to the Django container.
- `nodePort: 31000` is the selected NodePort.

I committed the manifests to the `main` branch of my existing GitHub repository.

---

## 16. Install Argo CD

Argo CD is a GitOps continuous delivery tool for Kubernetes.

It monitors a Git repository and synchronizes the Kubernetes cluster with the desired configuration stored in Git.

### Step 1: Create the namespace

```bash
kubectl create namespace argocd
```

### Step 2: Install Argo CD

```bash
kubectl apply -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml
```

### Step 3: Verify Argo CD pods

```bash
kubectl get pods -n argocd
```

I waited for the Argo CD components to become Running.

### Step 4: Check Argo CD services

```bash
kubectl get svc -n argocd
```

### Step 5: Expose the Argo CD server

I configured the Argo CD server as a NodePort Service.

```bash
kubectl patch svc argocd-server -n argocd -p '{"spec":{"type":"NodePort","ports":[{"name":"http","port":80,"targetPort":8080,"protocol":"TCP","nodePort":30080},{"name":"https","port":443,"targetPort":8080,"protocol":"TCP","nodePort":30443}]}}'
```

### Step 6: Configure HTTP access for the forwarding setup

```bash
kubectl patch configmap argocd-cmd-params-cm -n argocd -p '{"data":{"server.insecure":"true"}}'
```

Restart the server:

```bash
kubectl rollout restart deployment argocd-server -n argocd
```

Verify:

```bash
kubectl get pods -n argocd
```

---

## 17. Access Argo CD through EC2

Minikube was running inside Docker. Its internal network was not directly exposed through the EC2 public IP.

I used `socat` to forward external EC2 traffic to the Minikube NodePort.

### Step 1: Install socat

```bash
sudo apt-get update
sudo apt-get install -y socat
```

### Step 2: Start the forwarding process

```bash
sudo nohup socat TCP-LISTEN:8088,bind=0.0.0.0,fork,reuseaddr TCP:192.168.49.2:30080 >/tmp/socat.log 2>&1 &
```

This forwarded:

```text
EC2 Public IP:8088
        |
        v
      socat
        |
        v
Minikube IP:30080
        |
        v
    Argo CD
```

### Step 3: Verify the listening port

```bash
sudo ss -lntp | grep 8088
```

### Step 4: Retrieve the initial admin password

```bash
kubectl -n argocd get secret argocd-initial-admin-secret \
-o jsonpath="{.data.password}" | base64 -d
```

Username:

```text
admin
```

I opened:

```text
http://<EC2-PUBLIC-IP>:8088
```

### AWS Security Group

The required inbound rules for this project were:

| Port | Purpose |
|---:|---|
| 8080 | Jenkins |
| 8088 | Argo CD |
| 8001 | Temporary Django application access test |

During our connectivity testing, port 8088 had to allow traffic from anywhere (`0.0.0.0/0`) for the browser connection to work.

For a secure setup, restrict this administrative port to trusted IP addresses or use private access. Do not leave the Argo CD dashboard publicly exposed.

---

## 18. Create an Argo CD application

I opened the Argo CD dashboard and clicked **NEW APP**.

I configured the following settings.

### General

| Field | Value |
|---|---|
| Application Name | django-todo |
| Project Name | default |
| Sync Policy | Automatic |
| Prune Resources | Enabled |
| Self Heal | Enabled |

### Source

| Field | Value |
|---|---|
| Repository URL | https://github.com/Yuvii2102/My-CI-CD-Journey.git |
| Revision | HEAD |
| Revision Type | Branches |
| Path | 07 - Dockerized Django To-Do Application Deployment on AWS EC2/deploy |

### Destination

| Field | Value |
|---|---|
| Cluster URL | https://kubernetes.default.svc |
| Namespace | default |

I kept Directory Recurse unchecked.

I clicked CREATE.

### Verify Argo CD

I opened the `django-todo` application.

The initial status became:

```text
Health: Healthy
Sync: Synced
```

This confirmed that Argo CD had successfully fetched and applied the Kubernetes manifests.

---

## 19. Verify the Django application in Kubernetes

I checked all Kubernetes resources:

```bash
kubectl get all -n default
```

I verified the Deployment:

```bash
kubectl get deployment django-todo
```

I verified the pods:

```bash
kubectl get pods
```

Expected result: two Django application pods running.

I verified the Service:

```bash
kubectl get svc
```

Expected Service:

```text
django-todo-service
```

with NodePort `31000`.

### Test application access

I forwarded the Kubernetes Service to the EC2 host:

```bash
kubectl port-forward svc/django-todo-service 8001:80 --address 0.0.0.0
```

I opened:

```text
http://<EC2-PUBLIC-IP>:8001/todos/
```

The Django To-Do application opened successfully.

---

# 20. Final End-to-End CI/CD Test

This was the final test to verify that Jenkins and Argo CD worked together.

### Step 1: Change the application code

I opened my GitHub repository.

I navigated to:

```text
07 - Dockerized Django To-Do Application Deployment on AWS EC2/index.html
```

I changed the heading from:

```text
Todo List - Yuvraj
```

to:

```text
Todo List - Yuvraj | CI/CD Pipeline Test
```

I committed the change directly to `main`.

### Step 2: Trigger Jenkins

I opened Jenkins and selected:

```text
django-todo-cicd
```

I clicked:

```text
Build Now
```

Jenkins executed all four pipeline stages.

### Step 3: Build the Docker image

Jenkins checked out the latest source code and built a new image.

The successful test produced:

```text
yuvi2102/django-todo:3
```

### Step 4: Push the image to Docker Hub

Jenkins pushed the new image to:

```text
https://hub.docker.com/r/yuvi2102/django-todo
```

### Step 5: Update the Kubernetes manifest

Jenkins updated `deploy.yaml`.

The image reference became:

```yaml
image: yuvi2102/django-todo:3
```

Jenkins committed and pushed the updated manifest to GitHub.

### Step 6: Argo CD detects the change

Argo CD monitored the GitHub repository and detected the new commit.

Since automatic synchronization was enabled, Argo CD synchronized the changes with Kubernetes.

The application returned to:

```text
Health: Healthy
Sync: Synced
```

### Step 7: Verify the deployed Docker image

I ran:

```bash
kubectl get deployment django-todo -o jsonpath='{.spec.template.spec.containers[0].image}'
```

Final output:

```text
yuvi2102/django-todo:3
```

This confirmed that the new Docker image had been deployed successfully.

---

# 21. Final Project Architecture

```mermaid
flowchart TD
    A[Developer] --> B[GitHub]
    B --> C[Jenkins]
    C --> D[Docker Build]
    D --> E[Docker Hub]
    E --> F[Update deploy.yaml]
    F --> G[GitHub]
    G --> H[Argo CD]
    H --> I[Kubernetes Cluster]
    I --> J[Django Pod 1]
    I --> K[Django Pod 2]
    J --> L[Django To-Do Application]
    K --> L
```

# 22. Final Verification Checklist

## Part 1

- [x] AWS EC2 instance created.
- [x] Docker installed.
- [x] Django application cloned.
- [x] Dockerfile configured.
- [x] Docker image built.
- [x] Container started.
- [x] Application accessed through port 8000.

## Part 2

- [x] GitHub repository created.
- [x] Docker Hub repository created.
- [x] Docker image pushed to Docker Hub.
- [x] Jenkins configured.
- [x] Docker Hub credentials configured.
- [x] GitHub credentials configured.
- [x] Jenkinsfile created.
- [x] Four-stage pipeline executed successfully.
- [x] Minikube installed and started.
- [x] Kubernetes Deployment created.
- [x] Kubernetes Service created.
- [x] Argo CD installed.
- [x] Argo CD connected to GitHub.
- [x] Automatic sync enabled.
- [x] Two Django replicas deployed.
- [x] Application accessed through Kubernetes.
- [x] New application code committed.
- [x] Jenkins built Docker image `:3`.
- [x] Docker image pushed to Docker Hub.
- [x] Kubernetes manifest updated by Jenkins.
- [x] Argo CD automatically synchronized the change.
- [x] Kubernetes verified the running image as `:3`.

---

# 23. What I Learned

Through this project, I learned:

1. How to containerize a Django application using Docker.
2. How to build, tag and push Docker images.
3. How to configure Jenkins credentials.
4. How to write a Jenkins declarative pipeline.
5. How to automate Docker image builds and pushes.
6. How to update Kubernetes manifests using Jenkins.
7. How to create Kubernetes Deployments and Services.
8. How to run Kubernetes using Minikube.
9. How to install and configure Argo CD.
10. How GitOps works in real deployment workflows.
11. How Argo CD automatically synchronizes Git changes with Kubernetes.
12. How Jenkins CI and Argo CD continuous delivery work together.

---

# 24. Documentation and Official Learning Resources

These are the official documentation sources I used as references for understanding and implementing the project.

| Technology | Documentation |
|---|---|
| Docker | https://docs.docker.com/ |
| Docker Hub | https://docs.docker.com/docker-hub/ |
| Jenkins Pipeline | https://www.jenkins.io/doc/book/pipeline/ |
| Jenkins Credentials | https://www.jenkins.io/doc/book/using/using-credentials/ |
| Kubernetes | https://kubernetes.io/docs/ |
| Kubernetes Deployments | https://kubernetes.io/docs/concepts/workloads/controllers/deployment/ |
| Kubernetes Services | https://kubernetes.io/docs/concepts/services-networking/service/ |
| kubectl | https://kubernetes.io/docs/reference/kubectl/ |
| Minikube | https://minikube.sigs.k8s.io/docs/ |
| Argo CD | https://argo-cd.readthedocs.io/en/stable/ |
| Argo CD Automated Sync | https://argo-cd.readthedocs.io/en/stable/user-guide/auto_sync/ |
| AWS EC2 | https://docs.aws.amazon.com/ec2/ |
| AWS Security Groups | https://docs.aws.amazon.com/vpc/latest/userguide/vpc-security-groups.html |
| socat | http://www.dest-unreach.org/socat/ |

I used these resources to understand the commands, configurations and concepts. The commands and YAML files were adapted to my own project environment.

---

# 25. Final Conclusion

I successfully built an end-to-end CI/CD pipeline for a Dockerized Django To-Do application using Jenkins, Docker Hub, GitHub, Kubernetes and Argo CD.

In Part 1, I learned how to containerize and deploy a Django application using Docker on AWS EC2.

In Part 2, I automated the build and deployment process using Jenkins and Argo CD.

Jenkins handled Continuous Integration by building Docker images, pushing them to Docker Hub and updating Kubernetes manifests in GitHub.

Argo CD handled GitOps-based Continuous Delivery by monitoring GitHub and synchronizing changes with the Kubernetes cluster.

Finally, I tested the complete workflow by changing the application code, triggering Jenkins Build #3 and verifying that Kubernetes was running the updated Docker image.

**Final Docker image:**

```text
yuvi2102/django-todo:3
```

**Final deployment status:**

```text
Jenkins Pipeline: SUCCESS
Argo CD: HEALTHY
Argo CD Sync: SYNCED
Kubernetes: 2/2 REPLICAS RUNNING
```

This project gave me practical experience with Docker, Jenkins, Kubernetes, GitOps and automated application deployment on AWS EC2.


## Important Notes for Reproducing the Project

Before repeating this project on a new EC2 instance, remember these important points.

### 1. Source Repository

I first used the original repository provided by my teacher to get the Django application.

After that, I copied the application files into my own GitHub repository, `My-CI-CD-Journey`.

For future setups, I can directly clone my own repository:

```bash
git clone https://github.com/Yuvii2102/My-CI-CD-Journey.git
```

### 2. Application Folder

The application folder name contains spaces. So, always use quotation marks when navigating into it.

```bash
cd "My-CI-CD-Journey/07 - Dockerized Django To-Do Application Deployment on AWS EC2"
```

This helps the terminal understand the complete folder name correctly.

### 3. Dockerfile Configuration

The original Dockerfile used `python:3` as its base image.

I changed it to `python:3.10` because the application uses Django 3.2 and needed a compatible Python version.

```dockerfile
FROM python:3.10
```

Keep the other working Dockerfile settings unchanged unless there is a specific reason to modify them.

### 4. Jenkins Pipeline Trigger

In this project, I started the Jenkins pipeline manually by clicking **Build Now**.

Jenkins did not automatically start when I pushed new code to GitHub because I did not configure a GitHub webhook.

A webhook can be added later to trigger Jenkins automatically after a code push.

### 5. After Restarting EC2

Whenever I stop and start the EC2 instance, I need to check whether the required services are running.

- Jenkins
- Minikube
- Argo CD
- `socat` forwarding process

The EC2 public IP address may change after restarting the instance.

If it changes, I need to use the new IP in my Jenkins and Argo CD access URLs and update any related Security Group rules if required.

### 6. GitHub Token Security

In my tested Jenkinsfile, I used a GitHub token in the HTTPS URL to push the updated Kubernetes manifest.

This worked successfully for the project.

However, putting a token directly in a Git URL can expose it through command details or Git configuration.

For a production setup, I should use a safer Git authentication method that uses Jenkins credentials without exposing the token in the URL or process arguments.

Never share GitHub tokens or passwords publicly.

### 7. Kubernetes and Database Storage

The Django application uses SQLite as its database.

In this project, I configured two application replicas to demonstrate how Kubernetes manages application pods.

However, SQLite is not a suitable database design for a production application running multiple replicas that need to share the same data.

For a real production application, I should use a proper database such as PostgreSQL or MySQL and configure suitable persistent storage and backups.

---

**Final Note:** These points will help me understand the important configurations and avoid common problems when setting up this project again on a fresh EC2 instance.

