---
layout: post
title: "How to Install Docker and Docker Compose on Raspberry Pi OS (rootful and rootless)"
date: 2025-05-03
author: mitja
category: "Homelab"
tags: [Raspberry Pi, Docker, Docker Compose, Tutorial]
---

This is a quick guide on how to install Docker and Docker Compose on Raspberry PI. I use this on various Raspberry Pis 4 with 4 and 8 GB RAM, it's tested with Raspberry Pi OS 64-bit 12 ("bookworm") and Docker `28.1.1`. 

At first, I thought, rootless would be better for my use case, but I later decided to run docker "rootful". This is why this tutorial also shows how to enable and disable Docker rootless mode.

## Rootful Installation of Docker and Docker Compose

### Step 1 - Install Docker

```bash
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
```

### Step 2 (optionl) - Add Your User to the Docker Group

This is optional, easier to use as it avoids typing `sudo` every time, less secure as access to the Docker demon equals root access. In effect you give the user root access without an extra authentication step. 

```bash
sudo usermod -aG docker $USER
newgrp docker
```

## Step 3 - Smoke tests

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

You can also run Docker "rootless", without root privileges. Each user account gets their own Docker daemon. Rootless is more secure as no docker container is running with root privileges. The downsides are that this is more limited and less documented. For example, you cannot use the `host` networking mode, can't easily bind to ports below 1024, and some tools and apps don't work out of the box. For example, KinD (Kubernetes in Docker) requires more work. It's probably also slightly slower than running as root.

Even though rootless is often recommended for development and testing and for the improved security posture, I decided against rootless to make my life easier. After all, my Raspberry Pi's are also not (yet?) security critical.

### Enable Rootless Mode

1. Install uidmap and run rootless setup:

```bash
sudo apt-get install -y uidmap
dockerd-rootless-setuptool.sh install
```

2. Enable lingering to run background services:

```bash
sudo loginctl enable-linger $USER
```

3. Add environment variables to your `.bashrc`

```bash
echo 'PATH=/usr/bin:$PATH' >> ~/.bashrc
echo 'export DOCKER_HOST=unix:///run/user/1000/docker.sock' >> ~/.bashrc
source ~/.bashrc
```

4. Test if Docker runs rootless.

The Docker Root Dir should be in your home directory:

```bash
docker info | grep "Docker Root Dir: /home"
```

---

### Disable Rootless Mode

This may look a bit over-the-top, but I struggled to get rid of an error where the Docker client still tried to connect to the rootless Docker demon for my user. As this did not exist anymore, it didn't work. I tried quite a few things,. in the end, below steps worked. Maybe some are redundant, but at least, these steps should work.

1. Stop Docker, remove the services, and kill any running processes

```bash
systemctl --user stop docker
systemctl --user disable docker.socket docker.service
pkill -u $(id -u) dockerd || true
```

2. Unset environment variables

```bash
unset DOCKER_HOST
export PATH=/usr/bin:$PATH
```

3. Remove local docker configs:

```bash
rm -rf ~/.config/docker ~/.local/share/docker ~/.docker
```

Also, remove `DOCKER_HOST` from `~/.bashrc`.

4. Disable lingering (change `mitja` to your username)

```bash
sudo loginctl disable-linger mitja
```

5. Start Docker (now "rootful"):

```bash
sudo systemctl start docker
```

6. Test if Docker runs "rootful" (Docker Root Dir should be in /var/lib/docker)

```bash
sudo docker info | grep "Docker Root Dir: /var"
```

7. Test if you can connect to the rootful Docker demon from your user:

```bash
docker context ls
docker info
```
