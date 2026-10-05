---
title: "Ereignisformat und Signaturprüfung"
slug: "ereignisformat"
summary: "CloudEvents 1.0, signiert nach Standard Webhooks. Felder, Typen, Ids und wie Dein Empfänger die Signatur prüft."
weight: 20
---

## Das Ereignis

Jede Zustellung ist ein `POST` mit `Content-Type: application/cloudevents+json` und einem CloudEvent 1.0 im Body:

```json
{
  "specversion": "1.0",
  "id": "bkr_61e06ee8…",
  "source": "/bookings-relay/tenants/<entra-tenant-id>/businesses/beratung@contoso.com",
  "type": "com.microsoft.bookings.appointment.created",
  "subject": "<appointment-id>",
  "time": "2026-10-04T20:26:00Z",
  "datacontenttype": "application/json",
  "data": {
    "tenant_id": "…",
    "business_id": "beratung@contoso.com",
    "appointment_id": "…",
    "self_service_appointment_id": "…",
    "start": "2026-10-06T09:00:00Z",
    "end": "2026-10-06T09:30:00Z",
    "duration_minutes": 30,
    "service_id": "…",
    "service_name": "Erstgespräch",
    "staff_member_ids": [],
    "customer": {"name": "Erika Mustermann", "email": "erika@beispiel.de", "phone": "+49 30 1234567", "answers": {"Firma": "Beispiel GmbH"}},
    "customers": [],
    "answers": {"Firma": "Beispiel GmbH"},
    "answers_by_question_id": {"q-firma": "Beispiel GmbH"},
    "online": true,
    "join_url": "https://teams.microsoft.com/l/meetup-join/…",
    "location": "…",
    "customer_notes": "…",
    "created_at": "…",
    "updated_at": "…",
    "fingerprint": "989a…"
  }
}
```

### Typen

| `type` | Wann |
|---|---|
| `com.microsoft.bookings.appointment.created` | Termin neu im Fenster (gestern bis 90 Tage voraus) |
| `com.microsoft.bookings.appointment.updated` | Fingerabdruck anders: Zeit, Dienst, Mitarbeitende, Kunde, Antworten, Online-Status, Teams-Link, Ort oder Label |
| `com.microsoft.bookings.appointment.cancelled` | Termin fehlt im Fenster und ist bei Microsoft nicht mehr abrufbar. Trägt nur Ids, letzten bekannten Start und Ende |

Zeiten sind UTC. Eine andere Schreibweise der Zeitzone oder die Umstellung auf Sommerzeit erzeugt kein `updated`.

### Ids

- `id` ist stabil je Termin, Typ und Fingerabdruck (`bkr_` + SHA-256). Eine Wiederholung trägt dieselbe Id. Dedupliziere darauf; Zustellung ist mindestens einmal.
- `appointment_id` ist die Id aus Microsoft Graph. `self_service_appointment_id` kommt mit, weil Microsoft diese für Zuordnungen über Änderungen hinweg empfiehlt.

## Signatur prüfen

Die Signatur folgt [Standard Webhooks](https://www.standardwebhooks.com/). Drei Header kommen mit:

```
webhook-id: bkr_61e06ee8…
webhook-timestamp: 1759609560
webhook-signature: v1,K5oZfzN95Z9UVu1EsfQmfVNQhnkZ2pfW…
```

Die Signatur ist `base64(HMAC-SHA256(secret, "<webhook-id>.<webhook-timestamp>.<body>"))`. Das Secret ist das `whsec_…`, das Du beim Anlegen des Ziels gesehen hast; der Teil nach `whsec_` ist Base64 und ergibt den Schlüssel.

Prüfe so:

1. Lies den Body als rohe Bytes, bevor irgendetwas ihn parst oder umformatiert.
2. Lehne Zeitstempel ab, die älter als fünf Minuten sind (Schutz vor Wiederholung).
3. Berechne den HMAC über `id.timestamp.body` mit dem dekodierten Schlüssel.
4. Vergleiche in konstanter Zeit mit jeder `v1,…`-Signatur im Header (es können mehrere stehen, durch Leerzeichen getrennt).

Für die meisten Sprachen gibt es fertige Bibliotheken auf standardwebhooks.com. Ein Beispiel in Python ohne Bibliothek:

```python
import base64, hmac, hashlib, time

def verify(secret: str, headers: dict, body: bytes) -> bool:
    key = base64.b64decode(secret.removeprefix("whsec_"))
    msg_id = headers["webhook-id"]
    ts = headers["webhook-timestamp"]
    if abs(time.time() - int(ts)) > 300:
        return False
    expected = base64.b64encode(
        hmac.new(key, f"{msg_id}.{ts}.".encode() + body, hashlib.sha256).digest()
    ).decode()
    for sig in headers["webhook-signature"].split():
        version, _, value = sig.partition(",")
        if version == "v1" and hmac.compare_digest(value, expected):
            return True
    return False
```

## Antworten und Wiederholungen

- Antworte mit `2xx`, sobald Du das Ereignis gespeichert hast. Verarbeite es danach; lange Antwortzeiten zählen als Fehlschlag.
- `408`, `429`, `5xx` und Netzfehler werden wiederholt: im Lauf dreimal (1 s, 2 s, 4 s), danach über die Läufe hinweg mit Backoff von 1, 2, 4 … Minuten bis höchstens 6 Stunden.
- Andere `4xx` gelten als endgültig abgelehnt und werden sofort zum Dead Letter. Ein Dead Letter sperrt nur diese Version des Termins; eine neuere Änderung wird wieder versucht.
- Nach zehn Fehlschlägen wird ein Ereignis zum Dead Letter. Dead Letters kann ich ansehen und erneut zustellen lassen; sie enthalten keine Inhalte, nur Ids. Eine erneute Zustellung holt den Termin frisch aus Graph.

## Mitjas CRM als Ziel

Statt eines Webhooks kann das Ziel ein Mitjas CRM sein. Der Relay schreibt dann `POST /v1/signals` mit Service-Token, Typen `booking.created|updated|cancelled`, Quelle `/plugins/microsoft-bookings`. Das CRM dedupliziert über Quelle und Id und legt Partner und Termine an; auf CRM-Seite ist kein Code nötig.
