from crewai import Agent, Crew, Process, Task, LLM
from crewai.project import CrewBase, agent, crew, task
from example.tools.nlp_tools import NLPAnalysisTool
from example.tools.classification_tool import NewsClassificationTool
from crewai.agents.agent_builder.base_agent import BaseAgent

# Structured outputs
from models.shared_state import (
    FinalVerdictOutput
)
from crewai_tools import ScrapeWebsiteTool
import os
from dotenv import load_dotenv
load_dotenv()
# If you want to run a snippet of code before or after the crew starts,
# you can use the @before_kickoff and @after_kickoff decorators
def make_judge(config: dict) -> Agent:
    """Judge Agents Factory"""

    return Agent(
        **config,
        verbose=True,
        llm=LLM(model=os.environ["MODEL"]),
        allow_delegation=False,
    )

@CrewBase
class FakeNewsCrew():
    """Fake News Debunking Crew"""

    agents: list[BaseAgent]
    tasks: list[Task]
    agents_config="config/agents.yaml"
    tasks_config="config/tasks.yaml"
    nlp_tool = NLPAnalysisTool()
    classification_tool = NewsClassificationTool()

    @agent
    def categorizer_agent(self) -> Agent:
            return Agent(
                config=self.agents_config["categorizer_agent"],
                tools=[self.nlp_tool, self.classification_tool],
                verbose=True,
                max_iter=2,
                max_retry_limit=1,
                respect_context_window=True,
            )

    @agent
    def domain_expert(self) -> Agent:
            return Agent(
                config=self.agents_config['domain_expert'], # type: ignore[index]
                verbose=True,
                llm=LLM(model=os.environ["MODEL"]),
                tools=[ScrapeWebsiteTool()],
                max_iter=3 #helps avoiding the online search fails, causing a global crash
            )
        
    @agent
    def left_wing_judge(self) -> Agent:
            return make_judge(self.agents_config['left_wing_judge'])
        
    @agent
    def right_wing_judge(self) -> Agent:
            return make_judge(self.agents_config['right_wing_judge'])

    @agent
    def neutral_judge(self) -> Agent:
            return make_judge(self.agents_config['neutral_judge'])
        
    @agent
    def influenced_judge(self) -> Agent:
            return make_judge(self.agents_config['influenced_judge'])
        
    @agent
    def self_centered_judge(self) -> Agent:
            return make_judge(self.agents_config['self_centered_judge'])
        
    @agent
    def decision_agent(self) -> Agent:
            return Agent(
                config=self.agents_config['decision_agent'], # type: ignore[index]
                verbose=True,
                llm=LLM(model=os.environ["MODEL"]),
                context=[                            
                self.left_wing_verdict_task(),
                self.right_wing_verdict_task(),
                self.neutral_verdict_task(),
                self.influenced_verdict_task(),
                self.self_centered_verdict_task(),
            ],
                allow_delegation=False
            )
        
    @task
    def categorization_task(self) -> Task:
            return Task(config=self.tasks_config["categorization_task"])
    
    @task
    def evaluate_task(self) -> Task:
            return Task(
                config=self.tasks_config['evaluate_task'], # type: ignore[index]
            )
    

    @task
    def left_wing_verdict_task(self) -> Task:
            return Task(
                config=self.tasks_config['left_wing_verdict_task']
            )
        
    @task
    def right_wing_verdict_task(self) -> Task:
            return Task(
                config=self.tasks_config['right_wing_verdict_task']
            )

    @task
    def neutral_verdict_task(self) -> Task:
            return Task(
                config=self.tasks_config['neutral_verdict_task']
            )

    @task
    def influenced_verdict_task(self) -> Task:
            return Task(
                config=self.tasks_config['influenced_verdict_task']
            )

    @task
    def self_centered_verdict_task(self) -> Task:
            return Task(
                config=self.tasks_config['self_centered_verdict_task']
            )
        
    @task
    def decision_task(self) -> Task:
            return Task(
                config=self.tasks_config['decision_task'],
                output_pydantic=FinalVerdictOutput, 
            )

    @crew
    def crew(self) -> Crew:
            """Creates the Fake News Debunking Crew"""

            return Crew(
                agents=self.agents,
                tasks=self.tasks,
                process=Process.sequential,
                max_rpm= 3, #In this way we can handle ratelimit, try to increase at your own risk
                            #UPPER BOUND: 5 (going above burns too much token)
                verbose=True,
            )