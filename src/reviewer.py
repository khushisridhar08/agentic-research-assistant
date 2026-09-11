from openai import OpenAI

from schemas import AnalysisResult, ReviewResult


def review_analysis(
    client: OpenAI,
    question: str,
    analysis: AnalysisResult
) -> ReviewResult:

    findings_text = "\n".join(
        f"- {finding}" for finding in analysis.findings
    )

    evidence_text = "\n".join(
        f"- {evidence}" for evidence in analysis.evidence
    )

    uncertainties_text = "\n".join(
        f"- {uncertainty}" for uncertainty in analysis.uncertainties
    )

    response = client.responses.parse(
        model="gpt-5.4-mini",
        input=[
            {
                "role": "system",
                "content": """
You are the reviewer component of an AI research system.

Evaluate the analysis for:
- relevance to the original research question
- completeness
- clarity
- internal consistency
- whether the findings are sufficiently supported
- whether major limitations or uncertainties were acknowledged

Return:
- a score from 0 to 100
- whether the analysis should be approved
- specific feedback explaining what should be improved

Approval rule:
Approve only if the analysis is strong enough to be used in a final research brief.
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
"""
            }
        ],
        text_format=ReviewResult
    )

    return response.output_parsed