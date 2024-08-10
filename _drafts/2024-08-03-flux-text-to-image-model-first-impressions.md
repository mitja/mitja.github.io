The Flux text to image model generates impressive results. I've been having fun playing with it but @fabianstelzer really hit the nail with his [traffic sign generator glif.app](https://glif.app/@fab1an/glifs/clzdw2bxh000cw4nyavmeqp1u).

Here is a sign for "sleeping poodle ahead" which sits nicely on my office door as our poodle puppy likes to sleep while i'm working.

![AI generated image of a traffic sign raising awareness of a sleeping poodle ahead](https://glif.app/@MitjaMartini/runs/vbk13ewxoivfj0sw7264wz71)

If you're curious how the glif is made, you can hit the [remix](https://glif.app/@MitjaMartini/glifs/clzefuu1o0003g8368cub6q1o/edit) icon to see the prompt flow. 

In a first step the user is asked to enter an answer to the question "Traffic sign about what?". 

In the second step, the user input is put into a *promptmagic* cell that asks Claude 3.5 Sonnet to generate a visual description of how this might look like:

```
Consider the following input: {input1} - including implied instructions!
Come up with a visual description of how this would be displayed on a traffic sign as a symbol, be apt and succinct and include any mention of words as a title, just go, no intro:
```

In the third and final step, the user input and the response fron Claude are passed to Flux Pro with this prompt:

```
photograph of a traffic sign showing {promptmagic}, {input1} traffic sign, with blurry bokeh background, shot on analog film, high detail
```

Nice and easy, right?
