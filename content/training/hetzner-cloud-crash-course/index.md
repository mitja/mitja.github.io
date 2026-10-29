---
title: "Hetzner Cloud crash course"
slug: "hetzner-cloud-crash-course"
weight: 10
kicker: "Training"
subtitle: "CLI, Terraform, Python"
status: "Pilot"
format: "3 × 2 h live + 3 h homework"
teaser: "Operate Hetzner Cloud the three ways teams actually do it: the hcloud CLI, Terraform, and Python scripts — against a live mockup of the Hetzner Cloud API with real virtual machines."
summary: "A crash course in operating Hetzner Cloud with the hcloud CLI, Terraform with the hcloud provider, and Python scripts with hcloud-python. Each participant gets a cloud project in a live mockup of the Hetzner Cloud API that runs real virtual machines."
layout: "training"
facts:
  - label: "Who it is for"
    text: "Developers and admins who deploy or will deploy on Hetzner Cloud; teams moving from clicking in the Console to code; people who know a shell and a little Python."
  - label: "Who it is not for"
    text: "People who want Kubernetes on Hetzner, or who already run Terraform against Hetzner in production."
  - label: "Format"
    text: "3 live sessions of 2 h (one day or three evenings), plus one homework workshop of about 3 h, self-paced. Up to 12 participants."
  - label: "Where the work happens"
    text: "A browser workspace (Educates) with `hcloud`, `terraform` and `uv` installed. Each session is its own project in the course cloud, with quotas, deleted when the session ends."
  - label: "Stack"
    text: "hcloud CLI 1.68, Terraform 1.16 with `hetznercloud/hcloud` 1.69, hcloud-python 2.24, cloud-init."
  - label: "You bring"
    text: "A browser."
  - label: "You walk out with"
    text: "A web setup (servers from cloud-init, private network, firewall, volume, floating IP, HTTPS load balancer) built three ways; a Terraform configuration you can point at a real project by changing two names; scripts for inventory, health and rolling rebuilds; the error codes and limits that matter."
  - label: "Price"
    text: "Free during the pilot, limited seats."
showDate: false
showReadingTime: false
showWordCount: false
showTableOfContents: false
showPagination: false
sharingLinks: false
---

## Sessions

- **Session 1 — the hcloud CLI** (2 h)
- **Session 2 — Terraform** (2 h)
- **Session 3 — Python** (2 h): the web servers are rebuilt one by one while the load balancer keeps answering, and afterwards `terraform plan` shows no drift
- **Homework — a small app like in a real cloud** (about 3 h)
