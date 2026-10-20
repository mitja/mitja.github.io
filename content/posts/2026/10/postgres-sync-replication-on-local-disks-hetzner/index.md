---
title: "Postgres with CloudNativePG on Hetzner Cloud and Kubernetes"
summary: "Commit latency, data loss and downtime compared between Cloud Volumes and local NVMe with synchronous replication"
slug: "postgres-sync-replication-local-disks-hetzner"
date: 2026-10-20
draft: false
categories:
  - Platform Engineering
tags:
  - PostgreSQL
  - CloudNativePG
  - Hetzner
  - Kubernetes
  - k3s
  - DRBD
showHero: false
---

My foundation for larger web applications is SaaS Pegasus, and it needs Postgres. I usually just run Postgres as one CloudNativePG instance on a Hetzner Cloud Volume. A load test of the portal showed that the Volume's flush limits performance quite a lot: every commit waits ~2.7 ms on the Volume. I wanted to know

- whether local NVMe with synchronous replication is faster than one instance on a Volume,
  - via Postgres between three nodes and 
  - via DRBD between two nodes with a tie-breaker node,
- whether it achieves zero data loss, and
- how long it takes until writes work again when a server dies.

Claude Code answered these questions for me with tests. Here are the results in brief:

| setup | per transaction, 1 client | TPS, 8 clients | lost when a server dies | until writes work again | servers |
|---|---|---|---|---|---|
| local NVMe, no replication | 0.93 ms | 8,617 | everything on that server | until the server is back | 1 |
| **local NVMe, `ANY 1` of two standbys** | **2.23 ms** | **4,212** | **0** | **~68 s** | 3 |
| Hetzner Volume, no replication | 3.66 ms | 1,311 | 0, if only the server fails | moving the pod and the Volume: minutes (estimate) | 1 |
| Hetzner Volume, `ANY 1` | 4.85 ms | 1,334 | 0 | not measured | 3 |
| **one instance on DRBD, 2 replicas** | **1.68–1.87 ms** | **3,801–3,869** | **0** | **70–108 s** | 3 (2 and a tie-breaker) |

The DRBD row comes from a second test on another day, with Postgres in a pod on k3s. One instance on `local-path` took 1.08–1.10 ms per commit.

For comparison: **SQLite** on local NVMe with `synchronous=FULL` takes 0.33–0.38 ms per commit. With Litestream it loses under a second of writes when a server dies, and on DRBD with two replicas it takes 0.90–0.93 ms per commit with zero loss and 54–65 s until writes work again ([the SQLite article](/en/posts/2026/10/sqlite-resilience-on-hetzner/)).

## My rules of thumb

- **Default:** three CNPG instances on `local-path`, `ANY 1`, `dataDurability: preferred`. This provides zero loss and about a minute until writes work again, and it's faster than one instance on a Volume.
- **Zero loss with one Postgres instance:** one CNPG instance on DRBD under the PVC. With one client it's about as fast as `ANY 1`, it gets by with one copy of Postgres instead of three, but the failover takes a little longer.
- **Simple:** one instance on a Cloud Volume.
- **Backups:** always barman to S3 in **another** location. A backup in the same location doesn't survive the location.
- **On k3s:** fix the StorageClass defaults first.
- **Not worth it:** `remote_write`, and three instances on Volumes.

## How fast is a durable Postgres commit?

A durable commit waits for the WAL flush, so the disk sets the floor:

| | mean | p50 | p99 |
|---|---|---|---|
| local NVMe, fdatasync (pg_test_fsync: 0.28–0.31 ms) | 0.30–0.34 ms | 0.29–0.32 ms | 0.47–1.04 ms |
| Hetzner Volume, fdatasync (pg_test_fsync: 2.69 ms) | 2.50 ms | 2.41 ms | 5.73 ms (p99.9 9.6) |
| private network, ICMP | | 0.19–0.24 ms | 0.30–0.50 ms |
| PostgreSQL `SELECT 1` | 0.26 ms | 0.25 ms | 0.41–0.45 ms |

