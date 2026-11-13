# Part 2: End-to-End CI/CD Pipeline Using Jenkins, Docker Hub, GitHub, Argo CD and Kubernetes

## 1. Introduction

In Part 1, I created a Dockerized Django To-Do application and deployed it on an AWS EC2 instance.

In Part 2, I extended the project by implementing an end-to-end CI/CD pipeline using Jenkins, Docker Hub, GitHub, Kubernetes and Argo CD.

The main goal was to automate the application deployment process. Whenever I make a code change and trigger the Jenkins pipeline, Jenkins builds a new Docker image, pushes it to Docker Hub and updates the Kubernetes deployment manifest in GitHub.

Argo CD monitors the GitHub repository and automatically deploys the updated application to Kubernetes.

## 2. Project Architecture

The project follows this workflow:

```mermaid
flowchart TD
    A[Developer changes application code] --> B[GitHub Repository]
    B --> C[Jenkins Pipeline]
    C --> D[Build Docker Image]
    D --> E[Push Image to Docker Hub]
    E --> F[Update Kubernetes Manifest]
    F --> G[Push Updated Manifest to GitHub]
    G --> H[Argo CD Detects Git Changes]
    H --> I[Kubernetes Cluster]
    I --> J[Deploy Updated Django Application]
```

### How the pipeline works

1. I make changes to the Django application and push them to GitHub.
2. I trigger the Jenkins pipeline.
3. Jenkins checks out the latest source code.
4. Jenkins builds a new Docker image.
5. Jenkins pushes the image to Docker Hub.
6. Jenkins updates the Kubernetes deployment manifest with the new image tag.
7. Jenkins pushes the updated manifest to GitHub.
8. Argo CD detects the GitHub changes.
9. Argo CD synchronizes the changes with the Kubernetes cluster.
10. Kubernetes deploys the updated application.

## 3. Tools and Technologies Used

| Tool | Purpose |
|---|---|
| AWS EC2 | Hosts Jenkins and the Kubernetes environment |
| Jenkins | Automates the CI pipeline |
| Docker | Builds application container images |
| Docker Hub | Stores Docker images |
| GitHub | Stores application code and Kubernetes manifests |
| Minikube | Provides a local Kubernetes cluster inside EC2 |
| Kubernetes | Runs and manages the application containers |
| Argo CD | Automates Kubernetes deployment using GitOps |
| kubectl | Communicates with the Kubernetes cluster |
| socat | Forwards external EC2 traffic to the Argo CD service |

## 4. Project Repository Structure

I continued using my existing GitHub repository instead of creating a separate repository for Kubernetes manifests.

GitHub repository:

https://github.com/Yuvii2102/My-CI-CD-Journey

Project folder:

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

The `deploy` folder contains the Kubernetes manifests required to deploy the Django application.

## 5. Docker Hub Setup

Before creating the Jenkins pipeline, I pushed the Docker image created in Part 1 to Docker Hub.

Docker Hub repository:

https://hub.docker.com/r/yuvi2102/django-todo

### Step 1: Log in to Docker Hub

```bash
docker login
```

I entered my Docker Hub username and Personal Access Token.

### Step 2: Tag the Docker image

```bash
docker tag django-todo:latest yuvi2102/django-todo:latest
```

This assigned my Docker Hub repository name to the local image.

### Step 3: Push the image

```bash
docker push yuvi2102/django-todo:latest
```

### Step 4: Verify the image

```bash
docker pull yuvi2102/django-todo:latest
```

This confirmed that the image was available in Docker Hub.

## 6. Jenkins Configuration

I used my existing Jenkins installation on the AWS EC2 instance.

Jenkins dashboard:

```text
http://<EC2-PUBLIC-IP>:8080
```

I created a Jenkins pipeline job named:

```text
django-todo-cicd
```

### Step 1: Configure Docker Hub credentials

Jenkins needs Docker Hub credentials to push the newly built images.

I navigated to:

Manage Jenkins → Credentials → System → Global credentials → Add Credentials.

I configured:

| Field | Value |
|---|---|
| Kind | Username with password |
| Username | yuvi2102 |
| Password | Docker Hub Personal Access Token |
| ID | dockerhub-credentials |
| Description | Docker Hub Credentials |

The ID is important because it is referenced in the Jenkinsfile.

### Step 2: Configure GitHub credentials

Jenkins also needs permission to update the Kubernetes manifest in GitHub.

