# 🚀 GitLab CI/CD Pipeline 

Basic example of a CI/CD pipeline with 3 stages, running via a custom GitLab Runner.


## 🏗️ Overview

This project demonstrates:
- A basic GitLab CI/CD pipeline with build, test, and deploy stages.
- A self-hosted GitLab Runner deployed on the cheapest AWS instance possible 
  * (⚠️ If *stop* a basic EC2 instance without an Elastic IP attached, AWS will assign a new public IP).
  *  (⚠️ If *reboot*, docker will survive but must re-run pipeline).

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
*Pipeline on shared gitlab server would fail because it's Runner:#12270859 (xS6Vzpvo) 5-green.saas-linux-small-amd64.runners-manager.gitlab.com/default* 

*ERROR: Job failed: exit code 1* 


Settings -> CICD -> Runners 
 - Toggle off the **Enable instance runners for this project**
 - Create Project Runner

 :tick for Run untagegd jobs

 ### Create Runner
 * Operating systems ➡️  Linux 
 * Spin  bob-gitlab-runner, which :

  🏠 Lives on your EC2 box.

  🔁 Resurrects himself after every reboot like a clingy necromancer.

  🐳 Can whisper to the host’s Docker daemon and spin up containers for your GitLab CI/CD jobs.

  📦 Stores his secrets (runner config) in /srv/gitlab-runner/config.
  
  🥐 gitlab/gitlab-runner:alpine ➡️ Light of carb image to use


 ```bash
 docker run -d \
  --name bob-gitlab-runner \
  --restart always \
  -v /srv/gitlab-runner/config:/etc/gitlab-runner \
  -v /var/run/docker.sock:/var/run/docker.sock \
  gitlab/gitlab-runner:alpine
```

### Register Runner - disposable container to register (one-time thing)

```bash
docker run --rm -it \
    -v /srv/gitlab-runner/config:/etc/gitlab-runner \
    gitlab/gitlab-runner:alpine register
  ```

#### Answer prompts for:

* GitLab URL (where your projects live) ➡️ https://gitlab.com

* Registration token (from GitLab UI ) ➡️ copy from 

* Enter a name for the runner (call him Bob, duh)
* Enter an executor: docker ( Bob spins up Docker containers to run jobs)
* Enter the default Docker image (for example, ruby:2.7): docker:dind



### Change config.toml 
```bash
cd /srv/gitlab-runner/config/
sudo vim config.toml
```
Change 
```bash 
volumes = ["/cache"]
```
to
```bash 
volumes = ["/var/run/docker.sock:/var/run/docker.sock", "/cache"]
```

✅ Verify:

Port 80 is on  LISTEN      33886/docker-proxy 
```bash
sudo netstat -tulnp
```

```bash
docker ps 
```
jt-backend-image:latest       "python main.py"   is running on **0.0.0.0:80->8000/tcp, :::80->8000/tcp   jt-backend-container**

