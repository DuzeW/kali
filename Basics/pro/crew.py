from crewai import Agent, Crew, Process, Task, LLM
from crewai.project import CrewBase, agent, crew, task
import os
from tools.WeatherTool import WeatherTool
from dotenv import load_dotenv
from metryki import MetricsLogger
import time

load_dotenv()

@CrewBase
class TravelingCrew():
    """Creating crew for traveling"""

    def __init__(self, model_name="gpt-4o-mini") -> None:
        self.openai_llm = LLM(
            api_key=os.getenv("OPENAI_KEY"),
            model=model_name,
        )
        self.metrics_logger = MetricsLogger()

    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'

    def _log_metrics(self, task_name, agent_name, model_name, start_time, result, success, error_count):
        response_size = len(str(result)) if success else 0
        execution_time = time.time() - start_time

        self.metrics_logger.log(
            task=task_name,
            agent=agent_name,
            model=model_name,
            response_time=execution_time,
            success=success,
            response_size=response_size,
            error_count=error_count,
            details=result
        )

    @agent
    def weather_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['weather_agent'],
            llm=self.openai_llm,
            tools=[WeatherTool()],
        )

    @task
    def weather_task(self) -> Task:
        start_time = time.time()
        model_name = self.openai_llm.model
        try:
            result = Task(
                config=self.tasks_config['weather_task'],
                agent=self.weather_agent(),
            )
            success = True
            error_count = 0
        except Exception as e:
            result = str(e)
            success = False
            error_count = 1
        self._log_metrics("Weather Task", "Weather Agent", model_name, start_time, result, success, error_count)
        return result

    @agent
    def attractions_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['attractions_agent'],
            llm=self.openai_llm,
        )

    @task
    def attractions_task(self) -> Task:
        start_time = time.time()
        model_name = self.openai_llm.model
        try:
            result = Task(
                config=self.tasks_config['attractions_task'],
                agent=self.attractions_agent(),
            )
            success = True
            error_count = 0
        except Exception as e:
            result = str(e)
            success = False
            error_count = 1
        self._log_metrics("Attractions Task", "Attractions Agent", model_name, start_time, result, success, error_count)
        return result

    @agent
    def accommodation_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['accommodation_agent'],
            llm=self.openai_llm,
        )

    @task
    def accommodation_task(self) -> Task:
        start_time = time.time()
        model_name = self.openai_llm.model
        try:
            result = Task(
                config=self.tasks_config['accommodation_task'],
                agent=self.accommodation_agent(),
            )
            success = True
            error_count = 0
        except Exception as e:
            result = str(e)
            success = False
            error_count = 1
        self._log_metrics("Accommodation Task", "Accommodation Agent", model_name, start_time, result, success, error_count)
        return result

    @agent
    def transport_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['transport_agent'],
            llm=self.openai_llm,
        )

    @task
    def transport_task(self) -> Task:
        start_time = time.time()
        model_name = self.openai_llm.model
        try:
            result = Task(
                config=self.tasks_config['transport_task'],
                agent=self.transport_agent(),
            )
            success = True
            error_count = 0
        except Exception as e:
            result = str(e)
            success = False
            error_count = 1
        self._log_metrics("Transport Task", "Transport Agent", model_name, start_time, result, success, error_count)
        return result

    @agent
    def summarizer_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['summarizer_agent'],
            llm=self.openai_llm,
        )

    @task
    def summarizer_task(self) -> Task:
        start_time = time.time()
        model_name = self.openai_llm.model
        try:
            result = Task(
                config=self.tasks_config['summarizer_task'],
                agent=self.summarizer_agent(),
            )
            success = True
            error_count = 0
        except Exception as e:
            result = str(e)
            success = False
            error_count = 1
        self._log_metrics("Summarizer Task", "Summarizer Agent", model_name, start_time, result, success, error_count)
        return result

    @agent
    def translator_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['translator_agent'],
            llm=self.openai_llm,
        )

    @task
    def translator_task(self) -> Task:
        start_time = time.time()
        model_name = self.openai_llm.model
        try:
            result = Task(
                config=self.tasks_config['translator_task'],
                agent=self.translator_agent(),
            )
            success = True
            error_count = 0
        except Exception as e:
            result = str(e)
            success = False
            error_count = 1
        self._log_metrics("Translator Task", "Translator Agent", model_name, start_time, result, success, error_count)
        return result

    @crew
    def crew(self) -> Crew:
        """Creates the traveling crew"""
        return Crew(
            agents=[
                self.weather_agent(),
                self.attractions_agent(),
                self.accommodation_agent(),
                self.transport_agent(),
                self.summarizer_agent(),
                self.translator_agent()
            ],
            tasks=[
                self.weather_task(),
                self.attractions_task(),
                self.accommodation_task(),
                self.transport_task(),
                self.summarizer_task(),
                self.translator_task()
            ],
            process=Process.sequential,
            verbose=True
        )
