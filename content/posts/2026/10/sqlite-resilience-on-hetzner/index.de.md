---
title: "SQLite mit Litestream auf Hetzner Cloud"
summary: "Die Commit-Latenz von SQLite auf lokaler NVMe und auf einem Cloud Volume, Datenverlust und Wiederherstellungszeit von Litestream nach einem harten Ausschalten, ein Warm Standby mit dem Follow-Modus, und DRBD und rqlite als Optionen ohne Datenverlust, mit rqlite als Alternative mit der schnellsten Übernahme."
slug: "sqlite-ausfallsicherheit-hetzner"
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

Für kleine bis mittlere serverbasierte KI-Anwendungen nutze ich gern SQLite mit Litestream und wollte schon immer wissen, wie hoch die Commit-Latenz auf lokaler NVMe und auf einem Cloud Volume tatsächlich ist, wie viele Daten verloren gehen können und wie lange die Wiederherstellung dauert. Außerdem wollte ich Alternativen ohne Datenverlust (DRBD und rqlite) und ihre Vor- und Nachteile kennenlernen.

Claude Code hat mir diese Fragen mit Tests beantwortet, hier sind die Ergebnisse in Form einer kleinen Entscheidungshilfe:

{{< sqlite-decision >}}

## Meine Faustregeln

- **Standard:** SQLite + Litestream auf lokaler NVMe, mit einem Alarm auf den Rückstand der Replik. Das bedeutet weniger als eine Sekunde Verlust und Sekunden für den Restore der Daten.
- **Einfach, ohne Verlust:** SQLite + Litestream auf einem Hetzner Cloud Volume.
- **Schnell, ohne Verlust und auf Kubernetes:** DRBD unter dem PVC. Das kann ein gemeinsamer Mechanismus für SQLite, Dateien und sogar ein einzelnes Postgres sein.
- **Schnellster Failover, die App kann umgebaut werden:** rqlite

## Wie schnell ist ein dauerhafter SQLite-Commit?

SQLite auf lokaler NVMe ist mit `synchronous=FULL` wirklich schnell und mit `synchronous=NORMAL` extrem schnell, aber:

- `NORMAL` übersteht einen Absturz der App, aber keinen Stromausfall. Auf einer Cloud-VM zählt ein Ausfall des Hosts als Stromausfall.
- `FULL` ruft pro Commit fsync auf das WAL auf, also ist der Commit so schnell wie der Flush der Disk: 0,28 ms lokal, 2,43 ms auf einem Volume.

| | `synchronous=FULL` | `synchronous=NORMAL` |
|---|---|---|
| lokale NVMe | 0,33–0,38 ms, ~2.450 Commits/s | 13 µs, ~48.000/s |
| Hetzner Volume | 2,3–2,65 ms, ~290 Commits/s | 26–32 µs, aber p99,9 31–60 ms |

## Wie viel verliert Litestream?

Claude hat das mit einem Writer getestet, der 200 Zeilen/s mit `FULL` schreibt und jede bestätigte ID an einen anderen Server meldet. Dann hat Claude den Server über die Hetzner-API hart ausgeschaltet, aus dem Garage-S3 wiederhergestellt und gezählt.

Litestream hat in drei Läufen 110, 129 und 22 Zeilen verloren, also **582 / 645 / 110 ms** an Schreibzugriffen. Mit `NORMAL` waren es 139 Zeilen, 695 ms. Das Standard-Sync-Intervall von Litestream ist 1 s, und der gemessene Datenverlust blieb unter diesem Intervall.

Ein Restore über Standorte hinweg dauerte für 100 MB 2,4 s und für 1 GB 21 s.

Als S3 für 72 s abgeschaltet wurde, ist Folgendes passiert:

- Die App hat nichts bemerkt (langsamster Commit 26 ms).
- Die Replik fiel ~65 s zurück und holte dann in ~9 s auf.
- **Litestream hat nichts geloggt.** Also: Alarme sollten auf seinen Metriken beruhen, nicht auf seinen Logs.

