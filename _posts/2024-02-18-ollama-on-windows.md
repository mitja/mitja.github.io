---
date: 2024-02-18
title: Ollama on Windows: How to Install and Use it with OpenWebUI
author: mitja
category: The Basics
tags:
 - Ollama
 - LLMs
 - Windows
 - OpenAI API
image:
  path: /assets/blog/2024/ollama-on-windows/ollama-windows.jpg
  alt: Ollama on Windows with OpenWebUI on top.
---
Ollama is one of the easiest ways to run large language models locally.

Thanks to llama.cpp, it can run models on CPUs or GPUs, even older ones like my RTX 2070 Super. It provides a CLI and an OpenAI compatible API which you can use with clients such as OpenWebUI, and Python.

In this blog post and it's acompanying video, you'll learn how to install Ollama, load models via the command line and use OpenWebUI with it.

{% include embed/youtube.html id='z8xi44O3hvY' %}

## About Ollama

[Ollama](https://ollama.com) is a desktop app that runs large language models locally. It is built on top of [llama.cpp](https://github.com/ggerganov/llama.cpp), a C++ library that provides a simple API to run models on CPUs or GPUs.

Ollama is designed to be good at "one thing, and one thing only", which is to run large language models, locally. This means, it does not provide a fancy chat UI. Instead, it gives you a command line interface tool to download, run, manage, and use models, and a local web server that provides an OpenAI compatible API.

Thanks to llama.cpp, Ollama can run quite large models, even if they don't fit into the vRAM of your GPU, or if you don't have a GPU, at all. This is possible, because, llama.cpp runs quantized models, which take less space, and llama.cpp can run some layers on the GPU and others on the CPU. This way you get faster inference than with a CPU, only.

Up until now, Ollama binaries were only available for MacOS and Linux. It was possible to run it on Windows with WSL or by compiling it on your own, but it was tedious and not in line with the main objective of the project, to make self-hosting large language models as easy as possible. On February, 15th, 2024, this changes, as the Ollama project made a Windows Preview available.

## Installing Ollama on Windows

With the new binary, installing Ollama on Windows is now as easy as it has already been on MacOS and Linux. You just download the binary, and run the installer. The only prerequisite is that you have current NVIDIA GPU Drivers installed, if you want to use a GPU.

**After the installation**, the only sign that Ollama has been successfully installed, is the Ollama logo in the toolbar. Here, you can stop the Ollama server which is serving the OpenAI API compatible API, and open a folder with the logs. 

You can **test the server** with the following PowerShell command, but you will realize, that it returns an error. This is because, there is no model called "llama" available, yet.

```PowerShell
(Invoke-WebRequest -method POST -Body '{"model":"llama2", "prompt":"Why is the sky blue?", "stream": false}' -uri http://localhost:11434/api/generate ).Content | ConvertFrom-json
```

At least, we can see, that the server is running. Let's get a model, next.

## Using the Ollama CLI to Load Models and Test Them

Ollama comes with the `ollama` command line tool. Enter `ollama` in a PowerShell terminal (or DOS terminal), to see what you can do with it:

```Powershell
ollama
Usage:
  ollama [flags]
  ollama [command]

Available Commands:
  serve       Start ollama
  create      Create a model from a Modelfile
  show        Show information for a model
  run         Run a model
  pull        Pull a model from a registry
  push        Push a model to a registry
  list        List models
  cp          Copy a model
  rm          Remove a model
  help        Help about any command

Flags:
  -h, --help      help for ollama
  -v, --version   Show version information
  ```

The interesting commmands for this introduction are `ollama run` and `ollama list`.

With `ollama run` you run inference with a model specified by a name and an optional tag. When you don't specify the tag, the **latest default** model will be used. For example, the following command loads `llama2`:

```PowerShell
ollama run llama2
```

If Ollama can't find the model locally, it downloads it for you. When it's ready, it shows a command line interface where you can enter prompts. At this point, you can try a prompt to see if it works and close the session by entering `/bye`.

If you add `--verbose` to the call to `ollama run`, you will see the number of tokens per second:

```PowerShell
ollama run llama2 --verbose
```

As the model has already been downloaded, the startup time is now much faster.

You can also serve more than one model. Just download another model with `ollama run`. For example, the following command downloads the [LLaVA](https://llava-vl.github.io). LLaVA stands for "Large Language and Vision Assistant". It is "multimodal", and can work with both text and images in the prompt.

```PowerShell
ollama run llava --verbose
```

With `ollama list`, you can see which models are available in your local Ollama instance.

When you want to learn more about which models and tags are available, go to the **[Ollama Models library](https://ollama.com/library)**. Here you can search for models you can directly download. When you click on a model, you can see a description and get a list of it's tags. The tags list displays the tag label, a hash, the download size, the last update, and it conveniently provides the command to run it.

With the **tag label**, you can usually decipher

- the model size (eg. 7b, 13b),
- the version,
- the level, and method of quantization.

There is always a "latest" tag, too. This is the model you use, if you don't specify a tag. By comparing the **hash values**, you can find out, which tag is actually used. For example, at the time of writing, the following tags all have the same hash value of `78e26419b446` and are thus the same:

- latest
- 7b
- 7b-chat
- 7b-chat-q4_0

This means, that `ollama run llama2` runs the 7b variant of the chat instruction tuned model with q4_0 quantization.

I don't want to go too much into detail about **quantizations**, here, but just state, that a quantization to 4 bit (the `q4`) is a sensible compromise and that it's usually recommended to run larger models with up to q4 quantization than smaller ones without or lower quantization. When it comes to **quantization methods**, I refer you to the excellent [TheBloke](https://huggingface.co/TheBloke). He provides many quantizations for many models and also desribes the recommended use cases. This is what he says about `Q4_0`:

> [Q4_0] - legacy; small, very high quality loss - prefer using Q3_K_M
>
> -- TheBloke

Anyway, let's stick with the default method, here, and try to run a model that is too large for my GPU, even in this level of quantization:

```PowerShell
ollama run llama2:13b-chat
```

It works. This is possible, because Ollama lets llama.cpp run only some of the layers on the GPU. You can configure how many, exactly, but I leave this for another post.

At this point, you have Ollama running on your mashine with three interesting large language models, and you can prompt them with the command line tool and use the models via an OpenAI API compatible REST API. Next, you will get a very nice chat web ui, but first, test if the server now runs and actually serves a model:

```PowerShell
(Invoke-WebRequest -method POST -Body '{"model":"llama2", "prompt":"Why is the sky blue?", "stream": false}' -uri http://localhost:11434/api/generate ).Content | ConvertFrom-json
```

## Installing and Using OpenWebUI with Ollama

[OpenWebUI](https://github.com/open-webui/open-webui) (Formerly Ollama WebUI) is a ChatGPT-Style Web Interface for Ollama. It's inspired by the OpenAI ChatGPT web UI, very user friendly, and feature-rich. Most importantly, it works great with Ollama.

The easiest way to install OpenWebUI is with Docker. To use this method, you need a Docker engine, like Docker Desktop or Rancher Desktop running on your local machine. I use it with Docker Desktop. With this in place, **installing OpenWebUI** is as simple as entering the following command:

```PowerShell
docker run -d -p 3000:8080 --add-host=host.docker.internal:host-gateway -v open-webui:/app/backend/data --name open-webui --restart always ghcr.io/open-webui/open-webui:main
```

If you get a security warning, you need to confirm it so that Docker is allowed to run a server.

Now you can browse to [http://localhost:3000/], register a local account and start chatting. Select a model from the list, and enter a prompt. You can also try the llava model by uploading an image, if you like.

Happy prompting.
