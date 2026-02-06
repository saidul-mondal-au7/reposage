from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, task
from crewai.agents.agent_builder.base_agent import BaseAgent

from typing import List, Dict
from pydantic import BaseModel, Field

# --------- Tools (Agent-1) ----------
from reposage.tools.repo_cloner import clone_repo
from reposage.tools.file_scanner import scan_repository
from reposage.tools.file_classifier import classify_files
from reposage.tools.language_detector import detect_languages

from pathlib import Path

class ScanRepositoryOutput(BaseModel):
    repo_path: str
    total_files_scanned: int
    main_directories: List[str]
    detected_languages: List[str]
    entry_points: List[str]
    config_files: List[str]
    dependency_files: List[str]
    file_summaries: Dict[str, str]


@CrewBase
class RepoSageCrew:
    """
    Crew definition for RepoSage.
    Agents and tasks are loaded from YAML.
    """

    agents: List[BaseAgent]
    tasks: List[Task]

    # ================================
    # AGENTS
    # ================================

    @agent
    def code_scanner(self):
        """
        Code Scanner Agent:
        Responsible for cloning (if needed) and scanning the repo.
        """
        return {
            "tools": [
                clone_repo,
                scan_repository,
                classify_files,
                detect_languages,
            ]
        }

    @agent
    def architecture_analyst(self):
        return {}

    @agent
    def security_analyst(self):
        return {}

    @agent
    def performance_analyst(self):
        return {}

    @agent
    def roadmap_planner(self):
        return {}

    # ================================
    # TASKS
    # ================================

    @task
    def scan_repository(self) -> Task:

        return Task(
        config=self.tasks_config['scan_repository'],  # YAML-driven
        agent=self.code_scanner(),
        output_pydantic=ScanRepositoryOutput,
        )

    @task
    def analyze_architecture(self):
        pass

    @task
    def security_analysis(self):
        pass

    @task
    def performance_analysis(self):
        pass

    @task
    def plan_roadmap(self):
        pass

    # ================================
    # CREW
    # ================================

    def crew(self):
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            verbose=True,
        )

