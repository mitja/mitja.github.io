---
title: "Tipps for Migrating to Hugo"
summary: "Lessons learned from migrating my blog from Jekyll to Hugo."
categories: ["Cloud Solution Design", "Blog"]
tags: ["Hugo", "Jekyll", "Static Site Builder"]
#externalUrl: ""
#showSummary: true
date: 2025-09-06
showHero: true
draft: true
---

Here are some tipps for migrating a blog to [Hugo](https://gohugo.io), the static website builder.

## Why Migrate? (Maybe don't)

A migration is always more effort than it may seem. Thus, it's important to be clear about the reasons to migrate and only migrate when necessary. My reasons for migrating my blog to Hugo were:

- Hugo is in my view the best static site generator, today, as it's flexible, focused, fast, and feature-rich. It can certainly serve the site, today and in the forseeable future.
- Due to it's focus and flexiblity, I plan to use Hugo also for other websites.
- Hugo supports multi-lingual sites out of the box. Jekyll does not really support it.
- Hugo can be used as a rendering target of Quarto and nbdev which means that I can write posts in Jupyter Notebook and don't need to manually transfer them to the blog. 

For me, the compelling reason to switch was the multi-language support. I also contemplated how I could continue to use Jekyll, but it would have been more effort later on.

## Chose the Right Theme

The theme is at least as important as the generator itself when chosing the migration target. I chose Blowfish. I like how it looks, it's well-maintained with a long history and has nice features like ... Also, its mainly a blogging theme which I prefer for this purpose. 

## Define Objectives

Your main objective should be to do as little as possible. It automatically gets more involved as you learn more. Writing down your objectives before detailed planning and starting the actual migration will help you keep on track. My objectives were:

- Hugo way
- Keep links working
- Use an existing Hugo theme, resist the urge to create your own theme - it's a lot of work..
- Keep the publishing workflow (in my case GH Actions and GH Pages)

My main goals were to benefit from Hugos additional features (especially multi-language support) while keeping all the links working. I also wanted a blog that's as easy to use, and keep up-to date as Jekyll has been. This meant, I should lean into the Hugo way of structuring content and not continue with the Jekyll way. I also wanted to ontinue to use GitHub Actions and GitHub Pages to publish the blog.

## Define Non-Objectives

Initially, I was looking into porting the Chirpy theme to Hugo. I also started vibe-coding it, and it even was looking ok-ish, but there were a myriad of things that would have needed to be improved and features like multi-lingual support were missing altogether. Not to speak of the code quality. Developing and maintaining a great theme is not a small task and needs dedication. I'm glad that really great open source themes exist for Hugo and abondoned the idea of porting the theme.

Another idea, I dropped after some consideration was to move to a different host. I will continue to use Github Actions and Pages to build and publish the blog.

## Draft and Follow a Plan

Easy to get carried away and do more than necessary. Draft a plan that takes the fewest and simplest steps possible to get from A to B. Try to convert a few pages by hand and see what's necessary.

In my case:

- create a blog with the Blowfish theme and a template (that includes GH Actions, already)
- customize the theme (title, ...)
- create a branch of the existing site git repo
- see where content is stored (pages, assets, drafts)
- look at the workflow and note things you need to transfer
- delete everything except content and CNAME
- move the new theme in
- transform the content, in my case:
  - move from file to folder with index.md
  - move linked assets to the folder
  - rename the frontmatter image to cover, drop the image ref in front matter
  - add a summary
  - rename category to categories, add category "Blog"
  - make sure every source has a permalink entry (most of my posts had), use that to create aliases (this creates redirect pages which keeps the links working)
  - replace link paths in the content
- check if all source links are present in target site (i used sitemap paths for source, and requested headers for the target)
- check the change, publish

## Use Scripts

Consider creating or adapting existing script for the migration. I believe a script is already worth it from twenty or more pages. Even with my blog... it was good to use scripts. Vibe coding makes it easy to adapt scripts from eg. https://gohugo.io/tools/migrations/ to your need. I created two scripts.

migrate

check

## The Plan

- in a day, simple and easy
- don't lose backlinks (use Hugo aliases to create redirects)
- no maintainance: use a standard well-maintained Hugo theme instead of reimplementing the Jekyll theme in hugo
- use the hugo way of organizing content
- drop cover images (cover images are fun and probably important for good CTRs but i want to focus on writng)

## Migration steps

My blog source is on GitHub, published as GitHub pages. I wanted to keep publishing on gh.

- create a the hugo site
- create a branch of the blog
- move the content and assets to a save place (?)
- delete everything except the content (`_posts` and `_drafts` and `assets` without `assets/lib`) - rename assets?
- in a tmp folder, create a new blow with the starter script, customize the theme/site
- move everything into the branch working directory
- run a script that
  - creates a folder for each old _post in content/posts
  - move the old _post to content/posts/<postname>/index.md
  - reads / adapts front-matter:
    - add an empty "summary"
    - rename category to categories, add "Blog"
    - read image filename, move it to cover.<ext>
    - add alias for the old permalink
  - finds linked assets in the content and moves it into the site bundle [/assets/...]
- add aliases to the index pages
  - ...
- change favicons

- Use github Actions to build (my theme has a workflow i can adapt)
- 

My

- use a standard Hugo theme (blowfish)
- use the standard content structure of hugo
- 

## Publish, check, then change

Publish the site, check it, eg by crawling for missing links. and looking through the content.

Site manager, and analytics to see if somethings missing.

Only then change futher (I removed images)

## Don't Underestimate the Effort

In my case, the migration took about a day (8h), not counting my attempt at vibe coding a Chirpy port and resarching static site generators and themes. Even though the effort was higher than I initially thought, I would consider it a success and quite effective. The site works, links work. 

My assumptions of why it takes longer is that it's basically a first-time, for me - migration is something not done every day. Also every situation is a bit different. Thu, it's certainly worth considering hiring an expert with experience in migrating sites to Hugo, especially if you have a medium sized blog or larger and you don't want to adapt a conversion script so that it fits your situation.