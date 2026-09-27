from openai import OpenAI

from schemas import ResearchPlan, AnalysisResult, ResearchResults


def analyze_plan(
    client: OpenAI,
    question: str,
    plan: ResearchPlan,
    research: ResearchResults
) -> AnalysisResult:

    subtasks_text = "\n".join(
        f"{i + 1}. {subtask}"
        for i, subtask in enumerate(plan.subtasks)
    )

    research_text = "\n\n".join(
    f"[{i}] {source.title}\n"
    f"URL: {source.url}\n"
    f"Content: {source.content}"
    for i, source in enumerate(research.sources, start=1)
)

    response = client.responses.parse(
        model="gpt-5.4-mini",
        input=[
            {
                "role": "system",
                "content": """
You are the analysis component of an AI research system.

Your job is to analyze the research question using the
provided research subtasks.

For the analysis:
- Base your analysis primarily on the retrieved research.
- Use the numbered retrieved sources to support your findings.
- When describing evidence, reference the relevant source number,
  for example [1] or [2].
- Do not invent source numbers, URLs, citations, or evidence.
- Clearly identify uncertainties, conflicting information, or
  information that is not sufficiently supported by the retrieved
  sources.
"""
            },
            {
                "role": "user",
                "content": f"""
Research question:
{question}

Research subtasks:
{subtasks_text}

Retrieved research:
{research_text}

Analyze the retrieved research and use it to answer the
research question.
"""
}
            
        ],
        text_format=AnalysisResult
    )

    return response.output_parsed