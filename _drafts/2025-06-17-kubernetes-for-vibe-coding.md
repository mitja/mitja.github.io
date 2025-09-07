- use kubernetes for vibe coding.
- vibe coding challenge, testing, separate env.
- best way: mockups
- integration tests, and trying out more complicated
- complete containerized dev with compose
- but also getting tedious: start, tear down, ...
- mainly bec. separation not good
- giving access to others also hard
- a solution: use per-branch environments in kubernetes
- local cluster or dev cluster in the cloud
- a preview env per branch.
- auto syncs from git, can also be used for auto integration testing
- for me: Django is most interesting, as I work with SaaSPegasus.
- in this article, I'll show how to set it all up.
- first, let me quickly demo what it looks like, in the end.

On-Demand Preview Environments for Agent Assisted Coding with Kubernetes