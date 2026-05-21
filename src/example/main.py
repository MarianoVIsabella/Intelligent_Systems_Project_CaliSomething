#!/usr/bin/env python
import sys
import warnings
from datetime import datetime

# Replace 'example.crew' with actual project crew folder name if different
from crew import Example 

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

def run():
    """ Run the crew normally from terminal """
    inputs = {
        'topic': 'AI LLMs',
        'current_year': str(datetime.now().year)
    }
    try:
        Example().crew().kickoff(inputs=inputs)
    except Exception as e:
        raise Exception(f"An error occurred while running the crew: {e}")

# --- ADDED FOR STREAMLIT UI (Independent Mock Mode) ---
def run_from_streamlit(news_text: str):
    """
    This function handles input from the Streamlit UI.
    NOTE: Currently returns MOCK data so you can develop independently.
    When Person 2 and 3 finish, connect this to:
    return Example().crew().kickoff(inputs={'news_text': news_text})
    """
    from models.shared_state import FinalVerdictOutput
    import time
    
    # Simulate agent discussion delay
    time.sleep(2) 
    
    # Return structured Pydantic mock data for your UI testing
    return FinalVerdictOutput(
        final_verdict="FAKE",
        judge_votes=["FAKE", "REAL", "FAKE"],
        reasoning="The submitted news lacks verification from credible primary sources. "
                  "Statistical data cited within the text appears to be manipulated or fabricated."
    )

def train():
    inputs = {"topic": "AI LLMs", 'current_year': str(datetime.now().year)}
    try:
        Example().crew().train(n_iterations=int(sys.argv[1]), filename=sys.argv[2], inputs=inputs)
    except Exception as e:
        raise Exception(f"An error occurred while training the crew: {e}")

def replay():
    try:
        Example().crew().replay(task_id=sys.argv[1])
    except Exception as e:
        raise Exception(f"An error occurred while replaying the crew: {e}")

def test():
    inputs = {"topic": "AI LLMs", "current_year": str(datetime.now().year)}
    try:
        Example().crew().test(n_iterations=int(sys.argv[1]), eval_llm=sys.argv[2], inputs=inputs)
    except Exception as e:
        raise Exception(f"An error occurred while testing the crew: {e}")