---
title: "Deploy a Static Site on Dokku"
date: 2024-10-03
categories: 
  - Self-Hosting with Dokku
tags: 
  - Dokku
  - Static Site
  - Tailwind CSS
  - Plausible
  - Email Octopus
  - Hetzner
aliases:
  - /blog/2024/10/03/deploy-static-site-on-dokku/
---
This article describes how to deploy a static site on Dokku, including activating Let's encrypt signed certificates for the domain.
<!-- more -->

## Configure DNS

Register the domain and point it to the Dokku server. I usually set these records in the domain's DNS zone:

```bash
A @ 7200 $DOKKU_SERVER_IPv4
A * 7200 $DOKKU_SERVER_IPv4
CNAME www 7200 $APP_DOMAIN
AAAA @ 7200 $DOKKU_SERVER_IPv6
AAAA * 7200 $DOKKU_SERVER_IPv6
```

## Create a git repository

Create a folder and turn it into a git repository:

```bash
mkdir static-dokku
cd static-dokku
git init .
```

Add an `index.html` file with the desired content:

```bash
echo "hi" > index.html
```

Create an empty  `.static` file. This tells Dokku that the repository contains a static site. Dokku then uses the Nginx builder to serve it.

```bash
touch .static
```

Commit the changes to git:

```bash
git add . 
git commit -m "initial commit"
```

## Create an app on the Dokku host and git push to deploy the app

Use these commands to create, configure, and deploy the site:

```bash
export DOKKU_HOST=<your dokku server>
export APP_DOMAIN=<your app domain>
export APP_NAME=<your app name>
ssh dokku@$DOKKU_HOST apps:create $APP_NAME
git remote add dokku dokku@$DOKKU_HOST:$APP_NAME
git push dokku main
ssh dokku@$DOKKU_HOST domains:add $APP_NAME $APP_DOMAIN
ssh dokku@$DOKKU_HOST letsencrypt:enable $APP_NAME
```

That's it. The site is now live at [your app domain]().

## Deploy updates

Updates can be deployed by checking them into git and running this command:

```bash
git push dokku main
```

## Serving from sub directory

Serving files from a subdirectory (eg. `public`) is possible by setting the `NGINX_ROOT` environment variable of the app on the Dokku host: 

```bash
ssh dokku@$DOKKU_HOST config:set $APP_NAME NGINX_ROOT=/app/www/public
```

## Building the site during deployment

If you want to build the site during deployment, you can use multiple [buildpacks](https://dokku.com/docs/deployment/builders/herokuish-buildpacks/), for example by adding a `.buildpacks` file to the root directory of the repository. 

This way, you can use the first buildpack for building and the second fro serving.

Another, even more flexible option is to use [Dockerfile deployments](https://dokku.com/docs/deployment/builders/dockerfiles/) with [multi-stage builds](https://docs.docker.com/build/building/multi-stage/).