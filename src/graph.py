from typing import TypedDict
from openai import OpenAI

from planner import create_plan
from analyzer import analyze_plan
from reviewer import review_analysis
from reviser import revise_analysis
from researcher import conduct_research
from brief_generator import generate_brief
from langgraph.graph import StateGraph, START, END

from schemas import (
    ResearchPlan,
    ResearchResults,
    AnalysisResult,
    ReviewResult,
    ResearchBrief,
)


class ResearchState(TypedDict, total=False):
    question: str

    plan: ResearchPlan
    research: ResearchResults
    analysis: AnalysisResult
    review: ReviewResult
    brief: ResearchBrief

    revision_count: int

def planner_node(state: ResearchState, client: OpenAI):
    plan = create_plan(
        client,
        state["question"]
    )

    return {
        "plan": plan,
        "revision_count": 0
    }

def researcher_node(
    state: ResearchState,
    client: OpenAI
):

    research = conduct_research(
        client,
        state["question"],
        state["plan"]
    )

    return {
        "research": research
    }

def analyzer_node(state: ResearchState, client: OpenAI):
    analysis = analyze_plan(
        client,
        state["question"],
        state["plan"],
        state["research"]
    )

    return {
        "analysis": analysis
    }


def reviewer_node(state: ResearchState, client: OpenAI):
    review = review_analysis(
        client,
        state["question"],
        state["analysis"]
    )

    return {
        "review": review
    }


def reviser_node(state: ResearchState, client: OpenAI):
    analysis = revise_analysis(
        client,
        state["question"],
        state["analysis"],
        state["review"]
    )

    return {
        "analysis": analysis,
        "revision_count": state.get("revision_count", 0) + 1
    }


def brief_node(state: ResearchState, client: OpenAI):
    brief = generate_brief(
        client,
        state["question"],
        state["analysis"],
        state["review"]
    )

    return {
        "brief": brief
    }

MAX_REVISIONS = 2


def route_after_review(state: ResearchState):

    review = state["review"]
    revision_count = state.get("revision_count", 0)

    if review.approved:
        return "brief"

    if revision_count >= MAX_REVISIONS:
        return "brief"

    return "revise"

def build_graph(client: OpenAI):

    workflow = StateGraph(ResearchState)

    workflow.add_node(
        "planner",
        lambda state: planner_node(state, client)
    )

    workflow.add_node(
    "researcher",
    lambda state: researcher_node(state, client)
    )
    
    workflow.add_node(
        "analyzer",
        lambda state: analyzer_node(state, client)
    )

    workflow.add_node(
        "reviewer",
        lambda state: reviewer_node(state, client)
    )

    workflow.add_node(
        "reviser",
        lambda state: reviser_node(state, client)
    )

    workflow.add_node(
        "brief",
        lambda state: brief_node(state, client)
    )

    workflow.add_edge(
        START,
        "planner"
    )

    workflow.add_edge(
        "planner",
        "analyzer"
    )

    workflow.add_edge(
        "planner",
        "researcher"
    )

    workflow.add_edge(
        "researcher",
        "analyzer"
    )

    workflow.add_conditional_edges(
        "reviewer",
        route_after_review,
        {
            "revise": "reviser",
            "brief": "brief"
        }
    )

    workflow.add_edge(
        "reviser",
        "reviewer"
    )

    workflow.add_edge(
        "brief",
        END
    )

    return workflow.compile()