---
title: "Hetzner Cloud Crashkurs"
slug: "hetzner-cloud-crashkurs"
weight: 10
kicker: "Training"
subtitle: "CLI, Terraform, Python"
status: "Pilot"
format: "3 × 2 h live + 3 h Hausaufgabe"
teaser: "Hetzner Cloud so bedienen, wie Teams es wirklich tun: mit der hcloud-CLI, mit Terraform und mit Python-Skripten – gegen ein Live-Mockup der Hetzner-Cloud-API mit echten virtuellen Maschinen."
summary: "Ein Crashkurs zum Betrieb von Hetzner Cloud mit der hcloud-CLI, Terraform mit dem hcloud-Provider und Python-Skripten mit hcloud-python. Alle bekommen ein Cloud-Projekt in einem Live-Mockup der Hetzner-Cloud-API, das echte virtuelle Maschinen startet."
layout: "training"
facts:
  - label: "Für wen"
    text: "Entwickler:innen und Admins, die auf Hetzner Cloud deployen oder es vorhaben; Teams, die vom Klicken in der Console zu Code wechseln; alle, die eine Shell und etwas Python kennen."
  - label: "Nicht für"
    text: "Kubernetes auf Hetzner, oder wer Terraform gegen Hetzner schon produktiv einsetzt."
  - label: "Format"
    text: "3 Live-Sessions à 2 h (ein Tag oder drei Abende) und ein Hausaufgaben-Workshop von ca. 3 h, selbstständig. Bis zu 12 Teilnehmende."
  - label: "Wo gearbeitet wird"
    text: "Ein Browser-Workspace (Educates) mit `hcloud`, `terraform` und `uv`. Jede Session ist ein eigenes Projekt in der Kurs-Cloud, mit Quotas, und wird am Ende gelöscht."
  - label: "Stack"
    text: "hcloud CLI 1.68, Terraform 1.16 mit `hetznercloud/hcloud` 1.69, hcloud-python 2.24, cloud-init."
  - label: "Du bringst mit"
    text: "Einen Browser."
  - label: "Danach hast Du"
    text: "Ein Web-Setup (Server per cloud-init, privates Netz, Firewall, Volume, Floating IP, HTTPS-Load-Balancer) auf drei Wegen gebaut; eine Terraform-Konfiguration, die Du durch Ändern von zwei Namen auf ein echtes Projekt richtest; Skripte für Inventar, Health und Rolling Rebuilds; die Fehlercodes und Limits, auf die es ankommt."
  - label: "Preis"
    text: "Kostenlos in der Pilotphase, begrenzte Plätze."
showDate: false
showReadingTime: false
showWordCount: false
showTableOfContents: false
showPagination: false
sharingLinks: false
---

## Ablauf

- **Session 1 — die hcloud-CLI** (2 h)
- **Session 2 — Terraform** (2 h)
- **Session 3 — Python** (2 h): die Webserver werden einer nach dem anderen neu gebaut, während der Load Balancer weiter antwortet, und danach zeigt `terraform plan` keinen Drift
- **Hausaufgabe — eine kleine App wie in einer echten Cloud** (ca. 3 h)
