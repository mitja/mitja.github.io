---
title: "Introducing litestar-tags: FastHTML-like tags for Litestar"
date: 2025-10-24
categories: ["AI Engineering", "Blog"]
#tags: ["Claude", "Devcontainer"]
draft: true
---
Litestar is a hidden gem of a Python web framework. It's async first, very well engineered and comes with more batteries included than FastAPI. It's also extremely fast.

What I like most compared to FastAPI is that Litestar has more guardrails and a better approach to dependency injection. B-List has written a nice post about it.

What I miss most is some kind of tag system so that I can write html in Python instead of in templates. With FastAPI there is the new and amazing Air framework by the authors of two scoops of django not to forget FastHTML itself which can be combined with FastAPI as both are based on Starlette.

To fill the gap, I've created a tags library for Litestar called litestar-tags. 

If you want to get an impression how litestar-tags compare to classic Jinja2 templates, take a look at the litestar-tags-crud-example repository. This is a complete CRUD app styled with Pico.css. It uses htmx for improved interactivity.

Here is an example of a view with Jinja2 compared to a version based on litestar-tags:

I have created the project in October 2025. At the time, LLMs were not as good as today at coding, and especially keeping the overview of long context windows. My assumption was to use approaches that are very concise to safe tokens. The tag libraries were really good at this.

Today, it's less of an issue with hosted inference, subsidized tokens in subscriptions. But for local inference with not as strong models, it's still relevant.

Here is a comparison: I created an app with pi, ds4 and deepseek 4.1 flash xxx with React and the tag library. A major drawback of my own library compared to React is, that it's not "in the weights" - the models doesn't know how to use it. So i needed to give good enough instructions. I used dspy to get a good llms.txt file that led to good enough results at a mini eval set. Then i did the impelmentation runs.

Results:
- time total
- tokens
- errors i needed to fix
- how it looks