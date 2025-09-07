Wanted a self-hosted docker registry for Ollama models.
Figured this is actually quite easy with Dokku.

https://hub.docker.com/_/registry

TODO:

- basic auth
- volumes
- dashboard

A caveat: Ollama doesn't support authentication. So, this is only useful for private networks or for testing. As a basic security measure, I added origin IP filtering to the Dokku app.

Here's how I did it - it's also an example of how to serve a Docker Image with Dokku:

1. Create a Dokku app
2. Set the original registry server to hub.docker.com (where I get the registry image from)
3. Create the app from the image
4. Set the registry to use the nginx proxy
5. Set the client-max-body-size to 3000m (to allow for large models)
6. configure port mapping from host port 80 to container port 5000 (default for the registry)
7. Re-build the nginx config (necessary for the client-max-body-size)
8. Enable Let's Encrypt for the app

```bash
dokku apps:create registry
registry:set registry server hub.docker.com
git:from-image registry registry:2
proxy:set registry nginx
nginx:set registry client-max-body-size 3000m
ports:set registry http:80:5000
proxy:build-config registry
letsencrypt:enable registry
```

Note that with the tag, it's sticking to the same image, even if the underlying image changes. A better way is to use the sha hash of the image in the `git:from-image` command.

Here are some useful commands for debugging

```bash
nginx:show-config registry 
ports:list registry
proxy:report registry 
```

In the end, it unfortunately didn't work...