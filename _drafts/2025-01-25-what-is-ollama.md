
comment by https://github.com/sammcj in https://github.com/ollama/ollama/pull/6279



In the interest of helping you understand the difference between Ollama and llama.cop I'll share you something I've shared before when I've heard people not quite get this right:

With llama.cpp running on a machine, how do you connect your LLM clients to it and request a model gets loaded with a given set of parameters and templates?

..You can’t, because llama.cpp is the inference engine - and it’s bundled llama-cpp-server binary only provides relatively basic server functionality - it’s really more of demo/example or MVP.

Llama.cpp is all configured at the time you run the binary and manually provide it command line args for the one specific model and configuration you start it with.

Ollama provides a server and client for interfacing and packaging models, such as:

Hot loading models (e.g. when you request a model from your client Ollama will load it on demand).
Automatic model parallelisation.
Automatic model concurrency.
Automatic memory calculations for layer and GPU/CPU placement.
Layered model configuration (basically docker images for models).
Templating and distribution of model parameters, templates in a container image.
Near feature complete OpenAI compatible API as well as it’s native native API that supports more advanced features such as model hot loading, context management, etc…
Native libraries for common languages.
Official container images for hosting.
Provides a client/server model for running remote or local inference servers with either Ollama or openai compatible clients.
Support for both an official and self hosted model and template repositories.
Support for multi-modal / Vision LLMs - something that llama.cpp is not focusing on providing currently.
Support for serving safetensors models, as well as running and creating models directly from their Huggingface model ID.
In addition to the llama.cpp engine, Ollama are working on adding additional model backend