I created a GitHub Personal Access Token with access to my `My-CI-CD-Journey` repository and the required Contents read and write permissions.

I added the credentials in Jenkins:

| Field | Value |
|---|---|
| Kind | Username with password |
| Username | Yuvii2102 |
| Password | GitHub Personal Access Token |
| ID | github-credentials |
| Description | GitHub Repository Credentials |

I used the following credential IDs in the pipeline:

- `dockerhub-credentials`
- `github-credentials`

**Important:** I never store my actual passwords or tokens directly in the Jenkinsfile.

## 7. Jenkins Pipeline Configuration

The Jenkins pipeline contains four main stages.

### Stage 1: Checkout

Jenkins downloads the latest application source code from GitHub.

### Stage 2: Build Docker Image

Jenkins builds a new Docker image using the Dockerfile present in the application folder.

The image is tagged using the Jenkins build number.

For example:

```text
yuvi2102/django-todo:1
yuvi2102/django-todo:2
yuvi2102/django-todo:3
```

### Stage 3: Push to Docker Hub

Jenkins logs in to Docker Hub using the stored credentials and pushes both the build-specific image and the latest tag.

### Stage 4: Update Kubernetes Manifest

Jenkins updates the image reference inside `deploy.yaml` with the current build number.

It then commits and pushes the updated manifest to GitHub.

### Final Jenkinsfile

I used the following Jenkinsfile:

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

### Understanding the Jenkinsfile

| Jenkinsfile section | Purpose |
|---|---|
| `agent any` | Runs the pipeline on any available Jenkins agent |
| `environment` | Defines the Docker image name and application directory |
| `Checkout` | Downloads the GitHub repository |
| `Build Docker Image` | Builds and tags the Docker image |
| `Push to Docker Hub` | Pushes the image to Docker Hub |
| `Update Kubernetes Manifest` | Updates the image tag and pushes the manifest to GitHub |
| `BUILD_NUMBER` | Provides the Jenkins build number |

### Pipeline execution

I opened the `django-todo-cicd` job in Jenkins and clicked **Build Now**.

I checked the Console Output to verify each stage.

The pipeline completed successfully.

## 8. Kubernetes Setup Using Minikube

After configuring Jenkins, I prepared a Kubernetes cluster using Minikube.

Minikube allows me to run a Kubernetes cluster on a single machine.

I used the Docker driver to run Minikube inside my EC2 instance.

### Step 1: Check kubectl

```bash
kubectl version --client
```

### Step 2: Check Minikube

```bash
minikube version
```

### Step 3: Start Minikube

```bash
minikube start --driver=docker
```

This created a Kubernetes cluster using Docker.

### Step 4: Check the cluster

```bash
kubectl get nodes
```

Expected result:

```text
NAME       STATUS   ROLES           AGE   VERSION
minikube   Ready    control-plane   ...   ...
```

### Step 5: Check Kubernetes pods

```bash
kubectl get pods -A
```

This displays the pods running in all Kubernetes namespaces.

I verified that the Kubernetes system components were running successfully.

## 9. Kubernetes Deployment Manifests

I created Kubernetes manifests inside the `deploy` folder of my existing GitHub repository.

### Step 1: Deployment manifest

File:

```text
deploy/deploy.yaml
```

Final configuration:

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

| Configuration | Explanation |
|---|---|
| `kind: Deployment` | Creates a Kubernetes Deployment |
| `name: django-todo` | Name of the deployment |
| `replicas: 2` | Runs two application pods |
| `selector` | Identifies the pods managed by the deployment |
| `image` | Docker image used by the application |
| `containerPort: 8000` | Application port inside the container |

The Jenkins pipeline automatically updates the image tag in this file.

### Step 2: Service manifest

File:

```text
deploy/service.yaml
```

Final configuration:

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

| Configuration | Explanation |
|---|---|
| `kind: Service` | Creates a Kubernetes Service |
| `type: NodePort` | Exposes the service through a node port |
| `port: 80` | Port exposed by the Service |
| `targetPort: 8000` | Port used by the Django container |
| `nodePort: 31000` | NodePort assigned to the application |
| `selector` | Connects the Service to the Django pods |

The Service provides a stable way to access the application pods.

## 10. Installing Argo CD

Argo CD is a GitOps continuous delivery tool for Kubernetes.

It continuously monitors the Git repository and compares the desired configuration stored in Git with the actual configuration running in Kubernetes.

