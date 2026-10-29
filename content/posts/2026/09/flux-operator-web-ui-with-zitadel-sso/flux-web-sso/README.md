# flux-web-sso

A Kustomize package for the flux-operator web UI with OIDC single sign-on, closed off from the rest
of the cluster and acting as the person who signed in rather than as cluster-admin.

Companion to the post *[Flux Operator Web UI with OIDC Single Sign-On](https://mitjamartini.com/en/posts/2026/09/flux-operator-web-ui-with-zitadel-sso/)*.
The manifests are the ones running in production, with the site-specific values lifted into one
file. Checked against flux-operator 0.59.0 and 0.61.0. [`../kind-demo`](../kind-demo/) shows the
default, the shortcut and this package on a local cluster; [`../educates`](../educates/) is the same
as a step-by-step workshop.

## What it does

The flux-operator chart starts the web UI by default, on `:9080`, with **no authentication**. It
reads with the operator's ServiceAccount, which is cluster-admin, and the chart's NetworkPolicy
admits every namespace. Without a web config the UI does not act (no reconcile, suspend, restart,
logs or downloads), but every pod in the cluster can read everything Flux knows through it: every
Flux object with its spec, HelmRelease values included, and the pod templates of the workloads Flux
manages, environment included. `Anonymous` authentication with a named identity switches the
actions on, for every pod as well. This package:

1. turns the chart's NetworkPolicy off, so Flux's own baseline in `flux-system` admits same-namespace
   traffic only; Setup A adds back the ingress controller (and the ACME solver), Setup B nothing,
2. points the UI at an OIDC provider and impersonates the signed-in user, so reads and actions are
   checked against RBAC as that person,
3. binds that user to a role you choose, including a read-only one that cannot read Secrets.

## Requirements

- Flux (this uses `OCIRepository` + `HelmRelease`), **with its NetworkPolicies in `flux-system`**.
  `kubectl -n flux-system get networkpolicy` must list `allow-egress`; a `FluxInstance` writes it when
  `cluster.networkPolicy` is `true`, its default. Without it, turning the chart's policy off leaves the
  operator pod selected by no policy, which means reachable from everywhere.
- The operator becomes a HelmRelease of Flux. If you installed the chart with `helm install` as
  `flux-system/flux-operator`, the helm-controller takes that release over and upgrades it.
- an OIDC provider you can register a client with
- Setup A only: an ingress controller and cert-manager with a working `ClusterIssuer`

## Use it

**1. Register an OIDC client.** Confidential / web application, authorization code (the UI adds
PKCE).

The redirect URI is **`<baseURL>/oauth2/callback`**. This path is not in ControlPlane's
documentation; it was read out of the operator binary. For a `http://localhost:9080` base URL most
providers need their "dev mode" allowance to accept a non-TLS redirect.

Make sure the provider puts `email` in the **ID token** — see the note in
`web-config.example.yaml`, it is the most common way this fails.

**2. Create the config Secret.**

```sh
cp web-config.example.yaml /tmp/web-config.yaml
$EDITOR /tmp/web-config.yaml          # baseURL, issuerURL, clientID, clientSecret (+ insecure for Setup B)
kubectl apply -f /tmp/web-config.yaml && rm /tmp/web-config.yaml
```

**3. Edit `kustomization.yaml`** — the values are at the top, and it is the only file to change.
For Setup B, comment out the `components/ingress` line.

**4. Apply.**

```sh
kubectl apply -k .
```

Setup A: browse to your host. Setup B:

```sh
kubectl -n flux-system port-forward svc/flux-operator 9080:9080
open http://localhost:9080
```

`port-forward` reaches the pod from the kubelet rather than as pod-to-pod traffic, so it bypasses
NetworkPolicy. That is why Setup B needs no allowance, and also why closing the UI off does not
lock you out of it.

Setup B is plain http, so set `insecure: true` in the web config. The UI's cookies are `Secure`
otherwise; Chrome and Firefox accept that on `localhost`, Safari drops the login state cookie and the
UI answers "Authentication failed" with nothing in the operator's log.

## Layout

```
kustomization.yaml            the values, and the Setup A / Setup B switch — edit this
web-config.example.yaml       the OIDC config Secret; applied separately, carries a secret
base/
  flux-operator.yaml          OCIRepository + HelmRelease, chart NetworkPolicy off
  rbac.yaml                   flux-web-viewer ClusterRole + the binding for your user
components/
  ingress/exposure.yaml       Setup A: Certificate, Ingress, and two NetworkPolicies
```

## Roles

`role` in `kustomization.yaml` picks one of three. The first two come from the chart.

| Role | May read Secrets | Can act | Notes |
|---|---|---|---|
| `flux-web-viewer` | no | no | defined here; read-only and enumerated |
| `flux-web-user` | **yes, all of them** | no | `apiGroups: ["*"], resources: ["*"]` |
| `flux-web-admin` | **yes, all of them** | yes | also `create jobs` + `patch deployments` |

The UI itself does not show Secrets. "May read" is what RBAC allows the identity, and it matters
wherever that identity reaches the API server another way, for example when the cluster trusts the
same OIDC provider for kubectl.

`flux-web-admin` is close to cluster-admin in practice: creating a Job runs an arbitrary image as
an arbitrary ServiceAccount. That is inherent to offering "restart my workloads" at all, but it
should not be a surprise.

`flux-web-viewer` was verified with SubjectAccessReviews (`get secrets` denied; Flux objects, pod
logs, Deployments and Events allowed; `patch kustomizations` denied) and by signing in as a user
bound to it: Flux objects, HelmReleases and Deployments are shown, a suspend is refused. Panels that
surface data derived from Secrets may show less or show an error.

No role protects a value written into a spec. Every viewer reads a HelmRelease's values and a
Deployment's environment; keep passwords in Secrets and reference them with `secretKeyRef`.

Do not bind your user to `cluster-admin`. It gives the UI back exactly the unrestricted power this
setup removes, with a login page in front of it.

## If the certificate will not issue

A 502 on `http://<host>/.well-known/acme-challenge/...` is the ingress controller failing to reach
the solver pod, not DNS. `components/ingress/exposure.yaml` carries the NetworkPolicy that fixes
it, and the comment there explains why it is needed. Check with:

```sh
kubectl -n flux-system describe certificate flux-web
kubectl -n flux-system get challenge -o wide
```
