---
title: "Launch VS Code from the Command Line"
summary: "A quick tip to make your life a bit easier with VSCode and Python."
date: 2024-09-28
showZenMode: true
categories: 
  - The Basics
tags: 
  - Python
  - Conda
  - VSCode
aliases:
  - /blog/2024/09/28/launch-vscode-from-the-cli/
---

Quick tip: It's much better to launch VS Code from the command line. Why? Because this way, the sessions' environment configuration is used by VS Code, too, and you don't need to configure the Python interpreter in VS Code. 

For example, I often check out a repository with GitHub Desktop and then open the project from GitHub Desktop in VS Code. This way, I also need to configure the Python interpreter in the VS Code workspace. On the other hand, when I open the working copy in the terminal, do the initialization there, and only then launch GitHub Desktop, the Python interpreter is automatically setup in VS Code, too.

Here is a step-by-step example with Anaconda. After cloning the repository, I open a terminal in the repository directory and create a new conda environment with:

```bash
conda create --name myenv python=3.11
```

Then I activate the environment with:

```bash
conda activate myenv
```

Now I install the required packages with:

```bash
pip install -r requirements.txt
```

Finally, I open the project in VS Code with:

```bash
code .
```

If the last command does not work, launch VS Code, open the command palette withe `Ctrl+Shift+P` or `CMD+Shift+P` on the Mac, and type `shell command` to **Install 'code' command in PATH**. Restart the terminal. Now it should work.