---
title: "Task-specific LLMs - are they worthwile?"
summary: "Is it worthwhile to hand-craft docs for context."
date: 2025-10-14
categories: ["AI Engineering", "Blog"]
tags: ["Claude", "Devcontainer"]
draft: true
---

Hypothesis: 

- Tasks-specific llms-ctx improve agentic coding (faster, fewer tokens, better results). 
- Improving an initial prompt based on error-analysis results lead to even better outcomes.
- combining with skaffold and tools further boosts productivity

approach:

- create interactive, improve fix, until satisfied
- use the whole contexts to ask for a llms txt that summarizes.
- optionally/additionally: ask to create a scaffold and tools
- do error analysis on this, fix


- Relevance: 
  - hand-crafted already valuable but limited to very common use cases due to the manual effort, 
  - an indicator that auto-crafted could help, too with much wider applicability
  - single lib, multi-lib

- Air is new, rel. unknown for the models
- with haiku (costs)
- use case: crudl app
- approaches:
  - 1. air-llms.txt
  - 2. air-llms-full.txt
  - 3. air-llms-crudl-initial.txt
  - 4. air-llms-crudl-improved.txt
- testbed: 
  - claude-code repo (basically empty)
  - air with uv sqlmodel foundation prepared (setting up, migrations outofscope, i know directions would be beneficial)
  - in devcontainers
- test data:
  - 100 tasks
  - 30 for initial error analysis on 1-3, 15 common, 15 unique (5 each) (=15*3+5*3=60 traces)
  - 70 for evaluation (240 traces)
  - also improve eval prompts based on common errors?
- cost estimation (conservative, for budgeting):
  - 300 traces
    - 2/3 input = 300 * 2/3 * 0,2 Mtokens * 1 USD/Mtokens = 40 USD
    - 1/3 output = 300 * 1/3 * 0,2 Mtokens * 5 USD/Mtokens = 100 USD
  - output maybe vastly overestimated, caching might improve input costs but hard to estimate
- process
  - hand-craft an initial crudl llms.txt (with help?)
  - instructions (create a crudl app... / at the end create tests if it works)
  - run unattended on a set of tasks (generated with chatgpt, some same, some unique)
  - error analysis and improvement
  - run unattended on a different set of tasks
  - check the apps, document flaws/errors
- compare, metrics
  - does it work, yes/no
  - how does it look? video?
  - how much context? costs?
  - how much wall-clock time?
  - how many turns?
  - how many flaws/errors remain
- prompt structure (Cache-friendly)
  - additional generic instructions (ie. CLAUDE.md)?
  - llms file
  - specific instruction
  - available tools etc:
    - search in docs (cached)
    - start stop logs of server

- next:
  - agent-crafted
    - ask to collect
    - maybe better: do the task, collect what was needed