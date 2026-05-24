from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent

# Structured outputs
from models.shared_state import (
    CategorizerOutput,
    ExpertOutput,
    FinalVerdictOutput
)

@CrewBase
class FakeNewsCrew():
    """Fake News Debunking Crew"""

    agents: list[BaseAgent]
    tasks: list[Task]

    # =====================================================
    # AGENTS
    # =====================================================

    @agent
    def categorizer_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['categorizer_agent'],
            verbose=True
        )

    @agent
    def expert_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['expert_agent'],
            verbose=True
        )

    @agent
    def conservative_judge(self) -> Agent:
        return Agent(
            config=self.agents_config['conservative_judge'],
            verbose=True
        )

    @agent
    def skeptical_judge(self) -> Agent:
        return Agent(
            config=self.agents_config['skeptical_judge'],
            verbose=True
        )

    @agent
    def neutral_judge(self) -> Agent:
        return Agent(
            config=self.agents_config['neutral_judge'],
            verbose=True
        )

    # =====================================================
    # TASKS
    # =====================================================

    @task
    def categorization_task(self) -> Task:
        return Task(
            config=self.tasks_config['categorization_task'],
            output_pydantic=CategorizerOutput
        )

    @task
    def expert_analysis_task(self) -> Task:
        return Task(
            config=self.tasks_config['expert_analysis_task'],
            output_pydantic=ExpertOutput
        )

    @task
    def judge_task(self) -> Task:
        return Task(
            config=self.tasks_config['judge_task'],
            output_pydantic=FinalVerdictOutput
        )

    # =====================================================
    # CREW
    # =====================================================

    @crew
    def crew(self) -> Crew:
        """Creates the Fake News Debunking Crew"""

        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True
        )