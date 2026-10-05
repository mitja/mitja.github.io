---
title: "Mitjas Relay"
subtitle: "Webhooks für Microsoft Bookings"
kicker: "App"
status: "Beta"
status_note: "Beta: Der Relay ist gegen einen Nachbau von Microsoft Graph und Ende-zu-Ende mit Mitjas CRM geprüft, aber noch nicht gegen einen echten Microsoft-365-Mandanten gelaufen. Die ersten Kunden begleite ich persönlich."
teaser: "Bookings meldet neue, geänderte und abgesagte Termine nicht nach außen. Der Relay gleicht die Kalender regelmäßig ab und liefert jede Änderung als signierten Webhook an Dein System, ohne Termininhalte zu speichern."
summary: "Microsoft Bookings hat keine Webhooks. Mitjas Relay gleicht Deine Buchungskalender regelmäßig ab und liefert jeden neuen, geänderten oder abgesagten Termin als signiertes Ereignis an Deinen Endpunkt oder an Mitjas CRM. Termininhalte werden nicht gespeichert."
primary:
  text: "30 Tage kostenlos testen"
  url: "TODO(Mitja): Polar-Checkout-Link"
secondary:
  text: "Fragen? hi@mitjamartini.com"
  url: "mailto:hi@mitjamartini.com?subject=Mitjas%20Relay"
trademark: "Mitjas Relay ist ein unabhängiges Produkt und steht in keiner Verbindung zu Microsoft. Microsoft und Microsoft Bookings sind Marken der Microsoft-Unternehmensgruppe."
docs_heading: "Dokumentation"
layout: product
cascade:
  layout: appdoc
  showDate: false
  showDateUpdated: false
  showReadingTime: false
  showWordCount: false
  showTableOfContents: true
  showPagination: false
  showTaxonomies: false
  showAuthor: false
  showHero: false
  sharingLinks: false
showDate: false
showReadingTime: false
showWordCount: false
showTableOfContents: false
showPagination: false
sharingLinks: false
plans:
  - name: "Starter"
    price: "9 € / Monat"
    yearly: "oder 90 € / Jahr"
    features: ["1 Buchungskalender", "Abgleich alle 60 Minuten", "1 Ziel"]
    checkout: "TODO(Mitja): Polar-Checkout-Link"
    cta: "Starter testen"
  - name: "Business"
    price: "29 € / Monat"
    yearly: "oder 290 € / Jahr"
    features: ["5 Buchungskalender", "Abgleich alle 15 Minuten", "3 Ziele"]
    checkout: "TODO(Mitja): Polar-Checkout-Link"
    cta: "Business testen"
  - name: "Partner"
    price: "ab 99 € / Monat"
    yearly: "für Dienstleister und MSPs"
    features: ["50 Buchungskalender", "Abgleich alle 5 Minuten", "10 Ziele"]
    checkout: "TODO(Mitja): Polar-Checkout-Link"
    cta: "Partner anfragen"
---

## Das Problem

Microsoft Bookings meldet Termine nicht nach außen. Microsoft Graph bietet für Bookings keine Change Notifications, und der Power-Automate-Connector ist Preview, auf fünf Flows je Postfach begrenzt und braucht für eigene Webhooks eine Premium-Lizenz. Wer eine Buchung im CRM, im Ticketsystem oder im eigenen Tool sehen will, muss selbst abfragen.

## So funktioniert es

1. **Einwilligung.** Ein Administrator Deines Microsoft-365-Mandanten öffnet einen Link und erteilt dem Relay die Leseberechtigung `Bookings.Read.All`. Mehr Rechte braucht er nicht, und Du kannst sie jederzeit im Entra-Portal widerrufen.
2. **Abgleich.** Der Relay liest Deine Buchungskalender regelmäßig über Microsoft Graph: alle 60, 15 oder 5 Minuten, je nach Plan. Ein Fingerabdruck je Termin erkennt, was sich wirklich geändert hat: Zeit, Dienst, Kunde, Antworten, Teams-Link. Eine andere Schreibweise der Zeitzone ist keine Änderung.
3. **Zustellung.** Jeder neue, geänderte oder abgesagte Termin wird ein Ereignis im Format CloudEvents 1.0, signiert nach Standard Webhooks (HMAC-SHA256), mit einer stabilen Id zum Deduplizieren. Ziel ist Dein eigener Endpunkt oder direkt Mitjas CRM. Zustellung mindestens einmal, mit Wiederholungen, Backoff und sichtbaren Dead Letters.

