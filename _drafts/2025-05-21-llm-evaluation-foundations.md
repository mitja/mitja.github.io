---
layout: post
title: "Fundamentals & Lifecycle of LLM Application Evaluation (Session Notes)"
date: 2025-05-16
author: mitja
category: "Building AI Apps"
tags: [Evals, LLM Pipeline, Session Notes]
image:
  path: /assets/blog/2025/deploying-voice-agents-to-production.jpg
  alt: "A colorful pop-art-meets-industrial style image symbolizing the idea of evals for voice agents. It shows a speech bubble with a diagram and a checkmark top left, a mockup of an app bottom left, and a humanoid bot with a headset at the right side with industrial skylines in the background. AI generated with GPT-4o."
---

These are my notes on **Lesson 1: Fundamentals & Lifecycle of LLM Application Evaluation** of [Shreya Shankar](https://www.sh-reya.com)'s and [Hamel Husain](https://www.hamel.dev/)'s course [AI Evals For Engineers & PMs](https://maven.com/parlance-labs/evals/). 

## About the Course

The course's objective is:

> Master the principles and practices of application-centric LLM evaluation to systematically improve AI-driven products. 

For me, it's about levelling up from "ad-hoc prompting" to a disciplined and structured approach that leads to better results.

For someone like me with no data science background, this course is an eye opener. If you're interested in developing "AI Applications", I highly recommend taking this course.

Sidenote: I put "AI Applications" in quotation marks, as I don't like the term so much anymore. In the end, it's software, that has an AI component, such as an LLM pipeline.

## What is LLM Eval?

- "systematic meausurement of llm pipeline quality"
- enables systematic improvement
- safe, reliable, useful suggestions lead to user trust
- detect degradations with monitoring system quality over time

## LLM Pipeline Development Challenges 

the 3 gulfs analogy:

- why is LLM pipeline development hard?
- developers wear diffent hats to build effective pipelines, the think about.
- each "gulf" represents a mindset/hat the developer has to engage in

|Gulf of|Where?|What's the challenge?|How to deal with it?|
|--|--|--|--|
|specification|between developer and LLM pipepline|Natural language is ambiguous. LLMs need explicit details.|detailed and data-specific prompts|
|generalization|between LLM pipeline and data|LLM behavior varies across different inputs. LLMs might fail on new or unusual inputs.|Understand models' capabilities, task decomposition, fine-tuning, better models, RAG|
|comprehension|between developer and data|Limited human bandwidth, you can't manually review every input and output. Errors and outliers are not obvious at scale.||

## The Evals Lifecycle: Analyze-Measure-Improve

Think about good and not good LLM behavior in context of practical LLM app, to inform prompt design.

|Step|Do|Pitfalls|
|--|--|--|
|Analyze|Collect representative examples and categorize failure modes|outsourcing annotation, not looking at enough examples|
|Measure|Translate qualitative insights into quantitative metrics|unaligned LLM judges, overfitting by testing LLM judges on examples in their prompts|
|Improve|Refine prompts, models, and pipeline architecture|Premature improvement, jumping to most complex solution, first|

## Prompting Fundamentals

- Before evals, figure out, what you are building.
- LLMs are powerful but imperfect components. 
- Leverage strengths, anticipate weaknesses.

LLM strengths:

- fluent, coherent, grammatically correct text
- summarize, translate, transform, answer questions with context
- few-shot learing: can generalize from a few examples

LLM weaknesses:

- unreliable, inconsistent: Same prompt, different outputs.
- Nondeterminism: Small prompt changes can drastically alter output.
- Factuality ("Halluciation"): LLMs predict likely text, not verified truths. Can confidently state incorrect information.

Sidenote: I think, LLM pipeline dev challenges and LLM strengths and weaknesses provide signal for valuable LLM app/pipeline ideas. When challenges and weaknesses are less pronounced, ad-hoc prompting might be a tough competition.

## Components of a Good Prompt

Components of a good prompt:

- Role and objective
- 

## Prompt Engineering

Prompt engineering is an **iterative process**: Your first prompt is a starting point. Test and refine it.

Sidenote: I like to say: "Your first thousand prompts are probably bad. Get them under your belt ASAP.". This seems to apply to specific LLM pipelines, as well, just with a smaller number.


Start with unhappiness: What is a bad result?
Specifications: 
Following specs - how can we check?
Agency: how much freedom does the LLM have?
Eliciting Ground Truth
Direct Grading vs Comparisons

I understand it like having three iteration loops:

1) small loop, starting, trying, refining while developing - fast iteration, included in development.
2) medium loop: eval with data (error analysis?) - slower, involves developer/domain expert, separate from developing itself.
3) big loop: over time, real user system behavior, moves into ml ops domain

## Sneak peek: Understanding failures with error analysis

Also refer to prompting guides by the model providers or general guides:

Project: Recipe bot. Homework 1: write it's initial prompt.

## Course Project and Homework

- over the course, we'll develop a recipe chatbot
- An app skeleton is provided on GitHub at [ai-evals-course/recipe-chatbot](https://github.com/ai-evals-course/recipe-chatbot), my fork is at [mitja/recipe-chatbot](https://github.com/mitja/recipe-chatbot)
- homework 1: create the initial prompt version
