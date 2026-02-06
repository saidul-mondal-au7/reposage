from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, task, crew
from crewai.agents.agent_builder.base_agent import BaseAgent
from crewai.tools import tool

from typing import List, Dict, Optional
from pydantic import BaseModel, Field

# --------- Tools (Agent-1) ----------
from reposage.tools.repo_cloner import clone_repo
from reposage.tools.file_scanner import scan_repository
from reposage.tools.file_classifier import classify_files
from reposage.tools.language_detector import detect_languages

from pathlib import Path

# --------------- Tools (Agent-3) ------------
from reposage.tools.security.secret_scanner import scan_for_secrets
from reposage.tools.security.auth_heuristics import analyze_auth_logic
from reposage.tools.security.endpoint_heuristics import detect_unsafe_endpoints

#  --------------- Tools (Agent-4) ------------
from reposage.tools.performance.n_plus_one import detect_n_plus_one
from reposage.tools.performance.pagination_check import detect_missing_pagination
from reposage.tools.performance.sync_io import detect_sync_io



class ScanRepositoryOutput(BaseModel):
    repo_path: str
    total_files_scanned: int
    main_directories: List[str]
    detected_languages: List[str]
    entry_points: List[str]
    config_files: List[str]
    dependency_files: List[str]
    file_summaries: Dict[str, str]

class ArchitectureAnalysisOutput(BaseModel):
    architecture_type: str  # monolith / microservices / modular monolith
    key_modules: List[str]
    service_interactions: List[str]
    detected_design_patterns: List[str]
    runtime_flow_summary: str

class SecurityIssue(BaseModel):
    issue: str
    severity: str  # Low / Medium / High
    affected_files: Optional[List[str]]
    recommended_fix: str

class SecurityAnalysisOutput(BaseModel):
    issues: List[SecurityIssue]

class PerformanceIssue(BaseModel):
    issue: str
    severity: str  # Low / Medium / High
    affected_file: Optional[str]
    likely_symptoms: Optional[str]
    recommended_fix: str


class PerformanceAnalysisOutput(BaseModel):
    issues: List[PerformanceIssue]

class RoadmapItem(BaseModel):
    priority: str  # P0 / P1 / P2
    task: str
    impact: str
    effort: str
    risk: str
    justification: str


class RoadmapOutput(BaseModel):
    immediate_fixes: List[RoadmapItem]
    short_term: List[RoadmapItem]
    medium_term: List[RoadmapItem]



@CrewBase
class RepoSageCrew:
    """
    Crew definition for RepoSage.
    Agents and tasks are loaded from YAML.
    """

    # agents: List[BaseAgent]
    # tasks: List[Task]

    agents_config = "config/agents.yaml"
    tasks_config = "config/tasks.yaml"


    # ================================
    # AGENTS
    # ================================

    @agent
    def code_scanner(self):
        """
        Code Scanner Agent:
        Responsible for cloning (if needed) and scanning the repo.
        """
        return Agent(
        config=self.agents_config['code_scanner'],
        tools=[
            clone_repo,
            scan_repository,
            classify_files,
            detect_languages,
        ],
        verbose=True,
    )

    @agent
    def architecture_analyst(self):
        return Agent(
        config=self.agents_config['architecture_analyst'],  # YAML-driven
        verbose=True,
        )

    @agent
    def security_analyst(self):
        return Agent(
        config=self.agents_config['security_analyst'],  # YAML-driven
        tools=[
            scan_for_secrets,
            analyze_auth_logic,
            detect_unsafe_endpoints,
        ],
        verbose=True,
        )

    @agent
    def performance_analyst(self):
        return Agent(
        config=self.agents_config['performance_analyst'],
        tools=[
            detect_n_plus_one,
            detect_missing_pagination,
            detect_sync_io,
        ],
        verbose=True,
        )

    @agent
    def roadmap_planner(self):
       return Agent(
        config=self.agents_config['roadmap_planner'],  # YAML-driven
        verbose=True,
    )

    # ================================
    # TASKS
    # ================================

    @task
    def scan_repository(self) -> Task:

        return Task(
        config=self.tasks_config['scan_repository'],  # YAML-driven
        # agent=self.code_scanner(),
        output_pydantic=ScanRepositoryOutput,
        )

    @task
    def analyze_architecture(self):
        return Task(
        config=self.tasks_config['analyze_architecture'],  # YAML-driven
        # agent=self.architecture_analyst(),
        output_pydantic=ArchitectureAnalysisOutput,  # optional but STRONG
    )

    @task
    def security_analysis(self):
        return Task(
        config=self.tasks_config['security_analysis'],  # YAML-driven
        # agent=self.security_analyst(),
        output_pydantic=SecurityAnalysisOutput,
    )

    @task
    def performance_analysis(self):
        return Task(
        config=self.tasks_config['performance_analysis'],  # YAML-driven
        # agent=self.performance_analyst(),
        output_pydantic=PerformanceAnalysisOutput,
    )

    @task
    def plan_roadmap(self):
        return Task(
        config=self.tasks_config['plan_roadmap'],  # YAML-driven
        # agent=self.roadmap_planner(),
        output_pydantic=RoadmapOutput,
    )

    # ================================
    # CREW
    # ================================

    @crew
    def crew(self) -> Crew:
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
        )