A Volume flush is ~8× a local flush. A second run in fsn1 the day before gave the same: 2.77 ms against 0.38 ms.

## What does synchronous replication cost?

Claude ran pgbench `-N` (simple update) on plain PostgreSQL 18.6 with a primary and two standbys, in every replication mode, on local disks and on a Volume:

| storage / mode | 1 client | 8 clients | 32 clients |
|---|---|---|---|
| local, no replication | 0.93 ms (1,079) | 0.93 ms (8,617) | 2.71 ms (11,832) |
| local, async | 1.06 ms (945) | 1.12 ms (7,171) | 3.04 ms (10,530) |
| local, sync `remote_write` | 1.90 ms (527) | 1.69 ms (4,730) | 3.50 ms (9,138) |
| local, sync `on`, one standby | 2.30 ms (435) | 2.02 ms (3,968) | 3.90 ms (8,206) |
| **local, `ANY 1` of two** | **2.23 ms (449)**, p99 3.7 | **1.90 ms (4,212)**, p99 3.1 | 3.71 ms (8,625) |
| local, `remote_apply` | 2.37 ms (421) | 2.32 ms (3,455) | 4.18 ms (7,652) |
| **Volume, no replication** | **3.66 ms (274)**, p99 7.3 | **6.10 ms (1,311)**, p99 11.2 | 6.03 ms (5,306) |
| Volume, `ANY 1` | 4.85 ms (206) | 6.00 ms (1,334) | 7.84 ms (4,080) |

- Mean latency, TPS in parentheses. TPC-B-like shows the same: 2.52 ms against 4.17 ms for one client, 3,669 against 1,191 TPS for eight.
- **Sync replication costs ~1.3 ms per commit** on local disks: more than the round trip plus the standby's flush (~0.55 ms). The rest is probably process wake-ups on shared vCPUs.
- **It still beats the Volume clearly.** With one client, it takes 39 % less time per commit than a single instance on a Volume. With eight clients, it has 3.2× the throughput at a quarter of the p99.
- **`remote_write` is not worth it.** It saves ~0.35 ms, but if the primary and that standby crash together, it can lose acknowledged writes.
- **Three instances on Volumes are the worst of both worlds:** 4.85 ms per commit.
- **The pod network adds up.** Over the `-rw` Service, with the client on another node, pgbench's five round trips per transaction add ~2 ms: 4.31 ms for one client. Keep the round trips of your app in mind, not only the flush.

## How much is lost when the primary dies?

Claude ran k3s v1.36.2 and CloudNativePG 1.29.1 with three instances on `local-path` and `synchronous: {method: any, number: 1, dataDurability: preferred}`, and hard powered off the primary's server through the Hetzner API while pgbench was writing.

- 112,483 acknowledged writes, **0 lost**.
- No write was acknowledged for ~66 s, then there was one more gap of 4.4 s.
- Timeline:
  1. +57.4 s: Kubernetes marks the node not ready;
  2. +60.1 s: CNPG starts the failover;
  3. +61.4 s: new primary;
  4. +68.0 s: first acknowledged write.
- After power-on, the old primary streamed again 89 s later, with no manual step.

**Most of the minute is Kubernetes noticing the node is gone, not CNPG.** Knobs to try:

- the controller manager's node-monitor grace period, which applies cluster-wide;
- the CNPG operator with two replicas, or a short unreachable toleration. If the operator dies with the primary, the failover waits for the operator's eviction, 300 s by default.

## What happens when the standbys go away?

Claude fenced one standby, then both:

- With one standby fenced, writes did not stall.
- With both fenced, writes stalled 27.3 s until CNPG emptied `synchronous_standby_names`, as `dataDurability: preferred` promises. Then they continued asynchronously, and 0 of 124,223 acknowledged writes were lost.
- After unfencing, it went back to `ANY 1 ("pg-1","pg-3")` by itself.

## One instance on DRBD

