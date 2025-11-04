---
author: mitja
categories:
- Cloud-Lösungsdesign
- Blog
date: 2025-05-05
draft: false
showTableOfContents: true
slug: docker-auf-dem-raspberry-pi
tags:
- Raspberry Pi
- Docker
- Docker Compose
- Anleitung
title: Docker auf dem Raspberry Pi installieren
---

Hier ist eine Anleitung zur Installation von Docker und Docker Compose auf dem Raspberry Pi rootless und "rootful".

<!-- more -->

Die Anleitung zeigt, wie Du

- Docker für den Betrieb mit dem root User ("rootful") installierst, 
- den Docker rootless Modus aktivierst, und
- den rootless Modus wieder ausschaltest.

Ich verwende Docker auf verschiedenen Raspberry Pi 4 mit 4 und 8 GB RAM und habe diese Schritte zuletzt mit einem Raspberry Pi OS 64-bit 12 ("bookworm") und Docker `28.1.1` getestet.

## Rootful-Installation von Docker und Docker Compose

### Docker installieren

```bash
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
```

### Benutzer zur Docker-Gruppe hinzufügen

Dieser Schritt ist optional und macht die Nutzung von Docker etwas bequemer (weniger `sudo`), ist aber auch weniger sicher. Der Zugriff auf einen Docker-Daemon, der mit Root-Rechten läuft, entspricht Root-Zugriff. Damit gibst Du Benutzerinnen und Benutzern Root-Zugriff ohne einen zusätzlichen Authentifizierungsschritt. 

```bash
sudo usermod -aG docker $USER
newgrp docker
```

### Smoke-Tests

Docker und das Docker Compose Plugin sollten jetzt funktionieren:

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

Aufräumen nach dem Test:

```bash
docker rm $(docker ps -a -q --filter "ancestor=hello-world")
docker rmi hello-world
```

## Rootless Docker Modus

Du kannst Docker auch im "rootless"-Modus betreiben. In diesem Fall hat jede Linux Nutzerin/jeder Nutzer einen eigenen Docker-Daemon. 

Rootless ist sicherer, da Anwender keine Docker-Container mit Root-Rechten starten können.

Der Nachteil von rootless ist, dass es eingeschränkter ist. Beispielsweise kann man den `host`-Netzwerkmodus nicht verwenden und Ports unterhalb von 1024 nicht ohne zusätzliche Schritte binden. Aufgrund dieser Einschränkungen funktionieren manche Tools und Apps nicht "out-of-the-box". Zum Beispiel erfordert KinD (Kubernetes in Docker) zusätzlichen Aufwand.

Rootless Docker ist außerdem etwas langsamer und verbraucht etwas mehr Ressourcen als ein unter Docker im Root Modus.

### Rootless-Modus aktivieren

#### uidmap installieren und rootless-Setup ausführen

Mit `uidmap` können Programme wie Docker User Namespace Mappings erzeugen können. Dabei werden vor User IDs (UIDs) und Group IDs (GIDs) vom Basissystem zu anderen IDs innerhalb eines User Namespace gemappt. 

`dockerd-rootless-setuptool.sh` richtet das Mapping ein. Nach der Docker Installation liegt `dockerd-rootless-setuptool.sh` in `/usr/bin`. Beachte, dass `dockerd-rootless-setuptool.sh` als non-root User ausgeführt werden muss.

```bash
sudo apt-get install -y uidmap
dockerd-rootless-setuptool.sh install
```

#### Lingering aktivieren, um Hintergrunddienste auszuführen

Lingering erlaubt es Anwendern Prozesse auch nach dem Logout laufen zu lassen. Das ist für langlaufende Dienste wie Docker nötig, damit der Prozess auch ohne aktive User Session aktiv bleibt.

```bash
sudo loginctl enable-linger $USER
```

#### Umgebungsvariablen in die `.bashrc` eintragen

Je user sollte ein eigener Socket angelegt werden, z. B. 1000 für die UID 1000.

```bash
echo 'PATH=/usr/bin:$PATH' >> ~/.bashrc
echo 'export DOCKER_HOST=unix:///run/user/1000/docker.sock' >> ~/.bashrc
source ~/.bashrc
```

#### Testen, ob Docker rootless läuft

Das Docker Root Directory sollte jetzt im Home-Verzeichnis liegen:

```bash
docker info | grep "Docker Root Dir: /home"
```

### Rootless-Modus deaktivieren

Diese Beschreibung ist vielleicht etwas umständlich, da ich zunächst nicht zurückdrehen konnte, dass der Docker-Client versucht, sich mit dem rootless Docker-Daemon meines Benutzers zu verbinden. Das lief auf einen Fehler, da dieser nicht mehr existierte. Ich habe etwas herumprobieren müssen bis es funktionierte. Am Ende konnte ich rootless mit folgenden Schritten deaktivieren.

#### Docker stoppen, die Services entfernen und laufende Prozesse beenden

```bash
systemctl --user stop docker
systemctl --user disable docker.socket docker.service
pkill -u $(id -u) dockerd || true
```

#### Umgebungsvariablen entfernen

```bash
unset DOCKER_HOST
export PATH=/usr/bin:$PATH
```

Entferne außerdem `DOCKER_HOST` aus der `~/.bashrc`.

#### Lokale Docker-Konfigurationen entfernen

```bash
rm -rf ~/.config/docker ~/.local/share/docker ~/.docker
```

#### Lingering deaktivieren

```bash
sudo loginctl disable-linger $USER

```

#### Docker starten (nun "rootful")

```bash
sudo systemctl start docker
```

#### Testen, ob Docker "rootful" läuft 

Das Docker Root Directory sollte jetzt in /var/lib/docker liegen:

```bash
sudo docker info | grep "Docker Root Dir: /var"
```

#### Testen, ob vom eigenen Benutzer aus eine Verbindung zum rootful Docker-Daemon möglich ist

```bash
docker context ls
docker info
```