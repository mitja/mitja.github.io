---
title: "Using VMware Workstation Pro and VMware Fusion for Labs"
author: mitja
date: 2024-11-01
category: Homelab
tags: [VMware, OpenShift, NetApp, Ubuntu, Bitnami]
#pin: true
#math: true
#mermaid: true
render_with_liquid: false
permalink: /blog/2024/10/22/using-vmware-workstation-and-fusion-for-labs/
image:
  path: /assets/blog/2024/dokku-ssh-alias.png
  alt: A Dokku command before and after applying this tip.
---

In May 2024, VMware made VMware Workstation Pro for Windows and VMware Fusion for MacOS free for personal use. Downloading it is a bit tricky, but a post by Mike Roy about [Downloading VMware Fusion and Workstation Free for Personal Use](https://www.mikeroysoft.com/post/download-fusion-ws/) got me on the right track. 

I need the home lab for my work and my side projects. For work, I like to have an OpenShift cluster, and Rancher to get quick hands-on experience with Kubernetes. For my side projects, I like to have a linux desktop, a Dokku server and the occasional, Linux VM and [Bitnami Appliance](https://bitnami.com/stacks/virtual-machine).


But that they're free is not the reason I'm using it for my labs. The main reasons are the broad support and the ease of use.

## Windows 11

## Ubuntu 24.04 Desktop

## OpenShift

## K3s Kubernetes

## Rancher

## Talos

## NetApp Virtual OnTap

## Linux with Cloud-Init

## Firewall

## Dokku

## Bitnami Virtual Appliances

There are many pre-built images and descriptions available. Some are even only supported on VMware like NetApp Virtual OnTap. Some of the best how-tos use VMware desktop products, for example [Run Windows 11 on Mac w/ free VMware Fusion Pro license](https://www.youtube.com/watch?v=LWXO4DhQRL0) by 9to5Mac, and [OpenShift on VMware Workstation](https://www.youtube.com/watch?v=RhLvWVDgyS4) by ANA Technology Partner. All common operating systems provide cloud images compatible with VMware, like [Ubuntu 24.04](https://cloud-images.ubuntu.com/noble/20241004/). Finally, there are many great Open Virtualization Appliances (OVA) by Bitnami ("by VMware"). [Bitnami Virtual Machines](https://bitnami.com/stacks/virtual-machine) are often the easiest way to get a local lab up and running.

My main virtualization host will be my Windows 11 desktop as it has the most resources of my systems. Still, I'll also use VMware Fusion on my MacBook to have small labs available on the go, too.

When you are used to cloud environments, you might miss cloud-init. A workaround is to get the qcow2 formatted cloud images (which usually have cloud-init installed), convert them to vmdk, create a cloud-init iso and attach it to the vm. Tom Bosmans has a great post called [cloud-init in VMware Workstation](https://www.gwbasics.be/2023/04/cloud-init.html) that describes how to do it.