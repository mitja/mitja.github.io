---
title: Hands-on ChatGPT in Excel (Book)
date: 2023-12-18 16:30:00 +0200
author: mitja
category: Excel is All You Need
permalink: /blog/2023/10/25/chatgpt-image-inputs-use-cases/
tags: 
 - ChatGPT
 - OpenAI
 - Excel
 - Book
render_with_liquid: false
permalink: /resources/ai-engineering/ebooks/hands-on-chatgpt-in-excel/
image:
  path: /assets/img/featured-chatgpt-in-excel-book-cover.png
  alt: The Hands-on ChatGPT in Excel book cover.
---

Excel is a suprisingly simple and effective tool to create solutions that make use of Generative AI.

In this book you will learn everything you need to know to create your own AI-infused Excel tools:

1. How to use the new `LABS.GENERATIVEAI` Excel function,
2. How to prompt ChatGPT to get results you can work with in Excel, and
3. How to use a hand full of other Excel functions to create prompts and work with completions.

You can buy this book on [Amazon](https://www.amazon.com/dp/B0CQ3CRBKJ/).

You can also buy my course [ChatGPT for Excel Users](https://courses.mitjamartini.com/courses/chatgpt-and-excel) which covers the same topics.

## Downloads

Here are the Excel workbooks referenced in the book. You can download them individually or as a [single zip archive](/assets/chatgpt-excel/handson-chatgpt-in-excel-examples.zip).

### Getting Started and Creating Prompts with Excel Formulas

| Download Link                                              | Description                                                                                                                                                                                                           |
|------------------------------------------------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| [chatgpt-capabilities.xlsx](/assets/chatgpt-excel/chatgpt-capabilities.xlsx) | A framework to think about ChatGPT's capabilities. Main point: ChatGPT is not only about creative writing.                                                                                                          |
| [concatenating-text.xlsx](/assets/chatgpt-excel/concatenating-text.xlsx)       | Shows how to create prompts for ChatGPT in Excel with text concatenation.                                                                                                                                              |
| [converting-numbers-to-text.xlsx](/assets/chatgpt-excel/converting-numbers-to-text.xlsx) | Shows how to convert numbers, dates, and times to a format that you can use in ChatGPT prompts.                                                                                                                       |
| [joined-lists.xlsx](/assets/chatgpt-excel/joined-lists.xlsx)                   | How to join lists in Excel so that the data can be used in ChatGPT prompts.                                                                                                                                           |
| [markdown.xlsx](/assets/chatgpt-excel/markdown.xlsx)                         | Demonstrates joining tabular cell ranges into a CSV table that ChatGPT can understand. ChatGPT converts Excel tables to Markdown tables.                                                                               |
| [largest-capital.xlsx](/assets/chatgpt-excel/largest-capital.xlsx)             | Demonstrates joining tabular cell ranges into a single CSV String with the TEXTJOIN Function. In this example, the data is added to the prompt that asks ChatGPT to select the largest capital in terms of population relative to the country's population. |
| [text-topic-verification-tool.xlsx](/assets/chatgpt-excel/text-topic-verification-tool.xlsx) | A workbook prepared for the lab about Text Topic Verification. The task is to convert a prompt template into a valid Excel formula. The tool can check if a text is about a given topic. This works even if the word for the topic is not mentioned in the text. |
| [text-topic-verification-tool-solution.xlsx](/assets/chatgpt-excel/text-topic-verification-tool-solution.xlsx) | A solution for the Text Topic Verification lab.                                                                                                                                                                      |

### Basic Prompt Engineering Techniques for Excel

| Download Link                                                              | Description                                                                                                     |
|----------------------------------------------------------------------------|-----------------------------------------------------------------------------------------------------------------|
| [concrete-and-water-density.xlsx](/assets/chatgpt-excel/concrete-and-water-density.xlsx)                 | Prompting ChatGPT to generate Numbers for Excel.                                                                |
| [days-since-man-on-moon.xlsx](/assets/chatgpt-excel/days-since-man-on-moon.xlsx)             | Prompting ChatGPT to generate dates for Excel.                                                                  |
| [time-extraction.xlsx](/assets/chatgpt-excel/time-extraction.xlsx)                             | Prompting ChatGPT to generate times for Excel.                                                                  |
| [cities-list.xlsx](/assets/chatgpt-excel/cities-list.xlsx)                                       | Prompting ChatGPT to generate lists for Excel.                                                                  |
| [fruits-table.xlsx](/assets/chatgpt-excel/fruits-table.xlsx)                                   | Prompting ChatGPT to generate tables for Excel.                                                                 |
| [date-transformer.xlsx](/assets/chatgpt-excel/date-transformer.xlsx)                           | A workbook prepared for the lab about date transformation.                                                      |
| [date-transformer-solution.xlsx](/assets/chatgpt-excel/date-transformer-solution.xlsx)         | A solution for the lab about date transformation.                                                               |
| [sentence-generator.xlsx](/assets/chatgpt-excel/sentence-generator.xlsx)                       | A workbook prepared for the lab about sentence generation.                                                      |
| [sentence-generator-solution.xlsx](/assets/chatgpt-excel/sentence-generator-solution.xlsx)     | A solution for the lab about sentence generation.                                                               |
| [sentence-generator-solution-improved.xlsx](/assets/chatgpt-excel/sentence-generator-solution-improved.xlsx) | An improved solution for the lab about sentence generation.                                                     |

### Adding Logic to Prompt Flows in Excel

| Download Link                                                  | Description                                                                                                                                                                                                                                                                                             |
|----------------------------------------------------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| [prompt-preparator.xlsx](/assets/chatgpt-excel/prompt-preparator.xlsx) | Demonstrates letting the user decide what to do next by asking the user to decide if the app should start prompting.                                                                                                                                                                                        |
| [logical-functions.xlsx](/assets/chatgpt-excel/logical-functions.xlsx) | Shows the effect of the XOR, AND, and OR functions on four variants of input values as well as the result of the NOT function on the result of the OR function.                                                                                                                                          |
| [comparison-operators.xlsx](/assets/chatgpt-excel/comparison-operators.xlsx) | Shows the effect of the six comparison operators on three variants of input values.                                                                                                                                                                                                                    |
| [combo-compass.xlsx](/assets/chatgpt-excel/combo-compass.xlsx)       | Demonstrates the use of logical functions and the IF functions to let Excel decide what to do next.                                                                                                                                                                                                    |
| [grammar-genie.xlsx](/assets/chatgpt-excel/grammar-genie.xlsx)       | Demonstrates the use of a ChatGPT result in the condition of an Excel IF function.                                                                                                                                                                                                                     |
| [dreamfit.xlsx](/assets/chatgpt-excel/dreamfit.xlsx)                 | Demonstrates the use of lookup tables together with the XLOOKUP function to look up parts of a prompt for ChatGPT.                                                                                                                                                                                     |
| [opti-response.xlsx](/assets/chatgpt-excel/opti-response.xlsx)       | Demonstrates a parallel prompt flow in Excel. The workbook contains an input cell for customer feedback and a list of products. The workbook uses parallel prompt flows to infer the sentiment and the product mentioned in the feedback. Then, it uses the results to generate a positive response.         |
| [context-check.xlsx](/assets/chatgpt-excel/context-check.xlsx)       | Demonstrates that LABS.GENERATIVEAI only forwards information to ChatGPT that you provide via the prompt attribute. It does not keep context information on its own.                                                                                                                                    |
| [chatsheet.xlsx](/assets/chatgpt-excel/chat-sheet.xlsx)               | Demonstrates how to build a chat sheet in Excel.                                                                                                                                                                                                                                                      |
| [tablejoin-function.xlsx](/assets/chatgpt-excel/tablejoin-function.xlsx) | An Excel workbook that contains the TABLEJOIN Excel LAMBDA function and an example how to use it. You can use the TABLEJOIN function to join tabular cell ranges into a CSV table with a single function call.                                                                                         |
| [data-dynamo.xlsx](/assets/chatgpt-excel/data-dynamo.xlsx)           | Contains an Excel LAMBDA function for creating example data with the help of ChatGPT.                                                                                                                                                                                                                  |
| [slogan-sheet.xlsx](/assets/chatgpt-excel/slogan-sheet.xlsx)         | A workbook prepared for the lab about creating Slogan Sheet. This can help you come up with and evaluate creative slogan ideas and is an example of a multi-step prompt flow in Excel.                                                                                                                  |
| [slogan-sheet-solution.xlsx](/assets/chatgpt-excel/slogan-sheet-solution.xlsx) | A solution for the Slogan Sheet lab.                                                                                                                                                                                                                                                                  |

### Advanced Prompt Engineering Techniques for Excel

| Download Link                                                                        | Description                                                                                                                                                                                                                                                                                                                                                                                                    |
|-----------------------------------------------------------------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| [number-extraction.xlsx](/assets/chatgpt-excel/number-extraction.xlsx)              | Demonstrates few-shot prompting with Excel and ChatGPT by extracting numbers from text.                                                                                                                                                                                                                                                                                                                        |
| [sentiment-classification-few-shot.xlsx](/assets/chatgpt-excel/sentiment-classification-few-shot.xlsx) | Demonstrates few-shot prompting with Excel and ChatGPT by classifying the sentiment of a text.                                                                                                                                                                                                                                                                                                                |
| [sentiment-classification-zero-shot.xlsx](/assets/chatgpt-excel/sentiment-classification-zero-shot.xlsx) | Shows that ChatGPT can classify the sentiment of a text with zero-shot prompting, too.                                                                                                                                                                                                                                                                                                                         |
| [reasoning-extraction-with-cot.xlsx](/assets/chatgpt-excel/resoning-extraction-with-cot.xlsx)   | Demonstrates chain-of-thought prompting for improved reasoning capabilities. ChatGPT solves a text challege. The resulting number is extracted with a second prompt. I found this example in the paper [When do you need Chain-of-Thought Prompting for ChatGPT?](https://arxiv.org/pdf/2304.03262.pdf) by Chen et al, 2023. I used it as it nicely compares chain-of-thought with zero shot reasoning. |
| [reasoning-extraction-without-cot.xlsx](/assets/chatgpt-excel/resoning-extraction-without-cot.xlsx) | Demonstrates that ChatGPT can solve the challenge also without chain-of-thought prompting. This shows that you do not always need to add the magic "let's think step by step" phrase to your prompts to get good results.                                                                                                                                                                                    |
| [are-you-open.xlsx](/assets/chatgpt-excel/are-you-open.xlsx)                       | Demonstrates retrieval augmented generation (RAG) with Excel and ChatGPT.                                                                                                                                                                                                                                                                                                                                      |
| [simupy.xlsx](/assets/chatgpt-excel/simupy.xlsx)                                   | Demonstrates the "acting" prompt engineering technique by letting ChatGPT act as a Python interpreter. With this, you get a simulated Python interpreter in Excel.                                                                                                                                                                                                                                              |
| [flash-function.xlsx](/assets/chatgpt-excel/flash-function.xlsx)                   | A workbook prepared for the lab about creating FLASH - a ChatGPT powered flash fill implemented as an Excel LAMBDA function.                                                                                                                                                                                                                                                                                  |
| [flash-function-solution.xlsx](/assets/chatgpt-excel/flash-function-solution.xlsx) | A solution for the FLASH lab.                                                                                                                                                                                                                                                                                                                                                                               |

## Your Feedback

If you find errors or have other feedback, please let me know: You can reach out to me via [Email](mailto:hi@mitjamartini.com), [Twitter](https://twitter.com/MitjaMartini) or [LinkedIn](https://www.linkedin.com/in/mitjamartini/).
