- RAG is a core app on its own (question answering on a large set of docs), and RAG is an important part of many use cases - whenever you have own information that you want to use but that is too big to fit into context windows.

- very simple RAG is quite easy, what's hard is optimiizing. Like the approach: Quickly establish as simple baseline (any RAG is better than no RAG), then enable evaluation and iterate to improve until desired quality is achieved.
Enable evaluation: initial eval dataset, human eval, automated eval, metrics, i/o collection to improve dataset



Can LLMs Be Trusted for Evaluating RAG Systems? A Survey of Methods and Datasets is a nice study from the University Innsbruck, Austria, that gives an overview of - well the methods:

This study systematically reviews
63 academic articles to provide a comprehensive overview of
state-of-the-art RAG evaluation methodologies, focusing on four
key areas: datasets, retrievers, indexing and databases, and
the generator component. Look for feasibility of automated evaluation.

Spoiler: They conclude that LLMs can help but human evaluation is still needed.

RAG Components:

- indexing
- retrieval
- generation

many knobs to turn.

define quality: 

- indexing: performance, speed (formats, metadata, accurate representation, chunking)
- retrieval: relevance, effectively contribute to answer
- generation: relevance, accuracy, and overall performance, cost
- ux, integration

RAGAS:
ARES:
eRAG: