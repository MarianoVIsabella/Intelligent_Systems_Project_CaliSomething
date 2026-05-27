from pydantic import BaseModel
from typing import List

# Output che dovrà generare la Persona 2
class CategorizerOutput(BaseModel):
    categories: List[str]

# Output che dovrà generare la Persona 3 (Esperto)
class ExpertOutput(BaseModel):
    expert_opinion: str

# Output finale generato dai Giudici (Persona 3)
class FinalVerdictOutput(BaseModel):
    final_verdict: str  # REAL, FAKE, o UNSURE
    judge_votes: List[str]
    reasoning: str

