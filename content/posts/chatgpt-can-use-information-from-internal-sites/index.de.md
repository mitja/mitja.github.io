---
aliases:
- /blog/2024/11/05/chatgpt-can-use-information-from-internal-sites/
author: null
categories:
- Arbeiten mit KI
date: 2024-11-05
draft: false
showHero: true
slug: chatgpt-kann-informationen-von-internen-websites-nutzen
tags:
- ChatGPT
- Caddy
- Cloudflare Tunnel
title: ChatGPT kann Informationen von internen Websites nutzen
---
Die neue ChatGPT Suchfunktion, die dazu gedacht ist, [„schnelle, aktuelle Antworten mit Links zu relevanten Webquellen zu liefern“](https://openai.com/index/introducing-chatgpt-search/), kann offenbar auch Informationen von internen Websites durchsuchen.

<!-- more -->

Ein erster Hinweis kam von Simon Willison, als er tweetete, dass [ChatGPT den Standort (vermutlich anhand der IP-Adresse) nutzen kann, um relevantere Antworten zu liefern](https://x.com/MitjaMartini/status/1853481953653141588).

Ich wurde neugierig, probierte es selbst aus und sah, dass ChatGPT herausfinden kann wer mein Internetprovider ist (über einen "What's my IP"-Service), was mich zu  der Annahme führte, dass ChatGPT das Internet nicht serverseitig, sondern clientseitig durchsucht.

Um herauszufinden, ob das stimmt, habe ich mit Caddy eine kleine Website aufgesetzt, die unter einer sowohl im Internet als auch im LAN erreichbaren Domain aufrufbar ist und nach Herkunft des Clients unterschiedlichen Inhalt ausliefert. Dafür nutzte ich [Caddys client_ip matcher](https://caddyserver.com/docs/modules/http.matchers.client_ip) und einen [Cloudflare Tunnel](https://www.cloudflare.com/de-de/products/tunnel/).

Nachdem ich die Domain mit der lokalen IP von Caddy in `/etc/hosts` eingetragen habe, um die Domain ohne Umweg über das Internet aufzulösen, sah ChatGPT die internen Inhalte. Als ich die Einträge entfernte (wodurch mein Client die Domain über die Internet-Öffentliche IP aufrief), sah ChatGPT die externen Inhalte.

Ich vermute, das war nicht unbedingt beabsichtigt, zumal es auch nicht von OpenAI dokumentiert ist. Obwohl das auch ein potenzielles Sicherheitsrisiko darstellt, gefällt mir das eher, denn so kann ich private Informationen in ChatGPT verwenden, selbst wenn ich sie nicht im Internet veröffentlicht habe. Ich muss sie nur lokal bereitstellen und ChatGPT sagen, wo sie zu finden sind.