Instead of replicating in Postgres, DRBD can replicate the disk under it, as in [the SQLite article](/en/posts/2026/10/sqlite-resilience-on-hetzner/). Claude set up k3s with Piraeus Operator v2.12, LINSTOR 1.35 and DRBD 9.3 as there: two replicas on n1 and n2, a diskless tie-breaker on n3, protocol C (a write completes when both disks have it). On top runs one CNPG instance with its PVC on DRBD, and for comparison one on `local-path` in the same cluster. pgbench ran inside the pod over the Unix socket, in two runs:

| one CNPG instance | 1 client | 8 clients | 32 clients | TPC-B-like, 8 clients |
|---|---|---|---|---|
| `local-path` | 1.08–1.10 ms (911–922) | 1.02–1.08 ms (7,397–7,869) | 2.94–3.28 ms (9,746–10,894) | 1.23–1.42 ms (5,622–6,510) |
| **DRBD, 2 replicas** | **1.68–1.87 ms (536–597)**, p99 3.5–3.8 | **2.07–2.11 ms (3,801–3,869)** | 4.10–4.12 ms (7,768–7,809) | 2.27–2.40 ms (3,336–3,532) |

- **The second copy costs ~0.6–0.8 ms per transaction.** That's about what it adds to each flush: `pg_test_fsync` measured 0.34 ms on `local-path` and 0.95 ms on DRBD.
- **Compared to `ANY 1`,** it's a little faster with one client (2.23 ms) and a little slower with 8 and 32 (1.90 and 3.71 ms). The `ANY 1` numbers come from the other test, so take this as "about the same".
- **It clearly beats one instance on a Volume:** 3.66 ms with one client, 1,311 TPS with eight.

Then Claude hard powered off the instance's server four times through the Hetzner API, with the same writer and pgbench load as above:

- 246,766 acknowledged writes in total, **0 lost**.
- No write was acknowledged for 69.7, 72.1 and 79.5 s in the second run, and 107.5 s in the first.
- After power-on, it took 156–162 s until DRBD was UpToDate on both nodes again, including the DRBD module's compile at boot.

**How the instance finds the other node.** CNPG doesn't pick a node. With one instance there is no standby to promote; CNPG creates the pod anew with the same PVC, and the Kubernetes scheduler places it. It can only land on the other replica, for two reasons:

1. LINSTOR's CSI driver gives the volume a node affinity to the nodes that hold a copy (`linbit.com/hostname` is n1 or n2), because the StorageClass sets `allowRemoteVolumeAccess: "false"`. The tie-breaker on n3 has no copy.
2. The dead node is NotReady and tainted.

Here is the timeline of the second run's first failover:

| after the power-off | what happens |
|---|---|
| +35.6 s | Piraeus' HA controller sees the DRBD resource on the dead node lose quorum, taints the node (`NodeStorageQuorumLost`) and evicts the pod. |
| +49.9 s | Kubernetes marks the node NotReady. Only now can the evicted pod go away. |
| +56.2 s | CNPG: "Creating new Pod to reattach a PVC". The scheduler puts it on n2. |
| +56.9 s | The volume is attached on n2. |
| +58.9 s | Postgres starts and replays its WAL (crash recovery). |
| +62.3 s | CNPG labels the pod as primary, so the `-rw` Service points to it again. |
| +71.0 s | The first acknowledged write. |

- **Detection:** The HA controller noticed after 28–36 s, Kubernetes after 42–50 s. As with `ANY 1`, most of the time is spent noticing that the node is gone.
- **The spread comes from the volume attachment.** The new pod can only start once the volume is released on the dead node. That took 1, 5 and 21 s in the second run, and ~37 s in the first, which is why that failover took 107.5 s.
- **Postgres itself needs 10–12 s** from start to the first write: crash recovery and the readiness probe.
- **One instance means no PodDisruptionBudget** (`enablePDB: false`), so nothing blocks the eviction.

The downside is the same as in the SQLite article: more parts, the DRBD module has to be built for the node's kernel, and with two copies a second failure during a resync is an outage.

