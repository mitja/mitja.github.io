---
title: "Pipecat Cloud Latency for EU Users"
summary: "Pipecat Cloud is located in the US. Is its latency ok for voice agents for EU Users."
categories: ["AI Engineering","Blog",]
tags: ["PipeCat","Daily.co","WebRTC", "Latency"]
#externalUrl: ""
#showSummary: true
date: 2025-05-11
draft: false
aliases: ["/blog/pipecat-cloud-latency-for-eu-users/",]
---

[Pipecat Cloud](https://www.daily.co/products/pipecat-cloud/) is the easiest way to run a [Pipecat](https://github.com/pipecat-ai/pipecat)-backed voice agent in production. 

I've heard in the Voice Agents course that Daily.co, the company behind Pipecat Cloud, currently has only US regions and wondered if Pipecat Cloud is already fast enough for users in the EU. 

At first, I planned to compare Pipecat Cloud with a VM based deployment hosted in Germany, but I skipped the comparison after testing the [pipecat-cloud-simple-chatbot](https://github.com/daily-co/pipecat-cloud-simple-chatbot) on Pipecat cloud. 

It's fast enough:

- about 10s startup time, but that was a cold start. Needs to be mitigated with information to the user, but acceptable.
- first bot reply took about 1200 ms, but every reply after that took less than 1000 ms, often around 800 ms which is exactly the realistic recommended range. 
- The numbers are from log timestamps of the client app, but match my experience. The conversation felt natural to me.

For reference: The bot uses a Cartesia voice, and OpenAI GPT-4o. In summary, I'm happy with the performance so far and will move on to building an own Voice Agent bot.
