import os

from dotenv import load_dotenv
from openai import OpenAI

from planner import create_plan
from analyzer import analyze_plan
from reviewer import review_analysis
from reviser import revise_analysis
from brief_generator import generate_brief


load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)


question = "How is generative AI changing software engineering?"

plan = create_plan(client, question)


print("\nRESEARCH QUESTION")
print(plan.question)
analysis = analyze_plan(client, question, plan)

print("\nRESEARCH PLAN")

for number, subtask in enumerate(plan.subtasks, start=1):
    print(f"{number}. {subtask}")

print("\nANALYSIS")

print("\nFindings:")
for number, finding in enumerate(analysis.findings, start=1):
    print(f"{number}. {finding}")

print("\nEvidence / Reasoning:")
for number, evidence in enumerate(analysis.evidence, start=1):
    print(f"{number}. {evidence}")

print("\nUncertainties:")
for number, uncertainty in enumerate(analysis.uncertainties, start=1):
    print(f"{number}. {uncertainty}")

review = review_analysis(client, question, analysis)

MAX_REVISIONS = 2
revision_count = 0

while not review.approved and revision_count < MAX_REVISIONS:

    print("\nAnalysis rejected by reviewer.")
    print("Revising analysis...")

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
for number, feedback in enumerate(review.feedback, start=1):
    print(f"{number}. {feedback}")

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
for number, finding in enumerate(brief.key_findings, start=1):
    print(f"{number}. {finding}")

print("\nUncertainties:")
for number, uncertainty in enumerate(brief.uncertainties, start=1):
    print(f"{number}. {uncertainty}")

print("\nRecommendations:")
for number, recommendation in enumerate(
    brief.recommendations,
    start=1
):
    print(f"{number}. {recommendation}")