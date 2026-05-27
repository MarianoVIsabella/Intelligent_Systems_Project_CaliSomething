from crewai import Agent, Task, Crew, Process
from models.shared_state import CategorizerOutput, ExpertOutput, FinalVerdictOutput

def run_debunking_crew(news_text: str):
    # --- AGENTI FINTI ---
    categorizer = Agent(
        role='Categorizer Finto',
        goal='Restituisci sempre categorie fisse per testare il sistema.',
        backstory='Sei un mock agent per i test.',
        allow_delegation=False
    )
    
    expert = Agent(
        role='Esperto Finto',
        goal='Genera un parere finto.',
        backstory='Sei un mock agent per i test.',
        allow_delegation=False
    )
    
    judge_panel = Agent(
        role='Giuria Finta',
        goal='Restituisci sempre FAKE per i test.',
        backstory='Sei un mock agent per i test.',
        allow_delegation=False
    )

    # --- TASK FINTI (che forzano l'uso dei modelli Pydantic) ---
    task_cat = Task(
        description=f"Analizza la notizia: '{news_text}'. Ignorala e restituisci ['health', 'politics'].",
        expected_output="Lista di categorie",
        agent=categorizer,
        output_pydantic=CategorizerOutput
    )
    
    task_exp = Task(
        description="Ricevi le categorie e la notizia. Genera un'opinione inventata.",
        expected_output="Opinione dell'esperto",
        agent=expert,
        output_pydantic=ExpertOutput
    )
    
    task_judge = Task(
        description="Ricevi i dati precedenti. Genera un verdetto finale FAKE con finte motivazioni.",
        expected_output="Verdetto finale strutturato",
        agent=judge_panel,
        output_pydantic=FinalVerdictOutput
    )

    # --- ASSEMBLAGGIO CREW ---
    crew = Crew(
        agents=[categorizer, expert, judge_panel],
        tasks=[task_cat, task_exp, task_judge],
        process=Process.sequential,
        verbose=True
    )

    # Eseguiamo la crew
    crew_result = crew.kickoff()
    
    # Restituiamo l'output Pydantic dell'ultimo task
    return task_judge.output.pydantic