from typing import TypedDict

from schemas import (
    ResearchPlan,
    AnalysisResult,
    ReviewResult,
    ResearchBrief,
)


class ResearchState(TypedDict, total=False):
    question: str

    plan: ResearchPlan
    analysis: AnalysisResult
    review: ReviewResult
    brief: ResearchBrief

    revision_count: int