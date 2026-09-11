import os

from dotenv import load_dotenv
from openai import OpenAI

from planner import create_plan
from analyzer import analyze_plan
from reviewer import review_analysis


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

print("\nREVIEW")
print(f"Score: {review.score}")
print(f"Approved: {review.approved}")

print("\nFeedback:")
for number, feedback in enumerate(review.feedback, start=1):
    print(f"{number}. {feedback}")