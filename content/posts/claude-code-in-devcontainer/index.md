---
title: "Claude Code in Devcontainers"
date: 2025-10-14
categories: ["AI Engineering", "Blog"]
tags: ["Claude", "Devcontainer"]
draft: false
---

[Development Containers](https://containers.dev) or just "devcontainers" add a layer of security, simplify developer onboarding enables developing in parallel with isolated environments. 

For me, Devcontainers are a great addition to an AI Engineer's toolbox, even though I don't use them day-to-day.

I have setup Devcontainers with Claude Code using VS Code and the devcontainers cli, adapted it to a Python FastAPI based project, and documented it in this article.
<!--more-->

## Claude Code in Devcontainers with VS Code

A good way to get started with Claude Code in a Devcontainer is Anthropic's own [claude-code](https://github.com/anthropics/claude-code) repository. 

Clone the [anthropics/claude-code](https://github.com/anthropics/claude-code) repository and open it in VS Code. It should immediately try to open the devcontainer workspace in a Docker container, if Docker Desktop or something similar is running on your machine.

If it does not open, you can start it with `> Dev Containers: Reopen in Container` from the VS Code command palette.

The first startup will take some time. When it's done, you can open a terminal in vs code and run `claude`.

## Claude Code in Devcontainers with a cli

The Devcontainers project provides the [devcontainers/cli](https://github.com/devcontainers/cli) as a reference implementation. With this, you can start Devcontainers from the terminal without VS Code. To try this, you can again use your clone of the [anthropics/claude-code](https://github.com/anthropics/claude-code) repository.

Install the cli on your local machine:

```sh
npm install -g @devcontainers/cli
```

Run a devcontainer:

```sh
devcontainer up --workspace-folder a-folder-with-a-.devcontainers
```

Run claude code inside the container:

```sh
devcontainer exec --workspace-folder claude
```

Or (even better): Run a shell inside the container from your favorite terminal emulator (Ghostty works great) and then start claude in this terminal session. `claude-code` comes with zsh:

```sh
devcontainer exec --workspace-folder zsh
```

You can also use tmux to disconnect and later reconnect.

To stop, exit Claude, exit the shell and stop or stop and delete the container. Unfortunately, there is no subcommand for this, yet. I just manually deleted unused devcontainers with Docker Desktop or the docker cli:

```sh
docker ps # find the container id you want to delete
docker stop the-id 
docker rm the-id
```

## Security Features

The configuration in `.devcontainer` provides several security features:

### Container Isolation

Claude code runs in a Docker container (or on GitHub Codespaces, but I haven't tried this).

### Network Firewall

The firewall script `.devcontainer/init-firewall.sh` restricts network access to only approved destinations:

- Allowed: GitHub, Anthropic API, npm registry, statsig, sentry
- Blocked: Everything else (including random internet sites)

You can customize this. For example, I've added the following line to prevent connections back to VS Code. Without this, Claude Code can still access the files you have open in VS Code, even if they were outside of the devcontainer.

```bash
# Block outbound connections on port 59778 so that claude code can't connect to vscode
# iptables -A OUTPUT -p udp --dport 59778 -j DROP
```

I mostly did this because Claude Code can get confused when there are files open it cannot find in the repo and because I get confused when Claude Code opens files in VS Code even if I want to work on something else.

### Limited File Access

Claude Code can only read/write in specific directories:

- Your workspace folder (read-write) (see `workspaceMount` in `devcontainer.json`)
- Command history and config (volumes) (see `mounts` in `devcontainer.json`)

Your home directory is NOT mounted - Claude Code cannot access your personal files.

### Non-root User

Commands in the container run under the `node` user with limited privileges.

### Limited bash commands (optionally)

There is also a `bash_command_validator_example.sh` which is a "Claude Code [PreToolUse hook](https://docs.claude.com/en/docs/claude-code/hooks#pretooluse)" for the bash tool that "validates bash commands a set of rules before execution". 

You can use this to limit which bash commands Claude Code can run in your sandbox.


## Adapting devcontainers to own projects

{{< alert "poo" >}}
This is not yet complete.
{{< /alert >}}

### Copy the baseline

Copy the baseline from `claude-code/.devcontainers` into the root of your project (or a subdirectory) and adapt the `Dockerfile` to meet your requirements. Claude or Codex can help you, but beware that this can be quite a task. I managed to quickly adapt it to a FastAPI / Air project, but struggled to get Playwright MCP going. In the end, I just instructed Claude to use the Playwright CLI, instead.

### Adapt the Dockerfile

### Adapt devcontainer.json

### Adapt the firewall script

## Summary

When Claude Code runs in a devcontainer configured as described, it can only

- Access files in /workspace (your project) and other mounted directories
- Make network requests to whitelisted domains
- Execute commands within the container, optionally with additional guardrails

Your personal files, documents, SSH keys from your host machine, browser data, etc., are all inaccessible to Claude Code running in this container. But:

- Claude Code can still access/modify any files in your mounted workspace, this includes `.env` files
- Git credentials inside the container may allow pushing to repos
- The container shares the Docker daemon if Docker-in-Docker (or Kubernetes-in-Docker) is enabled. This surprised me a bit when I wanted to run an app in a KinD cluster in a devcontainer.
- Data exfiltration is still possible via DNS, for example.

Devcontainers add a layer of security but nothing is perfectly secure. Devcontainers also simplify onboarding to a project, or running experiments in isolated environments in parallel. Devcontainers' downsides are that setting them up is time-consuming and working with them is less convenient and slower than working directly on a local machine.