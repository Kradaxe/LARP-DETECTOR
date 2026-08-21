live at : https://larp-detector-plum.vercel.app/

backend live at : https://larp-detector.onrender.com/

# LARP Detector

> **AI-powered credibility analysis for technical claims, resumes, and candidate profiles.**

LARP Detector is an AI-driven recruiter intelligence platform designed to analyze technical claims made by candidates and estimate how well those claims are supported by concrete technical evidence.

The system combines **LLM-based semantic analysis**, deterministic signal extraction, and a weighted credibility-scoring engine to identify potentially exaggerated or weakly supported technical claims.

The long-term goal is to turn LARP Detector into a tool that helps recruiters and hiring teams perform deeper technical screening before interviews.

---

## Why LARP Detector?

Modern technical resumes and professional profiles often contain statements such as:

> "Built a highly scalable distributed system handling millions of requests."

The problem is not necessarily that the statement is false — it's that a recruiter has limited time and often cannot determine whether the claim contains meaningful technical evidence.

LARP Detector analyzes claims for characteristics such as:

* Specificity
* Technical depth
* Evidence
* Implementation detail
* Technologies mentioned
* Quantitative metrics
* Technical reasoning

It then produces a **credibility score** and an explanation of why the claim appears credible, weak, or potentially exaggerated.

---

## Core Architecture

```text
                   ┌─────────────────────┐
                   │     Candidate       │
                   │ Resume / Text /     │
                   │ Technical Claims    │
                   └──────────┬──────────┘
                              │
                              ▼
                   ┌─────────────────────┐
                   │    FastAPI API      │
                   │      Layer          │
                   └──────────┬──────────┘
                              │
                              ▼
                   ┌─────────────────────┐
                   │  Analysis Service   │
                   └──────────┬──────────┘
                              │
             ┌────────────────┼────────────────┐
             ▼                ▼                ▼
      ┌─────────────┐  ┌─────────────┐  ┌─────────────┐
      │ Technology  │  │   Metrics   │  │    LLM      │
      │  Analyzer   │  │  Analyzer   │  │  Analysis   │
      └─────────────┘  └─────────────┘  └─────────────┘
             │                │                │
             └────────────────┼────────────────┘
                              ▼
                   ┌─────────────────────┐
                   │   Feature / Signal  │
                   │     Extraction      │
                   └──────────┬──────────┘
                              │
                              ▼
                   ┌─────────────────────┐
                   │ Credibility Scoring │
                   │      Engine         │
                   └──────────┬──────────┘
                              │
                              ▼
                   ┌─────────────────────┐
                   │ Recruiter-Facing    │
                   │ Analysis / Report   │
                   └─────────────────────┘
```

---

## Current Features

### 1. Technical Claim Analysis

The `/analyze` endpoint accepts technical text and runs it through the analysis pipeline.

Example:

```http
POST /api/v1/analyze
```

Input:

```json
{
  "text": "Built backend services using Python and FastAPI."
}
```

The system extracts deterministic signals and combines them with LLM-generated analysis.

---

### 2. Technology Signal Extraction

The analyzer identifies technologies mentioned in a candidate's claim.

Example:

```text
"Built REST APIs using Python, FastAPI and PostgreSQL."
```

Can produce signals such as:

```json
{
  "technology_count": 3,
  "technologies_found": [
    "python",
    "fastapi",
    "postgresql"
  ]
}
```

The technology analyzer is intentionally separated from the LLM so that deterministic signals can be used alongside probabilistic model output.

---

### 3. Metrics Detection

The system detects quantitative evidence such as:

```text
10,000 requests/sec
200ms latency
50GB dataset
99.9% uptime
3x performance improvement
```

Metrics provide an additional signal because concrete quantitative claims can be evaluated differently from generic statements.

---

### 4. LLM-Based Semantic Analysis

The LLM evaluates claims across several dimensions:

