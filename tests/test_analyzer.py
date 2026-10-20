
from unittest.mock import Mock

from analyzer import analyze_plan
from schemas import (
    ResearchPlan,
    ResearchResults,
    ResearchSource,
    AnalysisResult,
)


def test_analyzer_receives_retrieved_sources():
    client = Mock()

    expected_analysis = AnalysisResult(
        findings=[
            "AI coding tools are changing software development."
        ],
        evidence=[
            "[1] Source One reports changes in developer workflows."
        ],
        uncertainties=[
            "Long-term effects remain uncertain."
        ],
    )

    client.responses.parse.return_value = Mock(
        output_parsed=expected_analysis
    )

    plan = ResearchPlan(
        question="How is AI changing software engineering?",
        subtasks=[
            "Research AI coding tools",
            "Research developer productivity",
            "Research software quality and reliability",
        ],
    )

    research = ResearchResults(
        sources=[
            ResearchSource(
                title="Source One",
                url="https://example.com/source-one",
                content="AI coding tools are changing developer workflows.",
            ),
            ResearchSource(
                title="Source Two",
                url="https://example.com/source-two",
                content="AI tools may improve developer productivity.",
            ),
        ]
    )

    result = analyze_plan(
        client,
        plan.question,
        plan,
        research,
    )

    assert result == expected_analysis
    client.responses.parse.assert_called_once()

    call_kwargs = client.responses.parse.call_args.kwargs
    user_message = call_kwargs["input"][1]["content"]

    assert "[1] Source One" in user_message
    assert "https://example.com/source-one" in user_message
    assert "AI coding tools are changing developer workflows." in user_message

    assert "[2] Source Two" in user_message
    assert "https://example.com/source-two" in user_message
    assert "AI tools may improve developer productivity." in user_message