When changes are detected, Argo CD can synchronize the cluster with the Git repository.

### Step 1: Create the Argo CD namespace

```bash
kubectl create namespace argocd
```

### Step 2: Install Argo CD

```bash
kubectl apply -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml
```

This installs Argo CD and its required Kubernetes resources.

### Step 3: Verify Argo CD pods

```bash
kubectl get pods -n argocd
```

I waited until the Argo CD components reached the Running state.

### Step 4: Check Argo CD services

```bash
kubectl get svc -n argocd
```

### Step 5: Expose Argo CD using NodePort

I changed the Argo CD server Service to NodePort and assigned ports 30080 and 30443.

```bash
kubectl patch svc argocd-server -n argocd -p '{"spec":{"type":"NodePort","ports":[{"name":"http","port":80,"targetPort":8080,"protocol":"TCP","nodePort":30080},{"name":"https","port":443,"targetPort":8080,"protocol":"TCP","nodePort":30443}]}}'
```

### Step 6: Configure Argo CD for HTTP access

For this project, I configured the Argo CD server to work without TLS behind the forwarding setup.

```bash
kubectl patch configmap argocd-cmd-params-cm -n argocd -p '{"data":{"server.insecure":"true"}}'
```

Restart the Argo CD server:

```bash
kubectl rollout restart deployment argocd-server -n argocd
```

Verify the pods:

```bash
kubectl get pods -n argocd
```

## 11. Accessing Argo CD Through the EC2 Public IP

Minikube was running inside Docker on the EC2 instance.

The Kubernetes NodePort was accessible through the Minikube node, but the Minikube internal network was not directly exposed through the EC2 public IP.

To forward external traffic from EC2 to the Argo CD service, I used `socat`.

### Step 1: Install socat

```bash
sudo apt-get update
sudo apt-get install -y socat
```

### Step 2: Forward EC2 port 8088 to the Minikube NodePort

```bash
sudo nohup socat TCP-LISTEN:8088,bind=0.0.0.0,fork,reuseaddr TCP:192.168.49.2:30080 >/tmp/socat.log 2>&1 &
```

This forwards traffic as follows:

```text
Browser
   |
   v
EC2 Public IP :8088
   |
   v
socat
   |
   v
Minikube Node IP :30080
   |
   v
Argo CD Server
```

### Step 3: Verify socat

```bash
sudo ss -lntp | grep 8088
```

I verified that `socat` was listening on `0.0.0.0:8088`.

### Step 4: Access the Argo CD dashboard

I opened the following URL in my browser:

```text
http://<EC2-PUBLIC-IP>:8088
```

### Step 5: Retrieve the initial admin password

```bash
kubectl -n argocd get secret argocd-initial-admin-secret \
-o jsonpath="{.data.password}" | base64 -d
```

Login details:

```text
Username: admin
Password: Initial password retrieved from Kubernetes Secret
```

The password should be kept private.

### AWS Security Group configuration

I configured the EC2 Security Group to allow the required inbound traffic.

| Type | Port | Purpose |
|---|---:|---|
| Custom TCP | 8080 | Jenkins dashboard |
| Custom TCP | 8088 | Argo CD dashboard |
| Custom TCP | 8001 | Temporary Django application test |

During the Argo CD connectivity test, I found that restricting port 8088 to my IP prevented access. Allowing traffic from `0.0.0.0/0` made the dashboard accessible.

**Security note:** Allowing `0.0.0.0/0` exposes the port to the internet. For a safer setup, restrict access to trusted public IP addresses or use a VPN or private access method. Do not leave the Argo CD administrative interface publicly accessible without appropriate protection.

Port 8001 was used for application verification and does not need to remain open after testing.

## 12. Creating an Argo CD Application

After accessing the Argo CD dashboard, I created a new application.

I clicked **NEW APP** and configured the following details.

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

The `HEAD` revision was selected from the Branches option in the Argo CD interface.

### Destination

| Field | Value |
|---|---|
| Cluster URL | https://kubernetes.default.svc |
| Namespace | default |

I kept Directory Recurse unchecked because my Kubernetes manifests were directly inside the `deploy` folder.

After entering the configuration, I clicked **CREATE**.

### Verify the application

I opened the `django-todo` application in Argo CD.

The application reached:

```text
Health Status: Healthy
Sync Status: Synced
```

This confirmed that Argo CD successfully retrieved the manifests from GitHub and deployed the application to Kubernetes.

