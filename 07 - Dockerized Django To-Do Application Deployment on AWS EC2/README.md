# Dockerized Django To-Do Application Deployment on AWS EC2

## 1. Project Overview

In this project, I deployed a Django To-Do application on an AWS EC2 instance using Docker.

I cloned the application from my GitHub repository, prepared the Dockerfile, built a Docker image and ran the application inside a Docker container.

I also customized the application title to display my name and configured the AWS Security Group to access the website through a browser.

The main objective was to understand how to package and deploy a Python application using Docker on AWS EC2.

## 2. Tools and Technologies

- AWS EC2
- Ubuntu Server 24.04
- Git and GitHub
- Docker
- Python 3.10
- Django 3.2
- SQLite
- HTML and CSS

## 3. Project Architecture

The application follows this deployment flow:

```text
GitHub Repository
       |
       | git clone
       v
AWS EC2 Instance
       |
       v
Django Application
       |
       v
Dockerfile
       |
       | docker build
       v
Docker Image
django-todo:latest
       |
       | docker run
       v
Docker Container
django-todo-app
       |
       v
Port Mapping
8000:8000
       |
       v
AWS Security Group
       |
       v
Web Browser
       |
       v
Django To-Do Application
```

## 4. Understanding the Important Concepts

### What is Docker?

Docker is a platform used to package applications and their dependencies into containers.

It helps applications run consistently across different environments.

### What is a Docker Image?

A Docker image is a packaged template containing the application and everything required to run it.

In this project, I created an image named:

```text
django-todo:latest
```

### What is a Docker Container?

A container is a running instance of a Docker image.

I used the image to create a container named:

```text
django-todo-app
```

### What is a Dockerfile?

A Dockerfile contains instructions used to build a Docker image.

It defines the base image, dependencies, application files, ports and startup command.

### What is Port Mapping?

Port mapping connects a port on the EC2 host to a port inside the Docker container.

For this project:

```text
-p 8000:8000
```

This means:

```text
EC2 Host Port 8000
        |
        v
Container Port 8000
        |
        v
Django Application Port 8000
```

### What is an AWS Security Group?

A Security Group acts as a virtual firewall for an EC2 instance.

It controls incoming and outgoing network traffic.

I configured an inbound rule to allow access to the Django application through TCP port 8000.

---

# 5. Project Repository

GitHub Repository:

https://github.com/Yuvii2102/My-CI-CD-Journey

Project Directory:

```text
07 - Dockerized Django To-Do Application Deployment on AWS EC2
```

The project folder contains:

```text
07 - Dockerized Django To-Do Application Deployment on AWS EC2/
│
├── Dockerfile
├── Jenkinsfile
├── README.md
├── db.sqlite3
├── deploy/
├── docker-compose.yml
├── manage.py
├── staticfiles/
├── todoApp/
└── todos/
```

Important files:

| File | Purpose |
|---|---|
| `Dockerfile` | Contains instructions to build the Docker image. |
| `manage.py` | Django project management utility. |
| `db.sqlite3` | SQLite database file. |
| `todoApp/` | Main Django project configuration. |
| `todos/` | Django application containing Todo functionality. |
| `staticfiles/` | Static application files. |

The repository also contains a Jenkinsfile and Docker Compose configuration. They are included as project files but are not required for this particular deployment.

---

# 6. Practical Implementation

## Step 1: Launch an AWS EC2 Instance

I created an EC2 instance using the following configuration:

| Configuration | Value |
|---|---|
| Instance Name | Django-Todo-Application |
| AMI | Ubuntu Server 24.04 LTS |
| Instance Type | Suitable instance for the application |
| Storage | 20 GB or more |
| SSH Port | 22 |
| Application Port | 8000 |

I configured the Security Group to allow:

- SSH (22) from My IP.
- Custom TCP (8000) from My IP.

After launching the instance, I connected using **EC2 Instance Connect** through the AWS Console.

No separate SSH client such as MobaXterm is required.

## Step 2: Update Ubuntu

First, I updated the package list and installed the required tools.

```bash
sudo apt update
sudo apt upgrade -y
```

Installed Git and other basic utilities:

```bash
sudo apt install -y git curl wget
```

## Step 3: Install Docker

I installed Docker using the Ubuntu package repository.

```bash
sudo apt install -y docker.io
```

Started and enabled Docker:

```bash
sudo systemctl enable --now docker
```

Verified Docker:

```bash
sudo docker --version
```

Tested Docker:

```bash
sudo docker run hello-world
```

The `Hello from Docker!` message confirmed that Docker was working.

**Note:** In this project, I use `sudo docker` so I do not need to configure additional Docker group permissions.

## Step 4: Clone My GitHub Repository

I cloned my GitHub repository onto the EC2 instance.

```bash
git clone https://github.com/Yuvii2102/My-CI-CD-Journey.git
```

Entered the repository:

```bash
cd My-CI-CD-Journey
```

Entered the project directory:

```bash
cd "07 - Dockerized Django To-Do Application Deployment on AWS EC2"
```

The quotation marks are important because the folder name contains spaces.

