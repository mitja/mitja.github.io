
- how coval works
- feedback from customers - dial-in your metrics
- a-b testing goes also hand-in-hand
- how much percentage is good?
  - regression sets (certain levels should again be reached)
  - gaining here, losing there - bottom line tradeoff benefit?
  - evals are part of product, unit testing is just a best practice SWE
- good to create hill climbing sets
  - where you are not good at
  - you want to be improving on these over time
- transcription is easiest to evaluate (word error rate), latency
- they also do constant testing / stability, 
- numeric accuracy 
- pronounciation is the hardest ()
- deepgram add to judge, does it pronounce this in that way (medication names)
- deepgram model tuning (trick to evaluate by Klaudia)
- user has a task -> more patience, but low acceptance of errors
- other use cases: other aspects are more important
- "look at this im talking to an agent"
- designing the voice ux is important
- auto evals don't make sense,
  - to many different hings optimized for
- e2e testing - can test very different platforms
- what you can control is different (eg. latency)
- Effie
  - Cartesia: pause before custom pronounciation
  - Brooke: pause analysis, eg. 1s pause is unnatural
- prosody problem is really really hard
- Deepgram is very good
- Gemini 2.5 Flash, issue, barreled through periods.
- disfluency (how often)
- how natural related to how well it fits in different situations
- voices from big labs are a bit too pushed towards realistic
  - too much laugh, giggle, etc. 
  - great for initial impression
  - not great for listening to for hours a day
- no tts is perfect
  - cartesia, deepgram
  - use cases where expressiveness is bad
  - serious use case, friendly use case
  - growing list of spreadsheets
- start with basic 
  - eg does it avoid repetition
- then eval, does it only pass the pin verification step once in a conversation
- schedule runs with specific evals, see if it has been regressing
- if its failing, resimulate it multiple times (eg. 10x or 100x), to find out which percentage fails, get a sense of how bad an issue is
- Yes, not just for voice. All LLMs seem to struggle with this. GPT4.1 pretty good though
- Thoughts on Chatterbox? https://www.resemble.ai/chatterbox/ Is it actually better than ElevenLabs?
- I did mini evals yesterday - it seems better with negative emotions like anger/frustration but not much better otherwise compared to sonic-2

- Brooke has examples for everything - she pulls out the right one in time...

(not presenting coval)

- appointment scheduling:
  - good mid-complex
  - often needed

- schedule
- reschedule
- cancel

(more like integration test)

- name phone number, etc. 
- repeatign, interrupting, etc.

- general questions first (Eg. did it book the appointment)

- appointment booked
- availability
- multiple procedures
- preferred times
- no duplicate availability checks
- capture email, lastname, xxx
- graph what the agent should be doing, graph what goes wrong
- metrics correlation, dashboard
- correleate with human judge
- specific, human judge aligned can be good to  (specific with criteria)
- iterative process, very simple at first, start with basic evals, watch, improve metric, add metrics, test sets, weekly multiple weeks, not only simulator, also monitoring calls
- should create processes and systems for evals, regression tests, hillclimbing sets, reliability sets, customer specific sets, feed from evals, traces, 
- time to first outcome (in one conversation): yes, multi-conv not yet
- multi-step simulation piece is part of it

how fast is the generation with flux? with 4image