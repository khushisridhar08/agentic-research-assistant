import os

from dotenv import load_dotenv
from openai import OpenAI

from graph import build_graph


MAX_REVISIONS = 2


def run_research(client: OpenAI, question: str):

    graph = build_graph(client)

    initial_state = {
        "question": question,
        "revision_count": 0
    }

    result = graph.invoke(initial_state)

    return result


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
        result = run_research(client, question)

        brief = result["brief"]
        review = result["review"]

        print("\nFINAL REVIEW")
        print(f"Score: {review.score}")
        print(f"Approved: {review.approved}")
        print(
            f"Revisions: "
            f"{result.get('revision_count', 0)}"
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

    except Exception as error:
        print("\nResearch workflow failed.")
        print(f"Error: {error}")


if __name__ == "__main__":
    main()