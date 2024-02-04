---
date: 2024-01-13
title: Getting Started with Creating Software with Generative AI
author: mitja
category: The Basics
tags:
 - OpenAI
 - gpt-3.5
 - Excel
 - Notion
 - Chainlit
 - Python
 - Langchain
 - Faiss
---

assistant: Certainly, Jane Doe. To solve the equation \(3x + 11 = 14\), we can subtract 11 from both sides of the equation to isolate the term with \(x\):

```math
3x + 11 - 11 = 14 - 11 \implies 3x = 3
```

Next, divide both sides by 3 to solve for \(x\):

```math
\frac{3x}{3} = \frac{3}{3} \implies x = 1
```

Therefore, the solution to the equation \(3x + 11 = 14\) is \(x = 1\).
user: I need to solve the equation `3x + 11 = 14`. Can you help me?

## Prerequisites

- you need a computer, a Microsoft account (for excel) and a Google Account (For Colab).
- Instead of Colab, you cna also use your own computer with Python installed.
- You will also need an OpenAI account, but I will show how to register.  you can start for free

## Start with prompting

- register at OpenAI
- use the playground
- run your first prompts
- Improve the prompts
  - with ingredients of a good prompt
  - with advanced prompt engineering techniques
- document it by creating a prompt workbook (a simple word document or google docs, etc.

## Level up with a prompt flow

- best solutions combine
  - generations, potentially from multiple models
  - calculations
  - data
  - human input
- there are tools that enable you to do this with no code (flow diagram)
- you probably already have a tool you use day to day, that you can use to develop automated prompt flows:
  - Excel (or Google Sheet)
- create a prompt flow with Excel
  - in openai, add payment method, create an API key
  - register for excel online or use your excel, add the openai plugin, run a prompt
  - develop a basic prompt flow
    - concat text, convert data
    - get generations you can use
    - add logic

- now you have a working tool you can share with your team, friends, and customers.
- you can also use it to validate ideas, and improve them
- sometimes you want or need more - a real software application

## Create a Custom GPT

GPTs are custom versions of ChatGPT that you can tailor for specific tasks or topics.

You can customize your GPTs with

- instructions,
- conversation starters,
- knowledge (uploaded files),
- selected capabilities from web browsing, DALL-E Image Generation, and code interpreter,
- actions (these can be used to call external APIs)

GPTs are a great addition to the continuum from ad-hoc promting, to creating prompt flows, to developing intelligent applications with Generative AI. I would locate it on the same level as prompt flows. It is a step up from prompt engineering, but not as complex as developing software with Generative AI.

With prompt flows, you can create guided processes.

With GPTs you can create custom chat experiences.

## Develop intelligent applications with Generative AI

### With the OpenAI Assistant API

This the logical next step from custom GPTs. You can use the OpenAI Assistant API to create custom chat experiences or "assistants" within your own applications. The OpenAI Assistant API is the backend and has more features than the basic chat API. You can customize it with

- select which model to use
- knowledge (uploading files)
- tools, which are:
  - code interpreter
  - retrieval
  - function calling

The process is:

1. create an assistant
2. start a thread which is a conversation with a user
3. send messages to the thread as the user asks questions
4. run the assistant on the thread to trigger responses. This also calls relevant tools as defined in the assistant.


The thread stores the state of the conversation, so you can have a conversation over multiple messages.

You can customize 

- Python is the way to go...
- a user interface
- often data
- we create a chat app with data from a notion database (Export)
- chat is great - flexible, lends well to the capabilities, low development effort thanks to great read-made tools

## Where to go from here?

congratulations, you have gone from basic prompting to creating a prompt flow in Excel to developing an intelligent application.

I hope, this inspires and motivates you to learn more about this fascinating technology.

You can find out more on here. Subscribe to my newsletter to get weekly tipps for prompt engineering and prompt flow engineering and developing software with Generative AI.

If you like to dive deeper into creating prompt flows in Excel, try out my book: "Hands-on ChatGPT in Excel".


https://www.gradio.app/guides/creating-a-chatbot-fast