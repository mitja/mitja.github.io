Ollama can pull models from the official libary at https://ollama.ai/ and now also from Huggingface. What's also possible, but not yet documented is to host your own models on a private Docker Registry. 

In this article, I'll describe how to self-host models for Ollama on a private Docker Registry. My use case for this feature is to serve models on a company's internal network to enable colleagues to easily pull images. Our standard laptops have restricted internet access. We can access the internet only with a few whitelisted apps, and Ollama is currently not yet part of the whitelist.

I also opened a ticket in the Ollama GitHub project with a pull request to update the documentation, but I wanted to share it here as well, as this is basically an unsupported feature, so I don't know when or if it will be merged.

I found the comments by [Blake Mizerany](https://github.com/bmizerany) in ticket [#2388](https://github.com/ollama/ollama/issues/2388) helpful:

```markdown
Ollama keeps a cache of your already download models under ~/.ollama or $OLLAMA_MODELS if set.

Ollama is currently compatible with Docker Registry, but we do not guarantee it will remain compatible.

It should be possible to host your own registry with authentication turned off (we implemented custom auth for our hosted version) for use as a private registry.

...

Currently, we do not have an official registry API, which is why we don't have any documentation available for Docker registry compatibility.

We are considering and working towards a solution for remote caching. There are no dates for its release currently.

For now, we unofficially use the GET layer, POST/PUT(upload) layer and read/commit manifests.
```

Well this already tells the whole story :) But let's do it step by step, anyway:

First, you need to have a Docker Registry running. I use the official Docker Registry image. You can start it with the following command:

```bash
docker run -d -p 5000:5000 --restart=always --name registry registry:2
```

This will start a Docker Registry on port 5000. You can now push images to it.

Next you can push a model to the registry. Ollama doen't have the tag command, but we can use cp to copy a model locally and then push it to the registry. Use `ollama list` to see a list of locally available models. Select one, in my example, I use `llama3.2:latest`. Now you can copy it and push it to the registry:

```bash
ollama cp llama3.2 http://localhost:5000/mitja/llama3.2:latest
ollama push http://localhost:5000/mitja/llama3.2:latest --insecure
```

Note that I use the `--insecure` flag to disable TLS. I use `mitja` for the namespace, but you can use any name you like. Just make sure to use the same namespace when pulling the model, later.

Now you can remove the model locally, check that it's removed, and pull the model from the registry, again or directly run it as in this example:

```bash
ollama rm llama3.2
ollama list
ollama run http://localhost:5000/mitja/llama3.2:latest --insecure --verbose
```

Note that the pulling should be almost instant if you kept the original model. This is because the layers are still stored locally for the original model. If you remove the original model, the layers will actually be pulled from the registry.