Bis zu einem Intervall Verzögerung sind Teil des Prinzips: Der Relay fragt, Microsoft pusht nicht. Für die meisten Anwendungsfälle, Benachrichtigungen, CRM-Einträge, Rechnungen, ist das ausreichend.

## Datenschutz

- **Keine Termininhalte im Relay.** Namen, E-Mail-Adressen und Notizen werden aus Graph geholt, weitergereicht und nicht gespeichert, weder in der Datenbank noch in Dead Letters. Gespeichert werden nur Termin-Id, Fingerabdruck (ein Hash), letzter Start und Ende und der Zustellstand, bis der Termin vorbei ist.
- **Logs ohne Inhalte.** Logs enthalten Ids, Zahlen und Fehlercodes; ein Test sichert das ab.
- **Rollen nach DSGVO.** Im Dienst (SaaS) bist Du Verantwortlicher für die Daten in Bookings, ich bin Auftragsverarbeiter nach Art. 28 DSGVO; dafür gibt es einen Auftragsverarbeitungsvertrag. Der Dienst läuft auf Kubernetes in Deutschland (Hetzner, Nürnberg).
- **Selbstbetrieb.** Wer Termindaten nicht durch Dritte leiten will oder darf, betreibt den Relay mit einem Lizenzschlüssel in der eigenen Azure-Subscription oder im eigenen Kubernetes. Dann fließen Termindaten nur von Deinem Mandanten zu Deinen Zielen; ich erhalte sie nie und bin dafür kein Auftragsverarbeiter. Nach außen geht nur die Lizenzprüfung bei Polar: Schlüssel, Aktivierungs-Id und Version, keine Termin- oder Mandantendaten.
- **Sicherheit.** Nur lesende Graph-Berechtigung, Transport nur über TLS, Ziel-Secrets AES-256-GCM-versiegelt, Container ohne Root und schreibgeschützt.

## Pläne

Alle Pläne mit 30 Tagen kostenlosem Test. Zahlung über Polar als Merchant of Record: Rechnung mit ausgewiesener Umsatzsteuer, bei Firmen mit USt-IdNr. per Reverse Charge. Der Selbstbetrieb mit Lizenzschlüssel kostet dasselbe wie der Dienst: gleiche Funktionen, gleiche Grenzen, nur der Ort ist anders.

{{< plans >}}

TODO(Mitja): Polar-Checkout-Links eintragen, Partner-Preis bestätigen, AVV bereitstellen.

## Häufige Fragen

**Wie schnell kommt ein Ereignis an?**\
Spätestens ein Intervall nach der Änderung: 60, 15 oder 5 Minuten je nach Plan. Ein Aufruf von `POST /sync` stößt einen sofortigen Abgleich an.

**Was passiert, wenn mein Endpunkt ausfällt?**\
Der Relay wiederholt mit Backoff (bis zu sechs Stunden Abstand) und legt nach zehn Fehlschlägen einen Dead Letter ab, den Du ansehen und erneut zustellen kannst. Ein ausgefallenes Ziel bremst die anderen nicht.

**Kann ich mehrere Ziele beliefern?**\
Ja, je nach Plan 1, 3 oder 10 Ziele, jedes mit eigenem Secret und eigenem Zustellstand.

**Brauche ich Power Automate oder Azure?**\
Nein. Einmal Admin-Einwilligung, dann kommen Webhooks. Azure brauchst Du nur, wenn Du den Relay selbst dort betreiben willst.

**Welche Daten stehen im Ereignis?**\
Start und Ende, Dienst, Mitarbeitende, Kunde mit Name, E-Mail, Telefon und Antworten, Online-Status und Teams-Link, Ort, Notizen. Das Format steht in [Ereignisformat und Signaturprüfung](ereignisformat/). Bei Absagen nur Ids und der letzte bekannte Zeitraum, weil der Termin bei Microsoft schon weg ist.

**Was ist mit dem Microsoft-Bookings-Connector für Power Automate?**\
Für einen Kalender und ein, zwei Flows innerhalb von Microsoft 365 reicht er. Der Relay ist für mehrere Ziele, ein einheitliches signiertes Format, zuverlässige Zustellung und Betrieb in der EU oder bei Dir gebaut.

## Support

E-Mail an [hi@mitjamartini.com](mailto:hi@mitjamartini.com?subject=Mitjas%20Relay), Antwort in der Regel am nächsten Werktag. Support-Fälle bearbeite ich mit Logs, die keine Termininhalte enthalten. Beim Selbstbetrieb liefere ich das Image und die Vorlage; Betrieb, Überwachung und Updates der Installation liegen bei Dir.
