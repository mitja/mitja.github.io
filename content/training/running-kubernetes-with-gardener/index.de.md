---
title: "Kubernetes mit Gardener betreiben"
slug: "kubernetes-mit-gardener-betreiben"
weight: 40
kicker: "Training"
subtitle: "Der zweite Tag für kleine Teams"
status: "Geplant"
format: "3 Wochen, ca. 20 h live"
teaser: "Die Cluster betreiben, die Gardener Dir gibt: Backups wiederherstellen, Upgrades beobachten, eine App mit Ingress, TLS, Storage und Alerting anbinden, einen Game Day durchspielen und ein eigenes Runbook schreiben."
summary: "Ein Live-Online-Kurs zum Betrieb von Kubernetes-Clustern, die Gardener Dir bereitstellt: Backups, die Du wiederhergestellt hast, Upgrades, die Du beobachtet hast, eine App, die einen Game Day überstanden hat, und ein Runbook, das Du selbst geschrieben hast."
layout: "training"
facts:
  - label: "Für wen"
    text: "Kleine Teams (2–5 Leute) und Solo-Gründer, die eigene Cluster für ihre Anwendungen wollen und kein Plattform-Team haben. Du hast `kubectl` schon benutzt, aber noch nie eine Control Plane betrieben."
  - label: "Nicht für"
    text: "Kubernetes-Grundlagen, Bedarf an SLA und Hotline, oder den Aufbau einer Gardener-Landschaft für viele Teams."
  - label: "Format"
    text: "3 Wochen. Pro Woche: zwei Live-Sessions à 2 h, ein Lab-Walkthrough à 90 min, eine optionale Sprechstunde à 60 min. Etwa 20 Kontaktstunden. 8–12 Teilnehmende."
  - label: "Wo gearbeitet wird"
    text: "Ein Browser-Workspace (Educates) und eine eigene Gardener-Landschaft mit Namen unter `<du>.paasbox.app`. Kein Token landet auf Deinem Laptop."
  - label: "Du bringst mit"
    text: "Einen Browser, etwas `kubectl`-Erfahrung und eine eigene Anwendung (ein Container-Image und ein paar Manifeste) – oder Du nimmst unsere."
  - label: "Danach hast Du"
    text: "Ein Runbook für Deinen Cluster mit jedem Befehl, den Du ausgeführt hast; drei Restores (Shoot-etcd, Landschaft an Ort und Stelle, Landschaft aus dem Nichts); ein beobachtetes Upgrade; eine App auf einem Shoot mit Ingress, TLS, Storage und Alerting; ein Game-Day-Protokoll; eine Checkliste zur Produktionsreife; eine Antwort auf „Solo oder HA, und ab wann“."
  - label: "Preis"
    text: "Noch nicht festgelegt."
showDate: false
showReadingTime: false
showWordCount: false
showTableOfContents: false
showPagination: false
sharingLinks: false
---

## Ablauf

- **Woche 0** — Einrichtung, selbstständig, ca. 1,5 h
- **Woche 1 — Was Dir jetzt gehört und wie Du es zurückbekommst:** die Landschaft, die Du bekommen hast; Recovery zuerst (Du löschst den Server Deiner Landschaft und holst sie aus dem S3-Snapshot zurück)
- **Woche 2 — Ändern ohne Angst:** Upgrades und Nodes; Deine Anwendung, richtig angebunden
- **Woche 3 — Sehen, benachrichtigt werden, der Tag, an dem es bricht:** Observability und Alerting; Game Day, Sicherheit, Kosten und die Entscheidung zwischen Solo und HA
