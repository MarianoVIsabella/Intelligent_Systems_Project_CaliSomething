from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai_tools import SerperDevTool
from example.tools.nlp_tools import NLPAnalysisTool
from example.tools.classification_tool import NewsClassificationTool

@CrewBase
class FakeNewsDetector:
    """Fake News Detector crew"""

    agents_config = "config/agents.yaml"
    tasks_config = "config/tasks.yaml"
    nlp_tool = NLPAnalysisTool()
    classification_tool = NewsClassificationTool()
    search_tool = SerperDevTool()

    @agent
    def interface_agent(self) -> Agent:
        return Agent(
            config=self.agents_config["interface_agent"],
            verbose=True,
            max_iter=2,
            max_retry_limit=1,
            respect_context_window=True,
        )

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
    def domain_expert_agent(self) -> Agent:
        return Agent(
            config=self.agents_config["domain_expert_agent"],
            tools=[self.search_tool],
            verbose=True,
            max_iter=2,
            max_retry_limit=1,
            respect_context_window=True,
        )

    @agent
    def supporting_judge_agent(self) -> Agent:
        return Agent(
            config=self.agents_config["supporting_judge_agent"],
            tools=[self.search_tool],
            verbose=True,
            max_iter=2,
            max_retry_limit=1,
            respect_context_window=True,
        )

    @agent
    def opposing_judge_agent(self) -> Agent:
        return Agent(
            config=self.agents_config["opposing_judge_agent"],
            tools=[self.search_tool],
            verbose=True,
            max_iter=2,
            max_retry_limit=1,
            respect_context_window=True,
        )

    @agent
    def neutral_judge_agent(self) -> Agent:
        return Agent(
            config=self.agents_config["neutral_judge_agent"],
            tools=[self.search_tool],
            verbose=True,
            max_iter=2,
            max_retry_limit=1,
            respect_context_window=True,
        )

    @agent
    def verdict_agent(self) -> Agent:
        return Agent(
            config=self.agents_config["verdict_agent"],
            verbose=True,
            max_iter=2,
            max_retry_limit=1,
            respect_context_window=True,
        )

    @task
    def interface_task(self) -> Task:
        return Task(config=self.tasks_config["interface_task"])

    @task
    def categorization_task(self) -> Task:
        return Task(config=self.tasks_config["categorization_task"])

    @task
    def domain_expert_task(self) -> Task:
        return Task(config=self.tasks_config["domain_expert_task"])

    @task
    def supporting_judge_task(self) -> Task:
        return Task(config=self.tasks_config["supporting_judge_task"])

    @task
    def opposing_judge_task(self) -> Task:
        return Task(config=self.tasks_config["opposing_judge_task"])

    @task
    def neutral_judge_task(self) -> Task:
        return Task(config=self.tasks_config["neutral_judge_task"])

    @task
    def verdict_task(self) -> Task:
        return Task(config=self.tasks_config["verdict_task"])

    @crew
    def crew(self) -> Crew:
        """Creates the Fake News Detector crew"""
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
         #    max_rpm=4,
        )
    