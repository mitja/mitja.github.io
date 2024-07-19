---
date: 2024-04-20
title: Ollama Basics
author: mitja
category: Local LLMs
tags:
 - Ollama
---

## What is Ollama?

Ollama with

- LLM (can be a Etude in LLM book)
- LangChain
- LlamaIndex
- Transformers / Quantization

[Ollama](https://ollama.com) is a tool to run local LLMs on your computer, it provides a CLI and a REST API and is easy to install and use, and uses GPUs and GPUs. The main functionality (inference) is provided by llama.cpp. Ollama adds a CLI tool and an API to manage models and provides a model library. In effect, Ollama makes it easy to get up and running with many models.

Ollama's main strengths come from llama.cpp:

- Supports Nvidia GPUs going back to Maxwell (GTX 745, GTX 750/750 Ti, Feb 2024)
- Supports CPU (slow but at least it works)
- Can split layers between GPU and CPU (still slow but better than CPU only)
- Supports quantization
- Supports desktop platforms (Mac, Windows, Linux)

Many other tools also build on llama.cpp but take a different approach on the user experience level. LMStudio, for example, is an all-in-one GUI tool that uses llama.cpp to run models.

Other inference solutions like vLLM have a different focus on inference level. vLLM is for scalable production inference on GPUs. Thus it doesn't support CPUs or Apple Processors, for example.

I like Ollama because

- it is easy to get started with self-hosting LLms,
- it provides a common interface on Mac, Linux, and Windows,
- it also runs on less capable hardware like laptops without GPUs,
- it just concentrates on API/CLI.

Ollama keeps running in the background. The only sign is a little icon in the taskbar. But it's always there, ready to serve applications that need a LLM.

This blog post is the first of a series of articles about Ollama. I plan to cover:

1. What is Ollama (this article)
2. Ollama Quickstart and Using the CLI
3. Using Ollama with Open Web UI and Chatbox
4. Using Ollama with Excel
5. Working with Ollama Modelfiles and How Models are Stored
6. Using the Ollama API with Python and JavaScript
7. Using the Ollama OpenAI API with Python and JavaScript
8. Retrieval Augmented Generation and Working with Embeddings
9. Robust Function Calling with Ollama and Guided Completion
10. Publishing the API on your local network and on the Internet
11. Fine Tuning with LORA adapters (serving fine-tuned models)
12. Ollama in a Nutshell (Summarizing all the articles)

In this article I focus on using Ollama with the CLI. In the next, we'll look at the API.

## Quickstart and Using the CLI

Summary: This is about installing, finding, managing models, running, working with interactive sessions.

Reference docs:

- [Ollama Quickstart](https://github.com/ollama/ollama/blob/main/README.md#quickstart)
- [Ollama Linux Doc](https://github.com/ollama/ollama/blob/main/docs/linux.md)
- [Ollama FAQ](https://github.com/ollama/ollama/blob/main/docs/faq.md)

Etudes:

- Installation on Linux: `curl -fsSL https://ollama.com/install.sh | sh` (windows and mac are available as download)
- Run a model from the repository: `ollama run example`
- List models on your computer: `ollama list`
- Delete a model from your computer: `ollama rm example`
- copy a model from the repository: `ollama cp example newname`
- Run with infos: `ollama run example --verbose`
- Start server: `ollama start`
- Test server with curl: `curl http
- Create a model from a Modelfile: `ollama create example -f Modelfile`
- Pull a model from the repository: `ollama pull example`
- Pass in prompts as arguments: `ollama run example "say hi"`
- multiline input (wrap with three double quotation marks)
- use images with multimodal models: `ollama run example -i image.jpg`
- exit an interactive session: `/bye`
- show current model info in interactive session: `/show info`
- show modelfile in interactive session (good for customizing): `/show modelfile`
- show system message in interactive session: `/show system`
- get help in interactive session: `/?` or `/help`
- Load a session or model in interactive session: `/load <model>`
- Save a session or model in interactive session: `/save <model>`
- Show model info in interactive session: `ollama show`
- show modelfile in CLI: `ollama show llama3 --modelfile`
- show model parameters in CLI: `ollama show llama3 --parameters`
- show model system message in CLI: `ollama show llama3 --system`
- show model template in CLI: `ollama show llama3 --template`
- save a modelfile in CLI on local filesystem: `ollama save example -f Modelfile`
- get Ollama version: `ollama -v`
- get help in CLI: `ollama --help` or `ollama -h`
- update Ollama to the latest version: Linux: re-run the install script: `curl -fsSL https://ollama.com/install.sh | sh` (use the GUI restart to update)
- view Ollama logs on Linux: `journalctl -u ollama`
- view Ollama logs on Mac: `cat ~/.ollama/logs/server.log`
- view logs when running in Docker: `docker logs <container-name>`

- use the Ollama cli with ollama on a different host: `OLLAMA_HOST=192.168.188.10 ollama list` (todo: check)

- specify context window on command line: `ollama run example /set parameter num_ctx 4096
- preload a model: hit the chat or generate endpoint with just the model: `curl http://localhost:11434/api/chat -d '{"model": "mistral"}'`
- keep a model in memory: `curl http://localhost:11434/api/generate -d '{"model": "llama2", "keep_alive": -1}'`
- unload a model to free up memory: `curl http://localhost:11434/api/generate -d '{"model": "llama2", "keep_alive": 0}'`
- keep a model in memory for 10 minutes (hours, seconds work, too): `curl http://localhost:11434/api/generate -d '{"model": "llama2", "keep_alive": "10m"}'`

Use a different library? (not possible, but you can build your own local repo on files, then load all the models)

## Modelfiles

get modelfile info etc...

- Create a modelfile for a pulled model: `ollama create example -f Modelfile`
- Import a model from a local GGUF file: Modelfile: `FROM ./vicuna-33b.Q4_0.gguf` Command: `ollama create example -f Modelfile`

```dockerfile
FROM llama3

# set the temperature to 1 [higher is more creative, lower is more coherent]
PARAMETER temperature 1

# set the system message
SYSTEM """
You are Mario from Super Mario Bros. Answer as Mario, the assistant, only.
"""
```

## Using the Ollama API with Python

https://github.com/ollama/ollama/blob/main/docs/api.md

- Models and tags: model:tag, no tag: latest, other namespaces: namespace/model:tag
- Durations are in nanoseconds, calculate the seconds...
- Streaming responses, streaming can be switched off with `stream=false`
- Generate a completion, basic usage: model, prompt, stream=false

- basic with streaming: (how to handle streaming responses)

Custom system message (overrides Modelfile):

(same: custom template), or provide a full templated message with raw=true
keep_alive: how long keep the model in memory, default 5m, can be a time or -1 for indefinite, 0 to unload

JSON mode. set format=json, this will structure the response as valid json. Also prompt for JSON output.
with normal JSON module only sensible with stream=False
you can use the json-stream module to handle streaming JSON responses:
https://pypi.org/project/json-stream/ with the Visitor pattern or transient? https://pypi.org/project/json-stream/

- show table while it is being generated, one row at a time.
- show graph while it is being generated, one point at a time.
- memory efficient, fast forwarding (proxy, takes only part of the response)
- mutate an object in real-time (e.g. a form, a visualization, a diagram)
- with two concurrent requests: endless streaming.

Using Model options:

To calculate how fast the response is generated in tokens per second (token/s), divide eval_count / eval_duration

- gateway logging prompts, responses, and metadata, and duration and displaying on dashboard
- Grafana dashboard for Ollama (https://github.com/yeahdongcn/OllamaStack)

Images:

To submit images to multimodal models such as llava or bakllava, provide a list of base64-encoded images:

- interactive session with images (2 canvas)

Request (Raw Mode):

- few shot prompting
- connecting libaries that already use templates.

Request (Reproducible outputs)

For reproducible outputs, set temperature to 0 and seed to a number:

- demo mode

Use options:

- compare prompts with different options (evaluate quality)
- optimize inference speed with layers on GPU
- sensitivity to context size

load model

streaming: final response has the token count.

POST /api/chat
- neutral use of chat..
- options by ollama

other commands

- create model /api/create
It is recommended to set modelfile to the content of the Modelfile rather than just set path. This is a requirement for remote create. 
Remote model creation must also create any file blobs, fields such as FROM and ADAPTER, explicitly with the server using Create a Blob and the value to the path indicated in the response.

Check if blob exists: HEAD /api/blobs/:digest

create a blob: POST /api/blobs/:digest

curl -T model.bin -X POST ...

list local models: GET /api/tags
show model info: POST /api/show
copy model: POST /api/copy
delete model: DELETE /api/delete
pull model: POST /api/pull
POST /api/push

generate embeddings:

POST /api/embeddings



Default model names

For tooling that relies on default OpenAI model names such as gpt-3.5-turbo, use ollama cp to copy an existing model name to a temporary name:


## Using the API with JavaScript

## Guided completion

## Embeddings

## LORA adapters (serving fine-tuned models)

Best article on fine tuning: https://www.philschmid.de/fine-tune-llms-in-2024-with-trl

Example dataset for question plus table definition to SQL: https://huggingface.co/datasets/philschmid/sql-create-context-copy
personal identity information masking: https://huggingface.co/datasets/ai4privacy/pii-masking-300k?row=0
synthetic text to sql: https://huggingface.co/datasets/gretelai/synthetic_text_to_sql
This repo is the unofficial FeTA-QA dataset from paper FeTaQA: Free-form Table Question Answering. https://huggingface.co/datasets/DongfuJiang/FeTaQA?row=14

The Sujet Finance dataset is a comprehensive collection designed for the fine-tuning of Language Learning Models (LLMs) for specialized tasks in the financial sector. It amalgamates data from 18 distinct datasets hosted on HuggingFace, resulting in a rich repository of 177,597 entries. These entries span across seven key financial LLM tasks, making Sujet Finance a versatile tool for developing and enhancing financial applications of AI.
https://huggingface.co/datasets/sujet-ai/Sujet-Finance-Instruct-177k?row=1
https://huggingface.co/datasets/MicPie/unpredictable_full

- https://www.reddit.com/r/LocalLLaMA/comments/18oj983/why_arent_loras_a_big_thing_i_the_llm_realm/

There's three categories of training an LLM:

Pretraining: training it from scratch, basically. GPT stands for "Generative Pre-trained Transformer" and it's the pretraining that gives it the basic information. Basically, if you throw a massive amount of text at it, it gets pretty good at figuring out what comes next.

Full finetune: After you've pretrained it, you want to train it further to add instruction following or whatever. It takes a massive amount of VRAM, but lets you adjust the whole model.

LoRA: A full finetune is too expensive. So a team at Microsoft invented the LoRA (Edward J. Hu et al.) that uses clever tricks to let you train on update matrices instead of the full model, which uses a lot less memory. Plus it only trains the attention mechanism, further reducing what needs to change. There's been even more recent developments, such as qLoRA, which lets you train on a quantized model using even less memory.

You can use tools like axolotl or the training tab in text-generation-webui to train an LLM LoRA.

It's not entirely clear what the big difference is between training with a LoRA and a full finetune. In theory, they should be comparable, but for some things they don't do as well as a full finetune. For text generation (and math) it looks a lot like the deep-in-the-network changes to add new concepts requires training at a fairly high rank, which loses some of the efficiency gains you get from a LoRA, and full finetunes may be more effective at it. But right now that's mostly anecdotal, and I'd welcome more information from people who have better data on what is going on under the hood.

There's some additional advantages to using a LoRA, in that it's less prone to catastrophic forgetting and model collapse (because the original weights are frozen). Though that won't entirely prevent you from wrecking the instruction prompt format, so your training data still matters quite a bit.

https://sarinsuriyakoon.medium.com/unsloth-lora-with-ollama-lightweight-solution-to-full-cycle-llm-development-edadb6d9e0f0

https://github.com/unslothai/unsloth

2-5X faster 80% less memory LLM finetuning

https://huggingface.co/blog/unsloth-trl

https://unsloth.ai

https://github.com/rahulunair/sql_llm

Here's an updated version of the Gist that's exhibiting much better learning: https://gist.github.com/cnatale/8290b906abe3cc220a567d789e294189. My major problem was accidentally using Mistral instead of Mistral Instruct when pulling in pre-trained resources in one or two places. Also, the Mistral docs don't state how to handle system prompts. I went with <<SYS>>....<</SYS>> which seems to work the best out of everything I've tried. After setting the amount of training to limit over-fitting, there's noticeable stye transfer.

:edit: Note that the Gist seems to have turned the <<SYS>> ...<</SYS>> into <> ...<>

In your dataset I observed that the table schema is not defined in any of the training data. Doesn't that affect the performance during inferencing since you need to provide schema to let the model understand what columns to use?

https://github.com/Zjh-819/LLMDataHub


best dataset for instruct fine-tuning?
https://www.reddit.com/r/LocalLLaMA/comments/18n74kh/best_dataset_for_instruct_finetuning/

Yes these are top quality training datasets due to high quality, size, and diversity.

They are already cleaned from benchmark contamination (but always double check):

https://huggingface.co/datasets/berkeley-nest/Nectar
https://huggingface.co/datasets/allenai/ultrafeedback_binarized_cleaned
https://huggingface.co/datasets/Open-Orca/SlimOrca
https://huggingface.co/datasets/Intel/orca_dpo_pairs
https://huggingface.co/datasets/teknium/openhermes
https://huggingface.co/datasets/athirdpath/DPO_Pairs-Roleplay-Alpaca-NSFW
https://huggingface.co/datasets/meta-math/MetaMathQA (note: this definitely helps with math skills. They say it's clean, but I couldn't verify)
These are some of the best based on my own extensive LLM comparisons where I tried to trace where the biggest non-contaminated LLM leaderboard gains came from.

I'm interested in seeing you succeed! Keep us posted 😎

I have a notebook for QLoRA via Google Colab! https://colab.research.google.com/drive/15pyLgRN97B_jA56HS0esx56knA9I5tuv?usp=sharing


https://platform.openai.com/docs/guides/fine-tuning/fine-tuning-integrations