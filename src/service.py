from openai import OpenAI
from graph import build_graph


def run_research(client: OpenAI, question: str):
    graph = build_graph(client)

    initial_state = {
        "question": question,
        "revision_count": 0
    }

    return graph.invoke(initial_state)
