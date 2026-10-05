---
title: "Grenzen und FAQ"
slug: "grenzen"
summary: "Was der Relay nicht tut, was noch nicht geprüft ist, und Antworten auf häufige Fragen."
weight: 40
---

## Grenzen

- **Verzögerung bis zu einem Intervall.** Der Relay fragt Microsoft Graph, Microsoft pusht nicht. Wer Sekunden braucht, ist mit dem Power-Automate-Connector innerhalb von Microsoft 365 besser bedient; ein Anstoß vom Connector an den Relay ist denkbar, aber nicht gebaut.
- **Fenster von gestern bis 90 Tage voraus.** Termine weiter in der Zukunft kommen, sobald das Fenster sie erreicht. Ein Termin, der auf später als 90 Tage verschoben wird, kommt als `updated` mit dem neuen Stand aus dem Einzelabruf; kehrt er ins Fenster zurück, kann ein weiteres `updated` folgen.
- **Vergangene Termine werden still vergessen.** Ein Termin, der schon vorbei ist, wenn er verschwindet, erzeugt kein `cancelled`.
- **Mindestens einmal, nicht genau einmal.** Wiederholungen tragen dieselbe `id`; Dein Empfänger dedupliziert darauf.
- **Keine Selbstbedienung in der Beta.** Kalender, Intervall und Ziele pflege ich über die Admin-API für Dich.
- **Plangrenzen werden durchgesetzt.** Überzählige Kalender und Ziele fallen weg, und der Abgleich meldet `limited`; ein zu kurzes Intervall wird auf das Minimum des Plans angehoben.
- **Lizenzprüfung ist eine Erinnerung, kein Kopierschutz.** Sie sorgt dafür, dass ein gekündigtes Abo nicht aus Versehen weiterläuft. Für Firmenkunden zählen die Lizenzbedingungen.

## Was noch nicht geprüft ist

Der Relay ist gegen einen Nachbau von Microsoft Graph und Microsoft Entra, gegen SQLite, Postgres und Azurite und Ende-zu-Ende mit Mitjas CRM getestet; die Signatur gegen den offiziellen Testvektor von Standard Webhooks. Noch nicht geprüft sind:

- ein echter Microsoft-365-Mandant und echtes Graph: der Feldumfang von `calendarView`, ob Termin-Ids über Änderungen stabil bleiben, Drosselung in der Praxis;
- eine echte Admin-Einwilligung;
- Polar live, auch die Lizenzschlüssel;
- das Ausrollen in Azure mit der Bicep-Vorlage.

Deshalb Beta. Die ersten Kunden begleite ich persönlich, und diese Liste wird kürzer.

## Häufige Fragen

**Welche Berechtigung braucht der Relay in meinem Mandanten?**
Nur `Bookings.Read.All` als Anwendungsberechtigung, lesend. Feiner als mandantenweit geht es bei Microsoft Graph für Bookings nicht; der Relay liest aber nur die konfigurierten Kalender.

**Sieht der Relay meine Kundendaten?**
Während eines Abgleichs im Arbeitsspeicher, ja; das ist nötig, um sie Dir zuzustellen. Gespeichert werden sie nicht. Beim Selbstbetrieb sieht sie niemand außer Dir.

**Was passiert bei Gruppenbuchungen?**
Ein weiterer Kunde an einem bestehenden Termin ist ein `updated`, kein `created`. Das Feld `customers` enthält alle.

**Erkennt der Relay, was sich geändert hat?**
Er erkennt, dass sich etwas Relevantes geändert hat, und liefert den neuen Stand. Welches Feld es war, musst Du mit Deinem letzten Stand vergleichen.

**Kann ich den Abgleich sofort anstoßen?**
Ja, `POST /sync` mit Deinem Token, etwa als Knopf in Deinem Tool.

**Was kostet Azure beim Selbstbetrieb?**
Ein Container Apps Job, der ein paar Mal pro Stunde wenige Sekunden läuft, und ein Table-Storage-Account: in der Praxis wenige Euro im Monat, über Deine Azure-Rechnung.

**Wie kündige ich?**
Im Polar-Kundenportal, jederzeit zum Periodenende. Beim Dienst werden Zustand und Ziel-Secrets Deines Mandanten gelöscht; übrig bleiben die Abo-Eckdaten für die Buchhaltung. Beim Selbstbetrieb hört der Relay mit der nächsten Lizenzprüfung auf.
