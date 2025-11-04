---
author: null
categories:
- AI Engineering
- Blog
date: 2025-10-17
draft: false
slug: mcp-im-chatgpt-developer-mode-beta
tags:
- ChatGPT
- MCP
title: MCP im ChatGPT Developer Mode (Beta)
---

OpenAI hat gerade MCP Connectors und den ChatGPT Developer Mode (Beta) veröffentlicht. In diesem Beitrag beschreibe ich, wie man MCP Server mit ChatGPT verbindet, zeige, wie MCP Konnektoren sich in einer Chat Session anfühlen, und gebe einen Überblick über die aktuellen Einschränkungen.

<!-- more -->

## Developer Mode aktivieren

MCP Konnektoren in ChatGPT können nur im Developer Mode erstellt und bearbeitet werden. Der Developer Mode wirkt dabei durchaus etwas angsteinflößend:

![Eingabeoberfläche von ChatGPT im Developer Mode](developer-mode-input.webp)

{{< alert >}}
**Hinweis:** Dieser Artikel ist aus der Perspektive eines Pro-Account Users geschrieben. OpenAIs [Dokumentation zu Developer Mode und MCP Connectors in ChatGPT](
https://help.openai.com/de-de/articles/12584461-developer-mode-and-full-mcp-connectors-in-chatgpt-beta) beschreibt, dass Admins MCPs in ihrer Organisation veröffentlichen können. Ich kann das nicht testen, gehe aber davon aus, dass MCP Konnektoren dann auch im normalen ChatGPT Modus nutzbar sind.
{{< /alert >}}

Der Developer Mode lässt sich unter `Settings > Apps & Connectors > Advanced Settings` aktivieren. 

## Einen MCP Connector erstellen

Sobald der Developer Mode aktiv ist, können MCP Serververbindungen unter `Settings > Apps & Connectors` hinzugefügt werden:

![ChatGPT Apps & Connector-Einstellungen](chatgpt-apps-and-connectors-settings.webp)

Konnektoren können ein Icon, Authentifizierungsinformationen und eine Beschreibung haben und brauchen einen Namen und die MCP-Server-URL. Sowohl SSE als auch Streaming-Transport werden unterstützt. Für die Authentifizierung kann nur OAuth 2.0 verwendet werden.

![ChatGPT MCP-Connector erstellen](chatgpt-create-mcp-connector.webp)

## Einen MCP Connector verwenden

MCP Verbindungen müssen in jeder Chatsitzung für jeden MCP Server aktiviert werden:

![MCP in einem Chat aktivieren](activate-custom-mcps-in-a-chat.webp)

In meinen Tests nutzt ChatGPT MCP Server nur, wenn es ausdrücklich dazu aufgefordert wird. Aktionen müssen bestätigt werden, was aber für die Dauer eines Chats gespeichert werden kann:

![Benutzerdefinierter MCP in einer Chatsitzung](custom-mcp-in-a-chat-session.webp)

{{< alert >}}
**Hinweis**: ChatGPT kennzeichnet diese Aktion als Write-Aktion, obwohl sie aus Nutzersicht eigentlich eine Read-Aktion ist. Ich weiß nicht, ob das ein Fehler auf Seiten des DeepWiki-MCP ist; interessant ist für mich, dass Pro-Accounts offenbar bereits Write-Aktionen unterstützen, obwohl das noch als Einschränkung dokumentiert ist.
{{< /alert >}}

MCP Konnektoren können nicht zu Custom GPTs hinzugefügt werden. Es gibt also keine Möglichkeit, die für den Aufruf eines MCP Servers erforderlichen Anweisungen zusammen mit der MCP Verbindung vorzukonfigurieren.

## Aktuelle Einschränkungen

Derzeit haben MCP Konnektoren in ChatGPT noch einige Einschränkungen:

- Nicht für Free-Accounts verfügbar.
- Pro-Accounts können nur Read/Fetch-Aktionen nutzen (laut Dokumentation; möglicherweise nicht mehr aktuell)
- Lokale MCPs sind nicht möglich.
- Agent Mode unterstützt keine Custom Connectors. 
- Deep Research Mode unterstützt nur Read/Fetch-Aktionen.
- Nur im Web verfügbar, nicht in der mobilen App. In der Desktop-App sind verbundene MCPs sichtbar, können aber (bei Pro-Accounts) nicht verwendet werden, da die Desktop-App den Developer Mode nicht unterstützt. Ich vermute, dass MCPs in Business- und Enterprise/Edu-Accounts nutzbar sein könnten.

## Versuch einer Einordnung

Im Moment sind MCP Konnektoren in ChatGPT aus meiner Sicht noch nicht alltagstauglich – kein Wunder, es ist schließlich eine Beta. Derweil sind "Actions" in Custom GPTs weiterhin nutzbar. Außerdem sind sie offener und nicht so angsteinflößend in der Bedienung.

OpenAI hätte MCP Connectors zu Custom GPTs hinzufügen und eine Option anbieten können, bestimmte Aktionen für bestimmte MCP Server vorab zu bestätigen. Es hat sich mit dem Developer Mode aber für einen anderen Weg entschieden.

Für mich sind MCP Server eine Möglichkeit, Chatbots anzupassen und ihnen eine gewisse "Agency" zu geben. Use-Case-spezifische MCP Server finde ich dafür besser geeignet als generische, die aus meiner Sicht dazu neigen, den Kontext aufzublähen und das LLM abzulenken.

Ich hoffe, dass OpenAI MCP Connectors in ChatGPT weiterentwickelt, ohne ein obligatorisches Validierungsverfahren, ähnlich wie in App Stores einzuführen; darauf wetten würde ich im Moment aber nicht.