---
title: "Using Galene as a lightweight WebRTC server for Voice Agents"
date: 2025-10-14
categories: ["AI Engineering", "Blog"]
tags: ["Claude", "Devcontainer"]
draft: true
---
[Galene](https://galene.org) is a lightweight WebRTC server written in Go. It supports voice and video, has a built-in client, runs on linux amd64, arm64, mips, macos and windows and is used in production at Université de Paris and Sorbonne Université. It has a simple Admin UI and REST API for managing groups and users.

It's built for multi-user sessions, but can be repurposed for 1-1 agent-user sessions.

- sample python auth server (and LDAP integration)
- buit-in turn server
- js client (for a/v videoconf)
- android client (audio only, with screensharing support)
- resource req. for 1-many (linear, 300 participants per core), many-to-many (quadratic 20 part/conf 1 core 40)
- interesting: how many for 1-1? (assume closer to linear, limiting factor: bandwidth?

<!-- more -->

- https://github.com/jech/galene
- https://galene.org

- awesome-webrtc: see also https://github.com/nuzulul/awesome-webrtc

- https://github.com/meetecho/janus-gateway
- https://janus.conf.meetecho.com/demos/echotest.html

