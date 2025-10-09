---
title: "A FastHtML UX Clone of NotebookLM"
summary: "."
date: 2025-09-21
categories: 
  - Building AI Apps
tags:
  - FastHTML
  - UX
showTableOfContents: true
#layout: "simple"
showZenMode: true
#layout: "simple"
draft: true
---

- great LLM app UX
- single space, not jumping between tabs
- dynamic 3 column layout
- from input to work to output
- each has 3 sizes: collapsed, default, wide-open
- chat plus

NotebookLM is a nice example of an LLM app that goes beyond basic chat interfaces. Jason Spielman
article: https://jasonspielman.com/notebooklm

Idea:

- can I recreate the basic ux in fasthtml
- first instance: does not have to be pixel-perfect. Structure and kinetic
- learn fasthtml
- learn to build ux for llm apps beyond basic chat ui
- create a foundation and building blocks for own llm apps
  - simple parts by applying
  - complex parts (eg. the SSE system)
- learn what is possible with fasthtml, and where the limits are (if I can build NotebookLM with it, it's probably not the limiting factor for building my own apps)

- use monsterui / daisy/tailwind
- start with the basic things that are structurally close, even if they look different

## Architecture

- 3 panel structure with header, tiny footer
- panels represent the flow of work from left to right:
  - input
  - actions
  - output
- 3-panel layouts very common, mostly used for navigation, canvas, details/properties
- the interesting new thing: for flow of work.

## Panel states

- each panel..
- animation
- the more interesting problem: how to maintain state across the panels
- htmx/fastapi: each panel a swappable, inside: elements swappable
- what if...
  - a long-running tasks updates a state, eg. ingest is done, input info needs to be updated
  - idea: sse for each panel
  
  - a state change in one panel results in an update in other panels

- sse stream (one)
- informs which elements need to refresh their state
- left and right panel: maybe whole-swap is ok
- main chat could be long, whole swap? attach only?

SSE messages consist of an event name and a data packet. No other metadata is allowed in the message. Here is an example:

```
event: EventName
data: <div>Content to swap into your HTML page.</div>
```

We’ll use the sse-swap attribute to listen for this event and swap its contents into our webpage.

```html
<div hx-ext="sse" sse-connect="/event-source" sse-swap="EventName"></div>
```

- event names in SSE messages must match `see-swap` valuse.
- browsers can only listen to events for eventnamaes that have been registered 
- other messages will be discarded
- sse messages without explicit event names have the implicit name `message`.
- catch it with `sse-swap="message"`
- mulitple message names can be catched in one element or in child elements:

```html
Multiple events in the same element
<div hx-ext="sse" sse-connect="/server-url" sse-swap="event1,event2"></div>

Multiple events in different elements (from the same source).
<div hx-ext="sse" sse-connect="/server-url">
    <div sse-swap="event1"></div>
    <div sse-swap="event2"></div>
</div>
```

- `hx-get` and similar can be triggered with `hx-trigger="sse:<event_name>"`

- `hx-swap` specifies how the response will be swapped in relative to the target of the ajax request 
- `beforeend` inserts after the last child of the target element
- register two events in the chat component: swap, append
- conditionally set `hx-swap="beforeend"` if the beforeend event is sent
- the server view must return only the single element in this case
- let the server know to only append, eg `hx-get="/chat/?append=1"` or even have a single chat msg. endpoint
- default is `innerHTML` which replaces the inner html of the target element
- in this case (default), the server view must return the whole chat history.

This enables a granular approach to ui updates depending on server state:

- each panel gets their event name
- each individually swappable detailed component gets their event name
- server-side: 
  - manual dependency resolution
    - if you update source, you know the chat and outcome needs to be updated, too.
    - works in coarse-grained state, with few elements that can be updated based on changes in other elements
    - even in simple situations error-prone, it's easy to forget a dependency
    - result is ui inconsistent with backend state (bad)
  - how to automatically maintain a state dependency tree and send the required messages?
    - explicit declaration of what goes into ui state of each element
    - template context and how it's filled
    - maintain state in db / models
    - model change signals, a graph system to find dependent elements and send the signals
    - in ORM (sqlalchemy events https://docs.sqlalchemy.org/en/20/orm/events.html) or django signals
    - but: what about DB changes not via the orm/app? what about mass updates (collapse into as few events as possible)
    - maybe CDC plus handler, but quite a hard problem
    - could also be other way round: 
      - CDC creates an event stream of updated models
      - the ui tells explicitely what info is needed (on which models / even fields it depends on)
      - a server-component resolves the dependencies and reduces the number of required updates and sends the events
    - a separate blog post!
    - with sqlite: 
      - capture changes with tablename,pk,fieldnames,timestamp using triggers
      - https://simonwillison.net/2023/Apr/15/sqlite-history/
      - an endpoint consumes it, and sends events, filtered by tables,pks,start-timestamp
      - clients register with sse endpoint, server resolves required pks of that session
      - how to maintain dependencies?
        - tablename, pks, fields (pks are dynamic) to view/component
      - at update time:
        - whenever sth of interest updates (table in X, send a swap message with message name of the component)
        - de-duplicate - send only once
        - timestamp of change event must be unique for a transaction (?)
        - cull - don't send updates to elements that are part of another element that is already being updated
        - pk can be made semi-static by maintaining a tree info which instances belong to a certain parent instance, for example a session, each object of that session gets the sessionid as field, which is also stored in the history table
        - filter is easy, then. 
        - limitation: changes "external" to the session are not captured. (full-refresh needed), acceptable for interactive, not so much for reporting where data comes from many sources. In this case, a dashboard data structure and ETL pipeline into it might be suitable.
        - sessionid could also be a virtual field/in aview or resolved at query time
        - db gets queried eg. 10x per second, clients updated accordingly, good would be if the db is only queried once for all clients.
      - **result** (developer experience): 
        - create ui, each element that could be updated from other elements gets a unique SSE message name and a sse-swap
        - view function (the function that determines what will be displayed) is annotated with info which tables are needed (and fields)
        - each html element sends info of which other elements it is part of (automatically resolved)
        - the element-tree info is also used on the server side for culling (only the outermost update is sent)
        - the app client registers to the sse stream
        - every update is only a post, no need to swap on a per-component basis, the swapping is done automatically as desired
      - **drawbacks and limitations**:
        - higher write load on db: user-manipulatable ui state must be maintained server-side (eg. which page on pagination, expanded), on the positive side: ui state can be manipulated by the agent server-side
        - how to deal with append? (the solution can only swap, append could be implemented as a special case where swap events are sent, but when refresh is needed the whole thing is swapped)
          - register both a swap and an append, when the element in question is fresh enough, append (invaldiate?)

## Major elements

### Sources Panel

### Chat Panel

### Studio Panel

## Design

## Beyond static UX

- tool is fluid, can adjust to current needs, intents. 
- feels natural with a single pane ui with elements in multiple states
- map stays the same, focus shifts
- can go beyond what is visible on a single screen with scrolling

- context-aware interfaces help reduce cognitive load (eg. by suggesting actions)
- anticipating needs, surfacing the right tools/actions at the right moment streamlines workflows and minimizes fricti

## Conclusion

- great exercise, learned a lot about htmx and designing ux for llm apps
- design the interface, but how use htmx principles best, even in this kind of complex spa
- "stumbled" across the cdc-sse approach, simplified working with htmx a lot
  - just declare the dependencies
  - define an sse message for each component
  - save ui state on server (this is data, too)
  - rely on sse events to trigger out-of-component updates
  - no complicated thinking about what to update when, get a reactive ux that agents can manipulate