## Step 5: Check the Project Files

I checked the project files using:

```bash
ls
```

I verified that the following important files and directories were available:

```text
Dockerfile
manage.py
db.sqlite3
todoApp/
todos/
staticfiles/
```

These files are required to build and run the Django application.

## Step 6: Understand the Dockerfile

The Dockerfile contains the instructions required to build the Django application image.

### Dockerfile

```dockerfile
FROM python:3.10

RUN pip install django==3.2

COPY . .

RUN python manage.py migrate

EXPOSE 8000

CMD ["python","manage.py","runserver","0.0.0.0:8000"]
```

### Explanation of Each Instruction

**1. FROM**

```dockerfile
FROM python:3.10
```

Defines Python 3.10 as the base image.

I used Python 3.10 to provide a compatible environment for the Django 3.2 application.

**2. RUN**

```dockerfile
RUN pip install django==3.2
```

Installs Django version 3.2 inside the Docker image.

**3. COPY**

```dockerfile
COPY . .
```

Copies the files from the current project directory into the Docker image.

The first dot represents the source directory, and the second dot represents the destination inside the image.

**4. RUN**

```dockerfile
RUN python manage.py migrate
```

Runs Django database migrations during the image build.

Migrations create or update the database structure required by the application.

**5. EXPOSE**

```dockerfile
EXPOSE 8000
```

Documents that the application uses port 8000 inside the container.

It does not publish the port automatically.

**6. CMD**

```dockerfile
CMD ["python","manage.py","runserver","0.0.0.0:8000"]
```

Defines the command that starts the Django application when the container runs.

The application listens on `0.0.0.0` so it can receive connections through the container's network interface.

### Complete Dockerfile Flow

```text
Python 3.10 Base Image
        |
        v
Install Django 3.2
        |
        v
Copy Application Files
        |
        v
Run Database Migrations
        |
        v
Expose Port 8000
        |
        v
Start Django Application
```

## Step 7: Build the Docker Image

After preparing the Dockerfile, I built the Docker image.

```bash
sudo docker build -t django-todo .
```

Explanation:

- `docker build` builds a Docker image.
- `-t django-todo` assigns a name to the image.
- `.` uses the Dockerfile and application files in the current directory.

After the build completed, Docker created:

```text
django-todo:latest
```

## Step 8: Verify the Docker Image

I checked the available Docker images:

```bash
sudo docker images
```

I verified that the image was available:

```text
REPOSITORY    TAG       IMAGE
django-todo   latest    <IMAGE ID>
```

This confirmed that the Docker image was created successfully.

## Step 9: Run the Docker Container

I started the Django application inside a Docker container.

```bash
sudo docker run -d -p 8000:8000 --name django-todo-app django-todo
```

### Explanation

| Command | Purpose |
|---|---|
| `docker run` | Creates and starts a container. |
| `-d` | Runs the container in the background. |
| `-p 8000:8000` | Maps EC2 port 8000 to container port 8000. |
| `--name django-todo-app` | Assigns a name to the container. |
| `django-todo` | Specifies the Docker image. |

The container now runs in the background.

## Step 10: Verify the Running Container

I checked the running containers:

```bash
sudo docker ps
```

The output showed:

```text
CONTAINER ID   IMAGE         STATUS       PORTS
<CONTAINER ID> django-todo   Up           0.0.0.0:8000->8000/tcp
```

The container was running and port 8000 was mapped successfully.

## Step 11: Customize the Django Application

I customized the application heading to display my name.

The original heading was:

```html
Todo List - Abhishek
```

I changed it to:

```html
Todo List - Yuvraj
```

The file I edited was:

```text
todos/templates/todos/index.html
```

I opened the file using Vim:

```bash
vim todos/templates/todos/index.html
```

I pressed `i` to enter Insert mode, updated the heading, and saved the file using:

```text
ESC
:wq
ENTER
```

After modifying the application source code, I rebuilt the Docker image.

```bash
sudo docker build -t django-todo .
```

Stopped the old container:

```bash
sudo docker stop django-todo-app
```

Removed the old container:

```bash
sudo docker rm django-todo-app
```

Started a new container using the updated image:

```bash
sudo docker run -d -p 8000:8000 --name django-todo-app django-todo
```

Verified the new container:

```bash
sudo docker ps
```

The updated application was now running with my customized heading.

## Step 12: Test the Application From EC2

I tested the Django application from the EC2 instance using:

```bash
curl http://localhost:8000
```

The application redirects the root URL `/` to `/todos/`.

To follow the redirect and retrieve the actual page HTML, I used:

```bash
curl -L http://localhost:8000
```

The `-L` option tells curl to follow HTTP redirects.

The output displayed the Django Todo page HTML.

## Step 13: Understand HTTP 302 Redirect

When I accessed the root URL:

```text
http://localhost:8000
```

Django returned an HTTP 302 redirect.

HTTP 302 means that the requested URL temporarily redirects to another URL.

In this application:

```text
/
 |
 v
/todos/
```

Therefore, the final application page is available at:

```text
http://EC2-PUBLIC-IP:8000/todos/
```

