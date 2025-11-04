---
aliases:
- /blog/a-note-about-the-hidden-complexities-of-websockets/
author: null
categories:
- KI-Engineering
- Blog
date: 2025-01-25
draft: false
slug: eine-notiz-zur-verborgenen-komplexitaet-von-websockets
tags:
- websockets
- echtzeit
title: Eine Notiz zur verborgenen Komplexität von WebSockets
---

KI-Apps benötigten of Nahe-Echtzeit-Kommunikation, z. B. beim Streamen von Chatbot Nachrichten. Im Web lässt sich Echtzeitkommunikation mit WebSockets implementieren. Ich habe mit WebSockets begonnen, um Chatbots und andere Live Interfaces zu entwickeln, bin dann aber aufgrund einiger Herausforderungen mit WebSockets für die meisten Einsatzzwecke auf SSE umgestiegen. Hier liste ich kurz einige Fallstricke von WebSockets auf.

<!-- more -->

## Meine Faustregel für WebSockets

Mein Faustregeln für die Entscheidung für oder gegen WebSockets sind: 

* Verwende WebSockets für Server-zu-Server-Kommunikation.
* Verwende SSE für Server-zu-Client-Kommunikation.
* Wenn Du WebSockets trotzdem für Server-zu-Client-Kommunikation einsetzen willst oder musst, ergänze einen Fallback auf SSE, da WebSocket oft von Unternehmensfirewalls blockiert werden.
* Verwende WebRTC für Echtzeit-Sprach-/Video-Server-zu-Client-Kommunikation.

## Die verborgene Komplexität von WebSockets

Falls Du jetzt trotzdem einen WebSocket-Dienst entwickeln willst, kann ich Dir Atul Jalans Blogpost über [The Hidden Complexity of Scaling WebSockets](https://composehq.com/blog/scaling-websockets-1-23-25) empfehlen. Hier ist eine kurze Zusammenfassung:

- Downtimeless Deployments sind deutlich komplexer als bei HTTP-Services.
- Etabliere ein gutes Nachrichtenschema (kurz, spezifisch für die Anwendung), z. B. 2-Byte-Präfixe und ein Zeichen als Feldtrenner.
- Verwende Heartbeats in beide Richtungen, um tote Verbindungen zu erkennen und entwickle Methoden, um verlorene Verbindungen Wiederherzustellen, auf Fallbacks zu gehen oder Ressourcen freigeben, wenn das nicht möglich ist.
- Implementiere ein HTTP-Fallback, da WebSockets oft blockiert werden. Üblicherweise: Server-Sent Events (SSE) für Server-zu-Client-Kommunikation und einfache Requests für Client-zu-Server.
- Viel Gewohntes fehlt bei WebSockets: Standard-Tooling (Rate Limiting, Validation, Error Handling), Caching am Edge, Authentifizierung pro Nachricht, etc.

## Was bieten Frameworks?

Frameworks wie Django, Litestar, FastAPI und Quart bieten gute Basisunterstützung für WebSockets, helfen aber wenig bis gar nicht bei den obengenannten Herausforderungen. Ich hoffe, Frameworks legen hier noch etwas nach, denn einige der Komplexitäten sind eher "undifferentiated heavy lifting".