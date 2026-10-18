---
title: "Your Mac Is a Trusted Device"
summary: "What a coding agent on your personal Mac can actually reach, and the cheap boundary that fixes most of it."
author: mitja
date: 2026-09-23
categories: ["AI Engineering", "Blog"]
tags: ["Agents", "macOS", "Security", "Prompt Injection"]
draft: true
slug: your-mac-is-a-trusted-device
---

I spent a day speccing macOS CI runners — a small fleet of Macs, each running throwaway VMs for one job at
a time — and most of that day went into one question: what stops a hostile job from taking the *hardware*?

The answer there turned out to be Activation Lock. Then I applied the same question to the Mac I was
typing on, the one that runs coding agents all day, and the answer inverted in a way I had not expected.

<!-- more -->

## The fleet answer, briefly

On a Mac that nobody has claimed, the nightmare is that somebody else claims it. Activation Lock arms
through Find My, and on an unsupervised Mac nothing stops a person with an admin session from signing in
with *their* Apple Account and switching it on. The machine can then no longer be erased or reinstalled
without their credentials. No exploit required. A rack of Macs becomes a rack of bricks.

The fix is to enrol the machines in device management before they ever run a job, because a supervised Mac
has Activation Lock disallowed by default.

Fine for a fleet. Useless as advice for my own laptop — which is already claimed, by me.

## The personal answer: you can't lose the hardware, you can lose the account

Your Mac is signed into your Apple Account and Find My is on. Nobody can re-claim it without first getting
that account. Good.

Except that your Mac *is* the thing that proves you own the account. From Apple's own instructions for
changing your Apple Account password:

> Choose Apple menu, then System Settings. Click [your name], then click Sign-In & Security. Click Change
> Password. **Enter the password used to unlock your Mac.**

That is the documented flow, and it is the right design for a human who forgot a password. It also means
your Mac's login password is a credential for your Apple Account. And your Apple Account is Find My, which
reaches every device you own, with "erase" on the menu.

So the question for a coding agent is not "can it brick my Mac". It is: **can it ever learn my login
password?**

## Three ways it can

None of these need a vulnerability in anything.

1. **You type it into a terminal the agent is driving.** Every `sudo` in an agent session is you typing
   your login password into a process tree the agent owns. If the agent runs the command, the agent can
   read the PTY.
2. **A dialog that looks exactly like macOS.** One line of `osascript` puts up a password prompt with the
   system's own look. An agent that has been talked into running it gets whatever you type.
3. **Your password manager, already unlocked**, because you keep the Mac password in it like everything
   else.

Note that none of this requires the agent to be malicious, which is the part I keep having to re-explain.
A coding agent reads a README, an issue, a stack trace, a web page. Any of those can carry instructions.
That is prompt injection, it is not solved, and the practical consequence is that **the agent's
trustworthiness is not the boundary** — what the agent can reach is.

## The boring loss is more likely than the dramatic one

Before any of that, an agent running as your user can already read, with no prompt and no password:

| | |
|---|---|
| `~/.ssh/id_*` | your keys, and whatever they open |
| `~/.aws/credentials`, `~/.config/gh/hosts.yml`, `~/.npmrc`, `~/.cargo/credentials` | long-lived tokens in plain text, which is where nearly everyone keeps them |
| every `.env` in every project | including the ones you meant to delete |
| `~/Library/Application Support/…` | browser profiles and cookie stores |
| everything, if you granted your terminal Full Disk Access | Mail, Messages, the lot |
| `~/Library/LaunchAgents` | writeable — so anything dropped there survives the reboot |

Losing your Apple Account is the headline. Losing a production token out of a dotfile is the Tuesday.

## What I actually do about it

Ordered by how much they buy for what they cost.

**1. A second macOS user, standard, not admin.** This is the big one and it takes ten minutes. Agent work
happens as `dev`, which has its own home directory: no `~/.ssh`, no cloud credentials, no browser profile,
no password manager. A standard user cannot `sudo` at all, so mechanism 1 above disappears — there is no
prompt to phish because there is nothing to elevate to. I switch with fast user switching and treat that
account as a place where nothing personal lives.

**2. Never type the login password into an agent-driven session.** If something genuinely needs admin, I
do it myself, in my own session, in a terminal no agent is attached to. "The agent asked for sudo" is a
reason to stop and look, not a reason to type.

**3. A VM for anything I did not write.** Unfamiliar repo, someone's install script, a `curl | sh` from a
blog: that runs in a VM, and the VM is throwaway. On Apple silicon a Linux VM costs almost nothing to keep
around, which is the same trick as the CI runners — the boundary is the machine, not the intent.

**4. Secrets out of dotfiles.** Short-lived and scoped where the service supports it, a separate GitHub
account with its own token for agent work, and nothing long-lived sitting in `~` for the convenience of a
tool I run twice a month.

**5. Apple Account hygiene, because it is the crown jewel now.** Two-factor obviously. A recovery key or a
recovery contact, understanding that a recovery key turns off Apple's standard recovery process — you then
need that key and your trusted phone number, so it is a real commitment rather than a checkbox. And the
Apple Account password does not live anywhere an agent session can read it.

**6. Backups I have actually restored from.** Time Machine plus a copy that is not attached to the
machine. The answer to "something erased my disk" is a restore, not forensics.

**7. A look at `~/Library/LaunchAgents` after anything unfamiliar.** Persistence is what turns a bad
afternoon into a bad month.

**8. Outbound visibility.** LuLu or Little Snitch, not because the alerts are pleasant, but because "why
is that talking to that" is a question worth being able to ask.

## So is it unsafe to run agents on your personal Mac?

Not as a yes or no. It depends entirely on what the agent reads.

An agent working on my own code, on inputs I wrote, in a repo I know, is roughly as risky as me working on
my own code — I am the one who pastes things into terminals, after all. The risk arrives with **untrusted
input**: a repository I cloned to look at, an issue thread, a scraped page, a dependency I have not read.
That is when the agent stops being a tool I am driving and becomes a program executing someone else's
instructions with my credentials.

And that is the same sentence I wrote in the runner spec, about a CI job. The two cases meet at exactly
the same rule:

> The blast radius should be smaller than your whole life.

For a CI fleet that means a VM per job and a supervised host. For a personal Mac it means a second user
account — an evening's work, and the cheapest security change I have made this year.

I am not a security researcher, and none of this is a threat model anyone audited. It is what I concluded
while writing a spec for something else, checked against Apple's own documentation, and then applied to my
own machine because it would have been silly not to.