## 13. Verifying the Kubernetes Deployment

After Argo CD synchronized the application, I checked the Kubernetes resources.

### Step 1: Check all resources

```bash
kubectl get all -n default
```

The expected resources included:

- Two Django application pods.
- One Django deployment.
- One ReplicaSet.
- One NodePort Service.

### Step 2: Check the deployment

```bash
kubectl get deployment django-todo
```

Expected result:

```text
NAME         READY   UP-TO-DATE   AVAILABLE
django-todo  2/2     2            2
```

### Step 3: Check the pods

```bash
kubectl get pods
```

Both Django pods should be Running and Ready.

### Step 4: Check the service

```bash
kubectl get svc
```

The service should show:

```text
django-todo-service   NodePort   ...   80:31000/TCP
```

## 14. Testing the Django Application

After confirming that the deployment was healthy, I tested the application through Kubernetes.

I used port forwarding to expose the Kubernetes Service through the EC2 host.

```bash
kubectl port-forward svc/django-todo-service 8001:80 --address 0.0.0.0
```

I kept this command running during the test.

I then opened:

```text
http://<EC2-PUBLIC-IP>:8001/todos/
```

The Django To-Do application opened successfully.

This confirmed that the application was accessible through the Kubernetes Service.

## 15. End-to-End CI/CD Testing

This was the final and most important part of the project.

I tested whether a code change could automatically move through the complete CI/CD pipeline.

### Step 1: Make a code change

I opened the following file in GitHub:

```text
07 - Dockerized Django To-Do Application Deployment on AWS EC2/index.html
```

I updated the page heading from:

```text
Todo List - Yuvraj
```

to:

```text
Todo List - Yuvraj | CI/CD Pipeline Test
```

I committed the change directly to the `main` branch.

### Step 2: Trigger Jenkins

I opened the Jenkins dashboard and selected:

```text
django-todo-cicd
```

I clicked **Build Now**.

Jenkins started the pipeline and executed all four stages.

### Step 3: Verify Jenkins execution

The pipeline completed successfully.

The stages were:

1. Checkout
2. Build Docker Image
3. Push to Docker Hub
4. Update Kubernetes Manifest

The new Docker image was created using the Jenkins build number.

The successful test produced:

```text
yuvi2102/django-todo:3
```

### Step 4: Verify Docker Hub

Jenkins pushed the new image to my Docker Hub repository.

Repository:

https://hub.docker.com/r/yuvi2102/django-todo

The image with tag `3` was available in Docker Hub.

### Step 5: Verify the GitHub manifest update

After pushing the Docker image, Jenkins updated the Kubernetes deployment manifest.

The image reference changed to:

```yaml
image: yuvi2102/django-todo:3
```

Jenkins committed and pushed the updated manifest to the GitHub repository.

### Step 6: Verify Argo CD synchronization

Argo CD detected the updated GitHub commit.

Because automatic synchronization was enabled, Argo CD applied the updated manifest to Kubernetes.

The application returned to:

```text
Health Status: Healthy
Sync Status: Synced
```

### Step 7: Verify the deployed image

Finally, I checked which Docker image was running in the Kubernetes Deployment.

```bash
kubectl get deployment django-todo -o jsonpath='{.spec.template.spec.containers[0].image}'
```

Final output:

```text
yuvi2102/django-todo:3
```

This confirmed that Kubernetes was running the new image created by Jenkins Build #3.

The end-to-end CI/CD test was successful.

## 16. Final Project Result

I successfully implemented an end-to-end CI/CD pipeline for my Dockerized Django To-Do application.

The completed workflow was:

```text
Code Change
    |
    v
GitHub
    |
    v
Jenkins Pipeline
    |
    v
Docker Image Build
    |
    v
Docker Hub
    |
    v
Update Kubernetes Manifest
    |
    v
GitHub
    |
    v
Argo CD
    |
    v
Kubernetes
    |
    v
Updated Django Application
```

### Final verification checklist

