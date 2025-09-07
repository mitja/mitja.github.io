---
title: "Evals for Voice Agents (Session Notes)"
summary: "Notes of a whirlwind intro to evals for voice agents by Kwindla and swyx"
categories: ["AI Engineering", "Blog"]
tags: ["Voice AI", "Session Notes", "Evals", "Coval", "WandB"]
#externalUrl: ""
#showSummary: true
date: 2025-06-30
draft: false
aliases: 
 - /blog/evals-for-voice-agents-session-notes/
---

These are my notes of a whirlwind intro to evals for voice agents, a session of [Kwindla's and swyx's Voice AI Course](https://maven.com/pipecat/voice-ai-and-voice-agents-a-technical-deep-dive). It was so packed that I catched many ideas only during note taking. 

I wrote the notes in a rough form on May 16, 2025, but was busy, so I published them only about six weeks later. I still need to catch up with publishing my notes on [Shreya's and Hamel's Evals course](https://maven.com/parlance-labs/evals).

For me the main takeaway of this session is: **Evals are a key aspect of AI Engineering, period.**

If you are interested in AI Engineering and want to learn more about evaluating actual AI apps (not just look at benchmarks or use tool-provided standard metrics) I would highly recommend you attend [Shreya's and Hamel's Evals course](https://maven.com/parlance-labs/evals). There is still time left to join and if you look on their X feeds, can get probably still get a 30% discount code. This will be the last live cohort for some time as Shreya and Hamel want to get back to building. So, take the course, while you can.

[Hamel](https://hamel.dev) kicked it off with a walk through of his blog post [A Field Guide to Rapidly Improving AI Products](https://hamel.dev/blog/posts/field-guide/). His mantra **Look at your data** is now the second meme of this course after **latency**. I will blog about Hamel's recommendations in separate posts with my notes on the Evals course.

[Ian](https://x.com/cairns) from Freeplay recommends to **start with evals from day one** and use them at every stage. He also pitched Freeplay's product highlights and demoed it with a meeting scheduler agent written in PipeCat. I liked Freeplay's 

* traces for all the prompts
* data collection to datasets, 
* prompt versioning, and
* playground with prompt comparison views.

[Sam](https://x.com/sammakesthings) from WandB jumped into a demo about hacking a CEO's bank account from a voice AI agent. He stressed how important evals are, and then walked through **five steps to evaluate voice agents** with Weights and Biases:

1. Setup good tracing in your app.

2. Identify bottlenecks and key points of value: Built-in metrics are not the most useful and a bit of a trap. Instead, you need to learn: where will the system succeed and where will fail? This needs to be specific based on things you've observed and  based on things you know your system needs to succeed.

3. Create datasets and evaluations, by getting the traces. For Sam, it's important to use real traces, at least as a base version. It's important in terms of realism. Only real traces help you understand what users are actually doing, and where real failure cases are. Traces can then be grouped into datasets, eg. by type of failure.

4. Setup the evaluations and user feedback. This is main step: Sam recommends to create an evaluation for a trace, improve the prompt until the evaluation gets better, and include the data in future evaluations. It's also good to get get feedback from end users and build custom, app-specifc eval dashboard. For him, looking at the semantics of users' responses is also helpful. For example, are the users happy, are they cursing out, etc. In voice agents, you could take audio snippets, pass to mulit-modal model and ask: what's the user's tone? How do the feel about the conversation? Multi-modal models are quite good at detecting things that are not present in the text but captured in audio. The collection can be explicit from user feedback or implicit from tone and semantics during the conversation. Sidenote: I assume this could be a challenge with AI regulations in the EU, since sentiment detection and classification is a high-risk application. Probably worth a separate blog post.
      
5. Monitoring: This step is to make sure your production system is just as good as it is in testing. You can take the evals, run them on every conversation, or on a sample of conversations. This way, you can see how the system's performance changes over time, eg. after changing the model, changing prompts, changing user preferences, and changing reference data. With monitoring, you can get notified if sth is going in the wrong direction early, rather than finding it out via unhappy users.

Sam's explanations were hands-on and practical. I also like his [weave-pipecat](https://github.com/SamMakesThings/weave-pipecat) GitHub repo that shows how to integrate WandB's Weave with Pipecat.

[Brooke](https://x.com/bnicholehopkins), the founder of Coval, closed the loop that Hamel started, by looking at the methodology, especially with simulation driven evals. I like her analogy that **"self-driving is just an agent on wheels"** and that she's now building **"self-driving for evals"** with her company. She says with voice AI, trust is especially important, since we all have painful experiences with old-school voice assistants. Even if the technology became so much better, we still have to prove that the systems now are better, too. And the only way to do this is evals. 

AI testing is slow, but this has been solved by self-driving teams ten years ago which faced a similar challenge:

  - get from (conversation) start to finish, with non-determinism
  - every single set has many possible next steps
  - exponential aspect of all possible test cases, because each step impacts the next step of the agent
  
Simulation can simulate many possible scenarios, and is able to estimate the possibiliy of certain types of events across different scenarios and paths to answer the main question; "What is the probability that my voice agent is able to achieve my objective."

Brooke highlighted that evaluating voice is inherently hard because voice AI apps need a model cascade, where each step is difficult in itself, and putting them together even more so. An error upstream can impact the performance of all the downstream steps. For example, if the speech to text performance is bad, it doesn't matter how smart the LLM is, because the input is wrong. At the end of her presentation, she gave a good list of **common challenges of voice AI apps**:

1. Latency vs. interruptions is a tradeoff. Making an app more proactive and responsive with reduced latency will likely lead to more interruptions and vice versa.
2. Workflow following in the sense of keeping the agent on topic is hard.
3. Tool calls are hard to evaluate: Does the agent take the right actions at the right time with the right arguments and does it lead to the agent completing the task successfully?
4. Alphanumeric performance, transcription errors, and translation quality are still difficult.
5. Compliance

This session reinforced my gut feeling that evals are a very important aspect of AI Engineering and provided a glimpse into how to approach it. It also made me even more excited about Shreya's and Hamel's Evals course. 