---
layout: post
title: "An Overview of the Voice AI Landscape (Session Notes)"
date: 2025-05-08
author: mitja
category: "Voice Agents"
tags: [Raspberry Pi, Docker, Docker Compose, Tutorial]
image:
  path: /assets/blog/2025/voice-ai-landscape.jpg
  alt: "An AI generated pop art style image showing a mic, a comic speech bubble, a human head speaking and listening to a loudspeaker. In a corner, there is a symbol for AI showing six circles, connected and arranged like a star."
---

I'm so happy to be part of the [Voice Agents Course](https://maven.com/pipecat/voice-ai-and-voice-agents-a-technical-deep-dive) by Kwindla and swyx. Yesterday, Kwindla kicked it off with an overview of the voice AI landscape. The pace, insights, and questions from the audience were just great.

Here are my personal notes, probably incomplete and maybe not always correct. For a more authoritative overview of the Voice AI landscape, check out their free online book [Voice AI & Voice Agents - An Illustrated Primer](https://voiceaiandvoiceagents.com).

- Voice AI has highly valuable use cases with actual real business value.
- Benefits:
  - Today: lower cost.
  - Soon: Better. (peak load response, better answers than most humans can give)
- RAG is still important
- Some challenges:
  - latency 
    - measure regularly end-to-end from/to clients, 
    - record conversation with mic, 
    - visually look at gaps in waveforms, 
    - test calls from different regions and cell phone providers
    - aim for 800ms, tough but possible to hit with hosted inference, 
    - very optimized/limited deployments can hit 500ms with quality compromises
    - 1000ms is not uncommon (still makes users happy)
  - turn detection 
    - from VAD to semantic
    - OpenAI shipped a good text mode TDM
    - Gemini flash in audio is ok, but needs to run as parallel flow ("greedily")
    - LifeKit vs. PipeCat is text vs. audio / end of speech, no audio cues vs. with audio cues
    - both a hard ML challenge and important for experience
  - interruption handling
  - context management
  - function calling, tool use
  - sripting, instruction following
- standard architecture
  - today: 3 models (STT - LLM - STT), easier to achieve robust results with LLMs in text mode
  - future probably converged
  - 3 models, because 
    - LLMs' text mode is their mode
    - we ride on the edge what the best models can do
    - today, we need to use their best mode
  - other use cases, like language learning, can better leverage the benefits of speech-to-speech (1 model)
- models used (speed and quality, time-to-first token/byte more important than tokens/s)
  - STT: 
    - Deepgram
    - Whisper (optimized for streaming, original not built for streaming), down at 400
    - Gladia (for non-english languages)
  - LLM:
    - GPT-4o 
      - still the workhorse, still more than 4.1
      - big model changes take work and good evals (nobody has good ones),
      - models usually not optimized for voice AI, 
      - not yet better results
      - 4o-mini was cheaper but slower and worse for tool/function
      - note from a fellow student: 4.1-mini might be interesting
    - Gemini 2.0 Flash 
      - very good, fast, cost efficient
      - best audio model for voice AI, today (gemini in audio input mode for voice-to-voice)
      - multi-lingual input is ok, output not so much (use English)
    - mid-sized open models get better, esp. fine-tuned Llama4 (upcoming OpenPipe finetuning session)
    - additional notes about LLM use in voice AI:
      - reliable function calling/tool use is mostly a question of how to prompt 4o against Gemini
      - llama can get there
      - evals are important as ever
  - TTS:
      - PlayAI, Grok
      - OpenAI, Google
      - Cartesia
      - Rime
      - Elevenlabs
  - network transport:
    - why network? We don't get capable enough models on mobile or laptop (yet), 
    - hybrid architectures might be relevant, already
    - telephone is a great transport for voice AI, too 
      - PSTN is with a phone number (eg. from Twilio)
      - SIP is for interconnectivity with digital telephony infra
    - WebSockets are not good for real time client-to-server audio (and video), but ok for server-to-server audio
    - WebRTC is best, complex, but PipeCat supports it ootb, local for testing, in the cloud offering for production,
  - Voice AI building blocks in 2025
    - evals - huge topic
    - hosting and scaling - very different (if you love k8s, your topic)
    - workflow/multi-agent/state machines
    - "perfect" speech
      - LLMs in text mode have passed the turing test
      - not quite reached the point for real-time audio recognition and generation 
      - eg. accurately recording email, postal addess
    - human-like turn detection 
      - very important for qualitative experience 
      - fun and hard ML problem
  - what's next?
    - speech to speech models
    - realtime video
    - programming with voice
    - voice as universal user experience
    - LLM as a judge
- orchestration and flows questions
  - voice in text out can be done with PipeCat aggregator (no great example, yet)
  - accents and voice models: Gladia input, PlayAI output
  - tip for Gemini: if you want accents, specify your country.
  - how to solve cold-start? 
    - Daily solved it for us 
    - own infra: Combine optimized startup and warm capacity
  - faster responses: 
    - greedily inference/speculative before turn-detection
    - helpful but more costly
  - multi-speaker:
    - hard, no great solution, so far. 
    - training data doesn't map well to multi-person/agent conversation
    - challenge: know when models should or shouldn't respond (emit a no-response-token)
  - observability tooling (multiple vendors, eg. Coval, will be in Discord and hold sessions)
 
Even after the first session, I can already say: If you are interested in Voice AI: **Take the course!**.