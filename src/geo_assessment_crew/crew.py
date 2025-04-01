from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task

@CrewBase
class GeoAssessmentCrew():
    """GeoAssessmentCrew using configuration files"""
    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'

    @agent
    def project_brief_analyst(self) -> Agent:
        return Agent(
            config=self.agents_config['project_brief_analyst'],
            verbose=True
        )

    @agent
    def geotechnical_data_reviewer(self) -> Agent:
        return Agent(
            config=self.agents_config['geotechnical_data_reviewer'],
            verbose=True
        )

    @agent
    def junior_geotechnical_engineer(self) -> Agent:
        return Agent(
            config=self.agents_config['junior_geotechnical_engineer'],
            verbose=True
        )

    @agent
    def technical_report_summarizer(self) -> Agent:
        return Agent(
            config=self.agents_config['technical_report_summarizer'],
            verbose=True
        )

    @task
    def extract_requirements_task(self) -> Task:
        return Task(
            config=self.tasks_config['extract_requirements_task'],
        )

    @task
    def review_data_task(self) -> Task:
        return Task(
            config=self.tasks_config['review_data_task'],
        )

    @task
    def bearing_capacity_task(self) -> Task:
        return Task(
            config=self.tasks_config['bearing_capacity_task'],
        )

    @task
    def reporting_task(self) -> Task:
        return Task(
            config=self.tasks_config['reporting_task'],
        )

    @crew
    def crew(self) -> Crew:
        """Creates the GeoAssessmentCrew"""
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
            telemetry=False  # Changed from config={"telemetry": False} to direct parameter
        )