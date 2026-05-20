from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent
from crewai_tools import ScrapeWebsiteTool
# If you want to run a snippet of code before or after the crew starts,
# you can use the @before_kickoff and @after_kickoff decorators
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
            reasoning=True,
            max_reasoning_attempts=3,
            tools=[ScrapeWebsiteTool()]
        )
    
    @task
    def evaluate_task(self) -> Task:
        return Task(
            config=self.tasks_config['evaluate_task'], # type: ignore[index]
        )

    @crew
    def crew(self) -> Crew:

        return Crew(
            agents=self.agents, # Automatically created by the @agent decorator
            tasks=self.tasks, # Automatically created by the @task decorator
            process=Process.sequential,
            verbose=True,
            
        )
