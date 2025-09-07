Gemini long context and video capabilities enable many interesting use cases.

Important: Don't use Vertex AI - it's more expensive (?)

https://ai.google.dev/gemini-api/docs?hl=de

Gute Anleitung (Upload mit chat): https://www.kaggle.com/code/paultimothymooney/how-to-upload-large-files-to-gemini-1-5

Analyze the attached video and audio like a productivity coach. The video is a screencast of me working and commenting my work. I am an indie hacker with limited time who wants to build SaaS apps. Summarize what I did, how I commented my work, what I've achieved, what I did well, and what I should improve with recommendations for improvement.

Analyzed with Flash, kind of worked, but got the instructions wrong I believe (I wanted to ha)

The followup was not too bad. I should now go on and record and analyze more, and then get a week-feedback on the summaries.

Maybe also try with Pro

https://aistudio.google.com/app/prompts/17v1M-eO-DDCsnPi3vfpa2ehLpq-XKQMD

Maybe I should also put in my initial recommendations from o1-preview as a guidance.


https://cloud.google.com/vertex-ai/generative-ai/docs/multimodal/video-understanding

https://cloud.google.com/vertex-ai/generative-ai/docs/samples/generativeaionvertexai-gemini-video-with-audio?hl=de#generativeaionvertexai_gemini_video_with_audio-python

https://blog.google/technology/ai/google-gemini-next-generation-model-february-2024/#build-experiment

https://ai.google.dev/gemini-api/docs/vision?hl=de&lang=python

Prices for long context, the 50 min video is the maximum, takes about xxx token (see docs), and assuming 5k output token.

| Model | Gemini 1.5 Pro | Gemini 1.5 Flash |
| --- | ---:| ---:|
| 1Mt in | $1.50 | $0.15 |
| 1Mt out | $10.00 | $0.60 |
| Video Token/s | 258 | 258 |
| Audio Token/s | 32 | 32 |
| Timestamp Token/s | 7 | 7 |
| Total Token/s | 297 | 297 |
| Token/50min | 891.000 | 891.000 |
| Token out | 4.000 | 4.000 |
| 50min Video | $1.38 | $0.14 |
| Caching 1Mt/h | $4.50 | $1.00 |