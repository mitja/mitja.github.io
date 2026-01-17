---
author: null
date: 2025-11-29 18:21:46+02:00
draft: true
slug: docling-document-pipeline
title: A docling pdf pipeline
categories: ["AI Engineering", "Blog"]
tags: ["claude code", ""]
---

- docling can parse multiple document formats incl. PDF, DOCX, PPTX, XLSX, , WAV, MP3, VTT, images (PNG, TIFF, JPEG, ...)
Advanced PDF understanding incl. page layout, reading order, table structure, code, formulas, image classification
- Structured [information extraction]
- Various export formats and options, including Markdown, HTML, DocTags and lossless JSON
- Support of several Visual Language Models (GraniteDocling)
Parsing of Web Video Text Tracks (WebVTT) files
- ASR, VLM, Parse web 
- very small Granite Docling VLM

- Linux Foundation AI & Data Foundation project by IBM

The VlmPipeline in Docling allows you to convert documents end-to-end using a vision-language model.

Docling supports vision-language models which output:

DocTags (e.g. SmolDocling), the preferred choice
Markdown
HTML

https://docling-project.github.io/docling/