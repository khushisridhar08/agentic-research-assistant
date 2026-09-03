# Agentic Research Assistant

An AI-powered research assistant that uses large language models and a multi-stage workflow to transform complex research questions into structured, reviewed research briefs.

The project explores agentic AI patterns including task decomposition, structured LLM outputs, automated review, validation, and iterative refinement.

## Overview

The Agentic Research Assistant breaks a research question into smaller, actionable subtasks and processes them through specialized components responsible for planning, analysis, and review.

The workflow is designed to go beyond a single LLM call by introducing structured intermediate outputs and an independent review stage that evaluates the quality and completeness of generated results.

## Architecture

```text
Research Question
       |
       v
+---------------+
|    Planner    |
+---------------+
       |
       | Research Plan
       v
+---------------+
|   Analyzer    |
+---------------+
       |
       | Analysis
       v
+---------------+
|   Reviewer    |
+---------------+
       |
       | Score + Feedback
       v
   Approved?
    /      \
   No      Yes
   |        |
   v        v
Revise   Research Brief
```

### Planner

The Planner decomposes a research question into 3–5 distinct and actionable research subtasks.

Rather than returning unstructured text, the Planner produces a validated `ResearchPlan` that can be consumed directly by later stages of the workflow.

### Analyzer

The Analyzer processes the research plan and generates structured findings, supporting information, and uncertainties for the identified subtasks.

### Reviewer

The Reviewer independently evaluates the generated analysis for criteria such as relevance, completeness, and consistency.

If the result does not satisfy the required quality threshold, reviewer feedback can be used to trigger a targeted revision before producing the final research brief.

## Key Features

- LLM-powered research question decomposition
- Multi-stage Planner → Analyzer → Reviewer workflow
- Structured outputs using Pydantic models
- Schema-based validation of LLM responses
- Automated quality review and scoring
- Conditional revision and retry workflow
- Modular Python architecture
- Secure API key management using environment variables

## Tech Stack

- **Python**
- **OpenAI API**
- **Pydantic**
- **python-dotenv**

Planned additions include LangGraph for workflow orchestration, tool calling for external research, automated testing, and a lightweight user interface.

## Project Structure

```text
agentic-research-assistant/
|
├── src/
│   ├── planner.py
│   ├── analyzer.py
│   ├── reviewer.py
│   ├── schemas.py
│   └── main.py
|
├── tests/
├── .gitignore
├── requirements.txt
└── README.md
```

## Getting Started

### 1. Clone the repository

```bash
git clone <repository-url>
cd agentic-research-assistant
```

### 2. Create a virtual environment

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file in the project root:

```text
OPENAI_API_KEY=your_api_key_here
```

The `.env` file is excluded from version control to prevent API credentials from being committed.

### 5. Run the application

```bash
python src/main.py
```

## Example

Input:

```text
How is generative AI changing software engineering?
```

The Planner decomposes the question into research areas such as:

```text
1. Analyze the impact of generative AI on developer productivity.
2. Examine its effect on software quality and reliability.
3. Investigate changes in software engineering roles and skills.
4. Evaluate security and governance concerns.
5. Examine changes to software development workflows.
```

These subtasks are then passed through the analysis and review stages before a final structured research brief is produced.

## Development Roadmap

- [x] Project setup and LLM API integration
- [x] Structured research plan schema
- [x] Planner component
- [ ] Analyzer component
- [ ] Reviewer component
- [ ] Conditional revision workflow
- [ ] LangGraph workflow orchestration
- [ ] Research tool integration
- [ ] Automated tests and evaluation
- [ ] User interface

## Goals

This project is intended to explore practical patterns for building reliable LLM-powered applications, including:

- Agent specialization
- Structured generation
- LLM output validation
- Multi-step reasoning workflows
- Automated response evaluation
- Failure handling and retry strategies
- Agentic workflow orchestration

## License

This project is for educational and portfolio purposes.
