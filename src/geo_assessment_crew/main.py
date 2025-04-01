#!/usr/bin/env python
import os
from crew import GeoAssessmentCrew

def run():
    """
    Run the Geotechnical Assessment crew.
    """
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
    # Assuming the output_file in tasks.yaml specifies 'output/...'
    if not os.path.exists('output'):
        os.makedirs('output')

    # Instantiate and run the crew
    # The .crew() method accesses the crew defined by the @crew decorator
    result = GeoAssessmentCrew().crew().kickoff(inputs=inputs)

    print("\n\n########################")
    print("## Crew Execution Finished")
    print("########################\n")
    print("Final Crew Result:")
    # The final result depends on the last task's output configuration.
    # If the last task writes to a file, the result might be the content or confirmation.
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
            print(f"\nError: Report file '{report_file}' was not created, and result object does not appear to be the report content.")
            print("Result object:", result)


if __name__ == "__main__":
    run()