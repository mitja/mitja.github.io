---
date: 2024-02-01
title: Running Production-Grade Generative AI Applications on Kubernetes
author: mitja
category: Cloud Native
tags:
 - Kubernetes
 - Generative AI
 - Python
 - OpenAI
 - GPT
---

## Introduction

In this article, I will explore how to run production-grade generative AI applications on Kubernetes. 

This is only about the app and auxiliary services, not about model hosting. I will use the OpenAI API to generate text and images and for embeddings and XXX as a vector database.

At first, a Gen AI app is just another app. As such it probably has a
frontend, backend, database, cache, it integrates with an identity management, uses other services, needs object storage, logging, monitoring, alerting, a deployment pipeline, blue/green deployments, secure communication, vulnerability scanning, intrusion detection, DDoS protection.

Here is a good setup for production-grade applications on Kubernetes:

Now, we can deploy it, it runs highly available, we can monitor it, scale it, recover it in case of a disaster, and apply good practices for security.

The good thing about this setup is that you can use it to run many apps on the platform and use infrastructure as code to reuse it when you build new plattforms.

## What is special about a Gen AI app?

- non-deterministic part:
  - the large language model, the generative model
  - streaming data, quite high response times
  - payg, costly

- llms can have different roles in the app:
  - orchestrator
  - auxiliary service

- interactive vs. batch
  - near real-time (websites)
  - within seconds to a minute (chatbots for Teams etc.)

- changing code, prompts, data, models (retraining/finetuning)

- new vulnerabilities (prompt injection), new risks (alingment)

- strong benefit: short time to market compared to traditional AI apps, based on supervised learning

- often also just an API...

- privacy, some models might need to be served on private cloud

Challenges for operation:

- more to monitor and keep track of
- tradeoff between latency and resilience
- protect against prompt injection (is it possible?) and mediate
- support fast development cycles from prototype to production

## Cloud-Native Solution Approaches

- Serverless: KNative
- Logging/Monitoring: Add metrics and logs for x
- Security: Add security for x: special hook to check input, output
- Fast development: way to get from Jupyter -> a Gradio app to production...
- Dashboards for developers: Backstage

## Conclusion

- just another app with some common additional special requirements
- Kubernetes and cloud-native tools are a good fit
- result:
  - developers can move fast, have additional assurance, and quality gates
  - get service quickly into production and integrated with other services
  - even in early dev lay, metrcis, logs, monitoring, alerting, security, for tracknig and compliance
  - scalable and secure
  - high availability, disaster recovery

## go from gradio to production

https://rcarrata.com/ai/gradio-k8s/

https://rcarrata.com/ai/seldon-k8s/
https://github.com/SeldonIO/seldon-core

https://istio.io/latest/docs/concepts/traffic-management/


https://distrikt.fi/blog/getting-started-with-training-models-using-argo-workflows


https://github.com/lancedb/lancedb

https://github.com/lancedb/aifunctools

https://lancedb.github.io/lancedb/notebooks/multi_lingual_example/

https://blog.min.io/lancedb-trusted-steed-against-data-complexity/

https://www.infoq.com/news/2023/11/real-time-generative-ai-gameplay/

https://www.ray.io

https://linuxhandbook.com/deploy-generative-microservices/
https://medium.com/@carlgira/generative-ai-api-in-kubernetes-b27f48666440

https://aws.amazon.com/de/blogs/containers/deploy-generative-ai-models-on-amazon-eks/ 

https://www.forbes.com/sites/forbestechcouncil/2023/07/24/from-code-to-creativity-how-generative-ai-is-transforming-kubernetes/?sh=35547209765d


https://github.com/flyteorg/flyte

https://pipekit.io/blog/fine-tune-llm-argo-workflows-hera

https://medium.com/@halilagin/auto-deploying-and-auto-scaling-llm-models-on-kubernetes-ef57f98d4905


https://huggingface.co/blog/dmsuehir/llama2-fine-tuning-k8s

https://www.union.ai/blog-post/fine-tuning-insights-using-llms-as-preprocessors-to-improve-dataset-quality


https://www.kubeflow.org/docs/components/katib/overview/

Prompt Tuning:
https://developer.ibm.com/tutorials/awb-automate-prompt-tuning-for-large-language-models/