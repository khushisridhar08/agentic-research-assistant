from openai import OpenAI

from schemas import ResearchPlan, ResearchResults, ResearchSource


def extract_sources(response):
    sources = []
    seen_urls = set()

    for item in response.output:

        if item.type != "message":
            continue

        for content in item.content:

            if content.type != "output_text":
                continue

            for annotation in content.annotations:

                if annotation.type != "url_citation":
                    continue

                if annotation.url in seen_urls:
                    continue

                seen_urls.add(annotation.url)

                sources.append(
                    ResearchSource(
                        title=annotation.title,
                        url=annotation.url,
                        content=content.text
                    )
                )

    return sources



def conduct_research(
    client: OpenAI,
    question: str,
    plan: ResearchPlan
) -> ResearchResults:

    sources = []
    seen_urls = set()

    for subtask in plan.subtasks:

        response = client.responses.create(
            model="gpt-5.6-luna",
            tools=[{"type": "web_search"}],
            input=f"""
Research the following subtask as part of answering
a larger research question.

Main research question:
{question}

Research subtask:
{subtask}

Find relevant and reliable information that helps answer
this subtask. Focus on factual information and recent
sources when appropriate.

Provide a concise, factual research summary and cite
the sources used.
"""
        )

        subtask_sources = extract_sources(response)

        for source in subtask_sources:
            if source.url not in seen_urls:
                seen_urls.add(source.url)
                sources.append(source)

    if not sources:
        raise ValueError(
            "Research failed: no cited sources were found "
            "for any of the research subtasks."
        )

    return ResearchResults(sources=sources)
