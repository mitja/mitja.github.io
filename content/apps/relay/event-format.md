---
title: "Event format and signature verification"
slug: "event-format"
summary: "CloudEvents 1.0, signed per Standard Webhooks. Fields, types, ids, and how your receiver verifies the signature."
weight: 20
---

## The event

Every delivery is a `POST` with `Content-Type: application/cloudevents+json` and a CloudEvent 1.0 in the body:

```json
{
  "specversion": "1.0",
  "id": "bkr_61e06ee8…",
  "source": "/bookings-relay/tenants/<entra-tenant-id>/businesses/consulting@contoso.com",
  "type": "com.microsoft.bookings.appointment.created",
  "subject": "<appointment-id>",
  "time": "2026-10-04T20:26:00Z",
  "datacontenttype": "application/json",
  "data": {
    "tenant_id": "…",
    "business_id": "consulting@contoso.com",
    "appointment_id": "…",
    "self_service_appointment_id": "…",
    "start": "2026-10-06T09:00:00Z",
    "end": "2026-10-06T09:30:00Z",
    "duration_minutes": 30,
    "service_id": "…",
    "service_name": "Intro call",
    "staff_member_ids": [],
    "customer": {"name": "Jane Doe", "email": "jane@example.com", "phone": "+49 30 1234567", "answers": {"Company": "Example Ltd"}},
    "customers": [],
    "answers": {"Company": "Example Ltd"},
    "answers_by_question_id": {"q-company": "Example Ltd"},
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

### Types

| `type` | When |
|---|---|
| `com.microsoft.bookings.appointment.created` | appointment newly inside the window (yesterday to 90 days ahead) |
| `com.microsoft.bookings.appointment.updated` | fingerprint changed: time, service, staff, customer, answers, online status, Teams link, location or label |
| `com.microsoft.bookings.appointment.cancelled` | appointment missing from the window and no longer retrievable at Microsoft. Carries only ids and the last known start and end |

Times are UTC. A different spelling of the time zone or a daylight-saving switch does not produce an `updated`.

### Ids

- `id` is stable per appointment, type and fingerprint (`bkr_` + SHA-256). A retry carries the same id. Deduplicate on it; delivery is at least once.
- `appointment_id` is the id from Microsoft Graph. `self_service_appointment_id` is included because Microsoft recommends it for matching across changes.

## Verifying the signature

The signature follows [Standard Webhooks](https://www.standardwebhooks.com/). Three headers accompany every delivery:

```
webhook-id: bkr_61e06ee8…
webhook-timestamp: 1759609560
webhook-signature: v1,K5oZfzN95Z9UVu1EsfQmfVNQhnkZ2pfW…
```

The signature is `base64(HMAC-SHA256(secret, "<webhook-id>.<webhook-timestamp>.<body>"))`. The secret is the `whsec_…` you saw when the target was created; the part after `whsec_` is Base64 and decodes to the key.

Verify like this:

1. Read the body as raw bytes before anything parses or reformats it.
2. Reject timestamps older than five minutes (replay protection).
3. Compute the HMAC over `id.timestamp.body` with the decoded key.
4. Compare in constant time against every `v1,…` signature in the header (there may be several, separated by spaces).

Libraries for most languages are listed on standardwebhooks.com. An example in Python without a library:

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

## Responses and retries

- Respond with `2xx` as soon as you have stored the event. Process it afterwards; slow responses count as failures.
- `408`, `429`, `5xx` and network errors are retried: three times within the run (1 s, 2 s, 4 s), then across runs with a backoff of 1, 2, 4 … minutes up to six hours.
- Other `4xx` responses count as final rejections and become a dead letter immediately. A dead letter blocks only that version of the appointment; a newer change is tried again.
- After ten failures an event becomes a dead letter. I can inspect dead letters and redeliver them; they contain no content, only ids. A redelivery fetches the appointment fresh from Graph.

## Mitjas CRM as a target

Instead of a webhook the target can be a Mitjas CRM. The relay then calls `POST /v1/signals` with a service token, types `booking.created|updated|cancelled`, source `/plugins/microsoft-bookings`. The CRM deduplicates on source and id and creates parties and appointments; no code is needed on the CRM side.
