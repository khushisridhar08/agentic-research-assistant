import os

from dotenv import load_dotenv
from openai import OpenAI

from planner import create_plan


load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)


question = "How is generative AI changing software engineering?"

plan = create_plan(client, question)


print("\nRESEARCH QUESTION")
print(plan.question)

print("\nRESEARCH PLAN")

for number, subtask in enumerate(plan.subtasks, start=1):
    print(f"{number}. {subtask}")