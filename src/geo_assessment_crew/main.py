#!/usr/bin/env python
import os
import sys
import argparse
from dotenv import load_dotenv
from crew import GeoAssessmentCrew
from crewai_tools import FileReadTool

# Load environment variables from .env file
load_dotenv()

def read_from_file(file_path):
    """Read content from a file using CrewAI's FileReadTool"""
    file_tool = FileReadTool()
    if not os.path.exists(file_path):
        print(f"Error: File '{file_path}' not found.")
        return None
    
    try:
        content = file_tool.read_file(file_path)
        return content
    except Exception as e:
        print(f"Error reading file '{file_path}': {e}")
        return None

def get_user_input(prompt_text, default_text=None):
    """Get input from user with an option to use default text"""
    if default_text:
        print(f"\n{prompt_text}")
        print(f"Default: \n{default_text}")
        use_default = input("Use default? (y/n): ").lower() == 'y'
        if use_default:
            return default_text
    
    print(f"\n{prompt_text}")
    print("Enter your text (type 'END' on a new line when finished):")
    lines = []
    while True:
        line = input()
        if line.strip() == 'END':
            break
        lines.append(line)
    return "\n".join(lines)

def run():
    """
    Run the Geotechnical Assessment crew with interactive or file-based inputs.
    """
    # Check for OpenAI API key
    if not os.environ.get("OPENAI_API_KEY"):
        print("Error: OPENAI_API_KEY environment variable not set.")
        print("Please ensure you have a .env file with your API key or set it in your environment.")
        sys.exit(1)
    
    # Set up argument parser
    parser = argparse.ArgumentParser(description='Run GeoAssessmentCrew with custom inputs')
    parser.add_argument('--brief', type=str, help='Path to project brief file')
    parser.add_argument('--site-data', type=str, help='Path to site data file')
    parser.add_argument('--interactive', action='store_true', help='Run in interactive mode')
    args = parser.parse_args()
    
    # Default inputs that will be used if no files or interactive inputs are provided
    default_project_brief = """
    Project: New Warehouse Construction
    Location: Industrial Zone North, Trondheim, Norway
    Structure Type: Single-story warehouse, concrete slab-on-grade.
    Estimated Foundation Loads: Column loads approx 500 kN. Wall loads approx 50 kN/m.
    """
    
    default_site_data = """
    Borehole BH-01 Log Summary:
    Layer 1: 0.0m - 2.0m depth; Fill Material (Sand & Gravel mix); Avg N-value=8
    Layer 2: 2.0m - 7.5m depth; Medium Dense Sand; Avg N-value=20; Est. Friction Angle=32 deg
    Layer 3: 7.5m - 15.0m depth; Stiff Clay; Avg Su=70 kPa; N > 30
    Groundwater observed at 3.0m depth.
    """
    
    # Initialize inputs with defaults
    project_brief_input = default_project_brief
    site_data_input = default_site_data
    
    # Handle input mode selection
    if (args.interactive):
        print("\n=== Interactive Mode ===")
        print("You'll be prompted to enter the project brief and site data.")
        
        project_brief_input = get_user_input(
            "Enter PROJECT BRIEF information:", 
            default_project_brief
        )
        
        site_data_input = get_user_input(
            "Enter SITE DATA information:", 
            default_site_data
        )
    
    # File inputs override interactive inputs if provided
    if args.brief:
        file_content = read_from_file(args.brief)
        if file_content:
            project_brief_input = file_content
            print(f"Successfully loaded project brief from {args.brief}")
    
    if args.site_data:
        file_content = read_from_file(args.site_data)
        if file_content:
            site_data_input = file_content
            print(f"Successfully loaded site data from {args.site_data}")
    
    # Create inputs dictionary
    inputs = {
        'project_brief': project_brief_input,
        'site_data_summary': site_data_input
    }
    
    # Create the output directory if it doesn't exist
    try:
        if not os.path.exists('output'):
            os.makedirs('output')
            print("Created output directory.")
    except Exception as e:
        print(f"Error creating output directory: {e}")
        sys.exit(1)

    # Show what inputs are being used
    print("\n=== Using the following inputs ===")
    print("\nPROJECT BRIEF:")
    print(project_brief_input)
    print("\nSITE DATA:")
    print(site_data_input)
    proceed = input("\nProceed with analysis? (y/n): ").lower()
    if proceed != 'y':
        print("Analysis cancelled by user.")
        sys.exit(0)

    # Instantiate and run the crew
    try:
        print("\nStarting GeoAssessmentCrew execution...")
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
            
            # Offer to display the report content
            show_report = input("Display report content? (y/n): ").lower() == 'y'
            if show_report:
                print("\n--- Report Content ---")
                report_content = read_from_file(report_file)
                if report_content:
                    print(report_content)
                print("----------------------")
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