---
title: "Self-hosting in Azure"
slug: "self-hosting"
summary: "Bring your own Azure: the relay runs in your subscription with a licence key. Appointment data leaves your tenant only towards your targets."
weight: 30
---

For everyone whose appointment data must not pass through a third party: healthcare, consulting under confidentiality, public sector, strict IT policies. You run the relay yourself in your Azure subscription ("bring your own Azure") or in your own Kubernetes. The licence costs the same as the service; Azure costs amount to a few euros a month and go on your own bill.

## What you need

- an Azure subscription with the right to create a resource group and assign roles (Owner, or Contributor plus User Access Administrator);
- a global administrator or privileged role administrator in the Microsoft 365 tenant for the consent;
- the licence key from Polar's purchase email (or from the Polar customer portal);
- a target: your webhook URL or a Mitjas CRM.

## Steps

1. **Create the Entra app.** In the Entra admin center, an app registration in your own tenant, single-tenant, without a redirect URI. Under API permissions → Microsoft Graph → Application permissions add only `Bookings.Read.All`, then "Grant admin consent". Create a client secret and put its expiry date in your calendar. A certificate from Key Vault is better than a secret; the template supports both.
2. **Generate the webhook secret.** `docker run --rm git.paasbox.com/paasbox/bookings-relay:<version> secret` prints a `whsec_…`. Store it at your receiver ([Event format and signature verification](../event-format/)).
3. **Deploy.** In the Azure Cloud Shell, apply the Bicep template with `az deployment`: a region of your choice (for example `germanywestcentral`, Frankfurt), tenant id, client id and secret of the Entra app, the licence key, the target URL and webhook secret, and a cron expression as the interval, for example `7 * * * *` for hourly. Shorter only within the plan: Business 15 minutes, Partner 5 minutes. The template creates a Container Apps job and a Table Storage account; secrets live in Key Vault.
4. **Start the first run.** `az containerapp job start --name bkrelay-sync --resource-group bookings-relay`. The result appears in the job's execution history. On the first run the relay activates the licence key at Polar; afterwards it checks it at most once a day. A rejected key fails the run with a message that names the variable, the reason and the remedy.
5. **Firewall.** Outbound, the relay needs `login.microsoftonline.com`, `graph.microsoft.com`, `api.polar.sh`, your targets, and the registry `git.paasbox.com`.

TODO(Mitja): add the exact `az` command and the link to the Bicep template once the image and template are available to customers.

## In operation

- **Polar unreachable:** the relay keeps working for 14 days from the last successful check and retries hourly. After that it pauses until the next successful check.
- **Subscription cancelled:** Polar revokes the key; the relay stops at the next check, at the latest after one day.
- **Moving** to another resource group or cluster: release the activation first, with `bookings-relay license deactivate` in the old environment or in the Polar customer portal. A key has exactly one activation.
- **Status:** `bookings-relay license status` prints plan, validity, last check and errors as JSON.
- **Updates:** set the new image tag on the job (`az containerapp job update … --image git.paasbox.com/paasbox/bookings-relay:<version>`). I announce new versions by email.

## What flows where

Appointment data flows from Microsoft Graph through your relay to your targets. Only the licence check goes to Polar: licence key, activation id, relay version and an installation label; no appointment or customer data, no Entra tenant id, no mailbox addresses. I have no access to your installation and receive no appointment data; for this processing I am not a processor. Microsoft (Azure) is your processor, not mine.

## In your own Kubernetes

Instead of Azure, your own cluster works too: a deployment with SQLite on a volume or with Postgres, secrets including `RELAY_LICENSE_KEY`, and `RELAY_ENTITLEMENTS=license`. The Kustomize base ships with the image.
