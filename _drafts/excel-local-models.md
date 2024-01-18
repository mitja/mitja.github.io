---
date: 2023-10-16
title: Calling Local LLMs from Microsoft Office
author: mitja
category: Excel is All You Need
tags:
 - Microsoft Office
 - Excel
 - Generative AI
 - LLMs
---

- you can call localhost from add-ins
- but you must still use TLS and valid certificates.
- see: https://stackoverflow.com/questions/48541660/office-2016-add-in-communicating-to-http-localhost
- workarounds are not recommended (often not possible due to security policies):
- install self-signed cert, allow unsafe in dev settings, allow not-safe in browser.
- best: get a valid cert for localhost

https://github.com/python-trio/trustme

- own unique dns names for internal systems
- use an internal CA or let's encrypt (with wildard or individual certs)
- https://blog.heckel.io/2018/08/05/issuing-lets-encrypt-certificates-for-65000-internal-servers/

mkcert is a simple tool for making locally-trusted development certificates. It requires no configuration.
https://github.com/FiloSottile/mkcert

you can make the local service available on the internet with an ephemeral tunnel, like https://tunnel.pyjam.as

https://web.dev/articles/how-to-use-local-https

maybe 127.0.0.1 works as this is considered safe by modern browsers even with http.
https://letsencrypt.org/docs/certificates-for-localhost/

https://github.com/anderspitman/awesome-tunneling

https://nip.io

https://kags.me.ke/post/office-add-in-mkcert-localhost-ssl-certificate/
https://kags.me.ke/post/office-mac-side-load-excel-add-in/


https://learn.microsoft.com/en-us/answers/questions/234390/officejs-add-in-communicate-with-external-local-na