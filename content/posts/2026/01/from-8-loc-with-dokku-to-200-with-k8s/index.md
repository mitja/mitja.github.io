---
author: null
date: 2026-01-13 18:21:46+02:00
draft: false
slug: from-8-lines-with-dokku-to-200-with-k8s
title: "From 8 Lines with Dokku to 200 with Kubernetes – Why I'm Still Switching"
categories: ["AI Engineering", "Blog"]
tags: ["Kubernetes", "Dokku"]
stream: false
---

So far, my web apps run on a Dokku server. I haven't tried Vercel or Fly because I didn't want to deal with complex pricing models that incur more costs with every additional project.

Dokku works like Heroku:

```bash
dokku apps:create myapp
dokku postgres:create myapp-db
dokku postgres:link myapp-db myapp
dokku config:set myapp APP_SECRET="$(openssl rand -base64 48)"
dokku git:from-image myapp myregistry.example.com/image:tag
dokku domains:set myapp myapp.mitjas.com
dokku ports:set myapp http:80:8000 https:443:8000
dokku letsencrypt:enable myapp
```

It doesn't get any simpler. After just 8 lines I have

- an app on the server,
- a PostgreSQL DB with a user and password,
- the app linked to Postgres,
- a secret configured,
- the app deployed from a Docker image,
- a reverse proxy configured to forward HTTP and HTTPS to the app's container, and
- TLS with certificates signed by Let's Encrypt (including automatic renewal).

With Kubernetes I need almost **200 lines of YAML** for this. Why do I still want to switch to Kubernetes?

Dokku is great for small projects that can make do with the Dokku plugins and run on a single server. But I believe Kubernetes is a better fit for me in the long run.

Kubernetes manifests tell me (and LLMs) what's running on the cluster, and I can continuously develop and improve them. Dokku, in contrast, feels like "fire, forget, and start from scratch." Other advantages of Kubernetes like better scalability, more choice, and security are nice, too, but for me the most important advantage right now is:

**Kubernetes is well-suited for Vibe Coding.**

That's my assumption, anyway. Let's see how it goes.
