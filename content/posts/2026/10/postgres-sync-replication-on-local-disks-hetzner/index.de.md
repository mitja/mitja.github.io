---
title: "Postgres mit CloudNativePG auf Hetzner Cloud und Kubernetes"
summary: "Commit-Latenz, Datenverlust und Ausfallzeit im Vergleich zwischen Cloud Volumes und Local NVMe mit synchroner Replikation."
slug: "postgres-synchrone-replikation-lokale-disks-hetzner"
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

Meine Grundlage für größere Webanwendungen ist SaaS Pegasus, und das braucht Postgres. Postgres betreibe ich meist einfach als eine CloudNativePG-Instanz auf einem Hetzner Cloud Volume. Ein Lasttest des Portals hat gezeigt, dass der Flush des Cloud Volumes die Leistung recht stark limitiert: Jeder Commit wartet ~2,7 ms auf das Volume. Ich wollte wissen,

- ob lokale NVMe mit synchroner Replikation schneller ist als eine Instanz auf einem Volume
  - via Postgres zwischen drei Knoten und 
  - via DRBD zwischen zwei Knoten mit einem Tie Break Knoten,
- ob damit Zero Dataloss erreichbar ist und 
- wie lange es dauert, bis wieder geschrieben werden kann, wenn ein Server ausfällt.

Claude Code hat mir diese Fragen mit Tests beantwortet, hier sind die Ergebnisse in Kürze:

| Aufbau | pro Transaktion, 1 Client | TPS, 8 Clients | Verlust, wenn ein Server ausfällt | bis wieder geschrieben werden kann | Server |
|---|---|---|---|---|---|
| lokale NVMe, ohne Replikation | 0,93 ms | 8.617 | alles auf diesem Server | bis der Server zurück ist | 1 |
| **lokale NVMe, `ANY 1` von zwei Standbys** | **2,23 ms** | **4.212** | **0** | **~68 s** | 3 |
| Hetzner Volume, ohne Replikation | 3,66 ms | 1.311 | 0, wenn nur der Server ausfällt | Pod und Volume umziehen: Minuten (geschätzt) | 1 |
| Hetzner Volume, `ANY 1` | 4,85 ms | 1.334 | 0 | nicht gemessen | 3 |
| **eine Instanz auf DRBD, 2 Replikate** | **1,68–1,87 ms** | **3.801–3.869** | **0** | **70–108 s** | 3 (2 und ein Tie-Breaker) |

Die DRBD-Zeile stammt aus einem zweiten Test an einem anderen Tag, mit Postgres in einem Pod auf k3s. Eine Instanz auf `local-path` brauchte 1,08–1,10 ms je Commit.

Zum Vergleich: **SQLite** auf lokaler NVMe mit `synchronous=FULL` braucht 0,33–0,38 ms pro Commit. Mit Litestream verliert es weniger als eine Sekunde an Schreibzugriffen, wenn ein Server ausfällt, und auf DRBD mit zwei Replikaten braucht es 0,90–0,93 ms pro Commit, ohne Verlust und mit 54–65 s, bis wieder geschrieben werden kann ([der SQLite-Artikel](/de/posts/2026/10/sqlite-ausfallsicherheit-hetzner/)).

## Meine Faustregeln

- **Standard:** drei CNPG-Instanzen auf `local-path`, `ANY 1`, `dataDurability: preferred`. Das bedeutet keinen Verlust und etwa eine Minute, bis wieder geschrieben werden kann, und es ist performanter als eine Instanz auf einem Volume.
- **Kein Verlust mit einer Postgres Instanz:** eine CNPG-Instanz auf DRBD unter dem PVC. Mit einem Client ist das etwa so schnell wie `ANY 1`, es kommt mit nur einer Postgres-Kopie aus, statt drei, die Übernahme dauert aber etwas länger.
- **Einfach:** mit einer Instanz und Cloud Volume.
- **Backups:** immer mit barman nach S3 an einem **anderen** Standort. Ein Backup am selben Standort übersteht den Ausfall des Standorts nicht.
- **Auf k3s:** zuerst die Standard-StorageClasses in Ordnung bringen.
- **Lohnt sich nicht:** `remote_write` und drei Instanzen auf Volumes.

## Wie schnell ist ein dauerhafter Postgres-Commit?

Ein dauerhafter Commit wartet auf den Flush des WAL, also gibt die Disk die Untergrenze vor:

