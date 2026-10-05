---
title: "Mitjas Relay"
subtitle: "Webhooks for Microsoft Bookings"
kicker: "App"
status: "Early access"
status_note: "Early access: the relay is tested against a replica of Microsoft Graph and end to end with Mitjas CRM, but it has not yet run against a real Microsoft 365 tenant. I work with the first customers personally."
teaser: "Bookings does not announce new, changed or cancelled appointments. The relay syncs your calendars on a schedule and delivers every change as a signed webhook to your system, without storing appointment content."
summary: "Microsoft Bookings has no webhooks. Mitjas Relay syncs your booking calendars on a schedule and delivers every new, changed or cancelled appointment as a signed event to your endpoint or to Mitjas CRM. Appointment content is never stored."
primary:
  text: "Try it free for 30 days"
  url: "TODO(Mitja): Polar-Checkout-Link"
secondary:
  text: "Questions? hi@mitjamartini.com"
  url: "mailto:hi@mitjamartini.com?subject=Mitjas%20Relay"
trademark: "Mitjas Relay is an independent product and is not affiliated with, endorsed or sponsored by Microsoft. Microsoft and Microsoft Bookings are trademarks of the Microsoft group of companies."
docs_heading: "Documentation"
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
    price: "€9 / month"
    yearly: "or €90 / year"
    features: ["1 booking calendar", "sync every 60 minutes", "1 target"]
    checkout: "TODO(Mitja): Polar-Checkout-Link"
    cta: "Try Starter"
  - name: "Business"
    price: "€29 / month"
    yearly: "or €290 / year"
    features: ["5 booking calendars", "sync every 15 minutes", "3 targets"]
    checkout: "TODO(Mitja): Polar-Checkout-Link"
    cta: "Try Business"
  - name: "Partner"
    price: "from €99 / month"
    yearly: "for service providers and MSPs"
    features: ["50 booking calendars", "sync every 5 minutes", "10 targets"]
    checkout: "TODO(Mitja): Polar-Checkout-Link"
    cta: "Ask about Partner"
---

## The problem

Microsoft Bookings does not tell the outside world about appointments. Microsoft Graph has no change notifications for Bookings, and the Power Automate connector is in preview, limited to five flows per mailbox, and needs a premium licence for your own webhooks. If you want a booking to show up in your CRM, your ticket system or your own tool, you have to poll for it yourself.

## How it works

1. **Consent.** An administrator of your Microsoft 365 tenant opens a link and grants the relay the read permission `Bookings.Read.All`. It needs nothing else, and you can revoke it in the Entra portal at any time.
2. **Sync.** The relay reads your booking calendars through Microsoft Graph on a schedule: every 60, 15 or 5 minutes depending on the plan. A fingerprint per appointment detects what really changed: time, service, customer, answers, Teams link. A different spelling of the time zone is not a change.
3. **Delivery.** Every new, changed or cancelled appointment becomes a CloudEvents 1.0 event, signed per Standard Webhooks (HMAC-SHA256), with a stable id for deduplication. The target is your own endpoint or Mitjas CRM directly. Delivery is at least once, with retries, backoff and visible dead letters.

Up to one interval of delay is part of the design: the relay asks, Microsoft does not push. For most uses, notifications, CRM records, invoices, that is enough.

## Privacy

- **No appointment content in the relay.** Names, email addresses and notes are fetched from Graph, forwarded, and not stored, neither in the database nor in dead letters. What is kept: appointment id, fingerprint (a hash), last known start and end, and the delivery state, until the appointment is over.
- **Logs without content.** Logs contain ids, numbers and error codes; a test enforces it.
- **GDPR roles.** In the hosted service you are the controller of the data in Bookings and I am the processor under Art. 28 GDPR; a data processing agreement covers that. The service runs on Kubernetes in Germany (Hetzner, Nuremberg).
- **Self-hosting.** If appointment data must not pass through a third party, run the relay with a licence key in your own Azure subscription or your own Kubernetes. Appointment data then flows only from your tenant to your targets; I never receive it and am not a processor for it. The only outbound call is the licence check at Polar: key, activation id and version, no appointment or tenant data.
- **Security.** Read-only Graph permission, TLS only, target secrets sealed with AES-256-GCM, containers without root and with a read-only file system.

## Plans

Every plan comes with a 30-day free trial. Payment is handled by Polar as merchant of record: an invoice with VAT, or reverse charge for businesses with a VAT id. The self-hosted licence costs the same as the service: same features, same limits, only the location differs.

{{< plans >}}

TODO(Mitja): add the Polar checkout links, confirm the Partner price, provide the DPA.

## FAQ

**How fast does an event arrive?**
At most one interval after the change: 60, 15 or 5 minutes depending on the plan. A call to `POST /sync` triggers an immediate sync.

**What if my endpoint is down?**
The relay retries with backoff (up to six hours apart) and files a dead letter after ten failures, which you can inspect and redeliver. A failing target does not slow down the others.

**Can I deliver to several targets?**
Yes, 1, 3 or 10 targets depending on the plan, each with its own secret and its own delivery state.

**Do I need Power Automate or Azure?**
No. One admin consent, then webhooks arrive. You only need Azure if you want to self-host the relay there.

**What is in an event?**
Start and end, service, staff, customer with name, email, phone and answers, online status and Teams link, location, notes. The format is described in [Event format and signature verification](event-format/). Cancellations carry only ids and the last known time span, because the appointment is already gone at Microsoft.

**What about the Microsoft Bookings connector for Power Automate?**
For one calendar and one or two flows inside Microsoft 365 it is enough. The relay is built for several targets, one signed format, reliable delivery, and operation in the EU or on your own infrastructure.

## Support

Email [hi@mitjamartini.com](mailto:hi@mitjamartini.com?subject=Mitjas%20Relay), replies usually by the next business day. Support cases are handled with logs that contain no appointment content. For self-hosting I provide the image and the template; running, monitoring and updating the installation is up to you.
