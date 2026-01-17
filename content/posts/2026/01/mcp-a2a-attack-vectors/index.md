---
author: null
date: 2026-01-14
draft: false
slug: mcp-a2a-attack-vectors
title: MCP and A2A Attack Vectors for AI Agents
stream: false
---

Christian Posta from Solo.io has written an interesting [Deep Dive into MCP and A2A Attack Vectors for AI Agents](https://www.solo.io/blog/deep-dive-mcp-and-a2a-attack-vectors-for-ai-agents).

Here is a shortlist. There are certainly more attack vectors, and the mitigations are a start, but certainly not perfect.

| Attack Vector | How it works | Mitigation |
|---------------|--------------|------------|
| Naming Attacks | Attackers create look-alike names or typosquatted services that trick the AI into picking a malicious resource instead of the legitimate one | Enforce unique identities, cryptographically verify server/agent identities, and use a trusted registry rather than blind name matching |
| Context Poisoning / Indirect Prompt Injection | An attacker embeds hidden instructions in context that steer the model to do harmful actions or leak data; in A2A this can happen via malicious task states or malformed skill descriptions | Sanitize and vet descriptions, use strict schema constraints, and limit or filter natural-language metadata that models see |
| Shadowing Attacks | A malicious service shadows a legitimate tool or agent by registering something that alters how other trusted components behave (e.g., injecting hidden guidance that changes billing logic or influences other agents' outputs) | Require authentication and authorization for every component, use whitelists, and ensure that tools/agents don't get used solely based on unverified contextual presence |
| Rug Pulls | An attacker initially builds trust by providing a useful tool or agent, but once widely adopted, subtly changes its behavior to perform harmful operations, manipulate outputs, or exfiltrate data | Continuous monitoring, evaluate behavioral changes over time, use policy controls and version gating so tools can't suddenly change semantics without review |

AI agents use protocols like MCP (Model Context Protocol) and A2A (Agent-to-Agent) and decide when and how to call tools or other agents. They do this dynamic discovery and usage based on natural language context which makes them susceptible to semantic manipulation.