| | Mittel | p50 | p99 |
|---|---|---|---|
| lokale NVMe, fdatasync (pg_test_fsync: 0,28–0,31 ms) | 0,30–0,34 ms | 0,29–0,32 ms | 0,47–1,04 ms |
| Hetzner Volume, fdatasync (pg_test_fsync: 2,69 ms) | 2,50 ms | 2,41 ms | 5,73 ms (p99,9 9,6) |
| privates Netz, ICMP | | 0,19–0,24 ms | 0,30–0,50 ms |
| PostgreSQL `SELECT 1` | 0,26 ms | 0,25 ms | 0,41–0,45 ms |

Ein Flush auf dem Volume dauert ~8× so lang wie ein lokaler. Ein zweiter Lauf in fsn1 am Vortag ergab dasselbe: 2,77 ms gegenüber 0,38 ms.

## Was kostet synchrone Replikation?

Claude hat pgbench `-N` (Simple Update) auf reinem PostgreSQL 18.6 mit einem Primary und zwei Standbys ausgeführt, in jedem Replikationsmodus, auf lokalen Disks und auf einem Volume:

| Storage / Modus | 1 Client | 8 Clients | 32 Clients |
|---|---|---|---|
| lokal, ohne Replikation | 0,93 ms (1.079) | 0,93 ms (8.617) | 2,71 ms (11.832) |
| lokal, asynchron | 1,06 ms (945) | 1,12 ms (7.171) | 3,04 ms (10.530) |
| lokal, synchron `remote_write` | 1,90 ms (527) | 1,69 ms (4.730) | 3,50 ms (9.138) |
| lokal, synchron `on`, ein Standby | 2,30 ms (435) | 2,02 ms (3.968) | 3,90 ms (8.206) |
| **lokal, `ANY 1` von zwei** | **2,23 ms (449)**, p99 3,7 | **1,90 ms (4.212)**, p99 3,1 | 3,71 ms (8.625) |
| lokal, `remote_apply` | 2,37 ms (421) | 2,32 ms (3.455) | 4,18 ms (7.652) |
| **Volume, ohne Replikation** | **3,66 ms (274)**, p99 7,3 | **6,10 ms (1.311)**, p99 11,2 | 6,03 ms (5.306) |
| Volume, `ANY 1` | 4,85 ms (206) | 6,00 ms (1.334) | 7,84 ms (4.080) |

- Mittlere Latenz, TPS in Klammern. TPC-B-ähnlich zeigt dasselbe: 2,52 ms gegenüber 4,17 ms für einen Client, 3.669 gegenüber 1.191 TPS für acht.
- **Synchrone Replikation kostet ~1,3 ms pro Commit** auf lokalen Disks: mehr als der Roundtrip plus der Flush des Standbys (~0,55 ms). Der Rest sind vermutlich Prozess-Wake-ups auf geteilten vCPUs.
- **Sie schlägt das Volume trotzdem deutlich.** Mit einem Client braucht sie 39 % weniger Zeit pro Commit als eine einzelne Instanz auf einem Volume. Mit acht Clients hat sie den 3,2-fachen Durchsatz bei einem Viertel des p99.
- **`remote_write` lohnt sich nicht.** Es spart ~0,35 ms, kann aber bestätigte Schreibzugriffe verlieren, wenn der Primary und dieser Standby gemeinsam abstürzen.
- **Drei Instanzen auf Volumes vereinen das Schlechteste aus beiden Welten:** 4,85 ms pro Commit.
- **Das Pod-Netz summiert sich.** Über den `-rw`-Service, mit dem Client auf einem anderen Knoten, fügen die fünf Roundtrips pro Transaktion von pgbench ~2 ms hinzu: 4,31 ms für einen Client. Behalte die Roundtrips deiner App im Blick, nicht nur den Flush.

## Wie viel geht verloren, wenn der Primary ausfällt?

Claude hat k3s v1.36.2 und CloudNativePG 1.29.1 mit drei Instanzen auf `local-path` und `synchronous: {method: any, number: 1, dataDurability: preferred}` betrieben und den Server des Primary über die Hetzner-API hart ausgeschaltet, während pgbench schrieb.

