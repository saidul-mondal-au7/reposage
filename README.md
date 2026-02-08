# Reposage — AI-Powered Repository Analysis Engine

Reposage is a CrewAI-based multi-agent system that analyzes any code repository and automatically generates:

- Architecture insights
- Security risk analysis
- Performance bottleneck detection
- Prioritized engineering roadmap
- Reports in JSON, Markdown, and PDF formats

It supports:
- GitHub repositories
- Local folders
- CLI execution
- CI/CD pipelines

---

## Features

- Multi-agent analysis using CrewAI
- Automatic repo cloning or local scanning
- Architecture detection (monolith / modular monolith / microservices)
- Security and performance risk detection
- Engineering roadmap generation (P0 / P1 / P2)
- Output formats:
  - `summary.json`
  - `report.md`
  - `report.pdf`

---

## System Requirements

- Python >= 3.10 and < 3.14
- Git installed
- macOS / Linux / Windows
- Internet access (for LLM calls)

---

## Installation

### 1. Clone the repository

# Reposage — AI-Powered Repository Analysis Engine

Reposage is a CrewAI-based multi-agent system that analyzes any code repository and automatically generates:

- Architecture insights
- Security risk analysis
- Performance bottleneck detection
- Prioritized engineering roadmap
- Reports in JSON, Markdown, and PDF formats

It supports:
- GitHub repositories
- Local folders
- CLI execution
- CI/CD pipelines

---

## Features

- Multi-agent analysis using CrewAI
- Automatic repo cloning or local scanning
- Architecture detection (monolith / modular monolith / microservices)
- Security and performance risk detection
- Engineering roadmap generation (P0 / P1 / P2)
- Output formats:
  - `summary.json`
  - `report.md`
  - `report.pdf`

---

## System Requirements

- Python >= 3.10 and < 3.14
- Git installed
- macOS / Linux / Windows
- Internet access (for LLM calls)

---

## Installation

### 1. Clone the repository
- git clone https://github.com/saidul-mondal-au7/reposage.git
- cd reposage
## set up
- python -m venv venv
- source venv/bin/activate

- pip install crewai
- pip install -r requirements.txt

## command

- export OPENAI_API_KEY=your api key
- export PYTHONPATH=$PWD/src

- python -m reposage.main --repo https://github.com/saidul-mondal-au7/rag_medical_chatbot.git 
or
- python -m reposage.main --path ./my-local-repo

### Folder structure
```text
reposage/
├── src/
│   └── reposage/
│       ├── __init__.py
│
│       ├── config/
│       │   ├── agents.yaml
│       │   └── tasks.yaml
│
│       ├── tools/
│       │   ├── __init__.py
│       │   ├── repo_cloner.py          # clone_repo (main/master hardcoded)
│       │   ├── file_scanner.py
│       │   ├── file_classifier.py
│       │   ├── language_detector.py
│       │
│       │   ├── security/
│       │   │   ├── __init__.py
│       │   │   ├── secret_scanner.py
│       │   │   ├── auth_heuristics.py
│       │   │   └── endpoint_heuristics.py
│       │   │
│       │   └── performance/
│       │       ├── __init__.py
│       │       ├── n_plus_one.py
│       │       ├── pagination_check.py
│       │       └── sync_io.py
│
│       ├── health/
│       │   ├── __init__.py
│       │   ├── scorer.py              # repo health score
│       │   ├── badge.py               # health badge (🟢🟡🟠🔴)
│       │   └── risky_files.py          # top risky files logic
│
│       ├── output/
│       │   ├── __init__.py
│       │   ├── normalize_output.py
│       │   ├── summary_generator.py   # summary.json
│       │   ├── report_generator.py    # report.md
│       │   └── report_pdf_generator.py# report.pdf
│
│       ├── crew.py                    # CrewBase + agents + tasks
│       └── main.py                    # CLI runner (repo / path)
│
├── outputs/
│   ├── summary.json
│   ├── report.md
│   └── report.pdf
│
├── .env                               # OPENAI_API_KEY
├── pyproject.toml
├── requirements.txt
└── README.md
