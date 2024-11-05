---
title: "ChatGPT Can Use Information from Internal Sites"
author: mitja
date: 2024-11-05
category: Working with AI
tags: [ChatGPT, Caddy, Cloudflare Tunnel]
#pin: true
#math: true
#mermaid: true
render_with_liquid: false
permalink: /blog/2024/11/05/chatgpt-can-use-information-from-internal-sites/
image:
  path: /assets/blog/2024/chatgpt-local-sites.png
  alt: The ChatGPT Search User Experience.
---
The new ChatGPT Search feature, which is meant to ["get fast, timely answers with links to relevant web sources"](https://openai.com/index/introducing-chatgpt-search/) apparently can use information from internal sites, too. 

A first hint was given by Simon Willison when he tweeted that [ChatGPT can use the location (presumably from the IP address) to provide more relevant answers](https://x.com/MitjaMartini/status/1853481953653141588).

I got curious, tried it myself and saw that ChatGPT also knows the ISP (via a What's my IP service) which led to the assumption that ChatGPT doesn't search the internet from the server side, but from the client side.

To find out if that's true, I setup a litte website with Caddy that serves different content on a public domain name depending on where the client is coming from. For this, I used [Caddy's client_ip matcher](https://caddyserver.com/docs/modules/http.matchers.client_ip) and a [Cloudflare Tunnel](https://www.cloudflare.com/de-de/products/tunnel/). As soon as I added entries for the domain in `/etc/hosts` to resolve the domain without going over the internet, ChatGPT saw the internal content. When I removed the entries, ChatGPT saw the external content.

I think this was not intentional, as it's also not documented by OpenAI. Even though it's also a potential security risk, I tend to like it, as I now can use private information in ChatGPT even if I haven't explicitely upload it. I just need to serve it locally and tell ChatGPT where to find it.
