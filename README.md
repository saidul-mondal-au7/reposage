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
- pip install -r ../requirements.txt

## command

- python -m reposage.main --repo https://github.com/saidul-mondal-au7/rag_medical_chatbot.git 
or
- python -m reposage.main --path ./my-local-repo

### Folder structure

reposage/
├── src/reposage/
│   ├── config/
│   │   ├── agents.yaml
│   │   └── tasks.yaml
│   ├── tools/
│   ├── output/
│   │   ├── summary_generator.py
│   │   ├── report_generator.py
│   │   
│   ├── crew.py
│   └── main.py
├── outputs/
│   ├── summary.json
│   ├── report.md
│   
├── .env
├── pyproject.toml
└── README.md
|__requirements.txt











