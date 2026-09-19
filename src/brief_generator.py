from openai import OpenAI

from schemas import AnalysisResult, ReviewResult, ResearchBrief


def generate_brief(
    client: OpenAI,
    question: str,
    analysis: AnalysisResult,
    review: ReviewResult
) -> ResearchBrief:

    findings_text = "\n".join(
        f"- {finding}" for finding in analysis.findings
    )

    evidence_text = "\n".join(
        f"- {evidence}" for evidence in analysis.evidence
    )

    uncertainties_text = "\n".join(
        f"- {uncertainty}" for uncertainty in analysis.uncertainties
    )

    feedback_text = "\n".join(
        f"- {feedback}" for feedback in review.feedback
    )

    response = client.responses.parse(
        model="gpt-5.4-mini",
        input=[
            {
                "role": "system",
                "content": """
You are the final synthesis component of an AI research system.

Create a concise, structured research brief from the completed
analysis.

The brief should:
- Directly address the original research question.
- Summarize the most important conclusions.
- Preserve important uncertainties and limitations.
- Provide practical recommendations where appropriate.
- Use clear and professional language.
- Do not invent sources, citations, or unsupported facts.
"""
            },
            {
                "role": "user",
                "content": f"""
Research question:
{question}

Findings:
{findings_text}

Evidence / reasoning:
{evidence_text}

Uncertainties:
{uncertainties_text}

Final reviewer feedback:
{feedback_text}
"""
            }
        ],
        text_format=ResearchBrief
    )

    return response.output_parsed