---
author: mitja
categories:
- KI-Engineering
date: 2025-05-09
draft: false
layout: post
slug: voice-agents-fuer-die-produktion-bereitstellen
tags:
- Voice Agents
- Session-Notizen
- PipeCat
- WebRTC
title: Voice Agents für die Produktion bereitstellen
---

Hier sind meine Notizen zu einer Lektion über die Bereitstellung von Voice Agents für die Produktion. Die Lektion ist Teil des [Voice Agents Course](https://maven.com/pipecat/voice-ai-and-voice-agents-a-technical-deep-dive).

{{< alert "lightbulb" >}}
Der Kurs ist von kwindla und swyx, dem CTO und einem Investoren von Daily.co, einem WebRTC und Voice AI Infrastruktur-Anbieter. Einige ihrer Empfehlungen sind entsprechend vorgeprägt. Ich gebe sie hier trotzdem direkt wider, da ich selbst nicht genug Erfahrung mit Voice Agents habe.
{{< /alert >}}

## TL;DR

- Für einfache, skalierbare Bereitstellung einen Voice-AI-Anbieter nutzen.
- Für Demos eine einzelne VM oder das eigene Homelab verwenden.

<!-- more -->

## Unterschiede zwischen Voice Agents und traditionellen Web Apps

- liegen überwiegend im Transport
- persistente Verbindung (Minuten)
- bidirektionales Streaming
- zustandsbehaftete Sessions

## Produktiv genutzte Voice Agents benötigen...

- Einen HTTP-Service für 
  - API-Endpunkte, 
  - die Website, 
  - Webhooks und
  - das Spawnen von Bots.
- Eine Media-Transport-Schicht oder ein Media-Transport-Service:
  - WebRTC-basiert für Client-zu-Server (udp), oder
  - websocket-basiert für Server-zu-Server (tcp).
- Bots (udp oder tcp, verbinden sich mit der Media-Transport-Schicht)

## Bots

 - Sind Instanzen der Agenten.
 - Können in Python mit PipeCat geschrieben werden.
 - Verwenden STT-, LLM- und TTS-Anbieter; das sind zugleich die Haupttreiber für Kosten und Latenz.
 - Sind oft mit kleinen Modellen gebündelt, z. B. für Voice Activity Detection (VAD)
 - Jeder gespawnte Bot bedient eine Session und benötigt während der gesamten Session reservierte Ressourcen:
   - 0,5 vCPU
   - 1 GB RAM
   - 40kbps für WebRTC-Audio (im Bereich 30-60 kbps)
   - Video erfordert mehr CPU (z. B. 1 vCPU) und Bandbreite
 - Müssen schnell verfügbar sein. Ziel für die Time-to-First-Word:
   - 2-3 Sek. (Web), 
   - 3-5 Sek. (Telefon)
 
## Wege, die "Fast-Start-Challenge" zu lösen

  - prozentbasierter Warm-Pool
  - schnelle Startzeiten (Caching, Pre-Loading)
  - proaktives/prädiktives Scheduling
  - Fallbacks aus der reaktiven Welt (z. B. UX-basierte Lösungen, nicht nur stille Fehler)

## Anforderungen an Infrastruktur-Anbieter

Infrastruktur-Anbieter

  - müssen tcp und udp unterstützen
  - Voice-AI-Anbieter sind am einfachsten (Pipecat Cloud, Daily, Vapi, Layercode)
  - Fly.io (und ggf. andere Container-Plattformen) sind gut, wenn sie udp unterstützen (Fly tut das)
  - ML-fokussierte Anbieter sind gut für konvergierte Bots mit größeren Modellen an Bord (GPU-Clouds)
  - Hyperscaler sind flexibel, aber komplex
  - BTW: CloudRun unterstützt kein udp
  - Demos können auf einzelnen VMs laufen oder sogar aus einem Homelab bereitgestellt werden
  - Wenn alles konvergiert bereitgestellt wird, kann die time-to-first word bis auf 500ms sinken
  - ansonsten sind 800-1000 ms gut genug und erreichbar
  - Nähe zu den Nutzerinnen und Nutzern ist wichtig (Daily plant globale Regionen für PipeCat Cloud, derzeit nur us-west)
  - Verbindungen zwischen Servern können mit WebSockets implementiert werden

## Was kommt als Nächstes?

Nach der Session habe ich mir die PipeCat-Beispiele angesehen und festgestellt, dass es recht einfach ist, einen simplen Voice Agent mit PipeCats [SmallWebRTCTransport](https://docs.pipecat.ai/server/services/transport/small-webrt) auf einem in Europa gehosteten virtuellen Server zu betreiben und dann den Transport zu wechseln und ihn in Produktion auf der PipeCat Cloud zu deployen.

Ich werde bei Gelegenheit einmal ausprobieren, ob die Latenz zwischen der US-basierten PipeCat Cloud und Anwendern in Europa schnell genug ist.
