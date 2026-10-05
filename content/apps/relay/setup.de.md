---
title: "Einrichtung"
slug: "einrichtung"
summary: "Vom Kauf bis zum ersten Ereignis: Einwilligung erteilen, Ziel anlegen, Signatur prüfen."
weight: 10
---

So kommt Dein erstes Ereignis an. Du brauchst einen Administrator Deines Microsoft-365-Mandanten (globaler Administrator oder Privileged Role Administrator) und einen Endpunkt, der HTTPS-POSTs annimmt, oder ein Mitjas CRM.

## 1. Plan wählen

Kaufe einen Plan oder starte den 30-Tage-Test über den Checkout auf der [Produktseite](../). Polar stellt die Rechnung und schickt eine Bestätigung per E-Mail. Mit dem Kauf entsteht Dein Mandant im Relay; die Einwilligung steht zunächst auf „ausstehend“.

## 2. Einwilligung erteilen

Du bekommst von mir einen Einwilligungslink (`consent_url`). Ein Administrator Deines Mandanten öffnet ihn, meldet sich bei Microsoft an und sieht den Dialog von Microsoft Entra: Die App bittet um `Bookings.Read.All`, lesend, für Anwendungen. Nach der Zustimmung landet der Administrator wieder beim Relay.

Was dabei passiert: Der Relay vertraut dem Rückruf nicht blind, sondern holt sich selbst ein Token für Deinen Mandanten und prüft, dass die Berechtigung wirklich erteilt wurde. Widerrufst Du sie später im Entra-Portal, pausiert der Relay Deinen Mandanten.

## 3. Buchungskalender und Intervall

Standardmäßig liest der Relay alle Buchungskalender Deines Mandanten. Du kannst ihn auf einzelne Kalender beschränken (die Postfachadresse, z. B. `beratung@contoso.com`). Der Plan begrenzt die Zahl der Kalender und das kürzeste Intervall; überzählige Kalender bleiben außen vor, und der Abgleich meldet das als `limited`.

## 4. Ziel anlegen

Ein Ziel ist eine Webhook-URL (`https://…`) oder ein Mitjas CRM. Für eine Webhook-URL erzeugt der Relay ein Secret `whsec_…`, das Du genau einmal siehst, beim Anlegen. Hinterlege es bei Deinem Empfänger; damit prüft er die Signatur ([Ereignisformat und Signaturprüfung](../ereignisformat/)). Für Mitjas CRM brauchst Du die Basis-URL des CRM und ein Service-Token mit den Scopes `read,write`.

In der Beta pflege ich Kalender, Intervall und Ziele für Dich über die Admin-API; eine Selbstbedienung gibt es noch nicht. Schick mir die Werte per E-Mail, Secrets gehen nie per Mail, die erzeugt der Relay.

## 5. Ersten Abgleich auslösen

Der Scheduler startet den ersten Abgleich automatisch. Wenn es schneller gehen soll, löse ihn aus: `POST /sync`. Danach siehst Du im Status Deines Mandanten, wann zuletzt abgeglichen wurde, wie viele Termine im Fenster lagen und ob etwas als Dead Letter hängen blieb.

Das Fenster reicht von gestern bis 90 Tage in die Zukunft. Termine, die beim ersten Abgleich schon darin liegen, kommen als `created`; Du bekommst also zu Beginn alle anstehenden Termine einmal.

## Checkliste

- [ ] Plan gekauft oder Test gestartet
- [ ] Einwilligung erteilt, Mandant im Relay auf „aktiv“
- [ ] Kalender und Intervall festgelegt
- [ ] Ziel angelegt, Secret beim Empfänger hinterlegt
- [ ] Signaturprüfung beim Empfänger getestet
- [ ] Erstes `created`-Ereignis angekommen
