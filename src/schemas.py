from pydantic import BaseModel, Field


class ResearchPlan(BaseModel):
    question: str
    subtasks: list[str] = Field(
        min_length=3,
        max_length=5
    )

class ResearchSource(BaseModel):
    title: str
    url: str
    content: str


class ResearchResults(BaseModel):
    sources: list[ResearchSource]
    
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