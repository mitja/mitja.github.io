---
author: null
date: 2026-01-14
draft: false
slug: mcp-a2a-angriffsvektoren
title: MCP- und A2A-Angriffsvektoren für KI-Agenten
stream: false
---

Christian Posta von Solo.io hat einen guten Artikel zum Thema [Deep Dive into MCP and A2A Attack Vectors for AI Agents](https://www.solo.io/blog/deep-dive-mcp-and-a2a-attack-vectors-for-ai-agents) geschrieben.

Hier ist eine kurze Übersicht über mögliche Angriffsvektoren. Es gibt bestimmt weitere, und die Gegenmaßnahmen sind ein Anfang aber sicher nicht perfekt.

| Angriffsvektor | Funktionsweise | Gegenmaßnahme |
|----------------|----------------|---------------|
| Naming-Angriffe | Angreifer erstellen ähnlich aussehende Namen oder Typosquatting-Dienste, welche die KI dazu bringen, eine bösartige Ressource anstelle der legitimen auszuwählen | Eindeutige Identitäten erzwingen, Server-/Agenten-Identitäten kryptografisch verifizieren und eine vertrauenswürdige Registry anstelle von blindem Namensabgleich |
| Context Poisoning / Indirekte Prompt Injection | Ein Angreifer bettet versteckte Anweisungen in den Kontext ein, die das Modell zu schädlichen Aktionen oder Leaks verleiten; bei A2A kann dies über bösartige Task-Zustände oder fehlerhafte Skill-Beschreibungen geschehen | Beschreibungen bereinigen und prüfen, strikte Schema-Constraints verwenden und natürlichsprachliche Metadaten begrenzen oder filtern bevor sie die Modelle sehen |
| Shadowing-Angriffe | Ein bösartiger Dienst überlagert ein legitimes Tool oder einen Agenten, indem er etwas registriert, das das Verhalten anderer vertrauenswürdiger Komponenten verändert (z.B. versteckte Anweisungen einschleusen, die Abrechnungslogik ändern oder die Ausgaben anderer Agenten beeinflussen) | Authentifizierung und Autorisierung für jede Komponente, Whitelists und sicherstellen, dass Tools/Agenten nicht allein aufgrund von unverifizierter Präsenz im Kontext verwendet werden |
| Rug Pulls | Ein Angreifer baut zunächst Vertrauen auf, indem er ein nützliches Tool oder einen Agenten bereitstellt, ändert aber nach breiter Akzeptanz subtil dessen Verhalten, um schädliche Aktionen durchzuführen, Ausgaben zu manipulieren oder Daten zu exfiltrieren | Kontinuierliches Monitoring, Verhaltensänderungen im Zeitverlauf bewerten, Policy-Controls und Versions-Gating, damit Tools ihre Semantik nicht plötzlich ohne Überprüfung ändern können |

KI-Agenten nutzen Protokolle wie MCP (Model Context Protocol) und A2A (Agent-to-Agent) und entscheiden, wann und wie sie Tools oder andere Agenten aufrufen. Diese dynamische Erkennung und Nutzung basiert auf natürlichsprachlichem Kontext, was sie anfällig für semantische Manipulation macht.