This is normal behavior of the Django application.

## Step 14: Check Docker Container Logs

I checked the application logs using:

```bash
sudo docker logs django-todo-app
```

Docker logs help me view application output and incoming HTTP requests.

They are useful for checking whether the Django application is running and receiving requests.

## Step 15: Configure the AWS Security Group

Docker port mapping alone does not make the application accessible from outside the EC2 instance.

I also configured the AWS Security Group to allow incoming traffic on port 8000.

Steps:

1. Open AWS Console.
2. Go to EC2.
3. Select the running instance.
4. Open the Security tab.
5. Select the attached Security Group.
6. Open Inbound Rules.
7. Add a new inbound rule.

Configuration:

| Setting | Value |
|---|---|
| Type | Custom TCP |
| Port Range | 8000 |
| Source | My IP |

I saved the inbound rule.

This allows my current public IP address to access the Django application.

## Step 16: Access the Application From a Browser

I copied the Public IPv4 address of my EC2 instance.

I opened the following URL:

```text
http://EC2-PUBLIC-IP:8000/todos/
```

The Django To-Do application appeared in the browser.

The application displayed my customized heading:

```text
Todo List - Yuvraj
```

The deployment was successful.

---

# 7. Complete Command Reference

These are the commands I used to execute the project from a fresh Ubuntu EC2 instance.

### Update Ubuntu and Install Tools

```bash
sudo apt update
sudo apt upgrade -y
sudo apt install -y git curl wget
```

### Install Docker

```bash
sudo apt install -y docker.io
sudo systemctl enable --now docker
sudo docker --version
sudo docker run hello-world
```

### Clone GitHub Repository

```bash
git clone https://github.com/Yuvii2102/My-CI-CD-Journey.git
```

### Enter Project Directory

```bash
cd My-CI-CD-Journey
cd "07 - Dockerized Django To-Do Application Deployment on AWS EC2"
```

### Build Docker Image

```bash
sudo docker build -t django-todo .
```

### View Docker Images

```bash
sudo docker images
```

### Run Docker Container

```bash
sudo docker run -d -p 8000:8000 --name django-todo-app django-todo
```

### Check Running Containers

```bash
sudo docker ps
```

### Test Application

```bash
curl -L http://localhost:8000
```

### View Container Logs

```bash
sudo docker logs django-todo-app
```

### Rebuild After Application Changes

```bash
sudo docker build -t django-todo .
```

### Stop and Remove the Existing Container

```bash
sudo docker stop django-todo-app
sudo docker rm django-todo-app
```

### Run the Updated Container

```bash
sudo docker run -d -p 8000:8000 --name django-todo-app django-todo
```

---

# 8. Important Docker Concepts Learned

## Docker Image vs Docker Container

| Docker Image | Docker Container |
|---|---|
| A packaged template | A running instance of an image |
| Created using `docker build` | Created using `docker run` |
| Example: `django-todo` | Example: `django-todo-app` |

## EXPOSE vs Port Mapping

**EXPOSE**

```dockerfile
EXPOSE 8000
```

Documents the port used by the application inside the container.

**Port Mapping**

```bash
-p 8000:8000
```

Maps the EC2 host port to the container port.

## 0.0.0.0 vs 127.0.0.1

`0.0.0.0` allows the application to listen on all available network interfaces inside the container.

`127.0.0.1` refers to the local loopback interface.

For this project, I used:

```text
0.0.0.0:8000
```

so Docker can forward incoming traffic to Django.

## Docker Logs

```bash
sudo docker logs django-todo-app
```

Displays the output generated by the container.

## Docker PS

```bash
sudo docker ps
```

Displays currently running containers.

## AWS Security Group

Controls which network traffic can reach the EC2 instance.

For this project, I allowed TCP port 8000 from my IP address.

---

# 9. Final Result

The Django To-Do application was successfully deployed on AWS EC2 using Docker.

The final deployment included:

- Cloned the application from GitHub.
- Installed Docker on Ubuntu.
- Created a Dockerfile using Python 3.10 and Django 3.2.
- Built the Docker image.
- Created and ran a Docker container.
- Customized the application heading to display my name.
- Configured Docker port mapping.
- Configured the AWS Security Group.
- Accessed the application through a web browser.

### Final Application URL

```text
http://EC2-PUBLIC-IP:8000/todos/
```

### Final Deployment Flow

```text
GitHub
   |
   v
AWS EC2
   |
   v
Dockerfile
   |
   v
Docker Image
   |
   v
Docker Container
   |
   v
Django Application
   |
   v
AWS Security Group
   |
   v
Web Browser
   |
   v
Todo List - Yuvraj
```

## 10. Key Learnings

Through this practical, I learned:

- How to deploy a Django application using Docker.
- How to write and understand a Dockerfile.
- How to build Docker images.
- How to create and manage Docker containers.
- How to map container ports to EC2 ports.
- How to customize an existing Django application.
- How to use Docker logs to check application activity.
- How to configure AWS Security Groups.
- How to access a containerized application through a public IP address.

This project helped me understand the complete process of packaging and deploying a web application using Docker on AWS EC2.
