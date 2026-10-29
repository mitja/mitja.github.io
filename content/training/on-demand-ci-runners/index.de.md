---
title: "CI-Runner on demand"
slug: "ci-runner-on-demand"
weight: 20
kicker: "Training"
subtitle: "Ein Runner pro Job, und eine Rechnung, die aufhört"
status: "Pilot"
format: "3 × 2 h live + 3 h Hausaufgabe, oder on demand"
teaser: "Forgejo-CI-Runner, die nur existieren, solange ein Job sie braucht: ein Server pro wartendem Job, eine Einmal-Registrierung pro Versuch, und gelöscht, bevor die nächste bezahlte Stunde beginnt."
summary: "Wie man CI-Runner betreibt, die nur existieren, solange ein Job sie braucht: ein Pool pro Label-Set, ein Server für wartende Jobs, eine Einmal-Registrierung pro Job-Versuch und Löschen, bevor die nächste bezahlte Periode beginnt."
layout: "training"
facts:
  - label: "Für wen"
    text: "Teams mit Forgejo (oder auf dem Weg dorthin), deren CI aus ein paar dauerhaft laufenden VMs besteht; Plattform-Leute, die für untätige Runner zahlen; alle, die je ein Runner-Token in eine VM kopiert und nie rotiert haben."
  - label: "Nicht für"
    text: "Wer ein gemanagtes CI-Produkt will, oder nur einen Job pro Woche hat (eine kleine VM ist dann billiger – das sagt der Kurs auch)."
  - label: "Format"
    text: "3 Live-Sessions à 2 h (ein Tag oder drei Abende) und ein Hausaufgaben-Workshop von ca. 3 h – oder dieselben vier Workshops on demand, selbstständig."
  - label: "Wo gearbeitet wird"
    text: "Ein Browser-Workspace (Educates) mit eigenem Forgejo, forgejo-fleet, `hcloud` und `jq`. Jede Session ist ein eigenes Projekt in der Kurs-Cloud und wird am Ende gelöscht."
  - label: "Stack"
    text: "[forgejo-fleet](https://git.paasbox.com/mitja/forgejo-fleet) v0.1.0, Forgejo 15 mit Actions, forgejo-runner 13.2, ein Live-Mockup der Hetzner-Cloud-API."
  - label: "Du bringst mit"
    text: "Einen Browser."
  - label: "Danach hast Du"
    text: "Eine Pool-Konfiguration, die Du durch Ändern von zwei Namen auf ein echtes Projekt richtest, ein mit Packer gebautes Runner-Image, ein Kostenmodell für Deinen Job-Mix, ein Runbook für die fünf Fehler, die wirklich passieren, und einen Untrusted-Pool für Pull Requests aus Forks."
  - label: "Preis"
    text: "Kostenlos."
showDate: false
showReadingTime: false
showWordCount: false
showTableOfContents: false
showPagination: false
sharingLinks: false
---

## Ablauf

- **Session 1 — Ein Job, ein Server, ein Lease** (2 h)
- **Session 2 — Pools, die kosten, was sie sollen** (2 h)
- **Session 3 — Vertrauen, Fehler und Betrieb** (2 h): der Orchestrator wird mitten im Job beendet; der Job läuft durch und der Server wird trotzdem zur richtigen Minute gelöscht
- **Hausaufgabe — Deine Flotte** (ca. 3 h, selbstständig)