- 112.483 bestätigte Schreibzugriffe, **0 verloren**.
- ~66 s lang wurde kein Schreibzugriff bestätigt, danach gab es noch eine Lücke von 4,4 s.
- Ablauf:
  1. +57,4 s: Kubernetes markiert den Knoten als nicht bereit;
  2. +60,1 s: CNPG startet die Übernahme;
  3. +61,4 s: neuer Primary;
  4. +68,0 s: erster bestätigter Schreibzugriff.
- Nach dem Einschalten streamte der alte Primary 89 s später wieder, ohne manuellen Schritt.

**Den größten Teil der Minute braucht Kubernetes, um zu bemerken, dass der Knoten weg ist, nicht CNPG.** Stellschrauben zum Ausprobieren sind:

- die Node-Monitor-Grace-Period des Controller Managers, die für den ganzen Cluster gilt;
- der CNPG-Operator mit zwei Replikaten oder eine kurze Unreachable-Toleration. Fällt der Operator zusammen mit dem Primary aus, wartet die Übernahme auf die Verdrängung des Operators, standardmäßig 300 s.

## Was passiert, wenn die Standbys wegfallen?

Claude hat erst einen Standby abgeschottet (Fencing), dann beide:

- Mit einem abgeschotteten Standby stockten die Schreibzugriffe nicht.
- Mit beiden stockten die Schreibzugriffe 27,3 s, bis CNPG `synchronous_standby_names` geleert hat, wie es `dataDurability: preferred` verspricht. Danach liefen sie asynchron weiter, und von 124.223 bestätigten Schreibzugriffen ging keiner verloren.
- Nach dem Aufheben des Fencings ging es von selbst zurück auf `ANY 1 ("pg-1","pg-3")`.

## Eine Instanz auf DRBD

Statt in Postgres zu replizieren, kann DRBD die Disk darunter replizieren, wie im [SQLite-Artikel](/de/posts/2026/10/sqlite-ausfallsicherheit-hetzner/). Claude hat k3s mit Piraeus Operator v2.12, LINSTOR 1.35 und DRBD 9.3 aufgesetzt wie dort: zwei Replikate auf n1 und n2, ein Tie-Breaker ohne Disk auf n3, Protokoll C (ein Schreibzugriff ist fertig, wenn beide Disks ihn haben). Darauf läuft eine CNPG-Instanz mit ihrem PVC auf DRBD und zum Vergleich eine auf `local-path` im selben Cluster. pgbench lief im Pod über den Unix-Socket, in zwei Läufen:

| eine CNPG-Instanz | 1 Client | 8 Clients | 32 Clients | TPC-B-ähnlich, 8 Clients |
|---|---|---|---|---|
| `local-path` | 1,08–1,10 ms (911–922) | 1,02–1,08 ms (7.397–7.869) | 2,94–3,28 ms (9.746–10.894) | 1,23–1,42 ms (5.622–6.510) |
| **DRBD, 2 Replikate** | **1,68–1,87 ms (536–597)**, p99 3,5–3,8 | **2,07–2,11 ms (3.801–3.869)** | 4,10–4,12 ms (7.768–7.809) | 2,27–2,40 ms (3.336–3.532) |

- **Die zweite Kopie kostet ~0,6–0,8 ms pro Transaktion.** Das ist etwa, was sie jedem Flush hinzufügt: `pg_test_fsync` hat 0,34 ms auf `local-path` und 0,95 ms auf DRBD gemessen.
- **Im Vergleich zu `ANY 1`** ist es mit einem Client etwas schneller (2,23 ms) und mit 8 und 32 Clients etwas langsamer (1,90 und 3,71 ms). Die `ANY 1`-Werte stammen aus dem anderen Test, also lies das als „etwa gleich“.
- **Eine Instanz auf einem Volume schlägt es deutlich:** 3,66 ms mit einem Client, 1.311 TPS mit acht.

Dann hat Claude den Server der Instanz viermal über die Hetzner-API hart ausgeschaltet, mit demselben Writer und derselben pgbench-Last wie oben:

- Insgesamt 246.766 bestätigte Schreibzugriffe, **0 verloren**.
- Im zweiten Lauf wurde 69,7, 72,1 und 79,5 s lang kein Schreibzugriff bestätigt, im ersten 107,5 s.
- Nach dem Einschalten dauerte es 156–162 s, bis DRBD auf beiden Knoten wieder UpToDate war, inklusive des Kompilierens des DRBD-Moduls beim Booten.

