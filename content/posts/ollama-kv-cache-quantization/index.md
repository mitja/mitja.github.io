---
title: "K/V Cache Quantization in Ollama"
categories: ["AI Engineering","Blog", "Local AI"]
tags: ["Ollama","Quantization","K/V Cache"]
#externalUrl: ""
#showSummary: true
date: 2025-05-10
draft: false
aliases: 
 - /blog/kv-cache-quantization-in-ollama/
---

A somewhat hidden feature of Ollama is K/V Cache quantization. This is relevant for local AI as it reduces memory consumption, especially for small LLMs with large context windows. 

This post describes how to activate K/V Cache in Ollama and gives an overview of its benefits, drawbacks and use cases.

<!-- more -->

## Activating K/V cache quantization in Ollama

K/V Cache quantization in Ollama is not on by default, so you need to activate it by setting the `OLLAMA_KV_CACHE_TYPE` environment variable. Supported values are documented in [How can I set the quantization type for the K/V cache?](https://github.com/ollama/ollama/blob/main/docs/faq.md#how-can-i-set-the-quantization-type-for-the-kv-cache):

- f16
- q8_0
- q4_0

## Benefits and Drawbacks

K/V Cache quantization can be the difference between being able to run a model on a machine, or not. You can use Sam McLeod's [vram-estimator](https://smcleod.net/vram-estimator/) to estimate the memory consumption of models with different quantization settings.

The benefit in brief is lower memory consumption which is most pronounced when using small models with large context windows.

The main drawback is reduced model accuracy. The lmdeploy team has written a blog post about [K/V cache quantization accuracy test results](https://lmdeploy.readthedocs.io/en/v0.2.3/quantization/kv_int8.html#accuracy-test) if you want to see quantified impacts of K/V quantization on model accuracy.

## Example numbers

Llama 3.2 8B supports 128.000 tokens context windows. 

When you run it with Q4_K_M quantization and the longest possible context length, it    consumes

  - 23.3 GB memory without K/V cache qantization, 
  - 17.0 GB with Q8_K_0 K/V cache quantization, and
  - 13.8 GB with Q4_K_0 K/V cache quantization.
  
With Q4_K_0 K/V cache quantization it now fits into 16 GB vRAM.

## Use cases

|Application|Benefit|
|--|--|
|code generation|more code in context|
|question answering|whole docs fit into the context|
|function calling|more tools|
|chat|longer conversations|
|multi-modal|images need many tokens|

## More Info

To learn more, read Sam McLeod's in-dept blog post about [Bringing K/V Context Quantisation to Ollama](https://smcleod.net/2024/12/bringing-k/v-context-quantisation-to-ollama/). Sam helped to implement this in Ollama.