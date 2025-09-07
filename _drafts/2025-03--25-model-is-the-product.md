If "The Model is the Product" article is true, a lot of AI companies are doomed

Discussion
Curious to hear the community's thoughts on this blog post that was near the top of Hacker News yesterday. Unsurprisingly, it got voted down, because I think it's news that not many YC founders want to hear.

I think the argument holds a lot of merit. Basically, major AI Labs like OpenAI and Anthropic are clearly moving towards training their models for Agentic purposes using RL. OpenAI's DeepResearch is one example, Claude Code is another. The models are learning how to select and leverage tools as part of their training - eating away at the complexities of application layer.

If this continues, the application layer that many AI companies today are inhabiting will end up competing with the major AI Labs themselves. The article quotes the VP of AI @ DataBricks predicting that all closed model labs will shut down their APIs within the next 2 -3 years. Wild thought but not totally implausible.


https://vintagedata.org/blog/posts/model-is-the-product

are ai wrappers doomed?


Fear mongering. The big labs have borrowed a lot of ideas from others. As they keep borrowing ideas, folks are going to stop sharing and go closed. We will find out that the big labs have smart folks, but not as creative as the world at large. Sama told the entire nation of India not to bother building their own LLM equivalent to gpt3.5, that it was out of reach, and less than 2 years later, OLMO built an open model that is > gpt3.5 with all the datasets. AI companies will actively try to discourage the smaller guys, but they can't eat all the market. As they become bigger, they become slower, they are more focused on profit and politics and quarterly results.

As an amateur AI researcher, this is the precise reason I have my own rigs and run my own models. I'm not putting my data into these closedAI companies that are super good at copy ideas...

"don't make a product around fixing model limitations". Building a product like implementing RAG or a coding assistant or something else that is a very broadly applicable topic means you will very soon find Anthropic and OpenAI and others drinking your milkshake

Where your AI is truly valuable is when you learn a very domain-specific need, like implementing a particular process for a particular company. Sam Altman isn't sending OpenAI engineers to sit down with your client's end-users and learning the detailed nuances of their purchasing workflows.

You won't compete with the big AI companies on developing an industry-wide technology that everyone can use. You will compete with the big AI companies by understanding your specific end-users better than they ever could and delivering a customized service to them.

I think model as product is undermining how difficult robust processes are to create.

The hard coded, rule based workflows that the author talks about are admittedly brittle. But the authors fails to mention that the ai agentic models are even more brittle. They hallucinate the wrong actions ALL the time, and it’s not clear if they ever will stop due to the nature of ai hallucinations being so embedded into our current LLM algos.

The “beacon of hope” that hallucinations will stop is increasing intelligence. But the author correctly points out that base models hit a wall for intelligence and reasoning models exponentially cost more for intelligence. And the smartest models STILL hallucinate.

If general intelligence requires being right 90% of the time to be useful, then agentic models need to be 100% right, ALL the time. This is because agentic models direct resource usage, they call other models. So they better be accurate or else they waste money calling the wrong model and the wrong model gets the wrong answer. Double whammy. 

Intelligence comes with the cost of hallucinations. 

That will never not be the case with our current algos. So unless we have a novel breakthrough in our algos, I think agentic models is still very far off.