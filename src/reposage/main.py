#!/usr/bin/env python
import argparse
import warnings
from pathlib import Path

from reposage.crew import RepoSageCrew
from reposage.output.summary_generator import generate_summary_json
from reposage.output.report_generator import generate_report_md
from reposage.output.normalize_output import normalize_output

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")


def parse_args():
    parser = argparse.ArgumentParser(
        description="RepoSage – Automated Repository Analysis"
    )

    parser.add_argument(
        "--repo",
        type=str,
        help="GitHub repository URL (e.g. https://github.com/user/repo)",
    )

    parser.add_argument(
        "--path",
        type=str,
        help="Local repository path (e.g. ./my-repo)",
    )

    parser.add_argument(
        "--out",
        type=str,
        default="outputs",
        help="Output directory (default: outputs/)",
    )

    args = parser.parse_args()

    # Exactly one input source required
    if not args.repo and not args.path:
        parser.error("One of --repo or --path is required")

    if args.repo and args.path:
        parser.error("Use only one of --repo or --path")

    return args


def run():
    args = parse_args()

    inputs = {}
    if args.repo:
        inputs["repo"] = args.repo
    else:
        inputs["repo"] = str(Path(args.path).resolve())

    # crew = RepoSageCrew().crew()
    # result = crew.kickoff(inputs=inputs)
    result = RepoSageCrew().crew().kickoff(inputs=inputs)

    # ------------------------------
    # Extract task outputs (CrewAI 1.9.x safe)
    # ------------------------------
    outputs = {}
    for task_output in result.tasks_output:
        outputs[task_output.name] = normalize_output(task_output.raw)

    out_dir = Path(args.out)
    out_dir.mkdir(parents=True, exist_ok=True)

    # ------------------------------
    # Generate artifacts
    # ------------------------------
    generate_summary_json(
        outputs.get("scan_repository"),
        outputs.get("analyze_architecture"),
        outputs.get("security_analysis"),
        outputs.get("performance_analysis"),
        outputs.get("plan_roadmap"),
        output_path=out_dir / "summary.json",
    )

    generate_report_md(
        outputs.get("scan_repository"),
        outputs.get("analyze_architecture"),
        outputs.get("security_analysis"),
        outputs.get("performance_analysis"),
        outputs.get("plan_roadmap"),
        output_path=out_dir / "report.md",
    )

    print("\n✅ RepoSage execution completed")
    print(f"📄 Outputs written to: {out_dir.resolve()}\n")

    return outputs


if __name__ == "__main__":
    run()


# python -m reposage.main \
#   --repo https://github.com/saidul-mondal-au7/rag_medical_chatbot.git
# python -m reposage.main --path ./my-local-repo
