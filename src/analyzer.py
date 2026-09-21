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
        source.content
        for source in research.sources
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
- Address every subtask.
- Produce clear and specific findings.
- Include supporting reasoning or evidence.
- Identify uncertainties, limitations, or missing information.
- Avoid repeating the same point across multiple findings.
- Do not invent sources or citations.
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