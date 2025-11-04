---
author: null
categories:
- KI-Engineering
- Blog
date: 2025-10-14
draft: false
slug: claude-code-in-devcontainers
tags:
- Claude
- Devcontainer
title: Claude Code in Devcontainers
---

[Development Containers](https://containers.dev) oder kurz `devcontainers`, fügen eine zusätzliche Sicherheitsebene hinzu, vereinfachen das Onboarding von Entwicklerinnen und Entwicklern und ermöglichen paralleles Arbeiten in isolierten Umgebungen. 

Für mich sind Devcontainers eine großartige Ergänzung im Werkzeugkasten eines AI Engineers, auch wenn ich sie noch nicht täglich benutze.

Ich habe Devcontainers mit Claude Code unter Verwendung von VS Code und der devcontainers cli eingerichtet, sie für ein auf Python FastAPI basierendes Projekt angepasst und das in diesem Artikel dokumentiert.
<!--more-->

## Claude Code in Devcontainers mit VS Code

Ein guter Einstieg in Claude Code in einem Devcontainer ist Anthropics eigenes [claude-code](https://github.com/anthropics/claude-code) Repository. 

Git Clone [anthropics/claude-code](https://github.com/anthropics/claude-code) öffne den Ordner in VS Code. Wenn auf deinem Rechner Docker Desktop oder etwas Vergleichbares läuft, sollte VS Code sofort versuchen, den Workspace in einem `devcontainer` zu starten.

Falls der devcontainer nicht automatisch startet, kannst du ihn über `> Dev Containers: Reopen in Container` aus der VS-Code-Befehlspalette manuell starten.

Der erste Start dauert eine Weile. Wenn er abgeschlossen ist, kannst du in VS Code ein Terminal öffnen und `claude` ausführen.

## Claude Code in Devcontainers mit einer CLI

Das Devcontainers-Projekt stellt die [devcontainers/cli](https://github.com/devcontainers/cli) als Referenzimplementierung bereit. Damit kannst du Devcontainers ohne VS Code direkt aus dem Terminal starten. Zum Ausprobieren kannst du den gleichen Git Clone des [anthropics/claude-code](https://github.com/anthropics/claude-code) Repositories verwenden.

Installiere die devcontainers CLI auf deinem Rechner:

```sh
npm install -g @devcontainers/cli
```

Starte den Devcontainer, angenommen Du bist im claude-code Ordner, alternativ kannst Du einen beliebigen Ordner mit einem `.devcontainers` Unterordner angeben:

```sh
devcontainer up --workspace-folder .
```

Claude Code im Container ausführen:

```sh
devcontainer exec --workspace-folder . claude
```

Oder (noch besser): Starte eine Shell im Container aus deinem bevorzugten Terminal-Emulator (Ghostty funktioniert großartig) und starte dann Claude in dieser Terminal-Session. `claude-code` bringt zsh mit:

```sh
devcontainer exec --workspace-folder . zsh
```

Du kannst auch tmux verwenden, um die Verbindung zu trennen und später wieder herzustellen.

Zum Beenden: Beende Claude, beende die Shell und stoppe oder stoppe und lösche den Container. Leider gibt es dafür noch keinen Subcommand. Ich habe ungenutzte Devcontainers einfach manuell mit Docker Desktop oder der docker cli gelöscht:

```sh
docker ps # find the container id you want to delete
docker stop the-id 
docker rm the-id
```

## Sicherheitsfunktionen

Die Konfiguration in `.devcontainer` bietet mehrere Sicherheitsfunktionen:

### Container-Isolation

Claude Code läuft in einem Docker-Container (oder auf GitHub Codespaces, das habe ich jedoch nicht ausprobiert).

### Netzwerk-Firewall

Das Firewall-Skript `.devcontainer/init-firewall.sh` beschränkt den Netzwerkzugriff auf nur zugelassene Ziele:

- Erlaubt: GitHub, Anthropic API, npm registry, statsig, sentry
- Blockiert: Alles andere (einschließlich beliebiger Internetseiten)

Du kannst das anpassen. Ich habe beispielsweise die folgende Zeile hinzugefügt, um Verbindungen zurück zu VS Code zu verhindern. Ohne dies kann Claude Code weiterhin auf Dateien zugreifen, die du in VS Code geöffnet hast, selbst wenn sie außerhalb des Devcontainers liegen.

```bash
# Block outbound connections on port 59778 so that claude code can't connect to vscode
# iptables -A OUTPUT -p udp --dport 59778 -j DROP
```

Ich habe das vor allem gemacht, weil Claude Code verwirrt ist, wenn Dateien offen sind, die es im Repo nicht findet, und weil es mich ablenkt, wenn Claude Code Dateien in VS Code öffnet, während ich an etwas Anderem arbeite.

### Eingeschränkter Dateizugriff

Claude Code kann nur in bestimmten Verzeichnissen lesen/schreiben:

- Dein Workspace-Ordner (Lese-/Schreibzugriff) (siehe `workspaceMount` in `devcontainer.json`)
- Befehlshistorie und Konfiguration (Volumes) (siehe `mounts` in `devcontainer.json`)

Dein Home-Verzeichnis ist *nicht* gemountet – Claude Code kann nicht auf deine persönlichen Dateien zugreifen.

### Nicht-Root-User

Befehle im Container laufen unter dem Benutzer `node` mit eingeschränkten Rechten.

### Eingeschränkte bash-Befehle (optional)

Es gibt außerdem ein `bash_command_validator_example.sh`, das ein "Claude Code [PreToolUse hook](https://docs.claude.com/en/docs/claude-code/hooks#pretooluse)" für das bash-Tool ist, der "bash-Befehle vor der Ausführung anhand eines Regelwerks validiert". 

Damit kannst du einschränken, welche bash-Befehle Claude Code in deiner Sandbox ausführen darf.


## Devcontainers für eigene Projekte anpassen

{{< alert "poo" >}}
Das ist noch nicht fertig.
{{< /alert >}}

### Basis übernehmen

Kopiere die Basis aus `claude-code/.devcontainers` in das Root-Verzeichnis deines Projekts (oder ein Unterverzeichnis) und passe das `Dockerfile` an deine Anforderungen an. Claude oder Codex können dir helfen, aber das Dockerfile anzupassen kann je nach Projekt schon recht aufwendig sein. Ich konnte es recht schnell für FastAPI-/Air-Projekt adaptieren, hatte aber Probleme, Playwright MCP zum Laufen zu bringen. Am Ende habe ich Claude stattdessen in der `CLAUDE.md` Datei gebeten, die Playwright CLI zu verwenden.

### Dockerfile anpassen

### devcontainer.json anpassen

### Firewall-Skript anpassen

## Zusammenfassung

Wenn Claude Code in einem wie beschrieben konfigurierten Devcontainer läuft, kann es nur

- Auf Dateien in /workspace (dein Projekt) und andere gemountete Verzeichnisse zugreifen
- Netzwerkanfragen an freigegebene Domains stellen
- Befehle innerhalb des Containers ausführen, optional mit zusätzlichen Leitplanken

Deine persönlichen Dateien, Dokumente, SSH-Schlüssel von deinem Host-Rechner, Browserdaten usw. sind für Claude Code in diesem Container nicht zugänglich. Aber:

- Claude Code kann weiterhin beliebige Dateien in deinem gemounteten Workspace lesen/ändern, dazu gehören auch `.env`-Dateien
- Git-Zugangsdaten im Container können das Pushen in Repos erlauben
- Der Container teilt sich den Docker-Daemon, wenn Docker-in-Docker (oder Kubernetes-in-Docker) aktiviert ist. Das hat mich etwas überrascht, als ich eine App in einem KinD-Cluster in einem Devcontainer ausführen wollte.
- Datenexfiltration ist weiterhin möglich, z. B. über DNS.

Devcontainers fügen eine Sicherheitsebene hinzu, aber nichts ist perfekt sicher. Devcontainers vereinfachen außerdem das Onboarding in ein Projekt oder das parallele Durchführen von Experimenten in isolierten Umgebungen. Nachteile von Devcontainers sind, dass die Einrichtung zeitaufwendig ist und die Arbeit damit weniger bequem und langsamer ist als direkt auf einer lokalen Maschine.