Übrigens: Der Bucket enthielt direkt nach dem ersten Snapshot ~3× die Datenbank.

## Der Follow-Modus von Litestream

Litestream v0.5 kann eine zweite Kopie aktuell halten: `litestream restore -f` stellt einmal wieder her, fragt dann die Replik ab und spielt neue Änderungen ein, standardmäßig jede Sekunde. Die Kopie lässt sich lesen.

Claude hat denselben Writer und Logger verwendet, Litestream auf dem Primary, `restore -f` auf einem zweiten Server und dort einen Leser, der alle 100 ms die neueste Zeile liest. Claude hat wieder den Primary über die Hetzner-API ausgeschaltet, und ein Skript hat sofort den Standby befördert: 

1. warten, bis der Follow-Modus nichts mehr einspielt, 
2. ihn stoppen, 
3. `PRAGMA quick_check` ausführen, 
4. den Writer und Litestream dort starten (mit einem neuen Replik-Pfad).

| Intervalle | verloren | Rückstand des Standbys, p50 / p99 | Promote |
|---|---|---|---|
| 1 s (Standard), 3 Läufe | 71–120 Zeilen, **355–612 ms** | 1,3 / 1,8–2,0 s | **3,1–3,2 s** |
| 250 ms, 2 Läufe | 14–22 Zeilen, **70–110 ms** | 0,15–0,18 / 0,31–0,35 s | **1,2 s** |
| 1 s, mit einer 1-GB-Datenbank | 153 Zeilen, 770 ms | 1,1 / 1,7 s | 4,1 s |

- „Intervalle“ meint `monitor-interval` und `sync-interval` von Litestream auf dem Primary und `-follow-interval` auf dem Standby.
- **Der Verlust ist derselbe wie bei einem Restore.** Was der Follow-Modus spart, ist der Restore: Die Kopie ist schon da, in jeder Größe. Ein Restore von 1 GB dauerte 21 s, die Beförderung zum Writer mit 1 GB 4,1 s, davon 1 s für `quick_check`.
- **Die Beförderung ist vor allem Warten.** Das Skript wartet drei ruhige Abfrageintervalle ab, um sicher zu sein, dass der letzte Upload des Primary angekommen ist. Stoppen, Prüfen und Starten dauern ~0,1 s.
- **Die Ausfallerkennung kommt hinzu.** Im Lab hat Claude den neuen Writer befördert, sobald der API-Aufruf zum Ausschalten zurückkam, und der dauerte selbst 7–9 s. Schreibzugriffe waren 8–11 s nicht möglich.
- **250-ms-Intervalle** senken den Verlust auf ~0,1 s und die Beförderung auf ~1 s. Der Preis sind etwa viermal so viele S3-Anfragen: ein Upload und ein Listing pro Intervall (nicht gemessen).
- **Leser auf dem Standby** treffen manchmal auf die Sperre des Follow-Modus, während er schreibt: 0,4–1,7 % der Lesezugriffe ohne Busy-Timeout. Ein `busy_timeout` verdeckt das.
- Ein Standby mit 1 GB war nach 52 s bereit: der erste Snapshot-Upload des Primary und der Restore. Seine ersten Lesezugriffe lagen 37 s zurück, und er holte innerhalb von 2 s auf.
- Alle sechs `quick_check`s meldeten ok.

Der neue Primary sollte nie auf den alten Replik-Pfad schreiben. Der alte Primary kann zurückkommen und weiter dorthin schreiben.

## DRBD

Claude hat Piraeus Operator v2.12 mit LINSTOR 1.35 und DRBD 9.3 auf k3s v1.36 verwendet, um zwei Replikate und einen Tie-Breaker ohne Disk auf dem dritten Knoten zu betreiben, und Protokoll C konfiguriert (ein Schreibzugriff ist fertig, wenn beide Disks ihn haben). SQLite nutzt dann PVCs auf diesem Storage.

