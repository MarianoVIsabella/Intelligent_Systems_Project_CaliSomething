from crew import FakeNewsCrew

def run_debunking_crew(news_text: str):
    """
    Executes the real multi-agent crew debate and verification workflow.
    No more mock agents used here.
    """
    # 1. Definiamo gli input che verranno interpolati nei file YAML (es: {news_text})
    inputs = {
        'news_text': news_text
    }

    try:
        # 2. Inizializziamo la Crew reale usando la classe strutturata
        fake_news_crew_instance = FakeNewsCrew()
        real_crew = fake_news_crew_instance.crew()
        
        # 3. Avviamo il dibattito reale passando gli input
        crew_result = real_crew.kickoff(inputs=inputs)
        
        # 4. Recuperiamo l'ultimo task eseguito (il decision_task)
        # e ne estraiamo direttamente l'oggetto Pydantic validato
        decision_task_object = real_crew.tasks[-1]
        
        return decision_task_object.output.pydantic

    except Exception as e:
        raise Exception(f"Real Crew execution failed: {e}")