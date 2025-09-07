---
title: "Deploy a Static Site on Dokku"
summary: "A step-by-step guide to deploying a static website to Dokku."
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

Today, I wanted to try a little experiment: In reaction to a tweet by Pieter Levels about preferring builder as opposed to talker, I created and launched a dead simple website called [Builder Habit](https://builderhabit.com). This is just a landing page for a reminder service to get into builder mode and "strengthen your builder habit."

The site has newsletter signup form for a list hosted by Email Octopus, and Plausible analytics. Otherwise it's just a static site with Tailwind CSS and some custom CSS for styling it in a kind of neo-brutalist way. The Domain is registered at Hetzner and I use Dokku to run the site. Admittedly, this is the first static site, I deployed on Dokku, and I wanted to share with you how easy it is. 

Here is everything that's needed to deploy the site, including activating Let's encrypt signed certificates for the domain:

1. Register the domain and point it to the Dokku server. I usually set these records in the domain's DNS zone:

```bash
A @ 7200 <DOKKU_SERVER_IP>
A * 7200 <DOKKU_SERVER_IP>
CNAME www 7200 <DOMAIN_NAME>
AAAA @ 7200 <DOKKU_SERVER_IP>
AAAA * 7200 <DOKKU_SERVER_IP>
```

2. Create a git repository
3. add an `index.html` file with the content.
4. Ad an an empty `.static` file. The `.static` file is needed to tell Dokku that this is a static site - Dokku then uses an Nginx builder to build and deploy it.
6. Commit the changes to git.
5. Use these commands to create, configure, and deploy the site:

```bash
export DOKKU_HOST=mitja.app
export APP_DOMAIN=builderhabit.com
export APP_NAME=builderhabit
ssh dokku@$DOKKU_HOST apps:create $APP_NAME
git remote add dokku dokku@$DOKKU_HOST:$APP_NAME
git push dokku main
ssh dokku@$DOKKU_HOST domains:add $APP_NAME $APP_DOMAIN
ssh dokku@$DOKKU_HOST letsencrypt:enable $APP_NAME
```

That's it. The site is live at [builderhabit.com](https://builderhabit.com).

Updates can be deployed by checking them into git and running `git push dokku main`.

Here are some more tips: 

Serving files from a subdirectory (eg. `public` in this example): 

```bash
ssh dokku@$DOKKU_HOST config:set $APP_NAME NGINX_ROOT=/app/www/public
```

Building the site during deployment:

When you want to automatically build a site during deployment, you can use [multiple buildpacks](https://dokku.com/docs/deployment/builders/herokuish-buildpacks/), for example by adding a `.buildpacks` file to the root directory of the repository. This way, you can use one buildpack for building and another, eg. [Nginx Buildpack](https://github.com/dokku/heroku-buildpack-nginx) for serving. Another option is to use [Dockerfile deployments](https://dokku.com/docs/deployment/builders/dockerfiles/).