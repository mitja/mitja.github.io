---
date: 2024-02-04
title: Summarizing Large Texts with LLMs and a Tree of Summaries
author: mitja
category: The Basics
tags:
 - Prompt Engineering
 - LLMs
 - Generative AI
 - Python
 - OpenAI
 - GPT
image:
  path: /assets/blog/2024/tree-of-summaries/memory-tree-construction.png
  alt: This is how a tree of summaries looks like in theory.
---

Large language models like GPT-3.5 and GPT-4 can summarize text quite well. But the text must fit into the context window. In this blog post and its acompanying video you will learn how to summarize texts that are too large for the context window with a tree of summaries.

{% include embed/youtube.html id='on8xoaeWcOE' %}

The **general approach** to this is an example of recursive task decomposition which is a fancy way of saying: "Break up a difficult task into easier ones and then, do it again, if the sub-tasks are still too difficult." In this case, it's about breaking up summarizing a long piece of text into summarizing several shorter pieces.

Here is how to do it **step by step**:

The first step is to split the text into multiple segments, for example chapters, and then summarize each segment. Then, you create a summary of the summaries. If you repeat this, you in effect create a tree of summaries. As this tree can be as deep as you like, you can create summaries of huge texts, and even unbounded texts.

If you want to see how to do it in Python, check out the video and see the **[Juypter notebook about Summarizing Large Texts](https://github.com/mitja/mitja.github.io/blob/main/assets/blog/2024/tree-of-summaries/summarize-large-texts.ipynb)**.

<a target="_blank" href="https://colab.research.google.com/github/mitja/mitja.github.io/blob/main/assets/blog/2024/tree-of-summaries/summarize-large-texts.ipynb">
  <img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"/>
</a>

In short: **You can summarize long texts by creating a tree of summaries.**

Here are some **advantages** compared to creating a summary in a single step:

- It works with large texts, in principle even unbounded streams of text.
- It is easy to evaluate the quality of the summaries.
- You can trace the summaries to the original text segments.
- You can use it for knowledge retrieval.

The **quality** of the summaries depend on:

- The model.
- The segmentation (boundaries, segment size).
- The prompts (on summary-of-segment level, on summary-of-summary level).

Here are some **ideas how to improve** the performance of this method:

- Taylor the prompts to the use case, eg. in terms of output, things to look out for, etc.
- Create information-dense summaries with chain-of-density prompting.
- Include sibling summaries when creating summaries to add context.
- Apply few-shot-prompting by giving good examples that demonstrate the desired output.
- Evaluate the quality of the summaries, compare approaches and select the best ones.

I think trees of summaries are an interesting technique that can create good high-level summaries of very large texts. It also enables other use cases, such as summary-based information retrieval.

As so often with Generative AI, trees of summaries look trivial at first but turn out to be deep and powerful, when you look closer.
