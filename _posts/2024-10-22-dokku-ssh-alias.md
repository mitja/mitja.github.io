---
title: "Quick Tip: Dokku SSH Alias"
author: mitja
date: 2024-10-03
category: Self-Hosting with Dokku
tags: [Dokku, ssh, bash, zsh]
#pin: true
#math: true
#mermaid: true
render_with_liquid: false
permalink: /blog/2024/10/22/dokku-ssh-alias/
image:
  path: /assets/blog/2024/dokku-ssh-alias.png
  alt: A Dokku command before and after applying this tip.
---
Here is a quick tip to make working with Dokku a bit easier.

You can create an alias for the ssh command to save some typing when working with your Dokku server.

Add the following line to your `.bashrc` or `.zshrc` file:

```bash
alias dokku="ssh dokku@<DOKKU_HOST>"
```

Replace `<DOKKU_HOST>` with the domain name or IP address of your Dokku server.

Now instead of typing `ssh dokku@<DOKKU_HOST>`, you can simply type `dokku` to connect to your Dokku server and run commands such as `dokku apps:list`, `dokku logs <APP_NAME>`, etc.