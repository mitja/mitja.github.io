---
title: Deploying a SaaS Pegasus Based Django App on Dokku
author: mitja
date: 2024-09-22
category: Building AI Apps
tags: [SaaS, Django, Dokku]
#pin: true
#math: true
#mermaid: true
render_with_liquid: false
permalink: /blog/2024/09/22/deploying-django-on-dokku/
#image:
#  path: /assets/blog/2024/furo-sphinx-theme/furo-customization.png
#  alt: A screenshot of the Furo Sphinx Theme
---

I am working on a SaaS app. Although I started it with [FastAPI](https://fastapi.tiangolo.com) I decided to go back to [Django](https://www.djangoproject.com) since I'm using Django on and off since end of 2005 (really!) thus, I know it much better than FastAPI. Also, I like its batteries included approch and the Django way of rendering frontends mostly server-side with some HTMX, jQuery and vanilla.js.

Until now, I used [Django Cookiecutter](https://cookiecutter-django.readthedocs.io/en/latest/) to start projects which were only personal and company-internal tools up to this point. As I'm now building a SaaS I switched to [SaaS Pegasus](https://saaspegasus.com/) as a project template.

SaaS Pegasus comes with quite a few options for deploying, including with [Kamal](https://kamal-deploy.org) on a single server. As I already had a [Dokku](https://dokku.com) server running, I buckled down and found a way to deploy it on Dokku.

In this post I'll share the steps I did to deploy a SaaS Pegasus bootstrapped Django app (Scriv from the SaaS Pegasus marketplace to be precise) with Celery, Redis and Postgres on a Dokku host. There were some hickups along the way, but I believe, once it's all described step-by-step, it is quite straightforward.

## Preconditions

The main precondition is, that you have a Dokku server running and that you can use it from your local machine with commands like `ssh dokku@<your-dokku-server> apps:list`. There are some commands you need to run on the server with `sudo` and the actual deployment is done from your local machine with `git push dokku main`, but you need to use `dokku` commands to configure your app. 

Of course, you could also logon to the server and run the commands, there, but it would be a bit more tedius, especially when configuring the the environment variables you need for the app. SaaS Pegasus already uses a `.env` example file for these variables. I created a little helper script that configures the `dokku` app environment variables based on the `.env` file. This very much simplifies configuring and updating the environment variables. The script is created in a way that it assumes you run it on your local machine.

Another precondition is that you have a domain pointing to the Dokku server. This is not strictly necessary, but required if you want to use TLS with Let's Encrypt.

## The Target Setup

The server is a [Hetzner Cloud](https://www.hetzner.com/cloud/) CPX31 instance located in Germany with 4 vCPU, 8 GB RAM, 160 GB NVMe, Shared AMD CPU, with Ubuntu 22.04. It costs a bit less than 20 EUR including sales tax here in Germany with backups enabled. 

In my experience this server size is a good starting point for MVPs which leaves a little head room. You can also use a smaller one, like the CPX21 with 3 vCPU and 4 GB RAM but I would not go smaller than that as Dokku not only runs the apps on the server, but also builds the container images there, which consumes about 1 GB RAM while building.

The application environment has quite a few components:

  - A PostgreSQL database instance
  - A Redis service
  - A storage volume for the media files
  - A cron jobs for letsencrypt certificate renewal
  - The web service part of the application
  - The worker part of the application
  - A release process that runs one-off commands during deployment
  - various circumfencing services, like S3, an email service, a payment service, a newsletter service, etc.

In addition, SaaS Pegasus runs the Docker build in a multi-stage build to compile the frontend assets and to collect the static files. This is good practice for production deployments, but it makes the deployment a bit more complex. Fortunately, this is all handled by the `Dockerfile.web` that SaaS Pegasus provides and which works perfectly in tandem with SaaS Pegasus' application code.

You may wonder why I chose such a complicated setup for an MVP. The answer is simple: SaaS Pegasus provides for all the necessary parts, already, and the aspect which complicates things during deployment and operation most is the separation between web instances and worker instances. However, I prefer to have this separation in place, as it is in my view necessary anyway after the very initial prototype, even if it's just for sending transactional emails. And in my experience, integrating it later is usually more painful than setting it up right from the start.

The drawback of this approach is, that managed cloud services can get quite expensive with all these components. This is why I like to run MVPs on a single server and only deploy to a managed cloud platform, if an MVP turns out to be a success.

## Set Basic Environment Variables

The code snippets in this post all use a few basic environment variables which are defined here. This way, you should be able to run all the commands just by copy-pasting them into your terminal.

```bash
export ADMIN_USER=<username-on-server>
export DOKKU_HOST=<your-dokku-server-domainname-or-ip>
export APP_DOMAIN=<the-domain-name-of-your-app>
export APP_NAME=<the-name-of-your-app-in-dokku>
```

## Create the Dokku App and Set the Builder

Let's kick things off by creating the app on Dokku. This way, you can also test, if you can run Dokku commands from your local system like this: `ssh dokku@<your-dokku-server> apps:list`.

The `builder-dockerfile:set` configuration is necessary, since SaaS Pegasus creates the production Dockerfile at `Dockerfile.web` and not `Dockerfile` which is what Dokku expexts by default.

```bash
ssh dokku@$DOKKU_HOST apps:create $APP_NAME  
ssh dokku@$DOKKU_HOST builder-dockerfile:set $APP_NAME dockerfile-path Dockerfile.web 
``` 

## Install Dokku Plugins and Configure Global Settings

Dokku plugins extend Dokku's basic functionality. The required plugins are:

  - [dokku-letsencrypt](https://github.com/dokku/dokku-letsencrypt) for handling SSL certificates
  - [dokku-postgres](https://github.com/dokku/dokku-postgres) for the PostgreSQL database
  - [dokku-redis](https://github.com/dokku/dokku-redis) for the Redis service

Plugins must be installed on the server. To do this, logon to the server:

```bash
ssh $ADMIN_USER@$DOKKU_HOST
```

On the server, run the following commands:

```bash
sudo dokku plugin:install https://github.com/dokku/dokku-letsencrypt.git
sudo dokku plugin:install https://github.com/dokku/dokku-postgres.git postgres
sudo dokku plugin:install https://github.com/dokku/dokku-redis.git redis
# don't keep `run` containers around
dokku config:set --global DOKKU_RM_CONTAINER=1
dokku letsencrypt:cron-job --add
```

## Create a Storage Volume for the Media Files

This step is also performed on the server. Often, you need a local media files volume even if you use S3 for the storage. This is for example required for temporary files during uploads.

I decided to create the storage path in the canonical location for Dokku. This way, standard Dokku backups include this volume, as well.

Run these commands on the dokku server to create and mount the storage volume:

```bash
export STORAGE_PATH="/var/lib/dokku/data/storage/$APP_NAME"
mkdir -p "$STORAGE_PATH"
chown -R 1000:1000 "$STORAGE_PATH"
export MEDIA_DIR="/code/media"
dokku storage:mount $APP_NAME "$STORAGE_PATH:$MEDIA_DIR"
```

Note that the `django` user inside the application containers has `UID=GID=1000` if not set differently. This is why I set the ownership of the storage path to `1000:1000`. Of course, you can set this to something else, for example to separate storage permissions between different apps.

## Create the Database Service

Next, create the db `$APP_NAME-db` and get the connection string (`DSN`) which you should then use to configure the `DATABASE_URL` in the `.env` file.

Notice that I use a special Docker image here. This is necessary, as the app I've created requires Postgres with the vector extension enabled. You can omit the `--image` option if you don't need a special image.

If you wonder, why you need to create the database service separately from installing the plugin: This is because the plugin only enables the management of database services. You can then use the plugin to create and manage as many database services as you need on your Dokku host, eg. separate database services per application, or two different database versions during database version upgrades. The same is true for Redis and other similar services.

```bash
ssh dokku@$DOKKU_HOST postgres:create $APP_NAME-db --image "pgvector/pgvector" --image-version "pg15"
ssh dokku@$DOKKU_HOST postgres:info $APP_NAME-db --dsn
```

## Create the Redis Service

Now, create the Redis service `$APP_NAME-redis` and get the connection string set the `REDIS_URL` in the `.env` file.

```bash
ssh dokku@$DOKKU_HOST redis:create $APP_NAME-redis
ssh dokku@$DOKKU_HOST redis:info $APP_NAME-redis --dsn
```

## Link the Database and Redis Services to the App

At this point, database and redis services for the app have been created, but the app cannot use them, because they are not yet reachable via the Dokku host internal network. To fix this, run the following commands. They will `link` the services to the app, which makes them reachable:

```bash
ssh dokku@$DOKKU_HOST postgres:link $APP_NAME-db $APP_NAME
ssh dokku@$DOKKU_HOST redis:link $APP_NAME-redis $APP_NAME
```

## Configure the App

If you want to configure the application environment variables based on an `.env` file, create a Python script called `dokku_config.py` with the following content:

```python
import os
import click

# This is based on https://github.com/Tobi-De/dokku-envs

def run_commands(command, host, app, env_dict):
    for env_name, env_value in env_dict.items():
        os.system(command.format(host_name=host, app_name=app, env_name=env_name, env_value=env_value))


def read_env_file(env):
    f = env.readlines()
    return {line.strip().split("=")[0]: line.strip().split("=")[1] for line in f if "=" in line}


@click.command()
@click.argument(
    "host"
)
@click.argument(
    "app"
)
@click.argument(
    "env",
    type=click.File("r"),
)
def set_dokku_app_envs(host, app, env):
    """Set environment variables of a Dokku app to values defined in an env file.

    This runs locally and assumes you can use your Dokku server via SSH, and
    execute commands like `ssh dokku@<server> config:set <app> <env_name>=<env_value>`.
    """
    command = "ssh dokku@{host_name} config:set {app_name} {env_name}={env_value}"
    env_dict = read_env_file(env=env)
    if not env_dict:
        return
    run_commands(command, host, app, env_dict)


if __name__ == "__main__":
    set_dokku_app_envs()
```

Then enter all necessary variables in the `.env` file. For reference, here is the list of environment variables in a realistic `.env` file. The application logic that makes use fo these variables is provided by the SaaS Pegasus template, the Scriv application from the SaaS Pegasus marketplace, the various Django packages, and Django itself.

```bash
SECRET_KEY='...'
DATABASE_URL='...'
REDIS_URL='...'
# web app analytics
GOOGLE_ANALYTICS_ID='...'
# app error tracking
SENTRY_DSN='...'
# bot detection
TURNSTILE_KEY='...'
TURNSTILE_SECRET='...'
# payment processing
STRIPE_LIVE_PUBLIC_KEY='...' 
STRIPE_LIVE_SECRET_KEY='...'
STRIPE_TEST_PUBLIC_KEY='...'
STRIPE_TEST_SECRET_KEY='...'
DJSTRIPE_WEBHOOK_SECRET='...'
# just to be sure...
ENABLE_DEBUG_TOOLBAR=False
# slack integration
SLACK_CLIENT_ID='...'
SLACK_CLIENT_SECRET='...'
SLACK_SIGNING_SECRET='...'
# openai integration
OPENAI_API_KEY="..."
OPENAI_MODEL="..."
# s3 media storage
USE_S3_MEDIA=True
AWS_ACCESS_KEY_ID='...'
AWS_SECRET_ACCESS_KEY='...'
AWS_STORAGE_BUCKET_NAME='...'
AWS_S3_CUSTOM_DOMAIN='...'
# newsletter
EMAIL_OCTOPUS_API_KEY='...'
EMAIL_OCTOPUS_LIST_ID='...'
# securing endpoints for health check and admin interfaces
HEALTH_CHECK_TOKENS='...'
ADMIN_URL_TOKEN="..."
# transactional email
MAILGUN_API_KEY='...'
MAILGUN_SENDER_DOMAIN='...'
SERVER_EMAIL='...'
DEFAULT_FROM_EMAIL='...'
EMAIL_SUBJECT_PREFIX='...'
```

Then run:

```bash
pip install click 
python dokku_config.py $DOKKU_HOST $APP_NAME .env
```

Note that I also needed to configure some variables directly in the `settings_production.py` and the `settings.py`files, notably the `ALLOWED_HOSTS`, the `PROJECT_METADATA`, and the `ADMINS` settings. I edited them there, as they were not part of the `.env` file, already and also a bit structured.

I also needed to replace the use of `Site.objects.get_current().domain` in `apps.web.meta.py` by a static reference of the domain, since this line resulted in errors when trying to run the initial migrations.

If some settings are missing or if you want to set them manually you can configure them like this (by example of the `SECRET_KEY`):

```bash
ssh dokku@$DOKKU_HOST config:set $APP_NAME SECRET_KEY=VALUE
```

## Create a Procfile

The `Procfile` defines the processes that run in the app. This is similar to the way Heroku works and in our case necessary, as we need to run multiple different processes for the app. I have three processes defined:

- `release` is a one-off command used to create and run the migrations
- `web` is the gunicorn worker process(es) that serve the web requests
- `worker` ist the celery worker process that processes background tasks

Create a `Procfile` in the root folder of the application with following content:

```bash
release: python manage.py makemigrations && python manage.py migrate sites --no-input && python manage.py migrate --no-input
web: gunicorn --bind 0.0.0.0:5000 --workers 1 --threads 8 --timeout 0 $APP_NAME.wsgi:application
worker: celery -A $APP_NAME worker -l INFO --beat --concurrency 2 -Q celery,background
```

Exchange the `$APP_NAME` placeholder with the name of the app **in Django** (not in Dokku, but I suggest to use the same name for both). Note that I use port `5000` for the web process, instead of the more common port `8000` for Django apps. This is because Dokku Nginx ingress uses port `5000` by default. This way, I don't need to adjust the Nginx configuration for this app.

I believe there is a better way of defining the web and worker processes, that allows scaling these processes with `dokku` commands, but I haven't tried this, yet.

## Deploy the App

Now for the fun part: Deploying the app. This is done by git-pushing the code to the Dokku server.

```bash
git remote add dokku dokku@$DOKKU_HOST:$APP_NAME   
git push dokku main
```

Note that with this setup, these are the only two commands you need to run when you want to deploy a new version of the app. However, when you run actual migrations, I would recommend to run a database backup before deployment. For example, the following command creates a backup of the database and saves it in the current directory of your local machine with a filename that contains the short hash of the current git commit. When you use this commit for the deployment, you can easily identify which backup belongs to which deployment: 

```bash
dokku postgres:export $APP_NAME-db > $APP_NAME-db$(git rev-parse --short HEAD).dump
```

If you need to rollback a deployment, you can deploy the previous version of the app and then import the dump with `dokku postgres:import $APP_NAME-db < $APP_NAME-db-the-hash.dump`.

Just for reference: Deploying a new version takes about 30 seconds, and you can see the progress directly in the terminal. I like this a bit more than jumping to GitHub Actions to check the progress. although GitHub Actions is admittedly more professional.

## Add the App Domain and Enable Letsencrypt

Right now, the app is already accessible via `http://$APP_NAME.$HOST_NAME`. If you also want to deploy the app on a custom domain with TLS, add `A` and `AAAA` records for your domain pointing to the IP of the `DOKKU_HOST`. I usually also add a `CNAME` entry for `www` to point to `$HOST_NAME` as I prefer to serve the main app on the apex domain and not under `www`. As soon as the DNS records have been propagated, you can add the domain to the Dokku app and enable TLS with Let's Encrypt signed certificates by entering following commands:

```bash
ssh dokku@$DOKKU_HOST domains:add $APP_NAME $APP_DOMAIN
ssh dokku@$DOKKU_HOST letsencrypt:enable $APP_NAME
```

## Congratulations

That's it. Congratulations. You have reached the end of this tutorial and now hopefully know how to deploy a SaaS Pegasus bootstrapped Django app on a Dokku host. I hope it was helpful and not too overwhelming. If you have any questions or suggestions, please let me know (eg. per email or on X/Twitter).

I may - if time permits - update this how-to. Ideas for improvement are, eg. 

- how to setup a Dokku host, 
- how to deploy a Django Cookiecutter based Django app, so that you can follow the instructions even if you haven't purchased SaaS Pegasus, 
- how to enable scaling of the web and worker processes with dokku commands, and 
- how to do day-two-operations, like monitoring, backup, recovery, and troubleshooting.

For now, here are some commands that may be helpful for day-two-operations:

Inspect logs:

```bash
ssh dokku@$DOKKU_HOST nginx:error-logs $APP_NAME
ssh dokku@$DOKKU_HOST logs $APP_NAME
ssh dokku@$DOKKU_HOST postgres:logs $APP_NAME-db
```

Run one-off commands defined as management commands in the Django app:

```bash
ssh dokku@$DOKKU_HOST run $APP_NAME python manage.py COMMAND OPTIONS
```

So long and happy deploying!
