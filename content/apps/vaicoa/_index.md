---
title: "Vaicoa"
weight: 30
subtitle: "Approvals for AI agents in IT operations"
kicker: "Project"
status: "Experiment"
status_note: "Experiment: Vaicoa is a personal project of mine, alpha software, not a product and not a commercial offer. There is no support, and the code is not public yet."
teaser: "Agents propose. You sign. The server checks. You see every change as a concrete plan, approve it on your phone, and the target system checks your signature itself before it runs anything."
summary: "Vaicoa is an approval layer for AI agents in IT operations: the core shows you every change as a concrete plan, you approve it on your phone, and the target system checks your signature itself before it runs anything."
primary:
  text: "Get in touch"
  url: "mailto:hi@mitjamartini.com?subject=Vaicoa"
secondary:
  text: "More on vaicoa.com"
  url: "https://vaicoa.com/en/"
layout: product
showDate: false
showReadingTime: false
showWordCount: false
showTableOfContents: false
showPagination: false
sharingLinks: false
---

**Agents propose. You sign. The server checks.**

## What it is about

Coding agents can do operations work today: roll out a deployment, create a server, silence an alert. For that they need write access to production. If you give them the keys, in the end the model decides what happens. If you don't, the work stays with you. Vaicoa is my attempt to find a way in between: the agent gets no keys, it may only propose.

## How it works

1. **Proposal.** The agent picks an action from a signed catalog, such as a deploy or a pull request. What is not in the catalog, it cannot propose.
2. **Plan.** The core validates the parameters, computes a plan from the current state (before → after) and lets the policy decide: reject, run, or require an approval.
3. **Approval.** If an approval is needed, it lands on your phone. The app shows you the plan, you approve it with Face ID, and the device signs with a key that never leaves it.
4. **Check and run.** The node on the target system picks up the change, checks the signature, the team roster and the plan itself, and runs exactly that plan.
5. **Record.** Every step lands in a hash-chained audit: who proposed, who approved, what ran.

You can approve with apps for iPhone, Android and Mac, or on the command line.

## What the server checks itself

The core is not the last word. The node on each host does not rely on it but checks before every change:

- **The signature.** You sign a digest over action, parameters, plan and evidence. If the core changes any part of it, your signature is invalid.
- **The roster.** Whether you may approve, the node checks against the signed team roster it has pinned itself.
- **The plan.** If the state has changed since your approval, the approval is invalid and a new one is needed.

On top of that, some rules apply to everyone: nobody approves their own proposal, and risky actions always need a human.

## Limits

- **Alpha.** Formats and interfaces change without notice. There has been no independent audit, only internal and automated reviews.
- **Actions against third-party APIs** such as Hetzner Cloud or Forgejo are checked by the core, not by a node. For them, the core is the control point.
- **Approvals by reviewer agents** cannot be checked by a node yet, only approvals by humans.
- **The apps** are built from source, not in the stores, and have so far only run in simulators and emulators, not on real devices.

The full list is on [vaicoa.com](https://vaicoa.com/en/docs/limitations/).

## Status and what comes next

Vaicoa is a personal experiment. I am trying it out in my own operations first, working through the handbook step by step. After that I will decide how it goes on. The idea for now is to publish it as open source.

## Contact

If the topic interests you or you have questions, write to me at [hi@mitjamartini.com](mailto:hi@mitjamartini.com?subject=Vaicoa).
