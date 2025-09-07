---
title: Monitor a Dokku Server with Prometheus and Grafana
author: mitja
date: 2024-10-03
category: Self-Hosting with Dokku
tags: [Dokku, Prometheus, Grafana]
#pin: true
#math: true
#mermaid: true
render_with_liquid: false
permalink: /blog/2024/10/04/monitor-a-dokku-server-with-prometheus-and-grafana/
image:
  path: /assets/blog/dokku.png
  alt: The Dokku logo which is a friendly whale with a captain's hat (I think).
---

I have a Dokku server on a Hetzner Cloud server and was missing the observability of common Kubernetes setups. It's really nice to have dashboards with metrics and alerts for the server, the apps, the datastores, etc. Fortunately, Prometheus and Grafana run on and work with Dokku, too.

The setup is honestly quite involved, but I'll try to make it simple. Here is what is installed:

- node exporter: for server metrics
- cAdvisor: for container metrics
- Prometheus: for metrics storage
- Grafana: for metrics visualization
- Alertmanager: for alerts

- dashboards...

- alert rules for 
  - node_exporter: https://gist.github.com/krisek/62a98e2645af5dce169a7b506e999cd8
  - lots of rules: https://samber.github.io/awesome-prometheus-alerts/rules.html#docker-containers

what I did:

install the [dokku-http-auth](https://github.com/dokku/dokku-http-auth) plugin (assuming the let's encrypt plugin is already installed):

```bash
dokku plugin:install https://github.com/dokku/dokku-http-auth.git
```




Source: https://kleinprojects.com/prometheus-and-grafana-with-dokku/