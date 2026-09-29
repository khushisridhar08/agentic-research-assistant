from types import SimpleNamespace

from researcher import extract_sources, conduct_research
from schemas import ResearchPlan
from unittest.mock import Mock



def test_extract_sources_returns_unique_citations():
    response = SimpleNamespace(
        output=[
            SimpleNamespace(
                type="message",
                content=[
                    SimpleNamespace(
                        type="output_text",
                        text="AI is changing software development.",
                        annotations=[
                            SimpleNamespace(
                                type="url_citation",
                                title="AI and Software Engineering",
                                url="https://example.com/ai-software",
                            ),
                            SimpleNamespace(
                                type="url_citation",
                                title="AI and Software Engineering",
                                url="https://example.com/ai-software",
                            ),
                            SimpleNamespace(
                                type="url_citation",
                                title="Developer Productivity Report",
                                url="https://example.com/productivity",
                            ),
                        ],
                    )
                ],
            )
        ]
    )

    sources = extract_sources(response)

    assert len(sources) == 2

    assert sources[0].title == "AI and Software Engineering"
    assert sources[0].url == "https://example.com/ai-software"
    assert sources[0].content == "AI is changing software development."

    assert sources[1].title == "Developer Productivity Report"
    assert sources[1].url == "https://example.com/productivity"


def test_extract_sources_returns_empty_list_without_citations():
    response = SimpleNamespace(
        output=[
            SimpleNamespace(
                type="message",
                content=[
                    SimpleNamespace(
                        type="output_text",
                        text="Research response without citations.",
                        annotations=[],
                    )
                ],
            )
        ]
    )

    sources = extract_sources(response)

    assert sources == []

def test_conduct_research_processes_all_subtasks():
    response_one = SimpleNamespace(
        output=[
            SimpleNamespace(
                type="message",
                content=[
                    SimpleNamespace(
                        type="output_text",
                        text="Research findings for subtask one.",
                        annotations=[
                            SimpleNamespace(
                                type="url_citation",
                                title="Source One",
                                url="https://example.com/source-one",
                            )
                        ],
                    )
                ],
            )
        ]
    )

    response_two = SimpleNamespace(
        output=[
            SimpleNamespace(
                type="message",
                content=[
                    SimpleNamespace(
                        type="output_text",
                        text="Research findings for subtask two.",
                        annotations=[
                            SimpleNamespace(
                                type="url_citation",
                                title="Source Two",
                                url="https://example.com/source-two",
                            )
                        ],
                    )
                ],
            )
        ]
    )

    response_three = SimpleNamespace(
    output=[
        SimpleNamespace(
            type="message",
            content=[
                SimpleNamespace(
                    type="output_text",
                    text="Research findings for subtask three.",
                    annotations=[
                        SimpleNamespace(
                            type="url_citation",
                            title="Source Three",
                            url="https://example.com/source-three",
                        )
                    ],
                )
            ],
        )
    ]
)

    fake_client = Mock()

    fake_client.responses.create.side_effect = [
        response_one,
        response_two,
        response_three,
    ]

    plan = ResearchPlan(
        question="How is AI changing software engineering?",
        subtasks=[
            "Research AI coding tools",
            "Research developer productivity",
            "Research software quality and reliability",
        ],
    )

    result = conduct_research(
        fake_client,
        plan.question,
        plan,
    )

    assert fake_client.responses.create.call_count == 3

    assert len(result.sources) == 3

    assert result.sources[0].title == "Source One"
    assert result.sources[0].url == "https://example.com/source-one"

    assert result.sources[1].title == "Source Two"
    assert result.sources[1].url == "https://example.com/source-two"

    assert result.sources[2].title == "Source Three"
    assert result.sources[2].url == "https://example.com/source-three"