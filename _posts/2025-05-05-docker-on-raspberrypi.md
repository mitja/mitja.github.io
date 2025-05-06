---
layout: post
title: "How to Install Docker and Docker Compose on Raspberry Pi OS (rootful and rootless)"
date: 2025-05-05
author: mitja
category: "Homelab"
tags: [Raspberry Pi, Docker, Docker Compose, Tutorial]
image:
  path: /assets/blog/2025/docker-rpi.jpg
  alt: "The Docker logo and a Raspberry Pi 5 Compute module side by side."
---

This is a quick guide on how to install Docker and Docker Compose on Raspberry PI. I use this on various Raspberry Pis 4 with 4 and 8 GB RAM, it's tested with Raspberry Pi OS 64-bit 12 ("bookworm") and Docker `28.1.1`. 

The tutorial first shows how to install Docker to run as root ("rootful") and concludes with switching rootless mode on and off.

## Rootful Installation of Docker and Docker Compose

### Step 1 - Install Docker

```bash
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
```

### Step 2 (optional) - Add Your User to the Docker Group

This step is optional and makes Docker a bit more convenient to use (less `sudo`), but it's also less secure. Access to a Docker demon running with root privileges equals root access. In effect you give users root access without an extra authentication step. 

```bash
sudo usermod -aG docker $USER
newgrp docker
```

### Step 3 - Smoke tests

Docker and the Docker Compose plugin now should just work.

```bash
docker --version
docker run hello-world
cat <<EOF > docker-compose.yml
version: '3'
services:
  hello-world:
    image: hello-world
EOF
docker compose up
docker compose down
```

Clean up:

```bash
docker rm $(docker ps -a -q --filter "ancestor=hello-world")
docker rmi hello-world
```

## Rootless Docker Mode

You can also run Docker in "rootless" mode. In this case, each user gets their own Docker daemon. Rootless is more secure as users cannot start Docker containers with root privileges. The downside of rootless is that it's more limited. For example, you cannot use the `host` networking mode and can't easily bind to ports below 1024. Because of these limitations, some tools and apps don't work out of the box. For example, KinD (Kubernetes in Docker) requires more work. Many installation instructions still assume Docker is running as root and you need to adapt them to rootless, yourself. Rootless Docker is also slightly slower and consumes slightly more resources than running Docker as root.

### Enable Rootless Mode

#### Step 1 - Install uidmap and run rootless setup

```bash
sudo apt-get install -y uidmap
dockerd-rootless-setuptool.sh install
```

#### Step 2 - Enable lingering to run background services

```bash
sudo loginctl enable-linger $USER
```

#### Step 3 - Add environment variables to your `.bashrc`

```bash
echo 'PATH=/usr/bin:$PATH' >> ~/.bashrc
echo 'export DOCKER_HOST=unix:///run/user/1000/docker.sock' >> ~/.bashrc
source ~/.bashrc
```

#### Step 4 - Test if Docker runs rootless

The Docker Root Dir should be in your home directory:

```bash
docker info | grep "Docker Root Dir: /home"
```

### Disable Rootless Mode

This may be bit redundant, but I struggled to get rid of an error where the Docker client still tried to connect to the rootless Docker demon for my user. As this did not exist anymore, it didn't work. I tried quite a few things. in the end, below steps worked.

#### Step 1 - Stop Docker, remove the services, and kill any running processes

```bash
systemctl --user stop docker
systemctl --user disable docker.socket docker.service
pkill -u $(id -u) dockerd || true
```

#### Step 2 - Unset environment variables

```bash
unset DOCKER_HOST
export PATH=/usr/bin:$PATH
```

#### Step 3 - Remove local docker configs

```bash
rm -rf ~/.config/docker ~/.local/share/docker ~/.docker
```

Also, remove `DOCKER_HOST` from `~/.bashrc`.

#### Step 4 - Disable lingering (change `mitja` to your username)

```bash
sudo loginctl disable-linger mitja
```

#### Step 5 - Start Docker (now "rootful")

```bash
sudo systemctl start docker
```

#### Step 6 - Test if Docker runs "rootful" 

The Docker Root Dir should be in /var/lib/docker:

```bash
sudo docker info | grep "Docker Root Dir: /var"
```

#### Step 7 - Test if you can connect to the rootful Docker demon from your user

```bash
docker context ls
docker info
```
