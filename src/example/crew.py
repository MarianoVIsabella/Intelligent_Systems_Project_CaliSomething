from crewai import Agent, Crew, Process, Task, LLM
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent
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
class Example():

    agents: list[BaseAgent]
    tasks: list[Task]
    agents_config="config/agents.yaml"

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
    def evaluate_task(self) -> Task:
        return Task(
            config=self.tasks_config['evaluate_task'], # type: ignore[index]
        )
    
    @task
    def right_wing_verdict_task(self) -> Task:
        return Task(
            config=self.tasks_config['right_wing_verdict_task'],
        )
    
    @task
    def left_wing_verdict_task(self) -> Task:
        return Task(
            config=self.tasks_config['left_wing_verdict_task']
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
            config=self.tasks_config['decision_task']
        )

    @crew
    def crew(self) -> Crew:

        return Crew(
            agents=self.agents, # Automatically created by the @agent decorator
            tasks=self.tasks, # Automatically created by the @task decorator
            process=Process.sequential,
            max_rpm= 2, #In this way we can handle ratelimit, try to increase at your own risk
                        #UPPER BOUND: 5 (going above burns too much token)
            verbose=True,
            
        )
