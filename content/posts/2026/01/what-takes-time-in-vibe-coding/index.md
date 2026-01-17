---
title: "What Takes Time in Vibe Coding"
date: 2026-01-13
categories: ["AI Engineering", "Blog"]
tags: ["Flet", "Vibe Coding"]
stream: false
---

Vibe scripting, for me, is when I develop small tools for myself with the help of coding agents. It works extremely well, especially for command-line tools.

I recently told a tax advisor about it. He was interested and wanted to see how it works. So I developed a small example on the spot: a VAT calculator. Not the best example, but I couldn't think of anything better on short notice.

It worked well, and after five minutes the VAT calculator with a Flet/Flutter GUI was up and running.

But I could also see: there's still room for improvement. For example, the layout wasn't great and the functionality was too limited.

As i wanted to know how long it would take to turn it into an actually useful app, I later developed it to become a VAT calculator for all EU countries, which uses a small AI pipeline to load rates and descriptions of which product categories are subject to which VAT rate from official EU pages and displays them in an improved GUI.

{{< figure
    src="vat-calculator.png"
    alt="EU VAT Calculator"
    caption="The EU VAT Calculator after 2h dev time"
    >}}

What started with five minutes for the simple version turned into about two hours. Of course, it's much better now. But it's interesting how big the effort difference is between a solution that serves a specific, narrowly defined purpose and a tool with a broader scope. There's a lot of work involved, and finesse is needed to make a tool that's truly useful. Personally, I need iterations with a human in the loop for that. Maybe there are developers who can perfectly specify everything upfront, but I usually need to see and use something to evaluate and improve it.

AI accelerates iterations enormously, and you can decide whether to consider it "good enough" sooner or do a few more iterations. I think this is an important reason why I don't develop faster with AI. I invest the time in more iterations and perhaps less thinking upfront, which then requires more iterations again.
