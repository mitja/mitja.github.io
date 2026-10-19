---
title: "SQLite with Litestream on Hetzner Cloud"
summary: "SQLite's commit latency on local NVMe and on a Cloud Volume, Litestream's data loss and time to recover after a hard power-off, a warm standby with its follow mode, and DRBD and rqlite as zero-loss options, with rqlite as the fastest-failover alternative."
date: 2026-10-19
draft: false
categories:
  - Platform Engineering
tags:
  - SQLite
  - Litestream
  - DRBD
  - LINSTOR
  - Kubernetes
  - Hetzner
  - rqlite
showHero: false
---

For small to medium server-based AI applications, I like to use SQLite with Litestream and always wanted to know the actual commit latency on local NVMe and on a Cloud Volume, the potential data loss and the time to recover. I also wanted to know alternative approaches to achieve zero data loss (DRBD and rqlite) and their tradeoffs.

Claude Code answered these questions for me with tests. Here are the results, as a little decision helper:

{{< sqlite-decision >}}

## My rules of thumb

- **Default:** SQLite + Litestream on local NVMe, with an alert on replica lag. This provides under a second of loss, seconds to restore the data.
- **Simple, zero loss:** SQLite + Litestream on a Hetzner Cloud Volume.
- **Fast, zero loss, and deployed on k8s:** DRBD under the PVC. This can be a common mechanism for SQLite, files and even a single Postgres.
- **Fastest failover, the app can be rebuilt:** rqlite.

## How fast is a durable SQLite commit?

SQLite on local NVMe is really fast with `synchronous=FULL`, and extremely fast with `synchronous=NORMAL`, but:

- `NORMAL` survives an app crash, but not a power loss. On a cloud VM a host failure counts as a power loss.
- `FULL` fsyncs the WAL per commit, so the commit is as fast as the disk's flush: 0.28 ms local, 2.43 ms on a Volume.

| | `synchronous=FULL` | `synchronous=NORMAL` |
|---|---|---|
| local NVMe | 0.33–0.38 ms, ~2,450 commits/s | 13 µs, ~48,000/s |
| Hetzner Volume | 2.3–2.65 ms, ~290 commits/s | 26–32 µs, but p99.9 31–60 ms |

## How much does Litestream lose?

Claude tested this with a writer that commits 200 rows/s with `FULL` and reports every committed id to another server. Then Claude hard powered off the server through the Hetzner API, restored from the Garage S3 and counted.

Litestream lost 110, 129, and 22 rows in three runs, i.e. **582 / 645 / 110 ms** of writes. With `NORMAL`, it lost 139 rows, 695 ms. Litestream's default sync interval is 1 s, and the measured data loss stayed below this interval.

A restore across locations took 2.4 s for 100 MB and 21 s for 1 GB.

When S3 was taken down for 72 s, this happened:

- the app didn't notice (slowest commit was 26 ms);
- the replica fell ~65 s behind, then caught up in ~9 s;
- **Litestream logged nothing**. Ergo: Alerting should be based on its metrics, not its logs.

By the way: The bucket held ~3× the database right after the first snapshot.

## Litestream's follow mode

Litestream v0.5 can keep a second copy current: `litestream restore -f` restores once, then polls the replica and applies new changes, by default every second. The copy can be read.

Claude used the same writer and logger, Litestream on the primary, `restore -f` on a second server, and a reader there that reads the newest row every 100 ms. Claude again powered off the primary through the Hetzner API, and a script promoted the standby right away:

1. wait until follow mode applies nothing more,
2. stop it,
3. run `PRAGMA quick_check`,
4. start the writer and Litestream there (to a new replica path).

| intervals | lost | standby behind, p50 / p99 | promotion |
|---|---|---|---|
| 1 s (the default), 3 runs | 71–120 rows, **355–612 ms** | 1.3 / 1.8–2.0 s | **3.1–3.2 s** |
| 250 ms, 2 runs | 14–22 rows, **70–110 ms** | 0.15–0.18 / 0.31–0.35 s | **1.2 s** |
| 1 s, on a 1 GB database | 153 rows, 770 ms | 1.1 / 1.7 s | 4.1 s |

- "intervals" means Litestream's `monitor-interval` and `sync-interval` on the primary, and `-follow-interval` on the standby.
- **The loss is the same as with a restore.** What follow mode saves is the restore: the copy is already there, at any size. A 1 GB restore took 21 s; the promotion to writer on 1 GB took 4.1 s, of which `quick_check` took 1 s.
- **Promotion is mostly waiting.** The script waits for three quiet poll intervals, to be sure the primary's last upload is in. Stopping, checking and starting take ~0.1 s.
- **Failure detection comes on top.** In the lab, Claude promoted the new writer as soon as the power-off API call returned, which took 7–9 s itself. The writes were unavailable for 8–11 s.
- **250 ms intervals** cut the loss to ~0.1 s and the promotion to ~1 s. The price is about four times the S3 requests: an upload and a listing per interval (not measured).
- **Readers on the standby** sometimes meet follow mode's lock while it writes: 0.4–1.7 % of reads without a busy timeout. A `busy_timeout` hides that.
- A 1 GB standby was ready after 52 s: the primary's first snapshot upload and the restore. Its first reads were 37 s behind, and it caught up within 2 s.
- All six `quick_check`s said ok.

The new primary should never write to the old replica path. The old primary may come back and keep writing to it.

## DRBD

Claude used Piraeus Operator v2.12 with LINSTOR 1.35 and DRBD 9.3 on k3s v1.36 to run two replicas plus a diskless tie-breaker on the third node, and configured protocol C (a write completes when both disks have it). SQLite then uses PVCs on this storage.

