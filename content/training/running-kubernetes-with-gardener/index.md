---
title: "Running Kubernetes with Gardener"
slug: "running-kubernetes-with-gardener"
weight: 40
kicker: "Training"
subtitle: "Day two for small teams"
status: "Planned"
format: "3 weeks, about 20 h live"
teaser: "Operate the clusters Gardener hands you: restore backups, watch upgrades, wire an app with ingress, TLS, storage and alerting, run a game day, and write your own runbook."
summary: "A live online course on operating Kubernetes clusters that Gardener hands you: backups you have restored, upgrades you have watched, an app that survived a game day, and a runbook you wrote yourself."
layout: "training"
facts:
  - label: "Who it is for"
    text: "Small teams (2–5 engineers) and solo founders who want their own clusters for their applications and have no platform team. You have used `kubectl`; you have never run a control plane."
  - label: "Who it is not for"
    text: "People who want Kubernetes basics, people who need an SLA and someone to call, and people building a Gardener landscape for many teams."
  - label: "Format"
    text: "3 weeks. Per week: two live sessions of 2 h, one lab walkthrough of 90 min, one optional office hour of 60 min. About 20 contact hours. 8–12 participants."
  - label: "Where the work happens"
    text: "A browser workspace (Educates) and a Gardener landscape of your own, with names under `<you>.paasbox.app`. No token touches your laptop."
  - label: "You bring"
    text: "A browser, some `kubectl` experience, and an application of your own (a container image and a few manifests), or use ours."
  - label: "You walk out with"
    text: "A runbook for your cluster with every command you ran; three restores (shoot etcd, landscape in place, landscape from nothing); one upgrade you watched; an app on a shoot with ingress, TLS, storage and alerting; a game-day record; a production-readiness checklist; an answer to \"solo or HA, and when\"."
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

- **Week 0** — setup, self-paced, about 1.5 h
- **Week 1 — What you own now, and how you get it back:** the landscape you were handed; recovery, before anything else (you delete your landscape's server and bring it back from the S3 snapshot)
- **Week 2 — Change without fear:** upgrades and nodes; your application, properly wired
- **Week 3 — Seeing, being told, the day it breaks:** observability and alerting; game day, security, cost, and the decision between solo and HA
