import os

from dotenv import load_dotenv
from openai import OpenAI

from planner import create_plan
from analyzer import analyze_plan
from reviewer import review_analysis
from reviser import revise_analysis
from brief_generator import generate_brief


MAX_REVISIONS = 2


def run_research(client: OpenAI, question: str):

    print("\nRESEARCH QUESTION")
    print(question)

    # --------------------
    # Planner
    # --------------------
    print("\nCreating research plan...")
    plan = create_plan(client, question)

    print("\nRESEARCH PLAN")
    for number, subtask in enumerate(plan.subtasks, start=1):
        print(f"{number}. {subtask}")

    # --------------------
    # Analyzer
    # --------------------
    print("\nAnalyzing research plan...")
    analysis = analyze_plan(client, question, plan)

    print("\nANALYSIS")

    print("\nFindings:")
    for number, finding in enumerate(
        analysis.findings,
        start=1
    ):
        print(f"{number}. {finding}")

    print("\nUncertainties:")
    for number, uncertainty in enumerate(
        analysis.uncertainties,
        start=1
    ):
        print(f"{number}. {uncertainty}")

    # --------------------
    # Reviewer
    # --------------------
    print("\nReviewing analysis...")
    review = review_analysis(
        client,
        question,
        analysis
    )

    revision_count = 0

    # --------------------
    # Revision loop
    # --------------------
    while (
        not review.approved
        and revision_count < MAX_REVISIONS
    ):
        print(
            f"\nRevision required "
            f"({revision_count + 1}/{MAX_REVISIONS})"
        )

        analysis = revise_analysis(
            client,
            question,
            analysis,
            review
        )

        revision_count += 1

        review = review_analysis(
            client,
            question,
            analysis
        )

    print("\nFINAL REVIEW")
    print(f"Score: {review.score}")
    print(f"Approved: {review.approved}")
    print(f"Revisions: {revision_count}")

    print("\nFeedback:")
    for number, feedback in enumerate(
        review.feedback,
        start=1
    ):
        print(f"{number}. {feedback}")

    # --------------------
    # Final brief
    # --------------------
    if not review.approved:
        print(
        "\nWarning: Maximum revisions reached "
        "without reviewer approval."
        )
    print("\nGenerating final research brief...")

    brief = generate_brief(
        client,
        question,
        analysis,
        review
    )

    print("\nFINAL RESEARCH BRIEF")

    print("\nExecutive Summary:")
    print(brief.executive_summary)

    print("\nKey Findings:")
    for number, finding in enumerate(
        brief.key_findings,
        start=1
    ):
        print(f"{number}. {finding}")

    print("\nUncertainties:")
    for number, uncertainty in enumerate(
        brief.uncertainties,
        start=1
    ):
        print(f"{number}. {uncertainty}")

    print("\nRecommendations:")
    for number, recommendation in enumerate(
        brief.recommendations,
        start=1
    ):
        print(f"{number}. {recommendation}")

    return brief


def main():

    load_dotenv()

    api_key = os.getenv("OPENAI_API_KEY")

    if not api_key:
        raise ValueError(
            "OPENAI_API_KEY was not found in the environment."
        )

    client = OpenAI(api_key=api_key)

    question = (
        "How is generative AI changing software engineering?"
    )

    try:
        run_research(client, question)

    except Exception as error:
        print("\nResearch workflow failed.")
        print(f"Error: {error}")


if __name__ == "__main__":
    main()