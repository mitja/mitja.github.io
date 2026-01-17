---
author: null
date: 2026-01-13 18:21:46+02:00
draft: false
slug: von-8-zeilen-mit-dokku-zu-200-zeilen-mit-k8s
title: Von 8 Zeilen mit Dokku zu 200 mit Kubernetes – warum ich trotzdem wechsle
categories: ["AI Engineering", "Blog"]
tags: ["Kubernetes", "Dokku"]
stream: false
---

Bislang laufen meine Web Apps auf einem Dokku Server. Vercel oder Fly hab ich nicht ausprobiert, weil ich mich nicht mit komplexen Preismodellen beschäftigen wollte, die mit jedem weiteren Projekt immer mehr Kosten verursachen.

Dokku funktioniert wie Heroku:

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

Einfacher geht's nicht. Nach nur 8 Zeilen habe ich

- eine App auf dem Server,
- eine PostgreSQL DB mit einem Benutzer und Passwort,
- die App mit postgres verknüpft,
- ein Secret konfiguriert,
- die App aus einem docker image bereitgestellt,
- einen Reverse Proxy konfiguriert, um http und https an den Container der App weiterzuleiten, und
- TLS mit von Let's Encrypt signierten Zertifikation (inklusive automatischer Verlängerung).

Mit Kubernetes brauche ich dafür fast **200 Zeilen yaml**. Warum will ich trotzdem zu Kubernetes wechseln?

Dokku passt perfekt zu kleinen Projekte, die mit den Dokku Plugins auskommen und auf einem Server laufen. Ich glaube aber, dass Kubernetes langfristig besser zu mir passt.

Kubernetes Manifeste sagen mir (und LLMs), was auf dem Cluster läuft und ich kann sie immer weiter entwickeln und verbessern. Dokku fühlt sich dagegen an, wie "Fire, forget, and start from scratch". Weitere Vorteile von Kubernetes wie bessere Skalierbarkeit, mehr Auswahl und Sicherheit sind auch nett, aber für mich ist der wichtigste Vorteil aktuell:

**Kubernetes passt gut zum Vibe Coding.**

Das ist jedenfalls meine Vermutung. Mal sehen, wie es läuft.
