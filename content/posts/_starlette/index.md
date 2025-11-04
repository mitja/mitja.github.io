---
title: "Starlette basics for creating AI apps with FastAPI, FastHTML, and Air"
date: 2025-10-14
categories: ["AI Engineering", "Blog"]
#tags: ["Claude", "Devcontainer"]
draft: true
---

- ASGI Framework, minimal ASGI toolkit
- used by FastAPI, FastHTML, Air
- https://www.starlette.dev

ASGI stands for Asynchronous Server Gateway Interface — it’s the modern, async-enabled successor to WSGI (the long-standing Python web standard).

<!-- more -->

- a specification, not a lib or framework
- It defines how web servers and Python apps talk to each other for web requests, WebSockets, background tasks, etc.
  - WSGI = sync-only (one request = one thread)
  - ASGI = async and extensible (supports HTTP, WebSockets, SSE, etc.)

minimal ASGI app:

```python
async def app(scope, receive, send):
    assert scope['type'] == 'http'
    await send({
        'type': 'http.response.start',
        'status': 200,
        'headers': [(b'content-type', b'text/plain')],
    })
    await send({
        'type': 'http.response.body',
        'body': b'Hello, world!',
    })
```

run with `uvicorn myapp:app`

minimal WSGI app: 

```python
def app(environ, start_response):
    assert environ["REQUEST_METHOD"] in {"GET", "HEAD"}
    start_response("200 OK", [("Content-Type", "text/plain; charset=utf-8")])
    return [b"Hello from WSGI!"]
```

run with `gunicorn hello_wsgi:app`

Minimal Starlette app:

```python
# starlette_asgi.py
from starlette.applications import Starlette
from starlette.responses import PlainTextResponse
from starlette.routing import Route

async def homepage(request):
    return PlainTextResponse("Hello from Starlette (ASGI)!")

app = Starlette(routes=[Route("/", homepage)])
```

run with `uvicorn starlette_asgi:app``

ASGI can do websockets:

```python
# starlette_ws.py
from starlette.applications import Starlette
from starlette.endpoints import WebSocketEndpoint
from starlette.routing import WebSocketRoute

class Echo(WebSocketEndpoint):
    encoding = "text"
    async def on_connect(self, websocket):
        await websocket.accept()
    async def on_receive(self, websocket, data):
        await websocket.send_text(f"echo: {data}")

app = Starlette(routes=[WebSocketRoute("/ws", Echo)])
```

run with `uvicorn starlette_ws:app`.

Connect with [websocat](https://github.com/vi/websocat):

websocat `ws://localhost:8000/ws`

WSGI cant do websockets, there are workarounds:

Short answer: **Not with *pure* WSGI.**
WSGI’s spec only supports a one-shot HTTP request→response. WebSockets require an HTTP “Upgrade” and a **bidirectional, long-lived** connection—outside WSGI’s model.

### What you *can* do instead

* **Use ASGI for WebSockets**
  Run an ASGI app (Starlette/FastAPI/Quart/Django Channels) behind your reverse proxy; keep your WSGI app for the rest. Common pattern: Nginx routes `/ws` → Uvicorn/Hypercorn; everything else → Gunicorn/uWSGI.

* **Use a server/framework that bypasses WSGI for WS**

  * **Flask-SocketIO** with **eventlet** or **gevent**. This doesn’t use pure WSGI for the WebSocket path; it uses the async server’s own protocol handling (e.g., Gunicorn + `geventwebsocket` worker). Works well but is a different execution model than standard WSGI.
  * Older approaches like **Flask-Sockets** + `gevent-websocket` (largely deprecated now).

* **Fallback techniques on WSGI**

  * **Server-Sent Events (SSE):** one-way (server→client) streaming over HTTP. Works in many WSGI servers, but no client→server push on the same stream.
  * **Long polling / polling:** simulate “real-time,” higher latency/overhead.

### Practical recommendations

* Need real WebSockets or high concurrency? **Add an ASGI sidecar** and proxy `/ws` to it.
* Sticking with Flask and okay with its ecosystem? **Flask-SocketIO + eventlet/gevent** is battle-tested—but understand it’s not pure WSGI.
* Only need server→client updates? **SSE** is simple and WSGI-friendly.

If you tell me your current stack (Flask? Gunicorn? Nginx? Docker/K8s?) I’ll sketch the cleanest wiring diagram and a minimal config.

---

WSGI can do Server-Sent Events (SSE) — with some caveats.

1. Why SSE works (and WebSockets don’t)
SSE = one-way stream (server → client) over a single HTTP response.
WSGI fully supports streaming responses (i.e., yielding data chunks instead of returning them all at once).
So: as long as your web server doesn’t buffer the output, you can stream SSE events from a WSGI app.
In contrast, WebSockets require bidirectional communication and an HTTP protocol upgrade, which WSGI explicitly doesn’t support.