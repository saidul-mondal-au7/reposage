from typing import List, Dict, Optional

from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, task, crew

from pydantic import BaseModel

# =======================
# TOOLS
# =======================

from reposage.tools.repo_cloner import clone_repo
from reposage.tools.file_scanner import scan_repository
from reposage.tools.file_classifier import classify_files
from reposage.tools.language_detector import detect_languages

from reposage.tools.security.secret_scanner import scan_for_secrets
from reposage.tools.security.auth_heuristics import analyze_auth_logic
from reposage.tools.security.endpoint_heuristics import detect_unsafe_endpoints

from reposage.tools.performance.n_plus_one import detect_n_plus_one
from reposage.tools.performance.pagination_check import detect_missing_pagination
from reposage.tools.performance.sync_io import detect_sync_io


# =======================
# OUTPUT SCHEMAS
# =======================

class ScanRepositoryOutput(BaseModel):
    repo_path: str
    total_files_scanned: int
    main_directories: List[str]
    detected_languages: List[str]
    entry_points: List[str]
    config_files: List[str]
    dependency_files: List[str]
    file_summaries: Optional[Dict[str, str]] = {}


class ArchitectureAnalysisOutput(BaseModel):
    architecture_type: str
    key_modules: List[str]
    service_interactions: List[str]
    detected_design_patterns: List[str]
    runtime_flow_summary: str


class SecurityIssue(BaseModel):
    issue: str
    severity: str
    affected_files: Optional[List[str]]
    recommended_fix: str


class SecurityAnalysisOutput(BaseModel):
    issues: List[SecurityIssue]


class PerformanceIssue(BaseModel):
    issue: str
    severity: str
    affected_file: Optional[str]
    likely_symptoms: Optional[str]
    recommended_fix: str


class PerformanceAnalysisOutput(BaseModel):
    issues: List[PerformanceIssue]


class RoadmapItem(BaseModel):
    priority: str
    task: str
    impact: str
    effort: str
    risk: str
    justification: str


class RoadmapOutput(BaseModel):
    immediate_fixes: List[RoadmapItem]
    short_term: List[RoadmapItem]
    medium_term: List[RoadmapItem]


# =======================
# CREW DEFINITION
# =======================

@CrewBase
class RepoSageCrew:
    """
    RepoSage Crew — stable, deterministic, CrewAI 1.9.3 compatible.
    """

    agents_config = "config/agents.yaml"
    tasks_config = "config/tasks.yaml"

    # =======================
    # AGENTS
    # =======================

    @agent
    def code_scanner(self) -> Agent:
        return Agent(
            config=self.agents_config["code_scanner"],
            tools=[
                clone_repo,
                scan_repository,
                classify_files,
                detect_languages,
            ],
            verbose=True,
        )

    @agent
    def architecture_analyst(self) -> Agent:
        return Agent(
            config=self.agents_config["architecture_analyst"],
            verbose=True,
        )

    @agent
    def security_analyst(self) -> Agent:
        return Agent(
            config=self.agents_config["security_analyst"],
            tools=[
                scan_for_secrets,
                analyze_auth_logic,
                detect_unsafe_endpoints,
            ],
            verbose=True,
        )

    @agent
    def performance_analyst(self) -> Agent:
        return Agent(
            config=self.agents_config["performance_analyst"],
            tools=[
                detect_n_plus_one,
                detect_missing_pagination,
                detect_sync_io,
            ],
            verbose=True,
        )

    @agent
    def roadmap_planner(self) -> Agent:
        return Agent(
            config=self.agents_config["roadmap_planner"],
            verbose=True,
        )

    # =======================
    # TASKS
    # =======================

    @task
    def scan_repository(self) -> Task:
        return Task(
            config=self.tasks_config["scan_repository"],
            agent=self.code_scanner(),
            expected_output="Structured repository scan JSON",
            output_pydantic=ScanRepositoryOutput,
            force_tool_output=True,   # critical
        )

    @task
    def analyze_architecture(self) -> Task:
        return Task(
            config=self.tasks_config["analyze_architecture"],
            agent=self.architecture_analyst(),
            output_pydantic=ArchitectureAnalysisOutput,
        )

    @task
    def security_analysis(self) -> Task:
        return Task(
            config=self.tasks_config["security_analysis"],
            agent=self.security_analyst(),
            expected_output="Structured security analysis JSON",
            output_pydantic=SecurityAnalysisOutput,
        )

    @task
    def performance_analysis(self) -> Task:
        return Task(
            config=self.tasks_config["performance_analysis"],
            agent=self.performance_analyst(),
            output_pydantic=PerformanceAnalysisOutput,
        )

    @task
    def plan_roadmap(self) -> Task:
        return Task(
            config=self.tasks_config["plan_roadmap"],
            agent=self.roadmap_planner(),
            output_pydantic=RoadmapOutput,
        )

    # =======================
    # CREW
    # =======================

    @crew
    def crew(self) -> Crew:
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
        )
