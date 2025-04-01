#!/usr/bin/env python
import os
import sys
from dotenv import load_dotenv
from crew import GeoAssessmentCrew

# Load environment variables from .env file
load_dotenv()

def run():
    """
    Run the Geotechnical Assessment crew.
    """
    # Check for OpenAI API key
    if not os.environ.get("OPENAI_API_KEY"):
        print("Error: OPENAI_API_KEY environment variable not set.")
        print("Please ensure you have a .env file with your API key or set it in your environment.")
        sys.exit(1)
        
    # Define inputs for the kickoff
    project_brief_input = """
    Project: New Warehouse Construction
    Location: Industrial Zone North, Trondheim, Norway
    Structure Type: Single-story warehouse, concrete slab-on-grade.
    Estimated Foundation Loads: Column loads approx 500 kN. Wall loads approx 50 kN/m.
    """
    # Simple representation of site data for demo purposes
    site_data_input = """
    Borehole BH-01 Log Summary:
    Layer 1: 0.0m - 2.0m depth; Fill Material (Sand & Gravel mix); Avg N-value=8
    Layer 2: 2.0m - 7.5m depth; Medium Dense Sand; Avg N-value=20; Est. Friction Angle=32 deg
    Layer 3: 7.5m - 15.0m depth; Stiff Clay; Avg Su=70 kPa; N > 30
    Groundwater observed at 3.0m depth.
    """

    inputs = {
        'project_brief': project_brief_input,
        'site_data_summary': site_data_input
        # Add more inputs here if your agents/tasks use different variables
    }

    # Create the output directory if it doesn't exist
    try:
        if not os.path.exists('output'):
            os.makedirs('output')
            print("Created output directory.")
    except Exception as e:
        print(f"Error creating output directory: {e}")
        sys.exit(1)

    # Instantiate and run the crew
    try:
        print("Starting GeoAssessmentCrew execution...")
        result = GeoAssessmentCrew().crew().kickoff(inputs=inputs)

        print("\n\n########################")
        print("## Crew Execution Finished")
        print("########################\n")
        print("Final Crew Result:")
        print(result)

        # Confirm the output file was created based on the task definition
        report_file = 'output/preliminary_geo_report.md' # Matches output_file in tasks.yaml
        if os.path.exists(report_file):
            print(f"\nReport successfully saved to: {report_file}")
        else:
            # If the result contains the markdown, print it directly
            if isinstance(result, str) and result.startswith("#"): # Basic check for markdown
                 print("\n--- Final Report Content (from result) ---")
                 print(result)
                 print("----------------------------------------")
            else:
                print(f"\nWarning: Report file '{report_file}' was not created, and result object does not appear to be the report content.")
                print("Result object:", result)
    except Exception as e:
        print(f"Error during crew execution: {e}")
        sys.exit(1)


if __name__ == "__main__":
    run()