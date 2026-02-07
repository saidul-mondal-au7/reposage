#!/usr/bin/env python
import warnings

from reposage.crew import RepoSageCrew
from reposage.output.summary_generator import generate_summary_json
from reposage.output.report_generator import generate_report_md
from reposage.output.normalize_output import normalize_output

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")


def run():
    inputs = {
        "repo": "https://github.com/saidul-mondal-au7/reposage.git"
    }

    # crew = RepoSageCrew().crew()
    # result = crew.kickoff(inputs=inputs)
    result = RepoSageCrew().crew().kickoff(inputs=inputs)

    print("result:", result)


    # ✅ Correct CrewAI 1.9.3 output extraction
    outputs = {}

    for task_output in result.tasks_output:
        outputs[task_output.name] = normalize_output(task_output.raw)

    print("OUTPUT KEYS:", outputs.keys())
    print("SCAN OUTPUT:", outputs["scan_repository"])


    # ✅ Generate artifacts
    generate_summary_json(
        outputs["scan_repository"],
        outputs["analyze_architecture"],
        outputs["security_analysis"],
        outputs["performance_analysis"],
        outputs["plan_roadmap"],
    )

    generate_report_md(
        outputs["scan_repository"],
        outputs["analyze_architecture"],
        outputs["security_analysis"],
        outputs["performance_analysis"],
        outputs["plan_roadmap"],
    )

    print("\n✅ Crew execution completed successfully.")
    print("📄 Outputs written to: outputs/summary.json, outputs/report.md\n")

    return outputs


if __name__ == "__main__":
    run()
