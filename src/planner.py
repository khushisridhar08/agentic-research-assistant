from openai import OpenAI

from schemas import ResearchPlan


def create_plan(client: OpenAI, question: str) -> ResearchPlan:

    response = client.responses.parse(
        model="gpt-5.4-mini",
        input=[
            {
                "role": "system",
                "content": """
You are the planning component of an AI research system.

Your responsibility is to decompose a research question
into specific research tasks.

Rules:
- Generate between 3 and 5 subtasks.
- Each subtask must investigate a distinct aspect of the question.
- Make each subtask specific and actionable.
- Do not answer the research question.
- Do not duplicate subtasks.
"""
            },
            {
                "role": "user",
                "content": question
            }
        ],
        text_format=ResearchPlan
    )

    return response.output_parsed