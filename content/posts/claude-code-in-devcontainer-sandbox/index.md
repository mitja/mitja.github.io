---
title: How to run Claude Code in a Devcontainer Sandbox
summary: "How to limit what Claude Code can do and see on your machine."
date: 2025-10-15
categories: 
  - AI Assisted Coding
  - Blog
tags: 
  - Claude
  - Devcontainer
---

Letting Claude Code run unattened on a personal computer can be quite scary. With [Development Containers](https://containers.dev) or just "devcontainer" you can put Claude Code in a sandbox on your local machine so you don't need to worry as much.

A good foundation to set this up is Anthropic's own [claude-code](https://github.com/anthropics/claude-code) repoaitory. The configuration is in `.devcontainer` and provides following security features:

## 1. Container Isolation

Claude code runs in a Docker container (or on GitHub Codespaces, but I haven't tried this).

## 2. Network Firewall

The firewall script `.devcontainer/init-firewall.sh` restricts network access to only approved destinations:

- Allowed: GitHub, Anthropic API, npm registry, statsig, sentry (check the )
- Blocked: Everything else (including random internet sites)
- Verification to ensure the firewall is working

You can customize this. For example, I've added the following line to prevent connections back to VS Code. Without this, Claude Code can still access the files you have open in VS Code, even if they were outside of the devcontainer.

```bash
# Block outbound connections on port 59778 so that claude code can't connect to vscode
# iptables -A OUTPUT -p udp --dport 59778 -j DROP
```

I mostly did this because Claude Code often got confused when there were files open it cannot find in the repo. I don't know if this is still the case.

## 3. Limited File Access

Claude Code can only read/write in specific directories:

- Your workspace folder (read-write)
- Command history and config (volumes)

Your home directory is NOT mounted - Claude Code cannot access your personal files.

## 4. Non-root User

It runs as the `node` user with limited privileges.

## 5. Limited bash commands (optionally)

There is also a `bash_command_validator_example.sh` which is a Claude Code PreToolUse hook for the bash tool that "validates bash commands a set of rules before execution". 

You can use this to limit which bash commands Claude Code can run in your sandbox.

## How to Use It

Clone the repo and open it in VS code. It should immediatly try to open the devcontainer workspace in a Docker container. Docker Desktop or something similar is required, of course.

If it does not open, you can select `> Dev Containers: Reopen in Container` from the VS Code command palette.

Startup will take some time. When it's done, you can open a terminal in vs code and run `claude`.

Claude Code can now only

- Access files in /workspace (your project)
- Make network requests to whitelisted domains
- Execute commands within the container

Your personal files, documents, SSH keys from your host machine, browser data, etc., are all
inaccessible to Claude Code running in this container. But:

- Claude Code can still access/modify any files in your mounted workspace, this includes `.env` files
- Git credentials inside the container may allow pushing to repos
- The container shares the Docker daemon if Docker-in-Docker (or Kubernetes-in-Docker) is enabled. This surprised me a bit when I wanted to run an app in a KinD cluster in a devcontainer.

Happy (secure) vibe coding and stay safe.