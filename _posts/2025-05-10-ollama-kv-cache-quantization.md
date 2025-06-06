---
title: "K/V Cache Quantization in Ollama"
author: mitja
date: 2025-05-10
category: Local AI
tags: [Ollama, K/V Cache, Quantization]
#pin: true
#math: true
#mermaid: true
render_with_liquid: false
permalink: /blog/kv-cache-quantization-in-ollama/
image:
  path: /assets/blog/2025/kv-cache-quantization-in-ollama.jpg
  alt: An AI generated image about K/V Cache Quantization in Ollama in the style of Dada art.
---
A somewhat hidden feature of Ollama is K/V Cache quantization. K/V Cache quantization in Ollama is not on by default, so you need to activate it by setting the `OLLAMA_KV_CACHE_TYPE` environment variable. Supported values are documented in [How can I set the quantization type for the K/V cache?](https://github.com/ollama/ollama/blob/main/docs/faq.md#how-can-i-set-the-quantization-type-for-the-kv-cache):

- f16
- q8_0
- q4_0

Benefits:

- lower memory consumption
- most pronounced when using small models with large context windows

Drawback:

- lower accuracy (not much)
- The lmdeploy team has written a blog post about [K/V cache quantization accuracy test results](https://lmdeploy.readthedocs.io/en/v0.2.3/quantization/kv_int8.html#accuracy-test).

Example numbers: 

- Llama 3.2 8B supports 128.000 tokens context windows. 
- Running it with Q4_K_M quantization and the longest possible context length, it    consumes 
  - 23.3 GB memory without K/V cache qantization, 
  - 17.0 GB with Q8_K_0 K/V cache quantization, and
  - 13.8 GB with Q4_K_0 K/V cache quantization.
- it now fits into 16 GB RAM...
- Sam McLeod's [vram-estimator](https://smcleod.net/vram-estimator/) is a nice tool to estimate the memory consumption of models with different quantization settings.

Use cases:

|Application|Benefit|
|--|--|
|code generation|more code in context|
|question answering|whole docs fit into the context|
|function calling|more tools|
|chat|longer conversations|
|multi-modal|images need many tokens|

To learn more, read Sam McLeod's in-dept blog post about [Bringing K/V Context Quantisation to Ollama](https://smcleod.net/2024/12/bringing-k/v-context-quantisation-to-ollama/). Sam helped implement this in Ollama.