- [x] Dockerized Django application created in Part 1.
- [x] Docker image pushed to Docker Hub.
- [x] Jenkins pipeline configured.
- [x] Docker Hub credentials configured in Jenkins.
- [x] GitHub credentials configured in Jenkins.
- [x] Jenkins pipeline completed successfully.
- [x] Kubernetes cluster created using Minikube.
- [x] Django application deployed with two replicas.
- [x] Argo CD installed successfully.
- [x] Argo CD connected to the existing GitHub repository.
- [x] Automatic synchronization enabled.
- [x] Django application accessed through Kubernetes.
- [x] Jenkins built and pushed a new Docker image.
- [x] Jenkins updated the Kubernetes manifest.
- [x] Argo CD detected and synchronized the new manifest.
- [x] Verified that Kubernetes was running `yuvi2102/django-todo:3`.

## 17. What I Learned

Through this project, I gained practical experience with:

- Creating Docker images and pushing them to Docker Hub.
- Writing Jenkins declarative pipelines.
- Managing Jenkins credentials securely through the Credentials section.
- Automating Docker image builds and pushes.
- Updating Kubernetes manifests using Jenkins.
- Deploying applications on Kubernetes using Minikube.
- Understanding Kubernetes Deployments, Pods, ReplicaSets and Services.
- Installing and configuring Argo CD.
- Understanding GitOps and automatic synchronization.
- Connecting Jenkins CI with Argo CD continuous delivery.
- Testing an end-to-end CI/CD workflow on AWS EC2.

This project helped me understand how application code moves from a GitHub repository to a running application in Kubernetes through an automated pipeline.

---

# 18. Official Documentation and Learning Resources

I used the following official documentation as references while learning and implementing this project. The commands were selected and adapted to the project environment.

### 1. Jenkins

**Used for:** Creating the Jenkins pipeline, configuring credentials and executing pipeline stages.

- Jenkins Pipeline Documentation: https://www.jenkins.io/doc/book/pipeline/
- Jenkins Pipeline Syntax: https://www.jenkins.io/doc/book/pipeline/syntax/
- Jenkins Credentials Documentation: https://www.jenkins.io/doc/book/using/using-credentials/

### 2. Docker

**Used for:** Building Docker images, tagging images, logging in to Docker Hub and pushing images.

- Docker Documentation: https://docs.docker.com/
- Docker Build Documentation: https://docs.docker.com/build/
- Docker Image Documentation: https://docs.docker.com/reference/cli/docker/image/
- Docker Hub Documentation: https://docs.docker.com/docker-hub/

### 3. Kubernetes

**Used for:** Creating Deployments and Services, managing Pods and checking cluster resources.

- Kubernetes Documentation: https://kubernetes.io/docs/
- Deployments: https://kubernetes.io/docs/concepts/workloads/controllers/deployment/
- Services: https://kubernetes.io/docs/concepts/services-networking/service/
- kubectl Reference: https://kubernetes.io/docs/reference/kubectl/

### 4. Minikube

**Used for:** Creating and managing the Kubernetes cluster using the Docker driver.

- Minikube Documentation: https://minikube.sigs.k8s.io/docs/
- Starting a Cluster: https://minikube.sigs.k8s.io/docs/start/

### 5. Argo CD

**Used for:** Installing Argo CD, connecting GitHub repositories and configuring automatic synchronization.

- Argo CD Documentation: https://argo-cd.readthedocs.io/en/stable/
- Installation: https://argo-cd.readthedocs.io/en/stable/getting_started/
- Automated Sync: https://argo-cd.readthedocs.io/en/stable/user-guide/auto_sync/

### 6. AWS

**Used for:** Managing EC2 instances and configuring Security Group inbound rules.

- Amazon EC2 Documentation: https://docs.aws.amazon.com/ec2/
- Security Groups: https://docs.aws.amazon.com/vpc/latest/userguide/vpc-security-groups.html

### 7. socat

**Used for:** Forwarding network traffic from the EC2 host to the Minikube NodePort.

- socat Project Documentation: http://www.dest-unreach.org/socat/

---

## Conclusion

This project helped me understand how CI/CD and GitOps work together in a real deployment workflow.

Jenkins handled the Continuous Integration part by building Docker images, pushing them to Docker Hub and updating the Kubernetes manifests.

Argo CD handled the Continuous Delivery part by monitoring GitHub and synchronizing the changes with Kubernetes.

Finally, I successfully tested the complete workflow by changing the Django application heading, triggering Jenkins Build #3 and verifying that Kubernetes was running the updated Docker image.

**Final Docker Image:**

```text
yuvi2102/django-todo:3
```

**Final Deployment Status:**

```text
Argo CD: Healthy and Synced
Kubernetes: 2/2 Replicas Running
CI/CD Pipeline: Successful
```
