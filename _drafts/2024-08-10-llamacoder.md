---
title: "Llama Coder: An Open Source Variant of Claude Artifacts"
author: mitja
date: 2024-08-10
category: Building AI Apps
tags: [Claude, Artifacts, Llama, together.ai]
#pin: true
#math: true
#mermaid: true
render_with_liquid: false
permalink: /blog/2024/08/10/llamacoder/
image:
  path: /assets/blog/2024/llamacoder/llamacoder-screenshot.png
  alt: A screenshot of the LlamaCoder App
---

Llama Coder is an Open Source variant of Claude Artifacts. It uses Llama 3.1 405B hosted by Together AI and Sandpack for the code sandboxes. 

The [code](https://github.com/Nutlope/llamacoder) is lean and simple. Amazing! Here is a Tweet by the author with a big picture of the architecture:

https://x.com/nutlope/status/1820299550269358582

The [main prompt](https://github.com/Nutlope/llamacoder/blob/main/app/api/generateCode/route.ts) is surprisingly simple, too - with some prompt engineering hacks thrown in. 

This is a somewhat complete list of the stack:

- Vercel for hosting
- [Next.js app router](https://nextjs.org/docs/app) for the app (The Next.js App Router introduces a new model for building applications using React's latest features such as Server Components, Streaming with Suspense, and Server Actions.)
- GitHub Actions for CI/CD
- Sandpack for the code sandbox (client side javascript, typescript)
- Together AI for inference hosting with 
- Llama 3.1 405B model
- Helicone for LLM observability
- Plausible for Analytics

It looks like a pragmatic and productive TypeScript LLM app stack stack for indie hackers to me.

I was curious to learn what Hassan would use for a database, and the auth provider. Peeking into his [PDFtoChat](https://github.com/Nutlope/pdftochat?tab=readme-ov-file) app, I found out, he used **MongoDB**, and **Clerk**. I normally use PostgreSQL and SQLite, so I didn't know that MongoDB also has a vector index feature. I also didn't know about Clerk but it sounds like a reasonable choice for indie hackers: It's a bit more expensive than eg. Firebase/GCP Identity Platform, Azure AD, or AWS Cognito, but it's probably easier to setup and manage.

I tried LlamaCoder with some tiny ideas I had. The first didn't work. The code abruptly ended, I assume it didn't fit in the output token limit. The next was even simpler and worked out of the box: It's a IBAN calculator. This is for EU residents like me who cannot remember their IBAN but know their old bank account number by heart. I normally use a very old website for this, but this is so ad-laden that I feel the urge to create my own every time I use it. Now, with the help of LlamaCoder, I finally did it.

I've created the backend with Python and Simon Willisons great llm CLI tool with the same prompt and model, but I adjusted it to generate Python/FastAPI code for the backend, instead. I deployed the app as Azure Function.

---

fastassistants.com 

- [ ] Create OpenAI Assistants API based apps with ...
- [ ] Create a FastHTML app with Llama Coder
- [ ] Use the OpenAI Assistants API or Open Assistants.
- [ ] Run code with ...

Following Hassan's great example of just putting apps out there, I adapted his approach to generate and run Python FastHTML apps in a sandbox. The app is of course developed in FastHTML and the sandbox is based on the great. xxx project. You can find the app here and the source code here. Happy coding!

---

runpeer.com

- run a local code sandbox like Llama Coder or Anthropic Artefacts and connect it to a custom GPT.
- how it works:
  - in your Chat, ask the @runpeer <filename> custom GPT to run code for you
  - the custom GPT will create a unique URL
  - open the URL in your browser: you are asked to sign in, then you get a code sandbox where ChatGPT will send the code to run it.
- reuse connections across chats with @runpeer token (same user only)
- rerun after longer downtime or by other users: use new token
- customize: prompt for the...
- you can also use it via the API as a tool...

what can you run?

- TS/React...
- customize the stack
- maybe later: anything supported by X (Python, Sqlite, Kubernetes, Linux...)

Pro features:

- longer kept open
- more sessions per day
- save configurations
- run serverside (not in browser)

"DE"
, "DE-de"
, "de-DE"
, "de"
, "de-de"
, "de-ch"
, "de-CH"
, "de-at"
, "de-AT"
, "ger-de"
, "de-Sie"
, "German"
, "ger"
, "deutsch"
, "De-de"
, "de-GER"
, "Deuts"
, "de-ch,gs"
, "de-De"
, "deu"
, "de_DE"
, "en-DE"
, "de-li"
, "de-lu"
, "en-de"
, "de-en"
---

select count(id), sum(episodeCount) from podcasts where newestItemPubdate > 1704067200 and language in ("DE"
, "DE-de"
, "de-DE"
, "de"
, "de-de"
, "de-ch"
, "de-CH"
, "de-at"
, "de-AT"
, "ger-de"
, "de-Sie"
, "German"
, "ger"
, "deutsch"
, "De-de"
, "de-GER"
, "Deuts"
, "de-ch,gs"
, "de-De"
, "deu"
, "de_DE"
, "en-DE"
, "de-li"
, "de-lu"
, "en-de"
, "de-en");


select 
  id, 
  title, 
  link, 
  url,
  episodeCount, 
  popularityScore, 
  priority,
  updateFrequency, 
  description, 
  category1, 
  category2,
  category3,
  category4,
  category5,
  category6,
  category7,
  category8,
  category9,
  category10
from podcasts 
where 
  newestItemPubdate > 1704067200 and 
  language in ("DE"
, "DE-de"
, "de-DE"
, "de"
, "de-de"
, "de-ch"
, "de-CH"
, "de-at"
, "de-AT"
, "ger-de"
, "de-Sie"
, "German"
, "ger"
, "deutsch"
, "De-de"
, "de-GER"
, "Deuts"
, "de-ch,gs"
, "de-De"
, "deu"
, "de_DE"
, "en-DE"
, "de-li"
, "de-lu"
, "en-de"
, "de-en");

--

## Prompt for Claude to download RSS feeds for Podcasts in German that have episodes in 2024

Create a python script that downloads RSS feeds. It gets the list of podcasts with their id, title, and feed url by querying the sqlite database `podcastindex_feeds.db` with following query:

```
select 
  id, 
  title, 
  url
from podcasts 
where 
  newestItemPubdate > 1704067200 and 
  language in ("DE", "DE-de", "de-DE", "de", "de-de", "de-ch", 
    "de-CH", "de-at", "de-AT", "ger-de", "de-Sie", "German", "ger", 
    "deutsch", "De-de", "de-GER", "Deuts", "de-ch,gs", "de-De", "deu",
    "de_DE", "en-DE", "de-li", "de-lu", "en-de", "de-en");
```

For each feed:

- it prints the title
- it downloads the RSS feed from the url
- it and saves the RSS feed as file named f'{id}.rss'

## Prompt for Claude to save episodes data in a sqlite database

Please create a python script that saves data about podcasts episodes from an RSS feed to a sqlite database.

The feeds have been downloaded and in a previous step and are saved as files named f'feed_{id}.xml'.

Create a table named `episodes` if it does not exist in the sqlite database `podcastindex_episodes.db` with an appropriate schema to store the episodes data. Please store at least:

- podcast_id (from file name, foreign key to column `id` of table `podcasts`)
- title
- description
- link ("" if not present or if this leads to an exception while parsing)
- duration (as string)
- pub_date
- enclosure_url ("" if not present of if this leads to an exception while parsing, the first only, if there are multiple)
- enclosure_length (0 if not present of if this leads to an exception while parsing, the first only, if there are multiple)
- multiple_enclosures (FALSE by default, TRUE if there are multiple enclosures)
- itunes_author
- transcript ("" if not present or if this leads to an exception while parsing)

Please batch the writes (eg. commit all episodes for a podcast at once).

## Normalize the duration

select 
  case when 
    duration like "%:%" 
  then 
    case when 
      length(duration) = 8 
        then 
          duration 
        else 
          "00:" || duration 
        end
  else
    time(duration, "unixepoch") 
  end as duration 
from 
  episodes 
limit 1000;

## Select Summarized data for Podcast Episodes in German since 2024

This is the query without duration normalization:

```sql
select 
  count(id), 
  time(
    sum(strftime('%s', duration)), 
    'unixepoch'
  ) as total_duration, 
  sum(enclosure_length)/1024/1024/1024/1024 as terabyte 
from 
  episodes 
where 
  pub_date > "2024-01-01";
```

This is the query with duration normalization:

```sql
select 
  count(id), 
       
    sum(strftime('%s', 
      case when 
        duration like "%:%" 
      then 
        case when 
          length(duration) = 8 
            then 
              duration 
            else 
              "00:" || duration 
            end
      else
        time(duration, "unixepoch") 
      end
      ) - strftime('%s', '00:00:00')) as total_duration, 
  sum(enclosure_length) as bytes
from                            
  episodes                            
where 
  pub_date > "2024-01-01";
```

Ergebnis:

`444958|803533710|18219201517327`

Also:

- 444958 Episoden
- 803533710 Sekunden (223203 Stunden)
- 18219201517327 Bytes (16.6 TB)

Dann noch im März 2024, April 2024, Mai 2024, Juni 2024:

```
2024-03|61100|114144558|2572254914220
2024-04|59956|111529910|2547845563502
2024-05|62679|115964970|2613496654616
2024-06|61506|109942016|2531212425247
2024-07|65445|110502130|2531300567472
```

Also z. B. im März 2024:

- 61100 Episoden
- 114144558 Sekunden (31707 Stunden)
- 2,4 TB

Und im Juli 2024:

- 65445 Episoden
- 110502130 Sekunden (30694 Stunden)
- 2,3 TB

Je Tag (bei 31 Tagen):

- 2111 Episoden
- 990 Stunden
- 0,08 TB

GPUs:

4090 2k (24 GB), ab 1800 €
4080 Super 1,05k (16 GB)
4070 Ti Super 850 € (16 GB)
4060 350 EUR, (12 GB)
4060 500 EUR TI (16 GB), sogar langsamere Mem Band als 3060 288.0 GB/s
3060 300 EUR, 12 GB 360 GB/s

https://technical.city/en/video/GeForce-RTX-4090-vs-GeForce-RTX-4080-SUPER

Dann noch in der Woche vom 1. bis 7. Juli 2024:


Das erfordert rund 1 Gbit/s zum Runterladen.
Speicherplatz: rd. 30 TB je Jahr, plus Backup.
2 Server mit den GPUs (redundanz)
je Lokation 1 Server mit dem Storage

119 EUR x 2 f. 1/3 Rack, 1 Gbit/s (aktiv/aktiv auf beiden seiten), 2 TB inklusive
extra Bandbreite je TB: 1 EUR/TB

Vlt reicht auch 2x der GPU Server. (RTX 4000, 20 GiB, 1 Gbit/s, 2 TB)
die Podcasts werden nicht aufgehoben
nur die Transscripte


Use feedparser to get data out

please create a python script that saves the episodes data in a sqlite database. It gets the list of podcasts with their id, title, and feed url by querying the sqlite database `podcastindex_feeds.db` with following query:

```

- it the episodes in the sqlite database "podcastindex_episodes.db" with the following schema:


podcastindex_feeds.db

popularityScore
updateFrequency
description
category1

Strategy:

- launch simple but useful apps
- for free, and with open source
- if an app gains traction: add a paid tier