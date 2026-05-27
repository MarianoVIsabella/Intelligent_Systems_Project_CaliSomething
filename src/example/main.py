#!/usr/bin/env python

from datetime import datetime
import sys
import warnings
import logging
import time

from crew import FakeNewsCrew
from models.shared_state import FinalVerdictOutput

# =====================================================
# LOGGING CONFIGURATION
# =====================================================

logging.basicConfig(level=logging.INFO)

# Suppress specific warnings from dependencies
warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

# =====================================================
# TERMINAL EXECUTION
# =====================================================

def run(news_text: str):
    """
    Run the real CrewAI pipeline from terminal.
    """

    logging.info("Starting fake news analysis from terminal")

    inputs = {
        "news_text": news_text,
        'current_year': str(datetime.now().year),
    }

    try:

        return FakeNewsCrew().crew().kickoff(
            inputs=inputs
        )

    except Exception as e:

        raise Exception(
            f"An error occurred while running the crew: {e}"
        )

# =====================================================
# STREAMLIT MOCK MODE
# =====================================================

def run_from_streamlit(news_text: str):
    """
    Temporary mock mode used while
    other team members complete their agents.

    Later replace this mock return with:

    return FakeNewsCrew().crew().kickoff(
        inputs={
            "news_text": news_text
        }
    )
    """

    logging.info("Received news from Streamlit UI")

    # Simulate multi-agent discussion delay
    time.sleep(2)

    # MOCK OUTPUT FOR UI DEVELOPMENT
    return FinalVerdictOutput(
        final_verdict="FAKE",

        judge_votes=[
            "FAKE",
            "REAL",
            "FAKE"
        ],

        reasoning=(
            "The submitted news lacks confirmation "
            "from trusted sources and contains suspicious claims."
        )
    )

# =====================================================
# REAL STREAMLIT EXECUTION (FUTURE INTEGRATION)
# =====================================================

def run_real_crew(news_text: str):
    """
    Real CrewAI execution for future integration.
    """

    logging.info("Running real CrewAI pipeline")

    return FakeNewsCrew().crew().kickoff(
        inputs={
            "news_text": news_text,
            'current_year': str(datetime.now().year)
        }
    )

# =====================================================
# CREW TRAINING
# =====================================================

def train():

    inputs = {
        "news_text": "Sample fake news for training"
    }

    try:

        FakeNewsCrew().crew().train(
            n_iterations=int(sys.argv[1]),
            filename=sys.argv[2],
            inputs=inputs
        )

    except Exception as e:

        raise Exception(
            f"An error occurred while training the crew: {e}"
        )

# =====================================================
# CREW REPLAY
# =====================================================

def replay():

    try:

        FakeNewsCrew().crew().replay(
            task_id=sys.argv[1]
        )

    except Exception as e:

        raise Exception(
            f"An error occurred while replaying the crew: {e}"
        )

# =====================================================
# CREW TESTING
# =====================================================

def test():

    inputs = {
        "news_text": "Sample fake news for testing"
    }

    try:

        FakeNewsCrew().crew().test(
            n_iterations=int(sys.argv[1]),
            eval_llm=sys.argv[2],
            inputs=inputs
        )

    except Exception as e:

        raise Exception(
            f"An error occurred while testing the crew: {e}"
        )