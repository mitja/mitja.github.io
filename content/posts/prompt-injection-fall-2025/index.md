---
title: "State of Prompt Injection (Fall 2025)"
categories: ["AI Engineering","Blog",]
tags: []
#externalUrl: ""
#showSummary: true
date: 2025-11-03
draft: true
slug: prompt-injection-fall-2025
---

As an AI Engineer and long-term fan and follower of Simon Willison, I watch prompt injection quite closely. Despite many efforts and advances in the industry, prompt injection is not yet solved and it's still undecided if it can be completely solved, at all.

This post is an overview of the latest developments and papers in prompt engineering as of fall 2025.

<!-- more -->

## What is Prompt Injection?

- term coined by Simon in ..., inspired by SQL injection, catches the new aspect extremely well: Attacks via the prompt to the llm. 
- thanks to the nature of Gen AI turned out extremely hard to mitigate.
- Despite best efforts of top labs to keep system prompts private, they have been exposed.
- can do
  - exfilration (system prompts, private data, secrets)
  - perform harmful actions
  - ...

## A short history

- xx
- Anhtropic now publishes system prompts
- ...

## The state of prompt injection Fall 2025

Two new papers, and recent security incidents.

### Acknowledge of the trifecta

### A quantitative study

### In the wild

- context injectection - any context can be dangerous. eg. supply chain attacks.
- 

## What to do about it?

- be careful, it's a thing and it's being exploited, if you always have guards down it's probably more a question of when not if it will hit you.
- push each circle of the venn diagram outside:
  - trustworthy users and other context sources, vet sources
  - limited actions and communication
  - limited access to sensitive data
- not perfect, tedious, but better than nothing and in many cases actually quite good, I assume
- up next: maybe I'll look into some of the advanced techniques discussed in the paper. Even them are not secure as the paper showed, but as an additional layer on top of the venn-pushing, it's "defense in dept" and probably right now the best we can do to prevent, detect or contain impacts of prompt injection attacks.

https://simonwillison.net/2025/Nov/2/new-prompt-injection-papers/