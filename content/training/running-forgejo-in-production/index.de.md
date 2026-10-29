---
title: "Forgejo produktiv betreiben"
slug: "forgejo-produktiv-betreiben"
weight: 30
kicker: "Training"
subtitle: "Weg von GitHub, ohne die CI zu verlieren"
status: "Pilot"
format: "9 Workshops, selbstständig"
teaser: "Ein Repository mit Issues und CI-Workflow in ein eigenes Forgejo migrieren und es dann betreiben: Runner, Backup und Upgrades, SSO, Skalierung und Kosten, und die echte Migration für eine ganze Organisation."
summary: "Ein Kurs über den Umzug von GitHub zu Forgejo und den Betrieb danach: die Migration selbst, Actions und Runner, Backup, Restore, Upgrades und SSO, Skalierung und Kosten, und die echte Migration für eine ganze Organisation."
layout: "training"
facts:
  - label: "Für wen"
    text: "Teams auf GitHub mit einem Grund für den Umzug (Kosten, Souveränität, eine schon getroffene Plattformentscheidung), und Teams, die Forgejo schon selbst betreiben, aber Backup, SSO oder Kapazitätsplanung noch nicht erledigt haben."
  - label: "Nicht für"
    text: "Teams ohne Anlass für einen Umzug, und Teams, die Forgejo für sich betreiben lassen wollen."
  - label: "Format"
    text: "9 Workshops zum Selbstlernen in einem gehosteten Browser-Lab. Keine Kohorte, keine festen Termine."
  - label: "Wo gearbeitet wird"
    text: "Ein Browser-Workspace (Educates) mit zwei eigenen Forgejo-Instanzen – eine als Stellvertreter für GitHub, eine als Ziel – und einem Projekt in der Kurs-Cloud für die Workshops mit Runnern."
  - label: "Stack"
    text: "Forgejo 15 mit Actions, forgejo-runner 13.2, forgejo-fleet v0.1.0, ein Live-Mockup der Hetzner-Cloud-API."
  - label: "Du bringst mit"
    text: "Einen Browser."
  - label: "Danach hast Du"
    text: "Aus Workshop 1: ein Repository samt Issues, Labels, Milestones und CI-Workflow migriert, der Workflow läuft grün, und Du kennst den einzeiligen Unterschied für ein echtes GitHub-Repository. Die anderen acht ergänzen einen dimensionierten Runner-Pool, geprobtes Backup, Restore und Upgrade, SSO/LDAP und Object Storage, ein Kostenmodell, einen Cutover-Plan und mehr."
  - label: "Preis"
    text: "Kostenlos in der Pilotphase, begrenzte Plätze."
showDate: false
showReadingTime: false
showWordCount: false
showTableOfContents: false
showPagination: false
sharingLinks: false
---

## Workshops

1. **Probelauf der Migration**
2. **Actions und Runner**
3. **Betrieb** — Backup, Restore, Upgrades, SSO/LDAP, Object Storage
4. **Skalierung und Kosten**
5. **Die echte Migration** — große Repositories, LFS, Benutzer, Rechte, Mirroring
6. **Ein Coding-Agent in der CI, auf eigener Infrastruktur**
7. **Das private Monorepo mit öffentlichen Teilen**
8. **Das offene Internet überleben** — Bots, Scraper und Missbrauch
9. **Geplante Jobs** — Dependency-Updates, Scans und SBOMs
