# 🚀 GitLab CI/CD Pipeline 

Basic example of a CI/CD pipeline with 3 stages, running via a custom GitLab Runner.


## 🏗️ Overview

This project demonstrates:
- A basic GitLab CI/CD pipeline with build, test, and deploy stages.
- A self-hosted GitLab Runner deployed on the cheapest AWS instance possible (you're welcome).

## 


## ☁️ Setting Up a Custom GitLab Runner: server to run jobs
*GitLab’s shared runners (hosted by GitLab.com, free/default ones) don’t come with Docker-in-Docker (DinD) or privileged access by default.*

### 💸 Step 1: Launch the AWS EC2 Instance

- Use an **Amazon Linux 2** or **Ubuntu (20.04 or higher)** instance.
- Recommended type: `t3.micro` (free tier eligible).

### 🔐 Step 2: SSH into Your Instance

```bash
ssh -i my-serveraccesskey.pem ec2-user@ec2-public-ip
```

### 🐧 Step 3: Install Git & Docker (Amazon Linux / Ubuntu)

**🧰 Installing Git**

For  `ec2-user` package manager is `yum`:

```bash
sudo yum install git -y
```
or Ubuntu
```bash
sudo apt-get install git -y
```
✅ Verify:
```bash
which git          # Should return: /usr/bin/git
git --version      # Displays installed Git version
rpm -ql git        # (Amazon Linux) Lists all installed Git files
```

**🐳 Install Docker**
```bash
sudo yum install -y docker
```
Add **```bash ec2-user```** to group ⚠️ Without this step, you'll need to prefix all Docker commands with **sudo***.

```bash
sudo usermod -a -G docker ec2-user
```
Reload group membership without logout:
```bash
newgrp docker
```

**🐳 Install Docker Compose**

Docker Compose isn't included by default, so pull the latest stable binary:

```bash
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" \
  -o /usr/local/bin/docker-compose
  ```
Make it executable:
```bash
sudo chmod +x /usr/local/bin/docker-compose
```

✅ Verify:
```bash
id ec2-user  
docker-compose --version
```

## Launch Gitlab Runner

