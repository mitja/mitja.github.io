---
title: "A look at the NVIDIA RTX 5090 specs for local LLM inference"
author: mitja
date: 2024-11-26
category: Local AI
tags: [NVIDIA, RTX5090, RTX4090]
#pin: true
#math: true
#mermaid: true
render_with_liquid: false
permalink: /blog/2024/11/26/a-look-at-rtx-5090-specs-for-local-ai/
image:
  path: /assets/blog/2025/nvidia-rtx-5090.png
  alt: "The NVIDIA RTX 5090 and the NVIDIA RTX 4090 dies side by side.""
---
Update (January 14, 2025): The RTX 5090 was officially announced at CES and will be available January 30, 2025. This post was updated with the aktual [RTX 5090 specs](https://www.nvidia.com/de-de/geforce/graphics-cards/50-series/rtx-5090/). I kept the rumored specs in the post for reference.

This is a quick look at the [specs of the RTX 5090](https://www.tomshardware.com/pc-components/gpus/leak-claims-rtx-5090-has-600w-tgp-rtx-5080-hits-400w-up-to-21760-cores-32gb-vram-512-bit-bus) which are most relevant for local inference with LLMs:

|Spec|Actual RTX 5090 Specs|Rumored RTX 5090 Specs (Nov 24)|RTX 4090 Specs|Delta (Actual RTX 5090 vs. RTX 4090)|
|--|--|--|--|--|
|Memory Bandwidth|1.792 TB/s|1.52 TB/s|1.01 TB/s|+77%|
|VRAM|32 GB|32 GB|24 GB|+50%|
|TDP|575 W|600 W|450 W|+28%|

The specs mean that the RTX 5090 is probably about 77% faster and can serve models that are 50% larger than the [RTX 4090](https://www.techpowerup.com/gpu-specs/geforce-rtx-4090.c3889). 

The RTX 5090 is a nice upgrade, especially as it's only about 10-20% more expensive as the RTX 4090. It's a great card, and probably the best we will get for the next two years or so (the 4090 was released September 2022, the 3090 was released September 2020). Unfortunately, the other cards of the new RTX 50xx line are not as interesting for local LLM inference.

On a practical level, various models up to the 30B parameter range should run with good speed at reasonable levels of quantization. With throttling, the performance should still be better at the same or lower power consumption as the RTX 4090.

**What about Macs?**

As I don't use local large language models with latency sensitive or high throughput apps, Macs are for me still the best value for local LLM inference. 

For example, I can buy the 48 GB Mac Mini M4 Pro with 0,5 TB SSD for 2.100 EUR and the Mac Book Pro 14 with the same specs for 2300 EUR. This is probably about the same as for the GPU alone, but I get a complete system that consumes not much power, is portable, and quiet. 

Memory bandwidth of the M4 Pro is almost 5.6x slower (273 GB/s), but still bearable for 30B class models. 

My go-to LLMs are hosted models from Anthropic, OpenAI, Google, etc., anyway. I use local models only for longer running experiments, for trying out new models, and when I work with sensitive data. For these use cases, I'm fine with the slower inference.

For other things like training, media production, gaming, a PC with this card is certainly well worth it and I will probably upgrade my GPU at one point anyway. Currently it's a 2070 Super, and my system can be equipped with an RTX 5090.

The first things I would try on the RTX 5090 is probably real-time inference and inference scaling. It would be interesting to see how the inference speed would feel with local voice-to-voice apps, for example.  With inference scaling, the 5090 can probably achieve much better performance with the same latency and model as an M4 Pro.

What I would not to at this point is buy an RTX 4090. The RTX 5090 is much more attractive spec-wise and I would wait until it's released. 

In the end, I don't have an immediate need for the RTX 5090, so I probably will not buy it at release time, but maybe upgrade my system at some time in the future.
