---
title: "A Whole Django Stack in 1 GB: Podman, Quadlet and Litestream on the Smallest Hetzner Server"
summary: "Notes, to be written up: a Django app with Celery, Valkey, Caddy, Litestream backups and its own logs and metrics, as one Podman pod of Quadlet units. It peaked at 726 MiB in a 1 GiB limit and ran on a 1 GB cpx02."
slug: "django-stack-in-1gb-podman"
date: 2026-10-15
draft: true
categories:
  - Platform Engineering
tags:
  - Podman
  - Quadlet
  - Django
  - Litestream
  - Hetzner
showHero: false
---

Kubernetes is my preferred platform for running applications but with the recent RAM prices, its getting a bit expensive. I managed to cram a whole operational platform, with Flux, Vector, Victoria Metrics etc. on a single k3s node into about 2.4 GiB before the app. With a SaaS Pegasus app (Django, Python, Postgres, Redis) this can run on a Hetzner Cloud CPX22 at about 24 EUR/Month.

I was curious if I could deploy an app on a similarly complete platform on one of the new 1 vCPU / 1 GiB RAM / 20 GiB NVMe CPX02 machines at less than 8 EUR/Month.

I settled on a stack based on my Garden Linux variant with Podman and Quadlet units with images pinned by digest:

- a Django app: gunicorn, a Celery worker and Celery beat, on SQLite;
- Litestream, replicating SQLite to S3;
- Caddy for TLS;
- Vector, shipping journald;
- VictoriaLogs and VictoriaMetrics single for logs and metrics on the box.

## How I measured

- Two servers:
  - a cx23 (4 GB) with the whole stack in a systemd slice, `MemoryMax=1G`, no swap;
  - a cpx02 (1 vCPU, **1 GB**), the smallest x86 type, with the stack alone.
- One hour idle with the app checking itself every minute, then 5 minutes of load (20 reads and 2 logged-in edits a
  second), then 5 minutes after.
- Working set = memory in use minus inactive file cache, per unit and in total.
- Cost of the run: €0.05.

## The numbers

| | MiB, mean / max |
|---|---|
| Django (gunicorn + worker + beat) | ~470 |
| Litestream | 14–23 |
| Valkey | 10 |
| Caddy | 15–23 |
| Vector | 24–82 |
| VictoriaLogs + VictoriaMetrics | 96–122 |
| conmon, for 10 containers | 5–12 |
| **whole stack under load (cx23 slice)** | **719 / 726** |
| **whole stack under load (cpx02)** | **643 / 652**, with 105–120 MiB left on the box |

- **Under load**: no errors. Reads at p95 5–10 ms, writes at p50 21–36 ms.
- **Cold start**: 3.6–6.3 s to the first page through Caddy. A "twin" start that restores the database from the
  replica first took 4.6–5.8 s.
- **No out-of-memory kill.** The limit was touched only while restarting, and that was cache the kernel reclaimed.

## What I take from it

- **The app is the elephant**: ~470 MiB of the ~720. The rest of a production-grade stack is ~180–240 MiB.
- A Go app would land at ~215–300 MiB total.
- Tuning Django (fewer gunicorn workers, Celery at concurrency 1, beat inside the worker) should save 150–250 MiB.
  I haven't measured that yet.


## The small things that bit

- Debian's podman needs `catatonit` for pods.
- An unescaped `&` in the replica URL broke the rendered systemd unit. A local dry run caught it first.
- For local testing, my coding agent (again) tried to use MinIO's community image, but it's now gone from Docker Hub; I used Garage as the S3 target on my machine, instead.

## Not yet

- **Postgres instead of SQLite.** I estimate tuned Postgres at 55–95 MiB, but with this app that's too close to
  1 GB to claim without measuring. That's the next run.
- My own image (Garden Linux with A/B updates) and its node agent.
- TLS through ACME, real Object Storage, longer retention, a realistic database size.

## Backups for everything that isn't the database

- SQLite has Litestream. For uploads and other volumes: a thin LVM snapshot (milliseconds), upload it with Kopia
  (incremental, deduplicated, encrypted, to S3), remove the snapshot.
- Kopia is also what Velero uses on Kubernetes, so it's one restore story on both.
- Outline only; numbers come with the implementation.
