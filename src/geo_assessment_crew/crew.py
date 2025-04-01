from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
# from crewai_tools import SerperDevTool, FileReadTool # Import tools if needed

# Uncomment the following line to use Ollama integration
# from langchain_community.llms import Ollama
# ollama_llm = Ollama(model="openhermes")

# Uncomment the following line to use Groq integration
# from langchain_groq import ChatGroq
# groq_llm = ChatGroq(temperature=0, model_name="mixtral-8x7b-32768")

# To use a specific OpenAI model, either set OPENAI_MODEL_NAME environment variable or use langchain_openai
# from langchain_openai import ChatOpenAI
# openai_llm = ChatOpenAI(model="gpt-4o") # Example for explicit GPT-4o

@CrewBase
class GeoAssessmentCrew():
    """GeoAssessmentCrew using configuration files"""
    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'

    # If you don't want to use YAML, comment out the lines above
    # and define agents/tasks directly in the methods below.

    @agent
    def project_brief_analyst(self) -> Agent:
        return Agent(
            config=self.agents_config['project_brief_analyst'], # Loads from YAML
            # llm=openai_llm # Uncomment to use explicitly defined LLM
            # tools=[tool1, tool2] # Add tools if needed
            verbose=True
        )

    @agent
    def geotechnical_data_reviewer(self) -> Agent:
        return Agent(
            config=self.agents_config['geotechnical_data_reviewer'], # Loads from YAML
            # llm=openai_llm
            # tools=[FileReadTool(file_path='/path/to/your/data.csv')] # Example tool usage
            verbose=True
        )

    @agent
    def junior_geotechnical_engineer(self) -> Agent:
        return Agent(
            config=self.agents_config['junior_geotechnical_engineer'], # Loads from YAML
            # llm=openai_llm
            # tools=[CodeInterpreterTool()] # Or a custom calculation tool
            verbose=True
        )

    @agent
    def technical_report_summarizer(self) -> Agent:
        return Agent(
            config=self.agents_config['technical_report_summarizer'], # Loads from YAML
            # llm=openai_llm
            verbose=True
        )

    # --- Tasks ---
    # Tasks load their configuration from tasks.yaml based on the method name
    # The agent for each task is specified within tasks.yaml

    @task
    def extract_requirements_task(self) -> Task:
        return Task(
            config=self.tasks_config['extract_requirements_task'],
            # agent=self.project_brief_analyst() # Agent is defined in YAML
        )

    @task
    def review_data_task(self) -> Task:
        return Task(
            config=self.tasks_config['review_data_task'],
            # agent=self.geotechnical_data_reviewer(), # Agent is defined in YAML
            # context=[self.extract_requirements_task()] # Context defined in YAML
        )

    @task
    def bearing_capacity_task(self) -> Task:
        return Task(
            config=self.tasks_config['bearing_capacity_task'],
            # agent=self.junior_geotechnical_engineer(), # Agent is defined in YAML
            # context=[...] # Context defined in YAML
        )

    @task
    def reporting_task(self) -> Task:
        return Task(
            config=self.tasks_config['reporting_task'],
            # agent=self.technical_report_summarizer(), # Agent is defined in YAML
            # context=[...] # Context defined in YAML
            # output_file defined in YAML
        )

    @crew
    def crew(self) -> Crew:
        """Creates the GeoAssessmentCrew"""
        return Crew(
            agents=self.agents,  # Agents are assigned automatically by the @agent decorator
            tasks=self.tasks,    # Tasks are assigned automatically by the @task decorator
            process=Process.sequential,
            verbose=2,
            # memory=True # Can enable memory for more complex workflows
            # manager_llm=openai_llm # Can specify a manager LLM for hierarchical processes
        )