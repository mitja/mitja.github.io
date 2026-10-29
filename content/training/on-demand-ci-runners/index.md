---
title: "On-demand CI runners"
slug: "on-demand-ci-runners"
weight: 20
kicker: "Training"
subtitle: "A runner per job, and a bill that stops"
status: "Pilot"
format: "3 × 2 h live + 3 h homework, or on demand"
teaser: "Run Forgejo CI runners that exist only while a job needs them: a server per waiting job, a single-use registration per attempt, and deletion before the next paid period starts."
summary: "How to run CI runners that exist only while a job needs them: a pool per label set, a server created for waiting jobs, one single-use runner registration per job attempt, and deletion before the next paid period starts."
layout: "training"
facts:
  - label: "Who it is for"
    text: "Teams running Forgejo (or moving to it) whose CI is a handful of always-on VMs; platform people who pay for idle runners; anyone who has pasted a runner registration token into a VM and never rotated it."
  - label: "Who it is not for"
    text: "People who want a managed CI product, or who run one job a week (a single small VM is cheaper — the course says so)."
  - label: "Format"
    text: "3 live sessions of 2 h (one day or three evenings), plus one homework workshop of about 3 h — or the same four workshops on demand, self-service."
  - label: "Where the work happens"
    text: "A browser workspace (Educates) with a Forgejo of your own, forgejo-fleet, `hcloud` and `jq`. Each session is its own project in the course cloud, deleted when the session ends."
  - label: "Stack"
    text: "[forgejo-fleet](https://git.paasbox.com/mitja/forgejo-fleet) v0.1.0, Forgejo 15 with Actions, forgejo-runner 13.2, a live mockup of the Hetzner Cloud API."
  - label: "You bring"
    text: "A browser."
  - label: "You walk out with"
    text: "A pool configuration you can point at a real project by changing two names, a runner image built with Packer, a cost model for your own job mix, a runbook for the five failures that actually happen, and an untrusted pool for fork pull requests."
  - label: "Price"
    text: "Free."
showDate: false
showReadingTime: false
showWordCount: false
showTableOfContents: false
showPagination: false
sharingLinks: false
---

## Sessions

- **Session 1 — A job, a server, a lease** (2 h)
- **Session 2 — Pools that cost what they should** (2 h)
- **Session 3 — Trust, failure and operations** (2 h): the orchestrator is killed while a job runs; the job finishes and the server is still deleted at the right minute
- **Homework — Your fleet** (about 3 h, self-paced)
