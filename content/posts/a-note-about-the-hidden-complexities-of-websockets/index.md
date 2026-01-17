---
title: "A note on the hidden complexities of WebSockets"
date: 2025-01-25
categories: ["AI Engineering", "Blog"]
tags: ["websockets", "realtime"]
aliases: [
  "/blog/a-note-about-the-hidden-complexities-of-websockets/", 
]
stream: true
---

AI Apps are often expected to be realtime. On the web, realtime communication can be implemented with WebSockets. I've started with WebSockets to create chatbots and other live-updated interfaces, but then switched to SSE and now mostly follow these rules of thumbs: 

* Use WebSockets for server-to-server communication.
* Use SSE for server-to-client communication.
* If you still want or need to use WebSockets for server-to-client communication, add a fallback to SSE.
* If you need realtime voice/video server-to-client communication, use WebRTC.

<!-- more -->

If you still want or need to build a websocket service, please read Atul Jalan's blog post about [The Hidden Complexity of Scaling WebSockets](https://composehq.com/blog/scaling-websockets-1-23-25). It's a quick read and captures important lessons to keep in mind when working with WebSockets. 

All of his lessons are important, even when working not at scale. Here is a quick summary:

- Downtimeless deployments are much more involved than in HTTP services.
- Establish a good message schema, eg. 2 byte prefixes and single character field delimiters.
- Use heartbeats to detect dead connections - both ways.
- Have an http fallback as WebSockets are often blocked. Usually: Server sent events (SSE) for server to client communication and simple requests for client to server.
- More, like standard tooling (rate limiting, validation, error handling), no caching at the edge, per-message authentication.

Standard framworks like Django, FastHTML, and Quart (an async Flask clone) have good basic support for WebSockets, but don't really help dealing with their hidden complexities. I hope, frameworks will level up a bit, as this is mostly "undifferentiated heavy lifting".