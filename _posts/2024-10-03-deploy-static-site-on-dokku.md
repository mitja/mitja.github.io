---
title: Deploy a Static Site on Dokku
author: mitja
date: 2024-10-03
category: Building AI Apps
tags: [Dokku, Static Site, Tailwind CSS, Plausible, Email Octopus, Hetzner]
#pin: true
#math: true
#mermaid: true
render_with_liquid: false
permalink: /blog/2024/10/03/deploy-static-site-on-dokku/
#image:
#  path: /assets/blog/2024/launch-vscode-from-the-cli/thumbnail.png
#  alt: Comparing the effect on settings of launching VS Code directly vs from the command line
---

Today, I wanted to try a little experiment: In reaction to a tweet by Pieter Levels about preferring builder as opposed to talker, I created and launched a dead simple website called [Builder Habit](https://builderhabit.com). This is just a landing page for a reminder service to get into builder mode and "strengthen your builder habit."

The site has newsletter signup form for a list hosted by Email Octopus, and Plausible analytics. Otherwise it's just a static site with Tailwind CSS and some custom CSS for styling it in a kind of neo-brutalist way. The Domain is registered at Hetzner and I use Dokku to run the site. Admittedly, this is the first static site, I deployed on Dokku, and I wanted to share with you how easy it is. 

Here is everything that's needed to deploy the site, including activating Let's encrypt signed certificates for the domain:

1. Create a git repository
2. add an `index.html` file with the content.
3. Ad an an empty `.static` file. The `.static` file is needed to tell Dokku that this is a static site - Dokku then uses an Nginx builder to build and deploy it.
4. use some commands to create, configure, and deploy the site:

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

Updates can be deployed by checking them into git and then with the command `git push dokku main`.