| in einem Pod | fsync | SQLite-`FULL`-Commit |
|---|---|---|
| local-path | 0,33 ms | 0,39–0,40 ms |
| LVM thin | 0,43 ms | 0,48 ms |
| DRBD, 1 Replikat | 0,45 ms | 0,45–0,47 ms |
| **DRBD, 2 Replikate** | **0,93 ms** | **0,90–0,93 ms** |

DRBD war für mich die größte Überraschung: Die zweite Kopie kostet nur ~0,5 ms pro fsync und ist damit immer noch ~2,5× schneller als ein Hetzner Cloud Volume. Sie ist ~2,4× schneller als Postgres mit einem synchronen Standby (2,23 ms). Übernahme nach dem Ausschalten des Knotens: 54–65 s bis zum ersten bestätigten Schreibzugriff ohne Datenverlust. Der HA-Controller verdrängt den Pod nach ~20–35 s. Der neue Pod wartet trotzdem, bis der Knoten NotReady ist (~50 s). Und: Die Ausfallzeit ist etwa dieselbe wie mit CNPG (eine Minute).

Der Nachteil: Es sind mehr Teile, die Einrichtung ist aufwendiger, und DRBD hat so seine Eigenheiten:

- **Ein Fenster für einen Doppelfehler.**
  - Ich habe den Primary ausgeschaltet, während der andere Knoten noch synchronisierte (39 %).
  - DRBD hat sich zu Recht geweigert, eine unvollständige Kopie zu befördern, und das Volume blieb nicht verfügbar, bis die Quelle zurückkam. Nichts ging verloren, aber es ließ sich auch nichts schreiben.
  - Zwei Kopien heißt: Ein zweiter Ausfall während eines Resyncs ist ein Ausfall.
- **`resource list` von LINSTOR zeigte UpToDate, während DRBD noch SyncTarget war.** Prüfe `drbdsetup status`.
- **Der Module Loader von Piraeus kompiliert DRBD bei jedem Boot aus den Quellen**: 75 s auf einem cpx32. Auf einem imagebasierten Betriebssystem solltest du
  das Modul ins VM-Image aufnehmen.
- **Wiedereintritt nach dem Einschalten**: 2–3 Minuten, inklusive dieses Kompilierens und eines gedrosselten Resyncs.

## rqlite

Claude hat rqlite v10.6.0 auf drei stimmberechtigten Knoten auf cpx32 betrieben und die HTTP-API verwendet.

| | pro Schreibzugriff, 1 Client | Schreiben nicht möglich nach einem harten Ausschalten | verloren |
|---|---|---|---|
| reines SQLite `FULL` | 0,33–0,38 ms | bis der Server zurück ist | die Daten dieses Servers |
| SQLite + Litestream | dasselbe | Restore + ein neuer Server | 0,1–0,7 s |
| SQLite + Litestream, Follow-Standby | dasselbe | Erkennung + 1–3 s | 0,1–0,6 s |
| SQLite auf DRBD | 0,90–0,93 ms | 50–65 s | 0 |
| Postgres CNPG `ANY 1` (anderer Artikel) | 2,23 ms | ~70 s | 0 |
| **rqlite** | **3,65–4,34 ms** über HTTP | **2,0–3,6 s** | **0** von 74.173 |

- Warum ist die Übernahme so schnell? Eine Raft-Wahl dauert etwa eine Sekunde, und nichts wartet darauf, dass Kubernetes einen toten Knoten bemerkt.
- Warum ist jeder Schreibzugriff so langsam? rqlite selbst kostet ~2 ms (HTTP, JSON, das fsync seines Logs), und die Replikation fügt ~1,7 ms hinzu.
- `?queue` macht Schreibzugriffe 0,5 ms schnell, bestätigt aber vor dem Konsens. Dabei gingen die letzten ~5 ms an Schreibzugriffen verloren (2 Zeilen).
- Wenn zwei von drei Knoten ausfallen, stoppt das Schreiben, und nur noch Lesezugriffe mit `none` antworten.
- Die Backups sind periodisch. Als alle drei Knoten 41 s nach einem Upload verloren gingen, waren 42 s an Schreibzugriffen weg,
  während Litestream fortlaufend liefert.
