---
title: "Limits and FAQ"
slug: "limits"
summary: "What the relay does not do, what is not verified yet, and answers to common questions."
weight: 40
---

## Limits

- **Up to one interval of delay.** The relay polls Microsoft Graph; Microsoft does not push. If you need seconds, the Power Automate connector inside Microsoft 365 serves you better; a nudge from the connector to the relay is conceivable but not built.
- **Window from yesterday to 90 days ahead.** Appointments further out arrive once the window reaches them. An appointment moved beyond 90 days arrives as `updated` with the state from the single fetch; when it returns into the window, another `updated` may follow.
- **Past appointments are forgotten silently.** An appointment that is already over when it disappears produces no `cancelled`.
- **At least once, not exactly once.** Retries carry the same `id`; your receiver deduplicates on it.
- **No self-service during early access.** I manage calendars, interval and targets for you through the admin API.
- **Plan limits are enforced.** Surplus calendars and targets are left out and the sync reports `limited`; an interval that is too short is raised to the plan's minimum.
- **The licence check is a reminder, not copy protection.** It makes sure a cancelled subscription does not keep running by accident. For business customers the licence terms apply.

## What is not verified yet

The relay is tested against a replica of Microsoft Graph and Microsoft Entra, against SQLite, Postgres and Azurite, and end to end with Mitjas CRM; the signature against the official Standard Webhooks test vector. Not yet verified:

- a real Microsoft 365 tenant and real Graph: the fields `calendarView` returns, whether appointment ids stay stable across changes, throttling in practice;
- a real admin consent;
- Polar live, including licence keys;
- deploying to Azure with the Bicep template.

That is why it is early access. I work with the first customers personally, and this list gets shorter.

## FAQ

**Which permission does the relay need in my tenant?**\
Only `Bookings.Read.All` as an application permission, read-only. Microsoft Graph has nothing finer than tenant-wide for Bookings; the relay reads only the configured calendars, though.

**Does the relay see my customer data?**\
In memory during a sync, yes; that is needed to deliver it to you. It is not stored. With self-hosting nobody but you sees it.

**What about group bookings?**\
Another customer on an existing appointment is an `updated`, not a `created`. The `customers` field contains all of them.

**Does the relay tell me what changed?**\
It detects that something relevant changed and delivers the new state. Which field it was, you compare against your last state.

**Can I trigger a sync immediately?**\
Yes, `POST /sync` with your token, for example as a button in your tool.

**What does Azure cost when self-hosting?**\
A Container Apps job that runs for a few seconds a few times an hour, and a Table Storage account: in practice a few euros a month, on your Azure bill.

**How do I cancel?**\
In the Polar customer portal, any time to the end of the period. In the hosted service your tenant's state and target secrets are deleted; the subscription records remain for accounting. With self-hosting the relay stops at the next licence check.
