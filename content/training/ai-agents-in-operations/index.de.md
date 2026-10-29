---
title: "KI-Agenten im Betrieb"
slug: "ki-agenten-im-betrieb"
weight: 70
kicker: "Training"
subtitle: "Einen Agent diagnostizieren und handeln lassen, mit Leitplanken"
status: "In Vorbereitung"
format: "2 Wochen, ca. 12 h live"
teaser: "KI-Agenten beim Betrieb selbst gehosteter Apps helfen lassen: was ein Agent lesen darf und was dabei abfließt, typisierte Aktionen mit Freigaben, Restore-Übungen und Updates mit Rollback durch einen Agent, und einen Agent messen, bevor man ihm vertraut."
summary: "Ein Live-Online-Kurs darüber, wie KI-Agenten beim Betrieb selbst gehosteter Apps helfen: was ein Agent lesen darf und was dabei abfließt, was er tun darf und wer es freigibt, wie eine Restore-Übung und ein Update mit Rollback aussehen, wenn ein Agent sie ausführt, und wie man einen Agent misst, bevor man ihm vertraut."
layout: "training"
facts:
  - label: "Für wen"
    text: "Teams, die selbst gehostete Apps für sich oder für Kunden betreiben und gefragt werden, ob ein Agent dabei helfen darf: Agenturen mit vielen kleinen Installationen, Mittelstands-IT, Plattform-Teams mit zwei bis fünf Leuten. Du hast `kubectl` und einen Coding-Agent benutzt und hattest schon Bereitschaft für eine App."
  - label: "Nicht für"
    text: "Kubernetes- oder Agent-Grundlagen, mit Agents bauen (das ist *Eine KI-Softwarefabrik bauen*), oder wer seinen Produktivbetrieb abgeben will."
  - label: "Format"
    text: "2 Wochen: 4 Live-Sessions à 3 h, eine Woche 0 zum Selbstlernen von ca. 2 h, eine optionale Sprechstunde pro Woche. Etwa 12 Kontaktstunden. Bis zu 10 Teilnehmende."
  - label: "Wo gearbeitet wird"
    text: "Eine Demo-Umgebung in Deinem eigenen Hetzner-Testprojekt: ein Single-Node-k3s-Cluster mit Backups und Observability, Forgejo und Umami, und die Agent-Werkzeuge im Lab-Modus. Jeder Lab-Tag beginnt mit einer frischen Demo und endet mit ihrer Löschung."
  - label: "Du bringst mit"
    text: "Einen Laptop, ein leeres Hetzner-Cloud-Testprojekt mit Token (ca. 4–6 € Hetzner-Kosten für die zwei Wochen), den Coding-Agent, den Du schon nutzt, einen API-Key mit Ausgabenlimit."
  - label: "Danach hast Du"
    text: "Eine Lese-Policy für Deinen Agent; eine Freigabe-Tabelle für Deine Apps; eine selbst geschriebene Aktion, die Du abgelehnt, freigegeben und auditiert gesehen hast; ein Protokoll einer Restore-Übung und eines Updates mit Rollback; ein Eval für Deine eigene Betriebsaufgabe mit Kosten pro Lauf; einen Entscheidungsbogen für Deinen Betrieb."
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

- **Woche 0** — Einrichtung, selbstständig, ca. 2 h
- **Session 1 — Lesen:** dieselbe Diagnose zweimal, einmal mit direktem Kubeconfig und einmal über einen Lese-Proxy, und was dabei abgeflossen ist
- **Session 2 — Handeln:** typisierte Aktionen, Gefahren-Flags, Freigaben und Audit
- **Session 3 — Restore und Update:** eine Restore-Übung und ein Update mit Rollback, ausgeführt von einem Agent
- **Session 4 — Messen:** ein Eval für eine Betriebsaufgabe, mehrere Läufe, zwei Modelle, Kosten pro Lauf
