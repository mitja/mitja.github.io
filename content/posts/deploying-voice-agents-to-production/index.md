---
layout: post
title: "Deploying Voice Agents to Production"
summary: "Notes on a session about deploying voice agents to production by kwindla"
date: 2025-05-09
author: mitja
draft: false
categories: ["AI Engineering", "Blog"]
tags: ["Voice AI", "Session Notes", "PipeCat", "WebRTC"]
---

These are my notes on the session about deploying voice agents to production of the [Voice Agents Course](https://maven.com/pipecat/voice-ai-and-voice-agents-a-technical-deep-dive).

TLDR:

- Use a voice AI provider for simple, scalable deployment for production.
- Use a single VM or your homelab for demos.

Differences between voice agents and traditional apps: 

- are mostly in the transport
- persistent connnection (minutes)
- bidirectional streaming
- stateful sessions

Voice agents in production need:

- A http service for 
  - API endpoints, 
  - a website, and 
  - webhooks,
  - spawning bots.
- A media transport layer or service:
  - WebRTC based for client-to-server (udp), or
  - websocket based for server-to-server (tcp).
- Bots (udp or tcp, connect to media transport layer)

Bots:

 - Are instances of the agents.
 - Can be written in Python with PipeCat.
 - Use STT, LLM, and TTS providers, which also are the main cost and latency drivers.
 - Usually come packaged with small models, eg. for voice activity detection (VAD)
 - Each spawned bot serves one session and needs allocated resources during the whole session:
   - 0,5 vCPU
   - 1 GB RAM
   - 40kbps for WebRTC audio (in 30-60 kbps range)
   - video requires more CPU (eg. 1 vCPU), and bandwidth
 - Need to be quickly available. Target time-to-first-word:
   - 2-3 secs (web), 
   - 3-5 secs (phone)
 
Ways to solve the "fast start challenge":

  - percentage-based warm pool
  - fast startup times (caching, pre-loading)
  - proactive/predictive scheduling
  - fallbacks from reactive world (eg. UX based solutions, not just silent fails)

Infra providers:

  - need to support tcp and udp
  - voice ai providers are easiest (Pipecat Cloud, Daily, Vapi, Layercode)
  - Fly.io (and potentially other container platforms) are good if they support udp (Fly does)
  - ML focused provides are good for converged bots with larger models included (gpu clouds)
  - hyperscalers are flexible but complex
  - BTW: CloudRun does not support udp
  - demos can run on single VMs or even be served from a home lab
  - by serving everything converged, time-to-first word can get down to 500ms
  - otherwise 800-1000 ms is good enough and achievable
  - proximity to users matters (Daily plans global regions for PipeCat cloud, currently only us-west)
  - conn between servers can be implemented with WebSockets

After the session I have looked at the PipeCat examples and realized it should be easy enough to run a basic voice agent with PipeCat's [SmallWebRTCTransport](https://docs.pipecat.ai/server/services/transport/small-webrt) on a virtual server hosted in Europe and then switch the transport and deploy it to production on PipeCat Cloud.

I will probably try that to see if the US based PipeCat cloud is fast enough for users in Europe and how much of a difference the longer network round trip time makes.
