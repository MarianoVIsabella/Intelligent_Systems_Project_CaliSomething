from crewai.tools import BaseTool
from pydantic import BaseModel, Field
from typing import Type
import spacy
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer


class NLPAnalysisInput(BaseModel):
    text: str = Field(..., description="News article text to analyze.")


class NLPAnalysisTool(BaseTool):
    name: str = "NLP Analysis Tool"
    description: str = (
        "Extracts named entities, keywords, and sentiment from a news article "
        "using spaCy and NLTK."
    )
    args_schema: Type[BaseModel] = NLPAnalysisInput

    def _run(self, text: str) -> str:
        try:
            nlp = spacy.load("en_core_web_sm")
        except OSError:
            return "spaCy model en_core_web_sm is missing. Run: uv run python -m spacy download en_core_web_sm"

        try:
            nltk.data.find("sentiment/vader_lexicon.zip")
        except LookupError:
            nltk.download("vader_lexicon")

        doc = nlp(text)

        entities = [
            {"text": ent.text, "label": ent.label_}
            for ent in doc.ents
        ]

        keywords = [
            token.lemma_.lower()
            for token in doc
            if token.pos_ in ["NOUN", "PROPN", "ADJ"]
            and not token.is_stop
            and token.is_alpha
        ]

        sentiment = SentimentIntensityAnalyzer().polarity_scores(text)

        return str({
            "entities": entities,
            "keywords": list(set(keywords))[:25],
            "sentiment": sentiment
        })