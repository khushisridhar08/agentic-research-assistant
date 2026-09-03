from pydantic import BaseModel, Field


class ResearchPlan(BaseModel):
    question: str
    subtasks: list[str] = Field(
        min_length=3,
        max_length=5
    )


class AnalysisResult(BaseModel):
    findings: list[str]
    evidence: list[str]
    uncertainties: list[str]


class ReviewResult(BaseModel):
    score: int = Field(ge=0, le=100)
    approved: bool
    feedback: list[str]


class ResearchBrief(BaseModel):
    executive_summary: str
    key_findings: list[str]
    uncertainties: list[str]
    recommendations: list[str]