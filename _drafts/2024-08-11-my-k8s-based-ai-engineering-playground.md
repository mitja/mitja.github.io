---
title: My Kubernetes Based AI App Launchpad
author: mitja
date: 2022-08-11
category: Building AI Apps
tags: [Kubernetes, AI Engineering, Rancher, k3s]
#pin: true
#math: true
#mermaid: true
render_with_liquid: false
permalink: /blog/2024/10/11/my-k8s-based-ai-engineering-playground/
#image:
#  path: /assets/img/featured-excel-q1-2022.png
#  alt: What is new in Excel in Q1 2022
---

A playground is something that invites playing and trying out new things.

For me, a playground for AI engineering has a launchpad that

- lets me quickly launch new apps, 
- lets me use diverse technologies (databases, caches, app frameworks),
- keeps costs low and predictable,
- is reasonably secure,
- has basic operations best practice in place (CI/CD, IaC, observability, backups),
- can scale up when needed.

After trying different self-hosted and PaaS options, I have settled on a Kubernetes-based solution. Here is some of the rationale behind it:

| Criteria | k8s | k8s+Knative | PaaS | Docker Compose | Dokku, etc. |
| --- | --- | --- | --- | --- | --- |
| **Quick Launch** | ok after initial setup | very good | best | ok | very good |
| **Diverse Technologies** | yes | yes | expensive | more effort | has limits |
| **Costs** | ok | higher | very high | low | low |
| **Security** | ok | ok | very good | lower than k8s | lower than k8s |
| **Operations** | very good after initial setup | same as k8s | very good | harder to do than with k8s | good start but has limits |
| **Scalability** | very good | very good | very good | ok | ok |

I eliminated PaaS offerings, and k8s+Knative because of the costs. A single app is ok, but if you want to run more, and if you want to use other services like Redis, and DBs, things get expensive, quickly. 

I eliminated Docker Compose and Dokku because of the limits in terms of which technologies I can easily use, operations and scalability. Granted: You can run everything you can run in k8s also in Docker Compose or Dokku, and a single server can go quite far, but beyond basic apps, it's more effort. With k8s you get many great Operators and Helm charts that simplify managing many components.

I run my k8s cluster on Hetzner Cloud with a small three-node k3s cluster setup by [Kube-Hetzner](https://github.com/kube-hetzner). The infrastructure is managed with Terraform, the OS and k3s are updated automatically without interrupting the services. Here is the complete "bill of material":

- 3x CPX31 instances (4vCPU, 8GB RAM, 160 GB NVMe, AMD), 3x 16.18 EUR/Month
- 1x CPX21 instance (3vCPU, 4GB RAM, 80 TB NVMe, AMD), Storage 8.39 EUR/Month + 1.68 EUR for Backup
- 1x Loadbalancer LB11 (6.41 EUR/Month)
- Volumes as needed (min. 10 GB each, at 0.0524 EUR/GB/Month)

In total, my playground costs me about 64 EUR/Month (including VAT).

There are two storage classes in the cluster:

- local-path: for fast storage
- hcloud-volumes: for persistent block storage (RWO)

I am not yet settled on an RWX storage: I am currently contemplating two options:

- zfs-generic-nfs: for shared storage (RWX) served by the separate [Hetzner Cloud VM with Debian and ZFS](https://github.com/terem42/zfs-hetzner-vm) and NFS with [democratic-csi](https://github.com/democratic-csi/democratic-csi) as the CSI driver.
- Longhorn: this takes more resources, is slower, and [more complex](https://open200.com/de/blog/surviving-cloud-outage-kubernetes-longhorn-database/) but highly available, and easier to setup and use. Here are some benchmarks and [Longhorn best pracices on Hetzner Cloud](https://gist.github.com/ifeulner/d311b2868f6c00e649f33a72166c2e5b)

I use Rancher for it's nice admin console, and pre-configured solutions for observability. My Rancher runs on a separate single-node k3s cluster on an Intel NUC in my basement.

I have a wildcard domain pointing to the loadbalancer of the k3s cluster. This way, I can quickly launch new apps with a subdomain without buying new domains. For custom domains, I use the external-dns operator with my DNS providers.

My application stack usually looks like this:

- Python FastAPI or Django for the backend with static html and htmx for the frontend.
- Or just a Gradio, Streamlit, or fasthtml app.
- PostgreSQL or SQLite for the database.
- Redis for caching and message queue.

PostgreSQL and Redis run with an Operator so that I create new databases and caches with a few short manifests. I use the [PostgreSQL Operator from Zalando](https://postgres-operator.readthedocs.io/en/latest/), and the [Redis Operator from Spotahome](https://github.com/spotahome/redis-operator).

For apps, I use KNative. With it, I can deploy Apps as functions, or as Serverless containers - again with very brief manifests. 

To simplify the process further, I created a Cookiecutter template to kickstart a new app.

TODO: Describe process of launching a new app, end-to-end.

If an app gets traction, I can launch a K8s cluster on a hyperscaler and deploy it there.

My launchpad is constantly evolving, and I have it only running since a few days, but it seems to give me the **fast time from idea to URL** I was looking for at comparably low and predictable costs and relatively low operation effort.

I will write a follow-up after some months to tell you how it turned out in practice. If you want to learn more about the setup, let me know.
