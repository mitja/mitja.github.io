---
title: "AI agents in operations"
slug: "ai-agents-in-operations"
weight: 70
kicker: "Training"
subtitle: "Let an agent diagnose and act, within guardrails"
status: "In preparation"
format: "2 weeks, about 12 h live"
teaser: "Let AI agents help operate self-hosted apps: what an agent may read and what that leaks, typed actions with approvals, restore drills and updates with rollback run by an agent, and measuring an agent before trusting it."
summary: "A live online course on letting AI agents help operate self-hosted apps: what an agent may read and what that leaks, what it may do and who approves it, how a restore drill and an update with rollback look when an agent runs them, and how to measure an agent before trusting it."
layout: "training"
facts:
  - label: "Who it is for"
    text: "Teams that run self-hosted apps for themselves or for clients and are asked whether an agent may help run them: agencies with many small installs, Mittelstand IT, platform teams of two to five. You have used `kubectl` and a coding agent, and you have been on call for an app."
  - label: "Who it is not for"
    text: "People who want Kubernetes or agent basics, people who want to build with agents (that is *Building an AI Software Factory*), and people who want someone to operate their production."
  - label: "Format"
    text: "2 weeks: 4 live sessions of 3 h, a self-paced week 0 of about 2 h, an optional office hour per week. About 12 contact hours. Up to 10 participants."
  - label: "Where the work happens"
    text: "A demo deployment in your own Hetzner test project: a single-node k3s cluster with backups and observability, Forgejo and Umami, and the agent tooling in lab mode. Each lab day starts from a fresh demo and ends with its deletion."
  - label: "You bring"
    text: "A laptop, an empty Hetzner Cloud test project with a token (about €4–6 of Hetzner costs for the fortnight), the coding agent you already use, an API key with a spend limit."
  - label: "You walk out with"
    text: "A read policy for your agent; an approval table for your apps; an action you wrote and saw refused, approved and audited; a restore-drill record and an update record with its rollback; an eval for your own operations task with its cost per run; a decision sheet for your own shop."
  - label: "Price"
    text: "Not fixed yet."
showDate: false
showReadingTime: false
showWordCount: false
showTableOfContents: false
showPagination: false
sharingLinks: false
---

## Sessions

- **Week 0** — setup, self-paced, about 2 h
- **Session 1 — Reading:** the same diagnosis twice, once with a direct kubeconfig and once through a read proxy, and what leaked
- **Session 2 — Acting:** typed actions, danger flags, approvals and audit
- **Session 3 — Restore and update:** a restore drill and an update with rollback, run by an agent
- **Session 4 — Measuring:** an eval for an operations task, several runs, two models, cost per run
