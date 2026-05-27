from crewai.tools import BaseTool
from pydantic import BaseModel, Field
from typing import Type
from transformers import pipeline


class ClassificationInput(BaseModel):
    text: str = Field(..., description="News article text to classify.")


class NewsClassificationTool(BaseTool):
    name: str = "News Classification Tool"
    description: str = (
        "Classifies a news article into politics, health, science, economy, "
        "sports, technology, crime, entertainment, or general using Hugging Face."
    )
    args_schema: Type[BaseModel] = ClassificationInput

    def _run(self, text: str) -> str:
        labels = [
            "politics",
            "health",
            "science",
            "economy",
            "sports",
            "technology",
            "crime",
            "entertainment",
            "general"
        ]

        classifier = pipeline(
            "zero-shot-classification",
            model="facebook/bart-large-mnli"
        )

        result = classifier(text[:1000], labels)

        return str({
            "category": result["labels"][0],
            "confidence": result["scores"][0],
            "all_scores": dict(zip(result["labels"], result["scores"]))
        })