---
title: "A look at the rumored NVIDIA RTX 5090 specs for local LLM inference"
author: mitja
date: 2024-11-26
category: Local AI
tags: [NVIDIA, RTX5090, RTX4090]
#pin: true
#math: true
#mermaid: true
render_with_liquid: false
permalink: /blog/2024/11/26/a-look-at-rtx-5090-specs-for-local-ai/
#image:
#  path: /assets/blog/2024/chatgpt-local-sites.png
#  alt: The ChatGPT Search User Experience.
---
This is a quick look at the [rumored specs of the upcoming RTX 5090](https://www.tomshardware.com/pc-components/gpus/leak-claims-rtx-5090-has-600w-tgp-rtx-5080-hits-400w-up-to-21760-cores-32gb-vram-512-bit-bus) which are most relevant for local inference with LLMs:

|Spec|5090|4090|Delta|
|--|--|--|--|
|Memory Bandwidth|1,52 TB/s|1.01 TB/s|+50%|
|VRAM|32 GB|24 GB|+50%|
|TDP|600 W|450 W|+33%|

The specs mean that the RTX 5090 will probably be about 50% faster and can serve models that are 50% larger than the [RTX 4090](https://www.techpowerup.com/gpu-specs/geforce-rtx-4090.c3889). 

A nice upgrade, let's hope the price will not be 50% higher, as well. If it's about the same price as the 4090, it should be a great card, and probably the best we will get for the next two years or so (the 4090 was released September 2022, the 3090 was released September 2020).

On a practical level, various models in the 30B parameter range should run with great speed at reasonable levels of quantization. With throttling the performance should still be great at the same or lower power consumption as the RTX 4090.

For real-time apps this is great news.

**What about Macs?**

As I don't use local large language models with latency sensitive or high throughput apps, Macs are for me still the best value for local LLM inference. 

For example, I can buy the 48 GB Mac Mini M4 Pro with 0,5 TB SSD for 2.100 EUR and the Mac Book Pro 14 with the same specs for 2300 EUR. This is probably about the same as for the GPU alone, but I get a complete system that consumes not much power, is portable, and quiet. 

Memory bandwidth of the M4 Pro is almost 5.6x slower (273 GB/s), but still bearable for 30B class models. 

My go-to LLMs are hosted models from Anthropic, OpenAI, Google, etc., anyway. I use local models only for longer running experiments, for trying out new models, and when I work with sensitive data. For these use cases, I'm fine with the slower inference.

For other things like training, media production, gaming, a PC with this card is certainly well worth it and I will probably upgrade my GPU at one point anyway. Currently it's a 2070 Super, and my system can be equipped with an RTX 5090.

The first things I would try on the RTX 5090 is probably real-time inference and inference scaling. It would be interesting to see how the inference speed would feel with local voice-to-voice apps, for example.  With inference scaling, the 5090 can probably achieve much better performance with the same latency and model as an M4 Pro.

What I would not to at this point is buy an RTX 4090. The RTX 5090 is much more attractive spec-wise and I would wait until it's released. 

In the end, I don't have an immediate need for the RTX 5090, so I probably will not buy it at release time, but maybe upgrade my system at some time in the future.
