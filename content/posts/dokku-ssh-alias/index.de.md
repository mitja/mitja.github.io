---
aliases:
- /blog/2024/10/22/dokku-ssh-alias/
author: null
categories:
- Self-Hosting mit Dokku
date: 2024-10-03
draft: false
slug: ssh-alias-fuer-dokku
tags:
- Dokku
title: SSH-Alias für Dokku
---
Hier ist ein schneller Tipp, um die Arbeit mit Dokku etwas zu vereinfachen.

<!-- more -->

Wenn Du Dir etwas Tipparbeit sparen möchtest, kannst Du Dir einen Alias für Dokku anlegen. Füge dazu die folgende Zeile zu deiner `.bashrc`- oder `.zshrc`-Datei hinzu:

```bash
alias dokku="ssh dokku@<DOKKU_HOST>"
```

Ersetze `<DOKKU_HOST>` durch den Domainnamen oder die IP-Adresse deines Dokku Servers.

Anstelle von `ssh dokku@<DOKKU_HOST>` kannst du nun einfach `dokku` eingeben, um dich mit deinem Dokku Server zu verbinden und Befehle wie `dokku apps:list`, `dokku logs <APP_NAME>` usw. auszuführen.