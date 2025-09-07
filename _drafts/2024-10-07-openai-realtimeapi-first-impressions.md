---
title: What is new in Excel in Q1 2022
author: mitja
date: 2022-04-24
category: Excel is All You Need
tags: [Excel]
#pin: true
#math: true
#mermaid: true
render_with_liquid: false
permalink: /blog/2022/04/24/what-is-new-in-excel-in-q1-2022/
image:
  path: /assets/img/featured-excel-q1-2022.png
  alt: What is new in Excel in Q1 2022
---

These are my first impressions of the OpenAI Realtime API. I read the announcement, followed coverage of the DevDay, read related OpenAI forum discussions, followed the [guide](https://platform.openai.com/docs/guides/realtime), read the documentation, played with it on the [playgroud](https://platform.openai.com/playground/realtime), deployed and used the example [openai-realtime-console](https://github.com/openai/openai-realtime-console) application based on the [openai-realtime-api-beta](https://github.com/openai/openai-realtime-api-beta) JS reference client, used the Azure example application and created an own sample application with a Python backend and a React frontend.

## What is the OpenAI Realtime API?

The OpenAI Realtime API lets you create a persistent WebSocket connection to exchange messages with a special variant of GPT-4o optimized for audio input and output. The API supports function calling and is designed for real-time applications, especially voice apps, that require high fidelity, low latency interactions such as coaching, language learning, customer or expert support, and more.

## It's much more complex than the Chat Completions API

- websockets are inherently more complex than REST
- audio complicates things, further
- it's stateful
- there are many message types and a hierarchy of events
- there is no Python client, yet 😢
- very few examples, yet

## Realtime Audio is 10x more expensive than a multi-model solution

The [OpenAI API Pricing](https://openai.com/api/pricing/) page lists the cost of the Realtime API. Currently there is only one model available (`gpt-4o-realtime-preview`). Costs are different for text and audio. Here is a price table, with the standard gpt-4o model as comparison:

| Model/Modality | $ per 1M input token | $ per 1M output token |
|----------------|----------------------|-----------------------|
| gpt-4o         | $3.75                | $15                   |
| Realtime Text  | $5                   | $20                   |
| Realtime Audio | $100                 | $200                  |

The cost of audio is very high. According to OpenAI, audio input costs about 6¢ per minute ($3.60/hour); Audio output 24¢ per minute ($14.40/hour). As both streams are active at the same time, the total cost is 30¢ per minute ($18/hour).

This is about on par with human labor costs in many countries. In addition: Advanced Voice Mode is included in the 20 USD/Month subscription plan. Thus, it's not only impossible to compete economically with OpenAI's product on similar general-purpose solutions. Also, it sets expectations of how much such a feature may cost.

For comparison: A multi-model solution based on Whisper for tts, gpt-4o for inference, and OpenAI TTS costs about $2 per hour, or 9x less:

```
  $0.36 / minute (Whisper) 
+ $0,56 / hour (gpt-4o input token, $3.75/1M tokens * 150,000 tokens/hour)
+ $0.45 / hour (gpt-4o output token, $15/1M tokens * 30,000 tokens/hour)
+ $0.60 / minute (TTS, $15/1M characters * 36000 characters per hour
= $1.97 / hour
```

I think, 10x less could be kept in mind as a rule of thumb, assuming some minor optimizations like speeding up STT and removing silences. An interesting aspect to look at is that the new Whisper Large v3 Turbo is a very fast speech-to-text model, which could run on a desktop to transcribe the audio in faster-than real-time. (see https://www.reddit.com/r/LocalLLaMA/comments/1fvb83n/open_ais_new_whisper_turbo_model_runs_54_times/)

By the way: I used TTS and not TTS HD in this comparison, as it's better suited for real-time applications: According to OpenAI's documentation, TTS is optimized for speed, whereas TTS HD optimized for quality. 

## Even though it's expensive, Realtime Audio is still a good value

Despite the very high price, I can still see quite a few use cases that are already econnomically sensible. For example, I think I would realtime audio for 

- tech demos, 
- proof-of-concepts,
- user experience benchmarks,
- solutions that provide a lot of value, eg.
  - recorded audio, 
  - high-value application domains, 
  - high-stakes situations, 
  - on-demand upgrade a conversation
- solutions where human-level like performance is needed, but where it's hard to get human labor, e.g. 
  - in the middle of the night,
  - short lead times, 
  - very high peak demand,
  - only for a short time,
- solutions that only work with the advanced voice capabilities, for example:
  - automatic adaption to mulitple languages
  - natural conversation experience, with interruptions, etc.
  - emotions, pitch, etc.

In addition, I expect the price to drop significantly over the next months. I expect this since the preview prices were always higher than the final prices, and since there are already rumors about a cheaper gpt-4o-mini realtime model.

## Realtime Text is only 33% more expensive

What's been a bit overlooked in the discussion is that the realtime API for text is actually not that expensive and even though the model is optimized for audio, it can be used in text only mode, as well:

1. When it comes to audio input, you can just send text instead of audio. 

2. Audio output can be disabled with the modalities parameter of a session. This parameter defines the set of modalities the model can respond with. It defaults to `["text", "audio"]`. To disable audio, set `modalities` to ["text"]. 

I assume, you can even update a running session and thus activate and deactive audio in between turns, but I haven't tried it, yet (see the [API documentation for session update](https://platform.openai.com/docs/api-reference/realtime-client-events/session-update) and a [discussion in the OpenAI forum](https://community.openai.com/t/how-to-get-text-only-output-from-the-realtime-api/967528/6) about this topic.

The realtime API is only 33% more expensive for text than the gpt-4o model when used with the chat completions API. This is a reasonable premium for a real-time API, given that it takes more resources to serve these requests.

## Realtime Text is x times faster

An interesting question is, how much faster is the realtime text API compared to the normal gpt-4o chat completions API in async mode? Of course, it highly depends on the use case and implementation, for example:

- Is there a relay in between? 
- How long are the input and output texts? 
- Are tools involved?

For longer conversations, a significant speedup is achieved because the streaming api is stateful. A session keeps the history, it does not need to be sent on every turn of the conversation. Although the history's token must be paid for they're not sent over the wire.

Despite this obvious benefit for longer conversations, I was more interested in the speed of **very fast turn-by-turn user experiences**. 

To explore this, I've build a simple demo application which implements a "chat-in-bio" app which influencers can link to from a social media bio. It's in a way a substitute for "link-in-bio" services. 

The app also has a chat interace, but it's meant to be used more via buttons. The user sees a list of buttons, on click of a button, more information is displayed and other link buttons are presented. The buttons are displayed by the app, the realtime api generates texts that define what is displayed.

Here is a video of the app in action, first with the gpt-4o chat completions API in async mode, then with the realtime API:

[![Realtime API Chat-in-Bio Demo](https://img.youtube.com/vi/VIDEO-ID/0.jpg)](https://www.youtube.com/watch?v=VIDEO-ID)

I think, the reatime API feels much snappier. It's also measurably faster... 

## Mixed Use is a good tactic to lower costs

The realtime api can also be used in mixed mode, eg. text in, audio out, or audio in, text out. This can mitigate the high costs quite a bit. For example, in an application with ouly short audio inputs, and longer outputs, it's much cheaper to use audio in, text out with realtime API, and then use TTS to generate the audio.

## Coming Soon: Audio in the Chat Completions API

OpenAI also has announced that audio will com to the chat completions API. It will be as expensive as audio in the realtime api, but its much easier to use.

"Audio in the Chat Completions API will be released in the coming weeks, as a new model gpt-4o-audio-preview. With gpt-4o-audio-preview, developers can input text or audio into GPT-4o and receive responses in text, audio, or both."

https://openai.com/index/introducing-the-realtime-api/
More context: OpenAI Forum threads:
- [Realtime API extremely expensive](https://community.openai.com/t/realtime-api-extremely-expensive/966825)
- [Realtime API Details (Costs, Usage, etc.)](https://community.openai.com/t/realtime-api-details-costs-usage-etc/966556)
