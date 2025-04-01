# Geotech AI Assessment Agents (using CrewAI)

This project demonstrates a multi-agent system built with [CrewAI](https://crewai.com/) to perform a preliminary geotechnical site assessment. The crew consists of specialized AI agents (powered by OpenAI's GPT-4o) that collaborate sequentially to:

1.  Analyze project requirements.
2.  Review summarized site investigation data.
3.  Perform a basic bearing capacity estimation.
4.  Compile the findings into a summary report.

This serves as a basic example of applying AI agent collaboration to a typical geotechnical engineering workflow.

## Features

* **Role-Based Agents:** Clearly defined roles for requirements analysis, data review, engineering calculation, and reporting.
* **Sequential Workflow:** Tasks are executed in a logical order using CrewAI's sequential process.
* **Configuration Driven:** Agents and Tasks are defined in YAML files (`config/agents.yaml`, `config/tasks.yaml`) for easy modification.
* **OpenAI Integration:** Uses GPT-4o for agent intelligence (requires an API key).
* **Markdown Reporting:** Generates a final summary report in Markdown format.

## Project Structure

* `geotech_ai_agents/`
    * `- .env`
    * `- pyproject.toml`
    * `- README.md`
    * `- src/`
        * `- geo_assessment_crew/`
            * `- __init__.py`
            * `- main.py`
            * `- crew.py`
            * `- config/`
                * `- __init__.py`
                * `- agents.yaml`
                * `- tasks.yaml`

## Prerequisites

* Python 3.10+
* Poetry (recommended for dependency management) or pip
* OpenAI API Key

## Setup

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/yaredwb/geotech_ai_agents.git
    cd geotech_ai_agents
    ```

2.  **Create a virtual environment (recommended):**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3.  **Install dependencies:**
    * **Using Poetry:**
        ```bash
        pip install poetry # If you don't have it already
        poetry install
        ```
    * **Using pip:**
        ```bash
        pip install -r requirements.txt # (If you generate one)
        # Or manually:
        # pip install crewai crewai-tools langchain-openai python-dotenv
        ```

4.  **Set up Environment Variables:**
    Create a file named `.env` in the project root directory (`geotech_ai_agents/.env`). Add your OpenAI API key to this file:
    ```plaintext
    OPENAI_API_KEY=sk-YOUR_OPENAI_API_KEY_HERE
    # You can optionally specify the model, though it's also set in agents.yaml
    # OPENAI_MODEL_NAME=gpt-4o
    ```
    Replace `sk-YOUR_OPENAI_API_KEY_HERE` with your actual key.

## Running the Crew

Ensure your virtual environment is activated. Run the main script from the project root directory:

```bash
python src/geo_assessment_crew/main.py
