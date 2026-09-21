from openai import OpenAI

from schemas import ResearchPlan, ResearchResults, ResearchSource


def conduct_research(
    client: OpenAI,
    question: str,
    plan: ResearchPlan
) -> ResearchResults:

    sources = []

    for subtask in plan.subtasks:

        response = client.responses.create(
            model="gpt-5.6-luna",
            tools=[
                {
                    "type": "web_search"
                }
            ],
            input=f"""
Research the following subtask as part of answering a larger
research question.

Main research question:
{question}

Research subtask:
{subtask}

Find relevant and reliable information that helps answer this
subtask. Focus on factual information and recent sources when
appropriate.
"""
        )

        sources.append(
            ResearchSource(
                title=f"Research for: {subtask}",
                url="",
                content=response.output_text
            )
        )

    return ResearchResults(
        sources=sources
    )