**Wie die Instanz den anderen Knoten findet.** CNPG wählt keinen Knoten. Bei einer Instanz gibt es keinen Standby, den es befördern könnte; CNPG erzeugt den Pod mit demselben PVC neu, und der Kubernetes-Scheduler platziert ihn. Er kann nur auf dem anderen Replikat landen, aus zwei Gründen:

1. Der CSI-Treiber von LINSTOR gibt dem Volume eine Node-Affinity auf die Knoten, die eine Kopie haben (`linbit.com/hostname` ist n1 oder n2), weil die StorageClass `allowRemoteVolumeAccess: "false"` setzt. Der Tie-Breaker auf n3 hat keine Kopie.
2. Der tote Knoten ist NotReady und hat einen Taint.

So sah die erste Übernahme des zweiten Laufs aus:

| nach dem Ausschalten | was passiert |
|---|---|
| +35,6 s | Der HA-Controller von Piraeus sieht, dass die DRBD-Ressource auf dem toten Knoten das Quorum verloren hat, setzt einen Taint auf den Knoten (`NodeStorageQuorumLost`) und verdrängt den Pod. |
| +49,9 s | Kubernetes markiert den Knoten als NotReady. Erst jetzt kann der verdrängte Pod verschwinden. |
| +56,2 s | CNPG: „Creating new Pod to reattach a PVC“. Der Scheduler setzt ihn auf n2. |
| +56,9 s | Das Volume ist auf n2 angehängt. |
| +58,9 s | Postgres startet und spielt sein WAL ab (Crash Recovery). |
| +62,3 s | CNPG markiert den Pod als Primary, damit zeigt der `-rw`-Service wieder auf ihn. |
| +71,0 s | Der erste bestätigte Schreibzugriff. |

- **Erkennung:** Der HA-Controller hat es nach 28–36 s bemerkt, Kubernetes nach 42–50 s. Wie bei `ANY 1` vergeht die meiste Zeit damit, zu bemerken, dass der Knoten weg ist.
- **Die Streuung kommt vom Anhängen des Volumes.** Der neue Pod kann erst starten, wenn das Volume auf dem toten Knoten freigegeben ist. Das dauerte im zweiten Lauf 1, 5 und 21 s und im ersten ~37 s, deshalb dauerte diese Übernahme 107,5 s.
- **Postgres selbst braucht 10–12 s** vom Start bis zum ersten Schreibzugriff: Crash Recovery und die Readiness-Probe.
- **Eine Instanz heißt kein PodDisruptionBudget** (`enablePDB: false`), also blockiert nichts die Verdrängung.

Der Nachteil ist derselbe wie im SQLite-Artikel: mehr Teile, das DRBD-Modul muss für den Kernel des Knotens gebaut werden, und mit zwei Kopien ist ein zweiter Ausfall während eines Resyncs ein Ausfall.

**Ist das die sparsamere Lösung?** Nur teilweise.

- **Sie spart zwei Postgres-Instanzen:** eine statt drei, also weniger CPU und RAM, und zwei Kopien der Daten statt drei.
- **Sie spart keine Server:** DRBD braucht den dritten Knoten als Tie-Breaker für sein Quorum, und Kubernetes will ohnehin drei Knoten. Der Tie-Breaker hat keine Kopie, er kann also ein kleiner Server sein, der andere Arbeit macht.
- **Dazu kommen Piraeus, LINSTOR und ein Kernel-Modul.** Was sie an RAM und CPU kosten, habe ich nicht gemessen. Bei einer einzelnen Datenbank kann das die Ersparnis auffressen; es lohnt sich, wenn DRBD ohnehin läuft, für mehrere Datenbanken, SQLite oder andere Volumes.
- **Sie gibt Wartung ohne Ausfall auf.** Mit drei Instanzen macht CNPG vor einem Postgres-Update, einer Konfigurationsänderung oder einem Drain des Knotens einen Switchover, mit Sekunden Unterbrechung. Mit einer Instanz ist jeder Neustart des Pods eine Ausfallzeit. Wie lang, habe ich nicht gemessen; nach der Crash Recovery und der Readiness-Probe oben schätze ich 10–30 s.
- **Sie gibt auch Lese-Replikate auf** und 2–40 s Übernahmezeit (70–108 s gegenüber ~68 s).

