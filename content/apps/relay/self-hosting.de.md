---
title: "Selbstbetrieb in Azure"
slug: "selbstbetrieb"
summary: "Bring your own Azure: der Relay läuft in Deiner Subscription, mit Lizenzschlüssel. Termindaten verlassen Deinen Mandanten nur zu Deinen Zielen."
weight: 30
---

Für alle, die Termindaten nicht durch einen Dritten leiten wollen oder dürfen: Gesundheitswesen, Beratung mit Verschwiegenheitspflicht, öffentliche Hand, strenge IT-Richtlinien. Du betreibst den Relay selbst in Deiner Azure-Subscription („Bring your own Azure“) oder in Deinem eigenen Kubernetes. Die Lizenz kostet dasselbe wie der Dienst; die Azure-Kosten liegen bei wenigen Euro im Monat und laufen über Deine Rechnung.

## Was Du brauchst

- eine Azure-Subscription mit dem Recht, eine Ressourcengruppe anzulegen und Rollen zuzuweisen (Owner, oder Contributor plus User Access Administrator);
- einen globalen Administrator bzw. Privileged Role Administrator im Microsoft-365-Mandanten für die Einwilligung;
- den Lizenzschlüssel aus der Kauf-E-Mail von Polar (oder aus dem Polar-Kundenportal);
- ein Ziel: Deine Webhook-URL oder ein Mitjas CRM.

## Schritte

1. **Entra-App anlegen.** Im Entra admin center eine App-Registrierung im eigenen Mandanten, Single-Tenant, ohne Redirect-URI. Unter API permissions → Microsoft Graph → Application permissions nur `Bookings.Read.All` hinzufügen, dann „Grant admin consent“. Ein Client Secret erzeugen und das Ablaufdatum in den Kalender eintragen. Besser als ein Secret ist ein Zertifikat aus Key Vault; die Vorlage unterstützt beides.
2. **Webhook-Secret erzeugen.** `docker run --rm git.paasbox.com/paasbox/bookings-relay:<version> secret` gibt ein `whsec_…` aus. Hinterlege es bei Deinem Empfänger ([Ereignisformat und Signaturprüfung](../ereignisformat/)).
3. **Ausrollen.** In der Azure Cloud Shell die Bicep-Vorlage mit `az deployment` anwenden: Region nach Wahl (z. B. `germanywestcentral`, Frankfurt), Tenant-Id, Client-Id und Secret der Entra-App, Lizenzschlüssel, Ziel-URL und Webhook-Secret, und ein Cron-Ausdruck als Intervall, z. B. `7 * * * *` für stündlich. Kürzer nur im Rahmen des Plans: Business 15 Minuten, Partner 5 Minuten. Die Vorlage legt einen Container Apps Job und einen Table-Storage-Account an; Secrets liegen in Key Vault.
4. **Ersten Lauf starten.** `az containerapp job start --name bkrelay-sync --resource-group bookings-relay`. Das Ergebnis steht im Ausführungsverlauf des Jobs. Beim ersten Lauf aktiviert der Relay den Lizenzschlüssel bei Polar; danach prüft er ihn höchstens einmal am Tag. Ein abgelehnter Schlüssel lässt den Lauf mit einer Meldung scheitern, die Variable, Grund und Abhilfe nennt.
5. **Firewall.** Ausgehend braucht der Relay `login.microsoftonline.com`, `graph.microsoft.com`, `api.polar.sh`, Deine Ziele und die Registry `git.paasbox.com`.

TODO(Mitja): Den genauen `az`-Aufruf und den Link zur Bicep-Vorlage ergänzen, sobald Image und Vorlage für Kunden abrufbar sind.

## Im Betrieb

- **Polar nicht erreichbar:** Der Relay arbeitet 14 Tage ab der letzten erfolgreichen Prüfung weiter und versucht es stündlich erneut. Danach pausiert er bis zur nächsten erfolgreichen Prüfung.
- **Abo gekündigt:** Polar widerruft den Schlüssel; der Relay hört mit der nächsten Prüfung auf, spätestens nach einem Tag.
- **Umzug** in eine andere Ressourcengruppe oder einen anderen Cluster: vorher die Aktivierung freigeben, mit `bookings-relay license deactivate` in der alten Umgebung oder im Polar-Kundenportal. Ein Schlüssel hat genau eine Aktivierung.
- **Stand ansehen:** `bookings-relay license status` zeigt Plan, Gültigkeit, letzte Prüfung und Fehler als JSON.
- **Updates:** neues Image-Tag im Job eintragen (`az containerapp job update … --image git.paasbox.com/paasbox/bookings-relay:<version>`). Neue Versionen kündige ich per E-Mail an.

## Was fließt wohin

Termindaten gehen von Microsoft Graph durch Deinen Relay zu Deinen Zielen. Zu Polar geht nur die Lizenzprüfung: Lizenzschlüssel, Aktivierungs-Id, Relay-Version und ein Label der Installation; keine Termin- oder Kundendaten, keine Entra-Tenant-Id, keine Postfachadressen. Ich habe keinen Zugang zu Deiner Installation und erhalte keine Termindaten; für diese Verarbeitung bin ich kein Auftragsverarbeiter. Microsoft (Azure) ist Dein Auftragsverarbeiter, nicht meiner.

## Im eigenen Kubernetes

Statt Azure geht auch Dein Cluster: ein Deployment mit SQLite auf einem Volume oder mit Postgres, Secrets inklusive `RELAY_LICENSE_KEY`, und `RELAY_ENTITLEMENTS=license`. Die Kustomize-Basis liefere ich mit dem Image.
