#!/usr/bin/env python
import sys
import warnings

from datetime import datetime

from reposage.crew import RepoSageCrew

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

# This main file is intended to be a way for you to run your
# crew locally, so refrain from adding unnecessary logic into this file.
# Replace with inputs you want to test with, it will automatically
# interpolate any tasks and agents information

def run():
    """
    Run the crew.
    """
    inputs = {
        'topic': 'AI LLMs',
        'current_year': str(datetime.now().year)
    }

    try:
        result = RepoSageCrew().crew().kickoff(inputs=inputs)
        print()
    except Exception as e:
        raise Exception(f"An error occurred while running the crew: {e}")