Also: Eine Instanz auf DRBD passt für wenige Datenbanken, bei denen eine kurze Unterbrechung bei Updates in Ordnung ist, und vor allem für einen Cluster, in dem DRBD ohnehin läuft. Drei CNPG-Instanzen bleiben die bessere Wahl, wenn Updates und Wartung das Schreiben nicht unterbrechen dürfen oder wenn du Lese-Replikate brauchst.

## Eine Falle auf k3s: zwei Standard-StorageClasses

k3s bringt `local-path` als Standard-StorageClass mit. Die Installation des Hetzner CSI fügt `hcloud-volumes` hinzu, ebenfalls als Standard.

- **`local-path` per `kubectl annotate` die Standard-Markierung zu nehmen, hält nicht.** k3s spielt sein mitgeliefertes `local-storage`-Manifest erneut ein, die Standard-Annotation inklusive.
- **Mit zwei Standards bekommt ein PVC ohne `storageClassName` die neueste.** Das kann sich unbemerkt ändern, und der PVC behält die Klasse, die er bekommen hat, für immer.
- **Die Lösung:** Mach eine Klasse zum einzigen Standard und verhindere, dass k3s das Manifest erneut einspielt, entweder mit einer Datei `local-storage.yaml.skip` im Manifest-Verzeichnis des Servers oder mit `--disable local-storage` und einem selbst deployten Provisioner. Nenne `local-path` dann explizit dort, wo du es willst, z. B. für CNPG.

## Wie Claude gemessen hat

Claude Code hat die Skripte geschrieben, sie in einem Wegwerf-Projekt bei Hetzner ausgeführt und danach alles wieder abgebaut. Der ganze Lauf hat 0,41 € gekostet.

- **Server:** drei cpx32 (4 geteilte vCPUs, 8 GB, lokale NVMe) in nbg1, auf getrennten Hosts (eine Spread Placement Group), ein privates Netz. Ein 10-GB-Volume auf dem ersten Server zum Vergleich.
- **Versionen:** PostgreSQL 18.6, k3s v1.36.2, CloudNativePG 1.29.1.
- **Flush und Netz:** fio und `pg_test_fsync` für den Flush der Disk, ICMP und `SELECT 1` für den Roundtrip.
- **Replikationsmodi:** pgbench über den Unix-Socket, Scale 50, 60 s pro Zelle, 1/8/32 Clients. Modi: ohne, asynchron, synchron `remote_write`, synchron `on` mit einem Standby, `ANY 1` von zwei, `remote_apply`.
- **DRBD:** ein zweiter Test am 19.10.2026, in zwei Läufen, zusammen 0,44 €: k3s v1.36.2, Piraeus Operator v2.12.0 mit LINSTOR 1.35.2 und DRBD 9.3.4, CloudNativePG 1.29.1 mit PostgreSQL 18.3, eine Instanz mit 10 GB auf einem Volume mit zwei Replikaten. Dieselben pgbench-Zellen im Pod, danach viermal der Knoten der Instanz ausgeschaltet; der Writer lief auf dem dritten Knoten, der nie ausgeschaltet wurde.
- **Übernahme:** ein hartes Ausschalten des Servers des Primary über die Hetzner-API, während pgbench schreibt, danach der Vergleich der bestätigten Schreibzugriffe mit denen, die überlebt haben.
- **Rauschen:** ein 60-s-Lauf pro Zelle, auf geteilten vCPUs, und eine Übernahme mit drei Instanzen; bei DRBD zwei Läufe pro Zelle und vier Übernahmen.
- **Nicht gemessen:** Im Test gab es kein WAL-Archiv. Die Archivierung liegt nicht im Commit-Pfad, aber die Restore-Zeit aus S3 ist hier nicht gemessen. Beim alten Aufbau, einer Instanz auf einem Volume, wurde keine Übernahme getestet. Den Pod umzuziehen heißt Verdrängung plus Detach und Attach des Volumes: mehrere Minuten mit den Standardwerten von Kubernetes (geschätzt).

Kleine Stolpersteine unterwegs:

- Die Hetzner-API meldet das Rechenzentrum eines Servers nicht mehr. Das Skript, das die Platzierung festhielt, ist daran abgestürzt.
- `--automount` der hcloud-CLI hat das neue Volume nicht eingehängt.
- fio braucht `--overwrite=1` für ehrliche fsync-Werte. Auf einer vorab angelegten Datei meldete es 1,0 ms statt 0,3 ms.
