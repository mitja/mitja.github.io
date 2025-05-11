---
title: "PipeCat Cloud Latency for EU Users"
author: mitja
date: 2025-05-11
category: Voice Agents
tags: [PipeCat, PipeCat Cloud, Daily.co, WebRTC, Latency]
#pin: true
#math: true
#mermaid: true
render_with_liquid: false
permalink: /blog/pipecat-cloud-latency-for-eu-users/
image:
  path: /assets/blog/2025/pipecat-cloud-latency-for-eu-users.jpg
  alt: An AI generated image of an old and incorrect map of the world with an arrow pointing from America to Europe.
---

[Pipecat cloud](https://www.daily.co/products/pipecat-cloud/) is the easiest way to run a [PipeCat](https://github.com/pipecat-ai/pipecat) driven voice agent in production. 

I've heard in the Voice Agents course that Daily.co, the company behind PipeCat Cloud, currently only have regions in the US and wondered if PipeCat Cloud is already fast enough for users in the EU. 

At first, I planned to compare PipeCat Cloud with a VM based deployment hosted in Germany, but I skipped the comparison after and testing the [pipecat-cloud-simple-chatbot](https://github.com/daily-co/pipecat-cloud-simple-chatbot) on PipeCat cloud. 

It's fast enough:

- about 10s startup time, but that was a cold start. Needs to be mitigated with information to the user, but acceptable.
- first bot reply took about 1200 ms, but every reply after that took less than 1000 ms, often around 800 ms which is exactly the realistic recommended range. 
- The numbers are from log timestamps of the client app, but match my experience. The conversation felt natural to me.

For reference: The bot uses a Cartesia voice, and OpenAI GPT-4o. In summary, I'm happy with the performance so far and will move on to building an own Voice Agent bot.
