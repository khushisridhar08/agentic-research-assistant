
from typing import Literal

from pydantic import BaseModel, Field
from pydantic import field_validator


class ResearchRequest(BaseModel):
    question: str = Field(
        min_length=10,
        max_length=1000,
        description="The research question to investigate."
    )

    @field_validator("question")
    @classmethod
    def validate_question(cls, value: str) -> str:
        cleaned = value.strip()

        if len(cleaned) < 10:
            raise ValueError(
                "Question must contain at least 10 non-whitespace characters."
            )

        return cleaned



class ResearchResponse(BaseModel):
    question: str
    status: Literal["completed", "disabled"]
    review: dict | None = None
    brief: dict | None = None
    revision_count: int = Field(default=0, ge=0)
    message: str | None = None