**Is it the leaner setup?** Only partly.

- **It saves two Postgres instances:** one instead of three, so less CPU and RAM, and two copies of the data instead of three.
- **It doesn't save servers:** DRBD needs the third node as a tie-breaker for its quorum, and Kubernetes wants three nodes anyway. The tie-breaker holds no copy, so it can be a small server that does other work.
- **It adds Piraeus, LINSTOR and a kernel module.** I didn't measure what they cost in RAM and CPU. For a single database that may eat up the savings; it pays off when DRBD is there anyway, for several databases, SQLite or other volumes.
- **It gives up maintenance without downtime.** With three instances, CNPG switches over before a Postgres update, a configuration change or a node drain, with seconds of interruption. With one instance, every restart of the pod is downtime. I didn't measure how long; going by the crash recovery and readiness probe above, I'd estimate 10–30 s.
- **It also gives up read replicas** and 2–40 s of failover time (70–108 s against ~68 s).

So: one instance on DRBD fits a few databases where a short interruption during updates is fine, and especially a cluster that runs DRBD anyway. Three CNPG instances stay the better choice when updates and maintenance must not interrupt writes, or when you need read replicas.

## A trap on k3s: two default StorageClasses

k3s ships `local-path` as a default StorageClass. Installing the Hetzner CSI adds `hcloud-volumes`, also as default.

- **Un-defaulting `local-path` with `kubectl annotate` doesn't stick.** k3s re-applies its packaged `local-storage` manifest, the default annotation included.
- **With two defaults, a PVC without `storageClassName` gets the newest.** That can change silently, and the PVC keeps the class it got forever.
- **The fix:** make one class the only default, and stop k3s re-applying the manifest, either with a `local-storage.yaml.skip` file in the server manifests directory, or with `--disable local-storage` and the provisioner deployed yourself. Then name `local-path` explicitly where you want it, e.g. for CNPG.

## How Claude measured it

Claude Code wrote the scripts, ran them against a disposable Hetzner project, and tore everything down afterwards. The whole run cost €0.41.

- **Servers:** three cpx32 (4 shared vCPUs, 8 GB, local NVMe) in nbg1, on separate hosts (a spread placement group), a private network. A 10 GB Volume on the first server for comparison.
- **Versions:** PostgreSQL 18.6, k3s v1.36.2, CloudNativePG 1.29.1.
- **Flush and network:** fio and `pg_test_fsync` for the disk's flush, ICMP and `SELECT 1` for the round trip.
- **Replication modes:** pgbench over the Unix socket, scale 50, 60 s per cell, 1/8/32 clients. Modes: none, async, sync `remote_write`, sync `on` with one standby, `ANY 1` of two, `remote_apply`.
- **DRBD:** a second test on 2026-10-19, in two runs, €0.44 together: k3s v1.36.2, Piraeus Operator v2.12.0 with LINSTOR 1.35.2 and DRBD 9.3.4, CloudNativePG 1.29.1 with PostgreSQL 18.3, one instance with 10 GB on a 2-replica volume. The same pgbench cells inside the pod, then four power-offs of the instance's node; the writer ran on the third node, which was never powered off.
- **Failover:** a hard power-off of the primary's server through the Hetzner API while pgbench writes, then comparing the acknowledged writes with the ones that survived.
- **Noise:** one 60 s run per cell, on shared vCPUs, and one failover with three instances; for DRBD, two runs per cell and four failovers.
- **Not measured:** no WAL archive was in the test. Archiving is not in the commit path, but the restore time from S3 is not measured here. The old setup, one instance on a Volume, was not failed over. Moving the pod means eviction plus the Volume's detach and attach: several minutes with Kubernetes' defaults (estimate).

Small gotchas on the way:

- The Hetzner API no longer reports a server's datacenter. The script that recorded placement crashed on that.
- The hcloud CLI's `--automount` did not mount the new Volume.
- fio needs `--overwrite=1` for honest fsync numbers. On a pre-allocated file it reported 1.0 ms instead of 0.3 ms.