| in a pod | fsync | SQLite `FULL` commit |
|---|---|---|
| local-path | 0.33 ms | 0.39–0.40 ms |
| LVM thin | 0.43 ms | 0.48 ms |
| DRBD, 1 replica | 0.45 ms | 0.45–0.47 ms |
| **DRBD, 2 replicas** | **0.93 ms** | **0.90–0.93 ms** |

DRBD was the biggest surprise for me: The second copy costs just ~0.5 ms per fsync, and it's still ~2.5× faster than a Hetzner Cloud Volume. It's ~2.4× faster than Postgres with a synchronous standby (at 2.23 ms). Failover after powering off the node: 54–65 s to the first acknowledged write, without data loss. The HA controller evicts the pod after ~20–35 s. The new pod still waits for the node to be NotReady (~50 s). And: The downtime is about the same as with CNPG (one minute).

The downside is that it's more parts, more complicated to set up, and DRBD has its quirks:

- **A double-fault window.**
  - Claude powered off the primary while the other node was still resyncing (39 %).
  - DRBD refused to promote an incomplete copy (correctly) and the volume stayed unavailable until the source came back. Nothing was lost, but nothing was writable either.
  - Two copies means a second failure during a resync is an outage.
- **LINSTOR's `resource list` said UpToDate while DRBD was still SyncTarget.** Check `drbdsetup status`.
- **Piraeus' module loader compiles DRBD from source at every boot**: 75 s on a cpx32. On an image-based OS you should put
  the module in the VM image.
- **Rejoin after power-on**: 2–3 minutes, including that compile and a throttled resync.

## rqlite

Claude ran rqlite v10.6.0 on three voting nodes on cpx32s and used the HTTP API.

| | per write, 1 client | writes unavailable after a hard power-off | lost |
|---|---|---|---|
| plain SQLite `FULL` | 0.33–0.38 ms | until the server is back | that server's data |
| SQLite + Litestream | same | restore + a new server | 0.1–0.7 s |
| SQLite + Litestream, follow-mode standby | same | detection + 1–3 s | 0.1–0.6 s |
| SQLite on DRBD | 0.90–0.93 ms | 50–65 s | 0 |
| Postgres CNPG `ANY 1` (other post) | 2.23 ms | ~70 s | 0 |
| **rqlite** | **3.65–4.34 ms** over HTTP | **2.0–3.6 s** | **0** of 74,173 |

- Why is failover so fast? A Raft election takes about a second, and nothing waits for Kubernetes to notice a dead node.
- Why is each write so slow? rqlite itself costs ~2 ms (HTTP, JSON, its log's fsync), and replication adds ~1.7 ms.
- `?queue` makes writes 0.5 ms, but it acknowledges before consensus. It lost the last ~5 ms of writes (2 rows).
- With two of three nodes down, writes stop and only `none` reads answer.
- Its backups are periodic. With all three nodes lost 41 s after an upload, 42 s of writes were gone, where
  Litestream ships continuously.
- What needs to be changed in the app?
  - an HTTP client must be used instead of the SQLite library;
  - one request is one transaction;
  - the client must know all nodes, use short timeouts and retry idempotently;
  - it picks a read consistency per query.

## The results

| setup | per durable commit | lost when a server dies | until writes work again | servers |
|---|---|---|---|---|
| SQLite on local NVMe, no replication | 0.33–0.38 ms | everything on that server | until the server is back | 1 |
| **SQLite + Litestream** | 0.33–0.38 ms | **0.11–0.65 s** | a restore (100 MB: 2.4 s, 1 GB: 21 s) and a new server: minutes | 1 |
| **SQLite + Litestream + a follow-mode standby** | 0.33–0.38 ms | 0.36–0.61 s (1 s intervals), 0.07–0.11 s (250 ms) | **1.2–3.2 s** plus failure detection (1 GB: 4.1 s) | 2 |
| SQLite on a Hetzner Volume | 2.3–2.65 ms | 0, if only the server fails | re-attaching the Volume: minutes (estimate) | 1 |
| **SQLite on DRBD**, 2 replicas | 0.90–0.93 ms | **0** | 54–65 s | 3 (2 and a tie-breaker) |
| **rqlite**, 3 nodes | 3.65–4.34 ms (over HTTP) | **0** | **2.0–3.6 s** | 3 |

Litestream's default sync interval is 1 s, and the data loss stayed below this in the test.

For comparison: **Postgres with CloudNativePG** and three instances on local disks and a synchronous standby (`ANY 1`) takes about 2.23 ms per commit with one client, with zero data loss after a hard server shutdown and a downtime of about 70 s until writes work again.

## How Claude measured it

Claude Code wrote the scripts, ran them against a disposable Hetzner project, and tore everything down afterwards. Three runs cost €1.10 in total.

- **Servers:** three cpx32 (4 shared vCPUs, 8 GB) in nbg1, on separate hosts (a spread placement group), a private network, Ubuntu 24.04.
- **S3 target:** as Litestream's and rqlite's target, Claude set up Garage v2.4.1 on a cx23 in fsn1 to simulate cloud storage downtimes.
- **Versions:** SQLite 3.45.1, Litestream v0.5.17, Piraeus v2.12.0 with LINSTOR 1.35.2 and DRBD 9.3.4 on k3s v1.36.2, rqlite v10.6.0.
- **Commit latency:** fio and `pg_test_fsync` for the disk's flush, then a Python writer, one row per transaction in WAL mode.
- **Data loss:** the writer commits 200 transactions a second and sends each committed id to a logger on another server. Claude hard powered off the writer's server through the Hetzner API, restored it or promoted another server to be the new writer, and compared the highest acknowledged id with the highest one that survived.
- **Time until writes work again:** for DRBD, from the power-off to the first acknowledged write; for rqlite, how long writes failed; for Litestream, the restore's time; for the standby, the promotion script's time.
