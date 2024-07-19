---
date: 2024-02-26
title: Publish Ollama and OpenWebUI on the Internet with Cloudflare Tunnels
author: mitja
category: The Basics
tags:
 - Ollama
 - OpenWebUI
 - Cloudflare Tunnel
 - Cloudflared
 - Caddy
 - Docker
image:
  path: /assets/blog/2024/publish-opllama-with-cloudflare-tunnels/ollama-on-the-go.jpg
  alt: Use Ollama on the go.
---

This is a guide on how to use Cloudflare Tunnels, Caddy, and Docker Compose to publish Ollama and OpenWebUI on the internet.

Here are two reasons why you might want to publish Ollama and OpenWebUI on the internet:

- You want to use Ollama and OpenWebUI on the go.
- You want to share your Ollama and OpenWebUI with your family, friends, classmates, or colleagues.

Ollama and OpenWebUI are just examples for an API and a web application. You can use this guide as a basis to publish any local web service on the internet.

I have also created project template for Docker Compose to simplify the setup. You can find it on GitHub at [mitja/llamatunnel](https://github.com/mitja/llamatunnel) and watch a video tutorial on [YouTube](https://youtu.be/-kmrfrL8W2QQ).

## Why use Cloudflare Tunnels?

In short: Cloudflare Tunnels is a reasonably secure and convenient way to publish local services on the internet.

A more detailed answer:

If you want to use your local LLM on the go, you have basically three options:

- Open a port on your local network and use dynamic DNS to access it from the internet,
- Connect to your local network with a VPN client, or
- create a reverse tunnel to a gateway service on the internet and let it forward the requests to your local LLM. A reverse tunnel is initiated from your local network to the gateway service, and the gateway service then forwards the requests from internet over the tunnel to you local services.

Each option has its pros and cons:

- Opening ports is easy to set up but you expose the IP and a port of your network directly on the internet.
- A VPN is more secure but you need to connect to your home network via VPN and share VPN access.
- A reverse tunnel is secure, easy to share, and you don't need to open ports on your network. But it is a bit more complex to set up.

Cloudflare Tunnel is one way to implement the reverse tunnel to gateway pattern. With a Cloudflare tunnel, you can expose local https services on the internet, without having to open ports on your router or firewall. Cloudflare Tunnels can be used for free, but more advanced features and higher volumes require paid service plans.

Another way to implement the reverse tunnel pattern is to run your own gateway service. This would also give you more control over who can access your local network. I maybe cover setting up a self-hosted gateway in another guide.

## Prerequisites

the only things you'll need are

- a domain name,
- a free Cloudflare account,
- a computer with Docker Compose (eg. with Docker Desktop), and
- Ollama running and listening on it's default port.

## A High-Level Overview of the Target Setup

Here is how the final setup will look like:

```
+-------------------+     +-------------------+     +-------------------+
|                   |     |                   |     |                   |
|  Your local LLM   |     |  Cloudflare       |     |  Your phone or    |
|                   |     |  Tunnels          |     |  another computer |
+-------------------+     +-------------------+     +-------------------+
```

By the way: You can also run the public endpoint on your own and recreate the Cloudflare service. This way,

You already have Ollama for your local LLM, and a docker-compose file with OpenWebUI.

Now we will add Cloudflare Tunnels and Caddy to the mix.

Cloudflare tunnels will create a secure connection between your computer and Cloudflare. You don't need to open a port on your network. Instead, a service called `cloudflared` will open an outbound connection to Cloudflare and establish a tunnel.

Then you configure Domain Name Service entries to reach local web services. For this, you need a Domain Name and have it managed by Cloudflare. For example, I use `mitja.dev` for my personal projects, and I want to make `ollama.mitja.dev` and `chat.mitja.dev` available on the internet.

Caddy will act as a reverse proxy in front of OpenWebUI, and Ollama. It will handle SSL certificates and adds a layer of security to the services. For Ollama, I also add a confiiguration to check an API token for authentication. This way, only authorized users can access the LLM. OpenWebUI is already secured with usernames and passwords, so I don't need this, here.

We'll cover a lot of ground. Don't worry! I will go through it step by step and explain everything you need to know. To give you an overview of the steps, here is what we will do:

1. Register a domain name with Cloudflare, and create an API key to manage the DNS entries. This is needed later to let Caddy get SSL certificates from Let's Encrypt with a "DNS challenge".
2. Install the `cloudflared` tool on your computer and use it to create a tunnel to Cloudflare and setup the routing for your domain.
3. Create a `cloudflared` configuration file for the tunnel.
4. Create a Caddy configuration file (called `Caddyfile`).
5. Create a `docker-compose.yml` file to start the services.

Domain name: `mitja.dev`

The domain name is how you address things on the internet. You can register a domain name with a domain registrar. I use Gandi for this, but you can use any other registrar.

Then, you need to configure the domain to use Cloudflare's nameservers. The nameservers are the actual "authoritative" name servers for your domain. It is like a hierarchy: There are domain servers for the `.dev` domain. Requests for `mitja.dev` are delegated to the registrar's nameservers or the nameservers you tell the registrar to use. The easiest way to switch to Cloudflare's nameservers is to add the domain, Cloudflare will then tell you, what to do.

Use cloudflared to create a tunnel to Cloudflare and setup the routing for your domain.

The `cloudflared` tool is a command-line tool that you can use to create a tunnel to Cloudflare and setup the routing for your domain. You can install it with `brew install cloudflare/cloudflare/cloudflared` on macOS, or `choco install cloudflared` on Windows. On Linux, you can download the binary from the Cloudflare website.

To create a tunnel, you need to run `cloudflared tunnel login` and `cloudflared tunnel create <tunnel-name>`. Then, you need to make the tunnel configuration and credentials file available to the `cloudflared` container. You can do this by creating a directory and copying the files to it.

To setup the routing for your domain, you need to run `cloudflared tunnel route dns <tunnel-id> <domain>`.

The `cloudflared` tool will create a tunnel to Cloudflare and setup the routing for your domain. This way, you can access your local LLM from the internet.

Up until now I have used `cloudflared` on the local machine, but I want to run the tunnel from a Docker container. Use the official `cloudflared` Docker Image as a base and add the configuration and credentials file to it. This way, you can start the tunnel in a container and keep it running in the background. Copy the configuration and credentials file to a place which you can easily reference when starting the containers. This is needed to start the tunnel. The configuration file contains the tunnel ID and the credentials file contains the certificate and the private key.

Make sure to not add the credentials file to your git repository. Add it to the `.gitignore` file.

Now, let's take care about encryption. The requests are encrypted with TLS. You can see it in the URL bar of your browser. It starts with `https://` and not `http://`. The encryption is done with SSL certificates. In our setup, we have two different encrypted connections:

1. From a client on the internet to Cloudflare.
2. From Cloudflare to your local Caddy.

The certificates are signed by a certificate authority. Your browser and mobile device trusts this authority because it has its public key stored in the keyring. With this it can check if the certificate presented by the web server (or Cloudflare) for the domain is valid.

The certificates on Cloudflare are managed by Cloudflare. You can get certs for the main domain and the first sublevel (Eg. `mitja.dev` and `ollama.mitja.dev`) for free. You can also get a wildcard certificate for all subdomains (Eg. `*.mitja.dev`). If you want another level (eg. `chat.home.mitja.dev`), you need a paid account. To distinguish between services and computers, I like to use a format like <service>-<computer>.<domain>.<tld>. For example, `ollama-home.mitja.dev`. To keep it simple, I will use `ollama.mitja.dev` and `chat.mitja.dev` in this guide.

The certificates on your local Caddy are managed by Caddy. Caddy can automatically get them from Let's Encrypt. To get it, Caddy needs to prove that it has control over the domain. This is done with a "challenge". There are different types of challenges. The DNS challenge is the easiest to use with Cloudflare. With this, Caddy gets a challenge from Let's Encrypt to add a certain text record to the DNS Zone. Let's Encrypt then checks if the record is present and hands out the certificate if this is the case. 

To make this work, we need to add a special module to Caddy and give it a Cloudflare API Key that has the permission to modify the DNS Zone. This is the only thing we need to do manually. Caddy will take care of the rest. It will get the certificates and renew them automatically.

Here is how to get the API Key:

1. Log in to your Cloudflare account.
2. Go to the "My Profile" page.
3. Scroll down to the "API Tokens" section.
4. Click on "Create Token".
5. Select "Edit Zone DNS" for the "Zone" resource.
6. Select the domain you want to use.
7. Click on "Continue to Summary".
8. Give the token a name and click on "Create Token".
9. Copy the token and store it in a safe place.

To add the Cloudflare module to Caddy, we need to build a custom Caddy Docker Image. We will use the official Caddy Docker Image as a base and add the Cloudflare module to it. The module is called `dns.providers.cloudflare`.

With that in place, we can create the `Caddyfile` and the `docker-compose.yml` file.

Here is the `Caddyfile`:

```caddy
ollama.mitja.dev {
  reverse_proxy ollama:80
  tls {
    dns cloudflare {env.CLOUDFLARE_API_TOKEN}
  }
}
chat.mitja.dev {
  reverse_proxy chat:80
  tls {
    dns cloudflare {env.CLOUDFLARE_API_TOKEN}
  }
}
```

The `Caddyfile` is a configuration file for Caddy. It tells Caddy how to handle requests for the domains `ollama.mitja.dev` and `chat.mitja.dev`. In this case, it tells Caddy to use the `reverse_proxy` directive to forward requests to the services. It also tells Caddy to use the `tls` directive to get SSL certificates from Let's Encrypt with the Cloudflare DNS challenge.

A special thing in the `Caddyfile` is the `{env.CLOUDFLARE_API_TOKEN}`. This is an environment variable. We will use it to pass the Cloudflare API Token to Caddy. This way, we don't need to hardcode the token in the `Caddyfile`.

Another special thing is that I check for an API token in the requests to the LLM. ...

Here is the `docker-compose.yml` file:

```yaml
version: '3.8'


services:
  ollama:
    image: ollama:latest
    container_name: ollama
    environment:
      - OLLAMA_API_TOKEN
    ports:
      - "80:80"
    networks:
      - ollama

  chat:
    image: chat:latest
    container_name: chat
    environment:
      - CHAT_API_TOKEN
    ports:
      - "80:80"
    networks:
      - chat

  caddy:
    build:
      context: .
      dockerfile: Dockerfile
    container_name: caddy
    environment:
      - CLOUDFLARE_API_TOKEN
    ports:
      - "443:443"
    networks:
      - ollama
      - chat
```

The `docker-compose.yml` file is a configuration file for Docker Compose. It tells Docker Compose how to start the services. In this case, it tells Docker Compose to start the services `ollama`, `chat`, and `caddy`. It also tells Docker Compose to use the `networks` directive to connect the services to the same network. This way, the services can communicate with each other.

The `caddy` service doesn't just use a prebuilt image but the `build` directive to build a custom Docker image. The `Dockerfile` for this image tells Docker to use the official Caddyx Docker Image to build another image with the Cloudflare module added to it.

Here is the `Dockerfile`:

```Dockerfile
FROM caddy:latest

RUN caddy-builder \
    github.com/caddy-dns/cloudflare
```

By the way: The `caddy` service uses widely trusted, signed SSL certificates for its service. This certificate is only used for the internal communication between Cloudflare and Caddy. Clients on the internet will see the certificate from Cloudflare. As both are for the same domain name, you can also address the Caddy service directly, without going over Cloudflare. For this, you could use a configurable DNS server in your home network. Point the DNS entries for your local services directly to the Caddy service on your local network. This way, you can access your local services with the same domain names as on the internet, but without going over the internet. When you are not in the home network, the public DNS entries are used and you can reach the services over the internet. This works seamlessly, without reconfiguration or changing the URL.

## Step by Step Guide

### Install Cloudflared and Login

I use the cloudflared CLI tool to create the tunnel and routes, as doing this with the Cloudflare web console would not give back the credentials.json file which we need to open the tunnel from a docker container.

This is how you can install it on macOS with Homebrew:

```bash
brew install cloudflare/cloudflare/cloudflared
```

On Windows:

```powershell
winget install --id Cloudflare.cloudflared
```

To learn how to install it on other systems, see the [Cloudflared Download Docs](https://developers.cloudflare.com/cloudflare-one/connections/connect-networks/downloads/).

Then login with the following command. This will open a browser window where you can log in with your Cloudflare account:

```bash
cloudflared tunnel login
```

### Create a Cloudflare API token for DNS Zone Editing

Create a Cloudflare API token with the permissions to modify the DNS zone. This is needed for the Caddy DNS challenge. Go to the Cloudflare dashboard and create a token as follows:

`My Profile` > `API Tokens` > `Create Token` > `Edit Zone DNS` > `Zone:DNS:Edit` > `Include:Specific Zone:<DOMAIN_NAME>` > `Continue to Summary` > `Create Token`

Then, create an `.env` file by copying the `.env.example` file:

```bash
cp .env.example .env
```

Copy the token from the Cloudflare Dashboard and save it to the `.env` file. Also set the `TUNNEL_NAME` and `DOMAIN_NAME` variables in the `.env` file:

```bash
CLOUDFLARE_API_TOKEN="<the-token>"
TUNNEL_NAME="mbp"
DOMAIN_NAME="<the-domain-name>"
```

### Create a Tunnel

You can create a tunnel with following commands:

```bash
source .env
cloudflared tunnel create \
  --credentials-file $DATA_DIR/cloudflared/credentials.json \
  $TUNNEL_NAME
```

This will create a tunnel with the name $TUNNEL_NAME and save the credentials to the `$DATA_DIR/cloudflared/credentials.json` file. The credentials file is used to authenticate the `cloudflared` service and also contains the `TunnelID` which we'll need later.

Note: **Don't** add the credentials file to your git repository. In fact: You should `.gitignore` the whole `$DATA_DIR` directory.

### Configure DNS routing

Configure DNS names to point to the cloudflared tunnel. See [Cloudflare Routing DNS to Tunnel docs](https://developers.cloudflare.com/cloudflare-one/connections/connect-networks/routing-to-tunnel/dns/).

I created two routes for the tunnel, one for Ollama, one for a chat app (OpenWebUI):

```bash
cloudflared tunnel route dns $TUNNEL_NAME ollama.$DOMAIN_NAME
cloudflared tunnel route dns $TUNNEL_NAME chat.$DOMAIN_NAME
```

### Configure the Caddyfile for the DNS Challenge and Test Responses

Configure the DNS challenge, named matchers, and handlers in a `Caddyfile`. You can have a look at the `./conf/caddy/simple-response/Caddyfile` to see the configuration. This is used in the next step to test the tunnel and the DNS routing:

```yaml
*.{$DOMAIN_NAME}:443 {

  tls {
    dns cloudflare {$CLOUDFLARE_API_TOKEN}
    resolvers 1.1.1.1
  }

  @chat {
    host chat.{$DOMAIN_NAME}
  }

  @ollama {
    host ollama.{$DOMAIN_NAME}
  }

  handle @ollama {
    respond @ollama "hi from ollama.{$DOMAIN_NAME}"
  }

  handle @chat {
    respond @chat "hi from chat.{$DOMAIN_NAME}"
  }
}
```

### Configure the Cloudflare Tunnel

Now configure the `cloudflared` service with hostname ingresses.

You can quickly create a configuration file for the `cloudflared` container with the following command:

```bash
source .env
source ./write_cloudflared_config.sh
```

This uses the template at `./conf/cloudflared/config.tpl.yaml` and replaces the `DOMAIN_NAME` placeholder with the variable from the `.env` file and the `TUNNEL_ID` placeholder with the value of `TunnelID` from the `./data/cloudflared/credentials.json` file and saves the result in a newly created `./conf/cloudflared/config.yaml` file. You can also manually create the `./conf/cloudflared/config.yaml` file by doing the same.

The `write_cloudflared_config.sh` script looks like this:

```bash
TUNNEL_ID="`cat $DATA_DIR/cloudflared/credentials.json | jq '.TunnelID'`"
sed "s/TUNNEL_ID/$TUNNEL_ID/g;s/DOMAIN_NAME/$DOMAIN_NAME/g" \
  ./conf/cloudflared/config.tpl.yaml \
  > ./conf/cloudflared/config.yaml
```

Here is the content of the `./conf/cloudflared/config.tpl.yaml` file. If you want to create the `./conf/cloudflared/config.yaml` by hand, you need to replace `TUNNEL_ID` with the id of your tunnel and the `DOMAIN_NAME` with your own domain name. Be sure to use the tunnel **id** here, as the tunnel name doesn't work in the `cloudflared` configuration file:

```yaml
tunnel: TUNNEL_ID
credentials-file: /etc/cloudflared/credentials.json

ingress:
  - hostname: 'chat.DOMAIN_NAME'
    service: https://caddy:443
    originRequest:
      originServerName: '*.DOMAIN_NAME'
      # noTLSVerify: true
      # disableChunkedEncoding: true
  - hostname: 'ollama.DOMAIN_NAME'
    service: https://caddy:443
    originRequest:
      originServerName: '*.DOMAIN_NAME'
  - service: http_status:404 # default service
```

I want to create two ingresses, one ingress for Ollama and one ingress for the chat app. `service` points to the upstream server name. I will call the Docker container `caddy`, this is why I can set `service` to `https://caddy:443`.

The `originRequest` section is optional, but needed in this case to make sure that the TLS handshake works. The value of `originServerName` tells `cloudflared` the server name of the TLS certificate. As Caddy is requesting a wildcard certificate for the `$DOMAIN_NAME`, I can set it to `*.$DOMAIN_NAME`. Alternatively, you could also set `noTLSVerify` to `true` to disable TLS verification.

The `disableChunkedEncoding` helps with some WSGI apps. Here, this is not needed, but I left it in the template as a comment. The `ingress` section ends with an obligatory catch service which returns a `404` error. This is the default service if no other service matches the request.

### Launch cloudflared and Caddy with Docker Compose

At this point, you can test if the tunnel and the DNS routing work. Take a look at `docker-compose.tunnel-test.yml`. This starts the `cloudflared` tunnel and Caddy with the Caddyfile in `./conf/caddy/simple-response`:

```yaml
version: '3'

networks:
  web:
    driver: bridge

services:
  #--- Caddy ---
  caddy:
    build:
      context: ./images/caddy
      dockerfile: ./Dockerfile
    restart: unless-stopped
    environment:
      - CLOUDFLARE_API_TOKEN=${CLOUDFLARE_API_TOKEN}
      - DOMAIN_NAME=${DOMAIN_NAME}
    volumes:
      - ./conf/caddy/simple-response/Caddyfile:/etc/caddy/Caddyfile
      - ${DATA_DIR-./data}/caddy:/data/caddy
    ports:
      - "443:443"
    networks:
      - web
  #--- Cloudflared ---
  cloudflared:
    image: cloudflare/cloudflared
    restart: unless-stopped
    depends_on:
      - caddy
    volumes:
      - ./conf/cloudflared/config.yaml:/etc/cloudflared/config.yml
      - ${DATA_DIR-./data}/cloudflared/credentials.json:/etc/cloudflared/credentials.json
    command: tunnel --config /etc/cloudflared/config.yml run #--loglevel debug run 
    networks:
      - web
```

the **web network** is created with the [Bridge Network driver](https://docs.docker.com/network/drivers/bridge/). As this is a user defined network, DNS resolution between containers is supported. It also provides a scoped network, which means, only containers in the same network can communicate with each other.

The **Caddy service** is based on a custom Docker image to include the Caddy module for the Cloudflare DNS acme challenge, which is not included in the default Caddy docker image.

the **volumes** bind the `Caddyfile` and the `caddy` data directory to the container. You should make sure to not commit the data directory to git as it contains the private keys for TLS certificate and the cloudflared credentials.

Port **443** is mapped to the host system. This way, you can also reach the services from your local machine or your local network without going over the Internet.

The **cloudflared** service depends on the caddy service, binds the `config.yaml` and `credentials.json` files to the container, and runs the `tunnel` command with the `run` option.

Start the service in the foreground with `docker-compose up`.

Test if it works by browsing to the domains (https://chat.$DOMAIN_NAME, https://ollama.$DOMAIN_NAME). You should see the "hi from chat.$DOMAIN_NAME" and "hi from ollama.$DOMAIN_NAME" messages. Alternatively, you can also use `curl` in another terminal to test the services:

```bash
curl -k https://chat.$DOMAIN_NAME
curl -k https://ollama.$DOMAIN_NAME
```

You can also use the service from the local machine and the local network with the public domain name. As Caddy presents a TLS certificate for the public domain name that's signed by Let's Encrypt, your browser and other clients will most probably trust the certificate.

If you have a local DNS server which you can configure, you can use the services both at home and on the go via internet without changing anything on the client side. Just point the $DOMAIN_NAME to the local network ip where Caddy is running. From then on requests will directly be served by the local service without going over the Internet when you are in your local home network.

You can test this `curl` even if you don't have a configurable DNS server with the `--resolve` switch:

```bash
curl --resolve 'ollama.$DOMAIN_NAME:443:127.0.0.1' \
-v https://ollama.$DOMAIN_NAME
```

The `--resolve` switch tells curl to resolve the domain to the local IP address. Be sure to append the port number after the domain name and *don't* append it again after the IP. 

If you want to test it from another computer in your local network, change the ip to the local network ip of the machine Caddy is running on.

The `-v` switch is for verbose output. With this, you can see that the SSL certificate is verified.

When you're done testing the tunnel and local access, stop the services with `ctrl-c`. If you are not running the service, enter `docker-compose down`.

### Configure Caddy as a Reverse Proxy

Now, reconfigure Caddy to act as a reverse proxy. On my system, Ollama is running directly on the host. 

As the Ollama API is not protected with an API_KEY, I also added a simple API_KEY check to the Caddyfile. This way, Ollama is protected when it's accessed via the Caddy reverse proxy (and the public `$DOMAIN_NAME`), but still unprotected, when accessed directly via localhost. The API key check protects against unauthenticated use of Ollama from the internet. The unprotected access is necessary for OpenWebUI, since OpenWebUI doesn't support API_KEY authentication for Ollama, yet.

Here is the content of the updated Caddyfile which you can find in `./conf/caddy/Caddyfile`:

```caddy
*.{$DOMAIN_NAME}:443 {
  tls {
    dns cloudflare {$CLOUDFLARE_API_TOKEN}
    resolvers 1.1.1.1
  }

  @ollamaValidApiKey {
    host ollama.{$DOMAIN_NAME}
    header Authorization "Bearer {$OLLAMA_API_KEY}"
  }

  @ollama {
    host ollama.{$DOMAIN_NAME}
  }

  handle @ollamaValidApiKey {
    reverse_proxy host.docker.internal:11434
  }

  handle @ollama {
    header Content-Type application/json
    root * /srv
    rewrite * /401.json
    file_server
  }

  @chat host chat.{$DOMAIN_NAME}
  reverse_proxy @chat open-webui:8080

  log
}
```

The `@ollamaValidApiKey` matcher checks for a valid API_KEY in the `Authorization` header for the Ollama service.

The `handle @ollamaValidApiKey` directive reverse proxies the Ollama service to the local host. 

The `host.docker.internal` is a special DNS name that resolves to the internal IP address of the host system. It is defined in the docker-compose.yml file for the caddy service (and the open-webui service) so that they can reach the Ollama service which is running directly on the host. You can also deploy Ollama in a container and use the container name as the host, but this is not covered, here.
- The `handle @ollama` directive now responds with a 401 error if no valid API_KEY is provided. Caddy acts as a file server, serving the `401.json` file from the `/srv` directory in all cases. This file replicates the respective error message of the OpenAI API.
- The `@chat` matcher is the same.
- The `reverse_proxy @chat` directive reverse proxies the OpenWebUI service to the local host.
- The `log` directive tells Caddy to log the requests to stdout which then shows up in the docker logs.

Caddy selects the most specific matcher that matches the request. If the client presents a correct API_KEY (which we set using the environment variable `OLLAMA_API_KEY`), the request is reverse proxied to the Ollama service. If the client doesn't present a correct API_KEY, the `@ollama` matcher matches and Caddy responds with a 401 error with the JSON body as defined in `./conf/caddy/401.json`:

```json
{
    "error": { 
        "message": "You didn't provide a valid API key. You need to provide your API key in an Authorization header using Bearer auth (i.e. Authorization: Bearer YOUR_KEY)",
        "type": "invalid_request_error",
        "param": null,
        "code": null
    }
}
```

The final `docker-compose.yml` file looks like this:

```yaml
version: '3'

networks:
  web:
    driver: bridge

services:
  #--- OpenWebUI  ---
  open-webui:
    image: ghcr.io/open-webui/open-webui:main
    restart: unless-stopped
    container_name: open-webui
    environment:
      - OLLAMA_API_BASE_URL=http://host.docker.internal:11434/api
      - WEBUI_SECRET_KEY=${WEBUI_SECRET_KEY}
    volumes:
      - ${DATA_DIR-./data}/open-webui:/app/backend/data
    ports:
      - ${OPEN_WEBUI_PORT-3000}:8080
    networks:
      - web
    extra_hosts:
      - "host.docker.internal:host-gateway"
  #--- Caddy ---
  caddy:
    build:
      context: ./images/caddy
      dockerfile: ./Dockerfile
    restart: unless-stopped
    depends_on:
      - open-webui
    environment:
      - CLOUDFLARE_API_TOKEN=${CLOUDFLARE_API_TOKEN}
      - OLLAMA_API_KEY=${OLLAMA_API_KEY}
    volumes:
      - ./conf/caddy/Caddyfile:/etc/caddy/Caddyfile
      - ./conf/caddy/401.json:/srv/401.json
      - ${DATA_DIR-./data}/caddy:/data/caddy
    ports:
      - "443:443"
    networks:
      - web
    extra_hosts:
      - "host.docker.internal:host-gateway"
  #--- Cloudflared ---
  cloudflared:
    image: cloudflare/cloudflared
    restart: unless-stopped
    depends_on:
      - caddy
    volumes:
      - ./conf/cloudflared/config.yaml:/etc/cloudflared/config.yml
      - ${DATA_DIR-./data}/cloudflared/credentials.json:/etc/cloudflared/credentials.json
    command: tunnel --config /etc/cloudflared/config.yml run #--loglevel debug run
    networks:
      - web
```

The `open-webui` service is configured to use the local Ollama service directly with the `OLLAMA_API_BASE_URL`. This way, the OpenWebUI service can access the Ollama service directly without going over the internet and Cloudflare, and without needing to present an API_KEY.

The **ports** section of the `open-webui` service maps the port 8080 of the container to the host system at port 3000 by default. You can configure the port with the `OPEN_WEBUI_PORT` environment variable. With this, , you can also reach the OpenWebUI service from your local machine or your local network directly at `http://localhost:3000/`, for example.

The `extra_hosts` section is needed to resolve the `host.docker.internal` DNS name to the internal IP address of the host system. This is needed because the OpenWebUI service is running in a container and needs to reach the Ollama service which is running directly on the host.

`WEBUI_SECRET_KEY` initializes the OpenWebUI backend with a secret key. This is used to secure the session and the cookies. You can generate a secret key with the following command and save it in an `.env` file (see also the `.env.example` file):

```bash
python -c "import secrets; print(secrets.token_urlsafe())"
```

The `caddy` service is configured to use the final Caddyfile with the reverse proxy configuration. The `CLOUDFLARE_API_TOKEN` and `OLLAMA_API_KEY` are set as environment variables. You can add the `OLLAMA_API_KEY` to the `.env` file with the same python command described above for the `WEBUI_SECRET_KEY`. The `CLOUDFLARE_API_TOKEN` should already be defined there. Finally, the service is also configured to depend on the `open-webui` service.

### Start and Test the Services

Start the services, this time, you can also start them in the background with `docker-compose up -d --build`.

Test from the internet with curl:

```bash
curl -H "Authorization: Bearer $OLLAMA_API_KEY" -v https://ollama.$DOMAIN_NAME/api/generate -d '{
  "model": "llama2",
  "prompt": "Why is the sky blue?"
}'
```

Test from local machine with curl:

```bash
curl -H "Authorization: Bearer $OLLAMA_API_KEY" --resolve "ollama.$DOMAIN_NAME:443:127.0.0.1" -v https://ollama.$DOMAIN_NAME/api/generate -d '{
  "model": "llama2",
  "prompt": "Why is the sky blue?"
}'
```