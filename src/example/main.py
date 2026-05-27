#!/usr/bin/env python
import sys
from example.crew import FakeNewsDetector


def run():
    """
    Run the Fake News Detector crew.
    """

    print("\n=== Fake News Detector Crew ===")
    print("Paste the news article or claim you want to verify.")
    print("When finished, press ENTER twice.\n")

    lines = []
    while True:
        line = input()
        if line == "":
            break
        lines.append(line)

    news_text = "\n".join(lines).strip()

    if not news_text:
        print("No news text provided.")
        sys.exit(1)

    inputs = {
        "news_text": news_text
    }

    result = FakeNewsDetector().crew().kickoff(inputs=inputs)

    print("\n=== FINAL FAKE NEWS VERDICT ===\n")
    print(result)


def train():
    """
    Train the crew for a given number of iterations.
    """
    inputs = {
        "news_text": "Sample news article for training."
    }

    try:
        FakeNewsDetector().crew().train(
            n_iterations=int(sys.argv[1]),
            filename=sys.argv[2],
            inputs=inputs,
        )
    except Exception as e:
        raise Exception(f"An error occurred while training the crew: {e}")


def replay():
    """
    Replay the crew execution from a specific task.
    """
    try:
        FakeNewsDetector().crew().replay(task_id=sys.argv[1])
    except Exception as e:
        raise Exception(f"An error occurred while replaying the crew: {e}")


def test():
    """
    Test the crew execution.
    """
    inputs = {
        "news_text": "A sample claim says that drinking coffee cures all diseases."
    }

    try:
        FakeNewsDetector().crew().test(
            n_iterations=int(sys.argv[1]),
            eval_llm=sys.argv[2],
            inputs=inputs,
        )
    except Exception as e:
        raise Exception(f"An error occurred while testing the crew: {e}")