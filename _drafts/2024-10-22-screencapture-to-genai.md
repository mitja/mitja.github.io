---
title: Using SnagIt Screen Captures in Google AI Studio
author: mitja
date: 2024-10-22
category: Using AI
tags: [vertexai, gemini, snagit]
#pin: true
#math: true
#mermaid: true
render_with_liquid: false
permalink: /blog/2024/10/22/using-snagit-screen-captures-in-google-ai-studio/
image:
  path: /assets/blog/2024/snagit-google-ai-studio.png
  alt: The Dokku logo which is a friendly whale with a captain's hat (I think).
---

I got inspired by Simon Wilisons article [Video scraping: extracting JSON data from a 35 second screen capture for less than 1/10th of a cent](https://simonwillison.net/2024/Oct/17/video-scraping/). In it, he describes how he used Gemini Flash to extract JSON data from manually selected emails via a 35-second screen capture.

It's actually quite a versatile usage pattern for Generative AI: Shoot a screencast, then analyze it with AI. Some use cases are summarization, information extraction, chatting with the content, and creating headlines with timecodes. 

Being a happy SnagIt user, I realized, this could even be a bit simpler with SnagIt than with QuickTime, which Simon used. SnagIt is a screen capture tool that can capture images, videos and images with scrolling. You can add annotations and edit the video or photo before saving it. The process has three steps (and is basically the same as with QuickTime):

1. Capture (and edit)
2. Save to file
3. Upload

If the AI service would support loading from the internet, it could be done in just two steps, as I could send the file to a classic hosting service with FTP upload support (capture, send to SFTP), and configure SnagIt to copy the web url after uploading into the clipboard. I could then paste the URL into the prompt. Unfortunately, Google's AI Studio doesn't support loading media from the internet, right now.

SnagIt can also send captures to other targets such as Youtube, Google Drive, directories, and custom tools. With this, I could create a "gateway tool" (let's call it "snagit2gemini") that interacts with the Gemini API to enable a fully automated  flow:

1. Capture screen
2. Send to snagit2gemini (can be preconfigured in SnagIt)
3. snagit2gemini adds pre-configured instructions, sends it to the Gemini API, and handles the generated response.

A minimum viable solution would be a CLI tool that takes a pre-configured prompt and writes the output to a file. A more elaborate version would have a GUI for interactive prompting.

On the other hand: Using Google's AI Studio and uploading the video manually is also not too cumbersome. I however needed to resize long videos to HD format with QuickTime to make it smaller (max. file size 2 GB). Also, Safari crashed on uploading, with Chrome it works.

I've tried it and came to the conclusion that it's actually better for one-off tasks than a half-baked custom tool: It's more flexible and doesn't add too much burden.

If I find myself doing some process very often, I'll probably come back to this idea and implement "snagit2gemini". But for now, I'll just use the AI Studio. By the way, if you have a Gemini Advanced subscription, you can activate the [YouTube Extension](https://gemini.google.com/extensions) to give Gemini access to your YouTube videos.