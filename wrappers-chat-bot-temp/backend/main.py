import warnings
warnings.filterwarnings("ignore", category=UserWarning, module="openpyxl")
from fastapi import FastAPI, UploadFile, File, HTTPException
import pandas as pd
import networkx as nx
from openpyxl import load_workbook

app = FastAPI()

@app.post("/upload/")
async def upload_file(file: UploadFile = File(...)):
    try:
        # Load and process the Excel file as a DataFrame
        df = pd.read_excel(file.file, engine='openpyxl', skiprows=5)
        df.columns = ['LD', 'UD', 'NTS', 'Course Title', 'Course #', 'Grade', 'Semester', 'Info']

        # Generate course recommendations categorized by type
        recommendations_by_type = recommend_classes(df)
        
        # Create a structured response for the chatbot
        response_message = "Here are the recommended courses by type for next semester:\n"
        for course_type, courses in recommendations_by_type.items():
            response_message += f"\n{course_type} Courses:\n" + ", ".join(courses)

        return {
            "confirmation": "File received and loaded into the system as a DataFrame.",
            "response": response_message
        }
    except Exception as e:
        # Print detailed error message to console for debugging
        print("Detailed error during file upload:", e)
        raise HTTPException(status_code=500, detail=f"File processing failed: {e}")

def recommend_classes(df):
    # Initialize an empty directed graph
    graph = nx.DiGraph()

    # Assuming the DataFrame has columns 'Course #', 'Course Title', and 'Course Type'
    for _, row in df.iterrows():
        course = row['Course #']
        course_type = row.get('Course Type', 'General')  # Default to 'General' if type not specified

        # Add courses to the graph
        if pd.notna(course):
            graph.add_node(course, course_type=course_type)
    
    # Set of completed courses
    completed_courses = set(['CS 1200', 'CS 1336', 'CS 1136'])  # Update with actual completed courses

    # Perform topological sort and filter out completed courses
    try:
        topologically_sorted_courses = list(nx.topological_sort(graph))
        recommended_courses = [
            (course, graph.nodes[course]['course_type'])  # Include course type in recommendation
            for course in topologically_sorted_courses
            if course not in completed_courses
        ]
    except nx.NetworkXUnfeasible:
        print("Error: Cycle detected in prerequisites")
        return ["Error: Cycle detected in prerequisites"]

    # Group recommended courses by type
    recommendations_by_type = {}
    for course, course_type in recommended_courses[:5]:  # Limit to 5 recommendations or customize as needed
        if course_type not in recommendations_by_type:
            recommendations_by_type[course_type] = []
        recommendations_by_type[course_type].append(course)
        print(f"Recommended {course_type} course: {course}")
    return recommendations_by_type