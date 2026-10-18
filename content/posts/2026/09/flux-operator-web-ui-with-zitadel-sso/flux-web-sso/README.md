# flux-web-sso

A Kustomize package for the flux-operator web UI with OIDC single sign-on, closed off from the rest
of the cluster and acting as the person who signed in rather than as cluster-admin.

Companion to the post *[Flux Operator Web UI with Zitadel SSO](../)*. The manifests are the ones
running in production, with the site-specific values lifted into one file.

## What it does

The flux-operator chart starts the web UI by default, on `:9080`, with **no authentication**, and
the operator's ServiceAccount is cluster-admin. Its bundled NetworkPolicy admits every namespace.
This package:

1. turns the chart's NetworkPolicy off and replaces it with one that admits the ingress controller
   and nothing else (Setup A) or nothing at all (Setup B),
2. points the UI at an OIDC provider and impersonates the signed-in user, so actions are checked
   against RBAC,
3. binds that user to a role you choose, including a read-only one that cannot read Secrets.

## Requirements

- Flux (this uses `OCIRepository` + `HelmRelease`)
- an OIDC provider you can register a client with
- Setup A only: an ingress controller and cert-manager with a working `ClusterIssuer`

## Use it

**1. Register an OIDC client.** Confidential / web application, authorization code with PKCE.

The redirect URI is **`<baseURL>/oauth2/callback`**. This path is not in ControlPlane's
documentation; it was read out of the operator binary. For a `http://localhost:9080` base URL most
providers need their "dev mode" allowance to accept a non-TLS redirect.

Make sure the provider puts `email` in the **ID token** — see the note in
`web-config.example.yaml`, it is the most common way this fails.

**2. Create the config Secret.**

```sh
cp web-config.example.yaml /tmp/web-config.yaml
$EDITOR /tmp/web-config.yaml          # baseURL, issuerURL, clientID, clientSecret
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

| Role | Reads Secrets | Can act | Notes |
|---|---|---|---|
| `flux-web-viewer` | no | no | defined here; read-only and enumerated |
| `flux-web-user` | **yes, all of them** | no | `apiGroups: ["*"], resources: ["*"]` |
| `flux-web-admin` | **yes, all of them** | yes | also `create jobs` + `patch deployments` |

`flux-web-admin` is close to cluster-admin in practice: creating a Job runs an arbitrary image as
an arbitrary ServiceAccount. That is inherent to offering "restart my workloads" at all, but it
should not be a surprise.

`flux-web-viewer` was verified with SubjectAccessReviews — `get secrets` denied, Flux objects, pod
logs, Deployments and Events allowed, `patch kustomizations` denied. It was **not** verified by
driving the UI as that user, so panels that surface data derived from Secrets may show less or show
an error. Click through it once before handing it to someone.

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