- Was muss sich in der App ändern?
  - ein HTTP-Client statt der SQLite-Bibliothek;
  - ein Request ist eine Transaktion;
  - der Client muss alle Knoten kennen, kurze Timeouts nutzen und idempotent wiederholen;
  - er wählt die Lesekonsistenz pro Abfrage.

## Die Ergebnisse

| Aufbau | pro dauerhaftem Commit | Verlust, wenn ein Server ausfällt | bis wieder geschrieben werden kann | Server |
|---|---|---|---|---|
| SQLite auf lokaler NVMe, ohne Replikation | 0,33–0,38 ms | alles auf diesem Server | bis der Server zurück ist | 1 |
| **SQLite + Litestream** | 0,33–0,38 ms | **0,11–0,65 s** | ein Restore (100 MB: 2,4 s, 1 GB: 21 s) und ein neuer Server: Minuten | 1 |
| **SQLite + Litestream + Follow-Standby** | 0,33–0,38 ms | 0,36–0,61 s (1-s-Intervalle), 0,07–0,11 s (250 ms) | **1,2–3,2 s** plus Ausfallerkennung (1 GB: 4,1 s) | 2 |
| SQLite auf einem Hetzner Volume | 2,3–2,65 ms | 0, wenn nur der Server ausfällt | das Volume neu anhängen: Minuten (geschätzt) | 1 |
| **SQLite auf DRBD**, 2 Replikate | 0,90–0,93 ms | **0** | 54–65 s | 3 (2 und ein Tie-Breaker) |
| **rqlite**, 3 Knoten | 3,65–4,34 ms (über HTTP) | **0** | **2,0–3,6 s** | 3 |

Das Standard-Sync-Intervall von Litestream ist 1 s, und der Datenverlust blieb im Test darunter.

Zum Vergleich: **Postgres mit CloudNativePG** und drei Instanzen auf lokalen Disks mit einem synchronen Standby (`ANY 1`) braucht mit einem Client etwa 2,23 ms pro Commit, verliert nach einem harten Ausschalten des Servers keine Daten und ist etwa 70 s ausgefallen, bis wieder geschrieben werden kann.

## Wie Claude gemessen hat

Claude Code hat die Skripte geschrieben, sie in einem Wegwerf-Projekt bei Hetzner ausgeführt und danach alles wieder abgebaut. Drei Läufe haben zusammen 1,10 € gekostet.

- **Server:** drei cpx32 (4 geteilte vCPUs, 8 GB) in nbg1, auf getrennten Hosts (eine Spread Placement Group), ein privates Netz, Ubuntu 24.04.
- **S3-Ziel:** Als Ziel für Litestream und rqlite habe ich Garage v2.4.1 auf einem cx23 in fsn1 aufgesetzt, um Ausfälle des Cloud-Speichers zu simulieren.
- **Versionen:** SQLite 3.45.1, Litestream v0.5.17, Piraeus v2.12.0 mit LINSTOR 1.35.2 und DRBD 9.3.4 auf k3s v1.36.2, rqlite v10.6.0.
- **Commit-Latenz:** fio und `pg_test_fsync` für den Flush der Disk, danach ein Python-Writer mit einer Zeile pro Transaktion im WAL-Modus.
- **Datenverlust:** Der Writer schreibt 200 Transaktionen pro Sekunde und schickt jede bestätigte ID an einen Logger auf einem anderen Server. Ich habe den Server des Writers über die Hetzner-API hart ausgeschaltet, ihn wiederhergestellt oder einen anderen Server zum neuen Writer befördert und die höchste bestätigte ID mit der höchsten verglichen, die überlebt hat.
- **Bis wieder geschrieben werden kann:** bei DRBD vom Ausschalten bis zum ersten bestätigten Schreibzugriff, bei rqlite wie lange Schreibzugriffe fehlschlugen, bei Litestream die Dauer des Restores, beim Standby die Dauer des Skripts, das ihn befördert.
