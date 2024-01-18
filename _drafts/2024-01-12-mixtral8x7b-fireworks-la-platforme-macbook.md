---
title: Mixtral 8x7B on Fireworks, Mistral's La Platforme, and a Macbook with 32 GB RAM
author: Mitja Martini
date: 2024-01-12 16:30:00 +0200
category: Playground
tags: [Mistral, Python, Fireworks]
render_with_liquid: false
---

Remaining notes:

- there is an instruct model, now, i should test it
- great discussion here: https://huggingface.co/TheBloke/Mixtral-8x7B-Instruct-v0.1-GGUF/discussions/1
- I was not expected opensource llm reach such level so fast because 9 moths ago openAI claimed opensource models with the power of GPT 3.5 will be available in 5 years ... (that MoE model is something totally a new level ) ... that is insane and if we are thinking that soon will be finetuned versions ... crazy.
Plus that works fast on my rtx 3090 ... 40 token /s and has 32k context
I wonder if a new llama 3 will be also MoE model ;D

This is a quick note on how to test Mixtral 8x7B online and how to run a quantized version of Mixtral with llama.cpp on a MacBook with 32 GB RAM.

## Introduction

Mixtral 8x7B is a new "sparse mixture of experts" model by Mistral which [outperforms Llama2 70B on most benchmarks with 6x faster inference](https://mistral.ai/news/mixtral-of-experts/) according to Mistral.

Mixtral uses only two of its 7B parameter sets or about 12B parameters at a time. This makes it very fast compared to models with a similar total number of tokens. Unfortunately, you still need to hold all the weights in memory. The unquantized model requires about 100GB RAM to run.

## How to Test Mixtral 8x7B Without Installing Anything?

An easy way to try out Mixtral 8x7B without installing anything is the [Vercel AI SDK Playgrond](https://sdk.vercel.ai):

Under the hood, Vercel uses [Fireworks.ai](https://app.fireworks.ai). This is how I learned that you can use Mixtral with the Fireworks API, as well.

## Use Mixtral with the Fireworks API

accounts/fireworks/models/mixtral-8x7b-instruct

You can get a free or a paid account at Fireworks and use Mixtral 8x7B from Python or any other programming language via the Fireworks API.

Fireworks has a pay-per-use service based on 1M tokens and Mixtral is even priced like a smaller model, probably thanks to its high inference throughput (see [Fireworks Pricing](https://readme.fireworks.ai/page/pricing)).

The [Fireworks Documentation](https://readme.fireworks.ai/docs/querying-text-models) says, that Fireworks supports the OpenAI SDK with the ChatCompletions endpoint but also has its own Python and JavaScript SDKs. This makes Fireworks is a great service to use the unquantized Mixtral 8x7B, today in own projects. Here is how to run an example with the Fireworks Python SDK:

Step 1: **Register an account at Fireworks**. You get 1M tokens free.

Step 2: **Create an API Key**.

Step 3: **Store the API Key** in a `.env` file or in an environment variable, eg. `FIREWORKS_API_KEY`.

Step 4: **Install the fireworks Python Package**:

```bash
pip install fireworks
```

Step 5: **Call the API from Python**

You can try the prompts at the [Fireworks Model Page for Mixtral MoE 8x7B Instruct](https://app.fireworks.ai/models/fireworks/mixtral-8x7b-instruct). This also generates basic Python, CURL, or JavaScript code for you.

```python
from dotenv import load_dotenv
from pprint import pprint as pp
import os
import fireworks.client

load_dotenv()

fireworks_api_key = os.getenv('FIREWORKS_API_KEY', 'YourAPIKey')

fireworks.client.api_key = fireworks_api_key

completion = fireworks.client.ChatCompletion.create(
  model="accounts/fireworks/models/mixtral-8x7b-instruct",
  messages=[
    {
      "role": "user",
      "content": "Which is the best figure in rock-paper-scissors (wins most of the times)?",
    }
  ],
  stream=True,
  n=1,
  max_tokens=100,
  temperature=0.1,
  top_p=0.9, 
)
print(response.choices[0].message.content)
```

## Use Mixtral 8x7B with Mistral's Le plateforme

Mistral's own service [La plateforme](https://mistral.ai/news/la-plateforme/) is probably the best way to use this model, as you also get access to an even stronger model of this family and with it, you support the development of Mistral, as well. You can apply to become a beta user. The platform provides APIs for the Mistral 7B, 8x7B a larger models, in the future.

## How to Run Mixtral 8x7B on a MacBook with 32 GB RAM?

There is also a way to run Mixtral 8x7B locally even with systems that have not 100GB vRAM.

At the moment, you can do this by using a patched version of llama.cpp in combination with quantized models published by TheBloke.

Chances are, that you can just use the binary distribution of llama.cpp when you read this, but at the time of writing the patch has not yet been merged.

Here is how run Mixtral with a patched version of llama.cpp:

Step 1: If you don't have it yet, **install Homebrew**:

```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

Step 2: **Install required packages**:

```bash
brew install cmake python@3.10 git wget
```

Step 3: **Clone the llama.cpp repository**:

```bash
git clone https://github.com/ggerganov/llama.cpp
cd llama.cpp
```

Step 4: **Fetch the Mixtral pull request and switch to it**. This step is only required until this pull request is merged:

```bash
git fetch origin pull/4406/head:mixtral
git switch mixtral
```

Step 5: **Compile llama.cpp**:

```bash
make
```

Step 6: **download the weights**.

You can find quantized model files at https://huggingface.co/TheBloke/Mixtral-8x7B-v0.1-GGUF/tree/main Here is how to download the varant that is quantized to 4 bit:

```bash
wget https://huggingface.co/TheBloke/Mixtral-8x7B-v0.1-GGUF/resolve/main/mixtral-8x7b-v0.1.Q4_K.gguf
```

Step 7: **Run the server**.

I needed to run the 4 bit variant on the CPU whith the `--n-gpu-layer 0` option. The 3 bit variant was small enough to run on the GPU so I dropped this option on this variant.

```bash
./main --n-gpu-layers 0 -m mixtral-8x7b-v0.1.Q4_K.gguf -p "Your prompt"
```

## My Impression of Mixtral 8x7B

I first tried Mixtral 8x7B with the Vercel Playground and was impressed. It really is a very strong model and probably the best model in terms of cost/performance trade-offs, at the moment - but only if you have the RAM to run it. This is not a problem with the hosted services.

With the level of quantization necessary to run it on a MacBook with 32 GB RAM you definitely need to do your own testing. I first tried `mixtral-8x7b-v0.1.Q3_K.gguf` but really did not like its performance. Next, I tried `mixtral-8x7b-v0.1.Q4_K.gguf` and found it to be much better, but still not as good as say an unquantized Mistral 7B or a 6 bit quantized OpenHermes Neural Chat 7B. Then I tested the instruction tuned variants and was again It certainly was much worse than the unquantized Mixtral 8x7B, too. I have not done extensive testing, but my first impression is "very positive" with the unquantized Mixtral 8x7B and "not good enough to switch models" with the quanizations necessary to run it on my 32 GB RAM MacBook.

The usability of the unquantized model even without instruction tuning is impressive. Wie instruction  will become better with fine tuning. In addition, I have not created well-crafted prompts during my tests which I assume are more important with a foundation model such as Mixtral 8x7B than with the instruction tuned models I compared it with. As the results of the unquantized Mixtral were great despite the simple test prompts, I believe the main reason for the quality loss is still the high level of quantization necessary to run it on my machine.

In conclusing: **Mixtral is a powerful and cost-effective model for data center inference not but well suited for local inference on somewhat normal laptops and desktops.**

## Example Completions

Here are completions for the following prompt:

**What is the best figure in rock-paper-scissors (the most likely to win)?**

The correct answer would state that there is no best figure as every figure
wins one third of the times.

By the way: In Germany, there is a variant of this game where you can also play a well. The well is the best figure, as both the stone, and the scissors fall into the well. Only the paper wins against the well as it can cover it. With this additional figure often, one player prefers the well right from the start, then, another player starts to prefer the paper as a reaction, then the other again reacts with scissors.

### Mixtral 8x7B Instruct via the Fireworks API

A very good answer, arguably the best overall, I changed to "what is the best choice" instead of "figure". It was fast, too: 891 ms time to first token, then 15.71 ms per token (63 tokens/second):

```none
In the game of rock-paper-scissors, there isn't a single choice that wins most of the times as it's largely based on chance and the strategy of the opponent. However, some studies suggest that people tend to throw rock as their first choice slightly more than the other options. So, if you want to use a very slight statistical advantage, you could choose paper. But remember, the key to winning in rock-paper-scissors is to observe your opponent.
```

### Mixtral 8x7B Instruct v01 Q4_K_M

This is very strong. It runs on my MacBook, but unfortunately very slow at below 1 tokens per second.

```none
Let me begin by saying that I have no idea what you 
mean by "figure" here. It seems like you could be asking 
about which of the three choices wins more often than it 
loses, or maybe you're referring to something else entirely.

Assuming that your question is about which choice has the 
highest probability of winning, the answer is: it depends. 
In a one-on-one game between two equally skilled players 
who randomly choose their moves, there isn't any figure 
that is inherently better than the others. That's because 
each move beats another (rock beats scissors, paper beats 
rock, and scissors beat paper) but loses to another as well, 
so they all have an equal chance of winning or losing in 
this scenario.
```

### Mixtral 8x7B Q3 K

This variant started well some times, but then got distracted:

```none
The question seems simple. There are three figures, 
so you would think each one has a 33% chance of winning. 
However, this isn’t quite true. The chances aren’t equal!

To explain why there is no way I can get around using 
some maths notation to describe the different “states” 
we will be considering and their probabilities in 
rock-paper-scissors (RPS).
... (goes into a blog article style, then repeats itself)
```

Here is another example. I should have turned down the temperature a bit. The line breaks are mine:

```none
The paper wins against all figures except for scissor 
which can cut through it like a knife cuts cheese on 
top of pizza! 

Pizza has three ingredients that make up 
its delicious taste, and each ingredient 
represents one side out there among us humans 

who are alive today but not tomorrow 
when we die because life is short 

so enjoy every moment while you still have time left  
before your last breath comes upon this world 

like a thunderstorm over the ocean waves 
crashing against shoreline sandcastles 

made by little children playing on beachfronts 
during summertime vacation season!
```

### Mixtral 8x7B Q4 K

Sometimes it was almost ok, but other times, it even did not answer the question, at all:

```none
If you’ve ever played Rock, Paper, Scissors with someone 
who was a bit better than you at it, then there are probably 
two questions going through your mind: 

“Why am I playing this game? 
What is the point of even having this thing?
...
```

### OpenHermes 2.5 Neural Chat 7B v3 Q6 K

An ok-ish answer. The zero-sum part is correct but not really
necessary to answer my question, also the strategy is nice, but
not the answer. The third sentence however is spot on.

```none
The game of Rock-Paper-Scissors (RPS) is a zero-sum game, 
meaning that one player's gain results in an equal loss 
for the other. The only way for players to make a decision 
is by randomizing their strategy. There is no best figure 
that will always win as each figure beats another and 
loses against the third one according to the following rules:
...(lists the rules)
```

### Mistral 7B Instruct (not quantized)

A very good answer:

```none
In rock-paper-scissors, there is no best figure that is 
the most likely to win because it is a game of chance 
and skill. Each move has an equal chance of winning,
depending on the opponent's move. The game is designed
so that no single move can always beat another, ensuring 
fairness and unpredictability. However, if one player
consistently chooses a particular move and their
opponent consistently chooses a counter-move, they may
develop an advantage over time.
```

### Mixtral 8x7B (not quantized)

A very good answer:

```none
In rock-paper-scissors, there is no best figure or 
strategy that guarantees a win. The game is designed 
to be fair and unbiased, with each player having an 
equal chance of winning with any of the three figures
(rock, paper, or scissors). The outcome of the game 
depends entirely on luck and the choices made by both
players.
```

### gpt-3.5-turbo

Nice and to the point right from the start:

```none
In rock-paper-scissors, each figure has an equal chance of winning. 
However, statistically speaking, there is no universally best 
figure as it ultimately depends on the strategy of the players 
involved and their ability to anticipate or read each other's 
moves.
```

### gpt-4-1106-preview

Long but correct and with a very good explanation and a discussion of strategies:

```none
Rock-paper-scissors is a hand game usually played 
between two people, where each player simultaneously 
forms one of three shapes with an outstretched hand. 
These shapes are "rock" (a fist), "paper" (an open hand), 
and "scissors" (a fist with the index and middle 
fingers extended, forming a V).

The game has three possible outcomes other than a tie:
rock crushes scissors, scissors cut paper, and paper 
covers rock. The strength of the game lies in its 
simplicity and the fact that it is based on a circular 
relationship, which creates a situation where no single 
choice is statistically more likely to win.

Assuming that both players are equally random in their choices:

- Each shape wins against one of the other shapes,
- Each shape loses to one of the other shapes,
- All choices have a 1/3 chance of winning against another random choice.

In non-competitive versions or when played casually without 
any psychological strategy or pattern prediction, no figure 
is statistically superior to others. They all have equal 
chances to win.

However, in competitive play or when patterns can be 
predicted (based on analyzing an opponent's behavior), 
certain strategies can increase the likelihood of winning. 

For example:

1. Some players might unconsciously favor one figure over
...
```
