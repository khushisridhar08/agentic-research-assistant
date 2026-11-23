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


## Backend API

The application uses FastAPI to expose the LangGraph
multi-agent research workflow through REST endpoints.

### API Endpoints

- `GET /api/health` — Check backend availability.
- `POST /api/research` — Submit a research question.

### Run the Backend

Install dependencies:

```bash
python -m pip install -r requirements.txt
```

Start the development server:

```bash
PYTHONPATH=src python -m uvicorn api:app --reload --app-dir src
```

Open the API documentation:

http://127.0.0.1:8000/docs

### API Safety

Live OpenAI API execution is disabled by default.

Set `ENABLE_LIVE_API=true` only when intentionally
running paid research requests.

### Run Tests

```bash
PYTHONPATH=src python -m pytest tests/ -v
```

The test suite uses mocked API calls to validate the
research workflow without consuming OpenAI credits.

## Phase 2 — FastAPI Backend

The Agentic Research Assistant includes a FastAPI backend that exposes the LangGraph multi-agent research workflow through REST API endpoints.

### Features

- REST API integration with the existing LangGraph research workflow
- Pydantic request and response validation
- Input validation for research questions
- Structured JSON responses containing research results and review feedback
- Error handling for failed research workflows
- Environment-based control of live OpenAI API execution
- Automated API testing using pytest and mocked OpenAI calls
- Interactive API documentation using Swagger UI

### Project Structure

The backend uses the following modules:

| File | Purpose |
|---|---|
| `src/api.py` | Defines FastAPI endpoints and handles HTTP requests |
| `src/api_schemas.py` | Defines Pydantic request and response models |
| `src/service.py` | Executes the LangGraph research workflow |
| `src/graph.py` | Defines the multi-agent workflow |
| `src/main.py` | Provides command-line execution |
| `tests/test_api.py` | Tests API behavior and error handling |

### Installation

Clone the repository and navigate to the project directory.

Create and activate a Python virtual environment:

```bash
python3 -m venv venv
source venv/bin/activate
```

Install dependencies:

```bash
python -m pip install -r requirements.txt
```

### Environment Configuration

Create a `.env` file in the project root:

```env
OPENAI_API_KEY=your_openai_api_key
ENABLE_LIVE_API=false
```

Live OpenAI API execution is disabled by default to prevent unintended API charges.

The `.env` file must not be committed to GitHub.

### Running the FastAPI Server

From the project root, run:

```bash
PYTHONPATH=src python -m uvicorn api:app --reload --app-dir src
```

Open Swagger UI:

http://127.0.0.1:8000/docs

### API Endpoints

**GET `/api/health`**

Checks whether the backend is running.

**POST `/api/research`**

Accepts a research question and invokes the multi-agent workflow when live API execution is enabled.

Example request:

```json
{
  "question": "How is AI changing software engineering?"
}
```

When live execution is disabled, the API returns a response with `"status": "disabled"`.

When enabled, a successful research request returns the generated brief, review feedback, and revision count.

### Input Validation

Research questions must:

- Contain at least 10 characters after trimming whitespace
- Not exceed 1,000 characters
- Not consist entirely of whitespace

Invalid requests return HTTP 422.

### Error Handling

- **200:** Request processed successfully or live research disabled
- **422:** Invalid research request
- **502:** Research workflow execution failed
- **503:** OpenAI API key is missing when live execution is enabled

### Automated Testing

Run the complete test suite:

```bash
PYTHONPATH=src python -m pytest tests/ -v
```

The current test suite contains **16 passing tests**, covering the multi-agent workflow, FastAPI endpoints, input validation, successful responses, and failure handling.

API integration tests use mocks to avoid unnecessary OpenAI API charges.

### Current Limitations

- Research execution is synchronous and may take time to complete.
- Research history is not yet persisted in a database.
- A frontend interface has not yet been implemented.
- Source citation traceability requires further improvement.
- Authentication and rate limiting are required before publicly exposing paid research execution.

### Next Steps

**Phase 3 — React + TypeScript Frontend**

Build a user interface for submitting research questions, displaying generated reports, viewing review results, and exporting research briefs.

**Phase 4 — Database and Background Processing**

Add PostgreSQL persistence, research history, and asynchronous job execution.

**Phase 5 — Deployment**

Add Docker, CI/CD with GitHub Actions, deployment configuration, and production documentation.