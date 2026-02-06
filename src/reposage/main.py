#!/usr/bin/env python
import sys
import warnings

from datetime import datetime

from reposage.crew import RepoSageCrew

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

from reposage.output.summary_generator import generate_summary_json
from reposage.output.report_generator import generate_report_md

def run():
    """
    Run the crew.
    """
    inputs = {
        "repo": "https://github.com/saidul-mondal-au7/reposage"
    }


    try:
        crew = RepoSageCrew().crew()
        result = crew.kickoff(inputs=inputs)
        # result = RepoSageCrew().kickoff(inputs=inputs)


        generate_summary_json(
        result["scan_repository"],
        result["analyze_architecture"],
        result["security_analysis"],
        result["performance_analysis"],
        result["plan_roadmap"],
        )

        generate_report_md(
            result["scan_repository"],
            result["analyze_architecture"],
            result["security_analysis"],
            result["performance_analysis"],
            result["plan_roadmap"],
        )

        print("\nCrew execution completed successfully.\n")
        return result
    except Exception as e:
        raise

if __name__ == "__main__":
    run()
