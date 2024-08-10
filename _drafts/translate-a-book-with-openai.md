

This tutorial is based on the OpenAI Cookbook article [Translate a book written in LaTeX from Slovenian into English](https://github.com/openai/openai-cookbook/blob/main/examples/book_translation/translate_latex_book.ipynb)

In diesem Artikel zeige ich Dir, wie Du ein Buch oder einen anderen langen Text mit Hilfe von GPT in eine andere Sprache übersetzen kannst.

Warum?

- Die Qualität ist sehr gut für viele Sprachen.
- Du kannst die Übersetzung anpassen (z.B. "Du" statt "Sie", spezielle Begriffe, Umgang mit Excel-Formeln)

Herausforderungen:

- den Text in Format überführen, das GPT gut verarbeiten kann und das die Formatierungen beibehält
- Token Limits, vor Allem Output Token, die z. B. bei GPT-4o auf etwas über 4000 Token und bei GPT-4o mini auf rund 16000 Token begrenzt sind. Das ist zwar viel, aber immer noch nicht genug für ein Buch.

Wie geht das?

- Schritt 1: Konvertiere den Text nach Markdown (Thema für ein anderes Video, kurz: Verwende pandoc für Word, HTML usw. Google Docs hat jetzt eine Markdown-Exportfunktion, verwende OCR oder GPT-4o Vision für PDFs ohne eingebetteten Text und Scans)
- Schritt 2: Die Übersetzung. Hierzu habe ich mit Hilfe von GPT ein Python Script erstellt, das folgendes macht:
  - Den Text laden, 
  - Den Text nach doppelten Zeilenumbrüchen aufteilen, dabei zu kleine Absätze zusammenfügen und zu große Absätze weiter unterteilen ("Chunking"). Das Chunking ist so eingestellt, dass ein Chunk möglichst zwischen  3000 Token enthält.
  - Den Text mit einem Prompt und einem Aufruf an die OpenAI Chat Completions API übersetzen.
- Schritt 3: Die Ergebnisse überprüfen, nachbearbeiten (verbessern...)

In this post, I will show you how you can translate a book or another long text with GPT into another language.

Why?

- quality is great for many languages.
- you can customize the translation (e.g. "Du" not "Sie", special terms, how to deal with Excel formulas)

Challenges:

- source format that GPT can handle and which preserves the formatting
- output token limit. (GPT-4o: about 4000 tokens, GPT-4o mini: 16000 tokens), a lot but not enough for a book.

How to do it?

- Step 1: convert the text to markdown (topic for another video, in brief: use pandoc for word, html, etc. Google Docs now has a markdown export feature, use OCR for PDFs or GPT-4o Vision for PDFs)
- Step 2: Translate the book
  - created a tool that loads the texts, chunks them by newlines, max. 2000 min 1000), asks GPT to translate them, and then saves the result.
  - also, created a custom GPT for this.
- Step 3: Check the results, post-process (improve...)

## Step 1: Prepare the book for translation

the book is already in markdown format which GPT can handle well. So this is done, already. If it would be in a different format, I would use other tools to convert it to markdown. Also, it's important to have clean input. Thus I would certainly quickly read through it to check for any errors or inconsistencies. For example, transforming from PDF to markdown often leaves header and footer informations in the text, which I would then remove.

## Step 2: Translate the book

I told GPT to create a Python script for me that takes all the files and converts them to markdown, which it did. Als an alternative, I also uploaded the book to ChatGPT+ and asked it to transfer it in place. Also done nicely. I've created a custom GPT for this linked in the comments.

## Step 3: Check the result and post-process

This is most important and most effort step. In my case, I used the translation only as a starting point and really rewrote many things. In addition, I had many Excel formulas in the content which needed special treatment. But this is a topic for another post.