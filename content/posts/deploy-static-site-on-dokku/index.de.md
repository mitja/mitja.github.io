---
aliases:
- /blog/2024/10/03/deploy-static-site-on-dokku/
author: null
categories:
- Selbsthosting mit Dokku
date: 2024-10-03
draft: false
slug: statische-website-auf-dokku-veroeffentlichen
tags:
- Dokku
- Statische Website
- Tailwind CSS
- Plausible
- Email Octopus
- Hetzner
title: Eine Statische Website auf Dokku veröffentlichen
---

Dieser Artikel beschreibt, wie Du eine statische Website auf einem Dokku Server veröffentlichst inklusive Let's-Encrypt-signierten Zertifikaten.

<!-- more -->

## DNS konfigurieren

Registriere die Domain und weise sie dem Dokku-Server zu. Ich setze meist folgende Einträge in der DNS-Zone der Domain:

```bash
A @ 7200 $DOKKU_SERVER_IPv4
A * 7200 $DOKKU_SERVER_IPv4
CNAME www 7200 $APP_DOMAIN
AAAA @ 7200 $DOKKU_SERVER_IPv6
AAAA * 7200 $DOKKU_SERVER_IPv6
```

## Ein git Repository erstellen

Erstelle einen Ordner und verwandle es in ein git Repository:

```bash
mkdir static-dokku
cd static-dokku
git init .
```

Füge eine `index.html` Datei mit dem gewünschten Inhalt hinzu:

```bash
echo "hi" > index.html
```

Erstelle eine leere Datei namens `.static`. Diese wird benötigt, um Dokku mitzuteilen, dass es sich um eine statische Website handelt. Dokku verwendet dann den Nginx-Builder, um sie zu bauen und bereitzustellen.

```bash
touch .static
```

Committe die Änderungen in git:

```bash
git add . 
git commit -m "initial commit"
```

## Die App auf Dokku anlegen und per git Push deployen

Verwende dann die folgenden Befehle, um die Website zu erstellen, zu konfigurieren und bereitzustellen:

```bash
export DOKKU_HOST=<dein-dokku-server>
export APP_DOMAIN=<deine-app-domain>
export APP_NAME=<dein-app-name-auf-dokku>
ssh dokku@$DOKKU_HOST apps:create $APP_NAME
git remote add dokku dokku@$DOKKU_HOST:$APP_NAME
git push dokku main
ssh dokku@$DOKKU_HOST domains:add $APP_NAME $APP_DOMAIN
ssh dokku@$DOKKU_HOST letsencrypt:enable $APP_NAME
```

Das wars. Die Website ist jetzt live unter [deine-app-domain]().

## Updates bereitstellen

Du kannst Änderungen veröffentlichen, indem du sie in git eincheckst und dann mit diesem Befehl auf den Dokku Server pushst:

```bash
git push dokku main
```

## Website im Unterverzeichnis

Die Website Dateien können auch in einem Unterverzeichnis des git Repositories liegen (z. B. `public`. Konfiguriere dazu die `NGINX_ROOT` Umgebungsvariable der Dokku Anwendung als Kombination von `/app/www/`und dem Unterverzeichnis (zum Beispiel `public`): 

```bash
ssh dokku@$DOKKU_HOST config:set $APP_NAME NGINX_ROOT=/app/www/public
```

## Die Website während der Bereitstellung bauen

Wenn du die Website während der Bereitstellung bauen möchtest, kannst du mehrere [buildpacks](https://dokku.com/docs/deployment/builders/herokuish-buildpacks/) verwenden, zum Beispiel, indem du eine Datei `.buildpacks` im Wurzelverzeichnis des Repositories  hinzufügst. 

Auf diese Weise kannst du das erste Buildpack zum Bauen und das zweite Buildpack als Webserver verwenden.

Eine weitere, noch flexiblere Option sind [Dockerfile deployments](https://dokku.com/docs/deployment/builders/dockerfiles/) mit [multi-stage builds](https://docs.docker.com/build/building/multi-stage/).