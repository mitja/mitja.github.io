---
title: "Introducing litestar-tags: FastHTML-like tags for Litestar"
date: 2025-10-24
categories: ["AI Engineering", "Blog"]
#tags: ["Claude", "Devcontainer"]
draft: true
---
Litestar is a hidden gem of a Python web framework. It's async first, very well engineered and comes with more features than FastAPI. It's also extremely fast.

What I like most compared to FastAPI is that Litestar has more guardrails and a better approach to dependency injection. B-List has written a nice post about it.

What I miss most is some kind of tag system so that I can write html in Python instead of in templates. With FastAPI there is the new and upcoming Air framework by the authors of two scoops of django not to forget FastHTML itself which can be combined with FastAPI as both are based on Starlette.

To fill the gap, I've created a tags library for Litestar called litestar-tags. 

If you want to get an impression how litestar-tags compare to classic Jinja2 templates, take a look at the litestar-tags-crud-example repository. This is a complete CRUD app styled with Pico.css. It uses htmx for improved interactivity.

Here is an example of a view with Jinja2 compared to a version based on litestar-tags:

