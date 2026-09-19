from openai import OpenAI

from schemas import AnalysisResult, ReviewResult


def revise_analysis(
    client: OpenAI,
    question: str,
    analysis: AnalysisResult,
    review: ReviewResult
) -> AnalysisResult:

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
You are the revision component of an AI research system.

Your task is to improve an existing analysis using reviewer feedback.

Rules:
- Address the reviewer feedback directly.
- Preserve useful findings from the original analysis.
- Improve weak, incomplete, or unclear reasoning.
- Add missing considerations when needed.
- Clearly identify uncertainties and limitations.
- Do not invent sources or citations.
"""
            },
            {
                "role": "user",
                "content": f"""
Research question:
{question}

Current findings:
{findings_text}

Current evidence / reasoning:
{evidence_text}

Current uncertainties:
{uncertainties_text}

Reviewer feedback:
{feedback_text}
"""
            }
        ],
        text_format=AnalysisResult
    )

    return response.output_parsed