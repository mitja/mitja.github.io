


session level: start with looking at what the user sees, not under the hood.

Practical strategies:

1. Collect initial traces (try to get to 100 diverse traces)
2. Manual review is key
3. Isolate errors (with simpler, single-turn test case)
4. Inherent multi-turn issues (eg. forgetting context): Truncate the trace before failue (n-1)
5. Optional advanced tip: Perturb real traces (eg. user changes mind mid convo) to test robustness

Multi-turn: Automation and key pitfalls

- run autom. on entire traces


Collaborative evaluation

- systematically engaging mutliple human stakeholders or experts
- first stap with llm - makes you too sloppy, do it yourself at first
- benevolent dictator, really helpful to put one person in charge, 
  one responsible, that really streamlines decisions. each additional
  decider makes it more complicated
- people don't do a good job annotatng, passed-around like hot potato
  two people makes it expon. harder to get it done
- in most cases benevolent dictator
- 

workflow

1. assemple team
2. draft initial rubric 
  - you will not get that right first time
  - who validates the validators paper
  - https://arxiv.org/pdf/2404.12272
3. select shared annotation set 
4. independent annotation (crucial!)
5. measure inter-annotator agreement (IAA)
6. alignemnt session(s)
7. revise and iterate
8. Finalize Rubric

are we on the same page (IAA)

- 

Better IAA. Cohen's Kappa (K) formula

- adjust the observed agreement to expected agreement by chance

<0: poos
0.61-0.8 consensus
0.81-1.0 almost perfect

judge example: put your product hat on, specific and compelling message from a sales perspective (only controversial are good to find out about disagreement, to align in the team)

helpfulness is a spectrum at what point is sth helpful enough and what makes sth helpful? Again: Don't outsouce!

how to make the criteria cleaner (so that sheya would also mark it as fail)?

- clarify defins and wordkng
- add illustrative examples to the rubric
- add decision rules for tricky situations
- if needed: Split the criterion (eg. factual relevance vs. proactivity) 

don't use llms too much, but you can use them...

- intependend labelling (open coding)
- don't let it pollute your thinking
- dont do too early (lazy, )
- later, still careful, you think outside of the box
- llm is good at refining the rubric (doc-etl)
- review very carefully, dont just let it create a rubrik
- after all said and done (incl. judgement), you can ask the llm to improve
- llm as a tool to help you go through the process, but not let the llm make the judgment call

everything is done to build a better flywheel

--- 

how to map out error modes?

- focus efforts
- use error analysis to guide the dimensions
- dimensions and tuples
- tuples just values, eg. different personas
- do error analysis first, what are the different failure modes?
- some dimensions are more signal - that is where you want to go. 
- you want to get to benefit really fast
- start focused and then branch out (get product feelings)

too ambitious systme prompt?

- string templating
- tuple does not have to be one word, can be entire parts of the prompt
- dimension, tone, user persona - cross product?
- rubric informs / becomes the prompt of the judge (add formal defintion to )
- a more detailed definition of the failure mode
- ideal rubric: all human judges come to the same judgement call
  - send that to a judge / llm - they can apply that to a trace

- evals in context of tool use / MCP
- what is the test harness?
- don't go into evals directly - if its obvious that you can fix sth (prompt, tool desc) go fix it
- tricky, persistent problem, where you need to iterate
- you have a way to trigger the behaviour
- debug contact lookup: let llm perturb input (what are tricky ways to trigger that tool call)
- small dataset that you can iterate through fast (second step before you go to eval) 

- query

- ambiguous user queries
- ask what is wrong with the product (need to change the product)

- good first rubric: few best examples
- the real dom expert shoud do th4 judgement - find out ho is the de?

later arch spec evals, also retrieval
retr is own thing, right docs retr. given a query

retr as tool: isolate retr and use

error eval - 5-6 clusters - evals
error anal let the cat emerging
if the project is too broadly scoped, tends to chatgpt - start to approach foundation model eval

test f isz prod too broad?

error analysis and evals for tools and later also evals for tools that regularly fail together

retrieval is the achilles heel often times in ai systems
there are special retrieval metrics

add as much intelligent metadata as possible
can you make the tool more agentic (search itself)

always look at reference metrics evals where you don'T need an llm (regex, reference data, etc)


error analysis is always useful!!!

ship before eval? why not? use those traces for error analysis.
how much refine before launching? a tradeoff between risk and benefits
real data is preferred

eval - is the user intent clear? is it correctly specified? don't want 3-4 follow-up questions
you need to find the user intent quickly/early.

try to stay session level, turn level is more tactical

reps! built tools, experience

"making an ai becoming a domain expert **is** the task" (it's the product)