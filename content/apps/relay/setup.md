---
title: "Setup"
slug: "setup"
summary: "From purchase to the first event: grant consent, add a target, verify the signature."
weight: 10
---

This is how your first event arrives. You need an administrator of your Microsoft 365 tenant (global administrator or privileged role administrator) and an endpoint that accepts HTTPS POSTs, or a Mitjas CRM.

## 1. Choose a plan

Buy a plan or start the 30-day trial through the checkout on the [product page](../). Polar issues the invoice and sends a confirmation by email. The purchase creates your tenant in the relay; consent starts as "pending".

## 2. Grant consent

I send you a consent link (`consent_url`). An administrator of your tenant opens it, signs in with Microsoft and sees the Microsoft Entra dialog: the app asks for `Bookings.Read.All`, read-only, as an application permission. After approval the administrator is sent back to the relay.

What happens behind the scenes: the relay does not trust the callback blindly. It fetches a token for your tenant itself and checks that the permission was really granted. If you revoke it later in the Entra portal, the relay pauses your tenant.

## 3. Booking calendars and interval

By default the relay reads all booking calendars of your tenant. You can restrict it to specific calendars (the mailbox address, for example `consulting@contoso.com`). The plan limits the number of calendars and the shortest interval; surplus calendars are left out and the sync reports that as `limited`.

## 4. Add a target

A target is a webhook URL (`https://…`) or a Mitjas CRM. For a webhook URL the relay generates a secret `whsec_…` which you see exactly once, when the target is created. Store it at your receiver; it verifies the signature with it ([Event format and signature verification](../event-format/)). For Mitjas CRM you need the CRM's base URL and a service token with the scopes `read,write`.

During early access I manage calendars, interval and targets for you through the admin API; there is no self-service yet. Send me the values by email. Secrets never travel by email, the relay generates them.

## 5. Trigger the first sync

The scheduler starts the first sync on its own. If you want it sooner, trigger it: `POST /sync`. Afterwards your tenant's status shows when the last sync ran, how many appointments were in the window, and whether anything is stuck as a dead letter.

The window reaches from yesterday to 90 days ahead. Appointments already inside it at the first sync arrive as `created`, so you receive every upcoming appointment once at the start.

## Checklist

- Plan bought or trial started
- Consent granted, tenant "active" in the relay
- Calendars and interval set
- Target created, secret stored at the receiver
- Signature verification tested at the receiver
- First `created` event received