| Dimension             | Description                                                    |
| --------------------- | -------------------------------------------------------------- |
| Specificity           | How concrete and precise is the claim?                         |
| Technical Depth       | Does the claim demonstrate meaningful technical understanding? |
| Evidence              | Does the candidate provide evidence supporting the claim?      |
| Implementation Detail | Does the claim explain what was actually implemented?          |

The model also produces reasoning explaining its assessment.

---

### 5. Deterministic + LLM Hybrid Scoring

Rather than allowing an LLM to arbitrarily return a final score, LARP Detector combines model-generated signals with deterministic features.

Current scoring model:

```python
score = (
    specificity * 0.25 +
    technical_depth * 0.30 +
    evidence * 0.25 +
    implementation_detail * 0.20
) * 10

score += min(technology_count * 2, 10)
score += min(metrics_count * 3, 10)

score = min(round(score), 100)
```

This creates a transparent scoring layer on top of the LLM.

---

## Credibility Classification

The score is converted into a recruiter-friendly verdict:

```text
80 - 100  → Highly Credible
60 - 79   → Likely Genuine
40 - 59   → Possibly Exaggerated
0  - 39   → Potential LARP
```

The thresholds and weighting system are designed to remain configurable as the project gains evaluation data.

---

## Backend Structure

The backend follows a service-oriented architecture:

```text
backend/
│
├── app/
│   ├── api/
│   │   └── v1/
│   │       └── routes/
│   │           └── analyze.py
│   │
│   ├── analyzers/
│   │   ├── technology_analyzer.py
│   │   └── metrics_analyzer.py
│   │
│   ├── services/
│   │   ├── analysis_service.py
│   │   ├── llm_service.py
│   │   └── signal_extractor.py
│   │
│   ├── schemas/
│   │   └── ...
│   │
│   ├── utils/
│   │   └── json_parser.py
│   │
│   └── main.py
│
├── tests/
│
├── .env
├── requirements.txt
└── ...
```

The architecture separates:

* API routing
* Business logic
* Signal extraction
* LLM interaction
* Scoring
* Data validation
* Utility functions

This makes individual components independently testable and replaceable.

---

## Tech Stack

### Backend

* **Python**
* **FastAPI**
* **Pydantic**
* **Uvicorn**

### AI / ML

* **Google Gemini API**
* LLM-based semantic evaluation
* Structured JSON extraction
* Hybrid deterministic + LLM scoring

### Document Processing

The planned candidate-analysis pipeline supports:

* PDF extraction with `pypdf`
* DOCX parsing with `python-docx`
* PDF processing with PyMuPDF

### Planned Infrastructure

* PostgreSQL
* Redis
* Qdrant
* Docker
* Alembic

---

## Candidate Analysis Roadmap

The current text-analysis engine is the foundation for a larger recruiter-focused system.

### Phase 1 — Technical Claim Analysis

* [x] FastAPI backend
* [x] `/analyze` endpoint
* [x] Technology extraction
* [x] Metrics extraction
* [x] LLM evaluation
* [x] Structured LLM output
* [x] Credibility scoring
* [x] Credibility verdicts

### Phase 2 — Resume Intelligence

* [ ] PDF resume upload
* [ ] DOCX resume upload
* [ ] Resume text extraction
* [ ] Automatic claim segmentation
* [ ] Per-claim credibility analysis
* [ ] Suspicious claim detection
* [ ] Recruiter-friendly candidate report

### Phase 3 — GitHub Intelligence

* [ ] GitHub profile ingestion
* [ ] Repository analysis
* [ ] Language analysis
* [ ] Repository activity analysis
* [ ] Stars/forks/activity signals
* [ ] Resume-vs-GitHub consistency analysis

### Phase 4 — ML Infrastructure

* [ ] Candidate embeddings
* [ ] Vector database
* [ ] Similarity search
* [ ] Duplicate/near-duplicate claim detection
* [ ] Candidate comparison
* [ ] Feedback collection
* [ ] Model evaluation pipeline

