---
title: "Installing Docker on Raspberry PI"
summary: "How to Install Docker and Docker Compose on Raspberry Pi OS (rootful and rootless)."
date: 2025-05-05
author: mitja
categories: ["Clud Solution Design", "Blog"]
showTableOfContents: true
tags: ["Raspberry Pi", "Docker", "Docker Compose", "Tutorial"]
---

This is a quick guide on how to install Docker and Docker Compose on Raspberry PI. I use this on various Raspberry Pis 4 with 4 and 8 GB RAM. At the time of writing, it's tested with Raspberry Pi OS 64-bit 12 ("bookworm") and Docker `28.1.1`. 

The tutorial shows 

- how to install Docker to run as root ("rootful"), 
- how to enable Docker rootless mode, and
- how to switch rootless mode off, again.

## Rootful Installation of Docker and Docker Compose

### Install Docker

```bash
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
```

### Add Your User to the Docker Group

This step is optional and makes Docker a bit more convenient to use (less `sudo`), but it's also less secure. Access to a Docker demon running with root privileges equals root access. In effect you give users root access without an extra authentication step. 

```bash
sudo usermod -aG docker $USER
newgrp docker
```

### Smoke tests

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

Clean up after testing:

```bash
docker rm $(docker ps -a -q --filter "ancestor=hello-world")
docker rmi hello-world
```

## Rootless Docker Mode

You can also run Docker in "rootless" mode. In this case, each user gets their own Docker daemon. 

Rootless is more secure as users cannot start Docker containers with root privileges. 

The downside of rootless is that it's more limited. For example, you cannot use the `host` networking mode and can't easily bind to ports below 1024. Because of these limitations, some tools and apps don't work out of the box. For example, KinD (Kubernetes in Docker) requires more work. 

Many installation instructions still assume Docker is running as root and you need to adapt them to rootless. 

Rootless Docker is also slightly slower and consumes slightly more resources than running Docker as root.

### Enable Rootless Mode

#### Install uidmap and run rootless setup

```bash
sudo apt-get install -y uidmap
dockerd-rootless-setuptool.sh install
```

#### Enable lingering to run background services

```bash
sudo loginctl enable-linger $USER
```

#### Add environment variables to your `.bashrc`

```bash
echo 'PATH=/usr/bin:$PATH' >> ~/.bashrc
echo 'export DOCKER_HOST=unix:///run/user/1000/docker.sock' >> ~/.bashrc
source ~/.bashrc
```

#### Test if Docker runs rootless

The Docker Root Dir should be in your home directory:

```bash
docker info | grep "Docker Root Dir: /home"
```

### Disable Rootless Mode

The way I describe it might be bit redundant, but I struggled to get rid of an error where the Docker client still tried to connect to the rootless Docker demon for my user. As this did not exist anymore, it didn't work. I tried quite a few things. In the end, below steps worked.

#### Stop Docker, remove the services, and kill any running processes

```bash
systemctl --user stop docker
systemctl --user disable docker.socket docker.service
pkill -u $(id -u) dockerd || true
```

#### Unset environment variables

```bash
unset DOCKER_HOST
export PATH=/usr/bin:$PATH
```

#### Remove local docker configs

```bash
rm -rf ~/.config/docker ~/.local/share/docker ~/.docker
```

Also, remove `DOCKER_HOST` from `~/.bashrc`.

#### Disable lingering (change `mitja` to your username)

```bash
sudo loginctl disable-linger mitja
```

#### Start Docker (now "rootful")

```bash
sudo systemctl start docker
```

#### Test if Docker runs "rootful" 

The Docker Root Dir should be in /var/lib/docker:

```bash
sudo docker info | grep "Docker Root Dir: /var"
```

#### Test if you can connect to the rootful Docker demon from your user

```bash
docker context ls
docker info
```