### Phase 5 — Production Infrastructure

* [ ] PostgreSQL persistence
* [ ] Redis caching
* [ ] Dockerized deployment
* [ ] Automated testing
* [ ] CI/CD
* [ ] Observability
* [ ] Rate limiting
* [ ] Production deployment

---

## Example Analysis

Input:

```text
I built a FastAPI backend using Python and optimized the
API to handle 50,000 requests per second with Redis caching.
```

The system can extract signals such as:

```json
{
  "technologies_found": [
    "python",
    "fastapi",
    "redis"
  ],
  "metrics": [
    "50,000 requests per second"
  ]
}
```

The LLM then evaluates the claim based on:

```text
Specificity
Technical Depth
Evidence
Implementation Detail
```

These signals are combined by the scoring engine to produce a final credibility assessment.

---

## Design Philosophy

### Hybrid AI

LARP Detector deliberately does **not** rely entirely on an LLM.

The system combines:

```text
Deterministic Signals
        +
LLM Semantic Reasoning
        +
Explicit Scoring Logic
        =
Credibility Assessment
```

This provides greater transparency and makes the scoring system easier to evaluate and improve.

---

### Explainability

A recruiter should not simply receive:

```text
Credibility: 42/100
```

The system should explain **why**.

For example:

```text
The candidate mentions FastAPI and Redis and provides a
quantitative throughput claim, but does not explain the
architecture, caching strategy, workload characteristics,
or how the throughput was measured.
```

This makes the system useful as a screening aid rather than a black-box classifier.

---

## Future ML Direction

As labeled recruiter feedback becomes available, the deterministic scoring system can evolve into a learned ranking model.

Potential future pipeline:

```text
Candidate Claim
      │
      ▼
Feature Extraction
      │
      ├── Linguistic Features
      ├── Technical Signals
      ├── Quantitative Evidence
      ├── LLM Features
      └── Profile Evidence
              │
              ▼
        Feature Vector
              │
              ▼
       ML Ranking Model
              │
              ▼
      Credibility Score
```

Potential models include:

* Logistic Regression
* Gradient Boosting
* XGBoost
* Neural ranking models
* Transformer-based classifiers

The system can eventually use recruiter feedback as training data rather than relying exclusively on manually chosen weights.

---

## Running Locally

### Clone

```bash
git clone <repository-url>
cd LARP-DETECTOR
```

### Create virtual environment

Windows:

```bash
cd backend

python -m venv venv
venv\Scripts\activate
```

Linux/macOS:

```bash
cd backend

python3 -m venv venv
source venv/bin/activate
```

### Install dependencies

```bash
pip install -r requirements.txt
```

### Configure environment

Create a `.env` file:

```env
GEMINI_API_KEY=your_api_key_here
```

### Start the API

```bash
uvicorn app.main:app --reload
```

The API will be available at:

```text
http://127.0.0.1:8000
```

Interactive API documentation:

```text
http://127.0.0.1:8000/docs
```

---

## API

### Analyze Technical Claim

```http
POST /api/v1/analyze
```

Request:

```json
{
  "text": "Built a Python FastAPI service handling 10,000 requests per second."
}
```

The endpoint returns the extracted signals, LLM analysis, credibility score, and verdict.

---

## Disclaimer

LARP Detector is designed as a **decision-support and screening tool**, not as an automated truth detector.

A low credibility score does not prove that a candidate is lying. Likewise, a high score does not prove that a claim is true.

The system is intended to help recruiters identify claims that may deserve deeper technical verification during interviews.

---

## Project Goals

The ultimate goal of LARP Detector is to build an AI-powered technical screening system that can answer:

> **"Does this candidate's technical profile contain enough concrete evidence to support the claims they're making?"**

Rather than replacing technical interviews, LARP Detector aims to make them **more targeted and evidence-driven**.
