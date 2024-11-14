from fastapi import FastAPI, UploadFile, File, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
import pandas as pd
import networkx as nx
import re

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Replace "*" with your frontend URL in production for security
    allow_credentials=True,
    allow_methods=["*"],  # This allows all HTTP methods (e.g., POST, GET, OPTIONS)
    allow_headers=["*"],  # This allows all headers
)

# Data model for chat requests
class ChatRequest(BaseModel):
    text: str
    use_wrapper: Optional[bool] = False

# Chat route to handle messages
@app.post("/chat/")
async def chat_endpoint(request: ChatRequest):
    user_message = request.text.lower()
    response_message = "I'm sorry, I don't understand. Could you clarify?"

    # Basic responses for different inputs
    if "hello" in user_message or "hi" in user_message:
        response_message = "Hi there! How can I assist you today?"
    elif "help registering for classes" in user_message:
        response_message = "Okay great! Please send me your ENCS_Degree_Plan.xlsm file."
    elif "thank you" in user_message or "thanks" in user_message:
        response_message = "You're welcome! Let me know if there's anything else I can help with."
    else:
        # Generic response for other inputs
        response_message = "I'm here to help. Could you please provide more details?"

    return {"response": response_message}

# Helper function for recommending classes
def recommend_classes(df):
    # Filter rows to include only those with valid course numbers
    # Assuming course numbers start with "CS" or are numeric (e.g., "CS 4348" or "2413")
    df = df[df['Course #'].apply(lambda x: bool(re.match(r"^(CS\s\d{4}|\d{4})$", str(x))))]

    # Initialize an empty directed graph
    graph = nx.DiGraph()

    # Set of completed courses based on non-null values in the 'Semester' column
    completed_courses = set(df[df['Semester'].notna()]['Course #'])

    # Assuming the DataFrame has columns 'Course #', 'Course Title', and optional 'Course Type'
    for _, row in df.iterrows():
        course = row['Course #']
        course_type = row.get('Course Type', 'General')  # Default to 'General' if type not specified

        # Add courses to the graph
        if pd.notna(course):
            graph.add_node(course, course_type=course_type)

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
        return {"error": "Cycle detected in prerequisites"}

    # Organize recommendations by course type
    recommendations_by_type = {}
    for course, course_type in recommended_courses[:5]:  # Limit to 5 recommendations or customize as needed
        if course_type not in recommendations_by_type:
            recommendations_by_type[course_type] = []
        recommendations_by_type[course_type].append(course)
    
    return recommendations_by_type

# Upload route to handle file uploads
@app.post("/upload/")
async def upload_file(file: UploadFile = File(...)):
    try:
        # Load and process the Excel file as a DataFrame
        df = pd.read_excel(file.file, engine='openpyxl', skiprows=5)
        df.columns = ['LD', 'UD', 'NTS', 'Course Title', 'Course #', 'Grade', 'Semester', 'Info']

        # Generate course recommendations categorized by type
        recommendations_by_type = recommend_classes(df)
        
        # Create a structured response message for the chatbot
        response_message = "Here are the recommended courses by type for next semester:\n\n"
        for course_type, courses in recommendations_by_type.items():
            response_message += f"\n{course_type} Courses:\n" + ", ".join(courses)

        return {
            "confirmation": "File received and loaded into the system as a DataFrame.",
            "response": response_message
        }
    except Exception as e:
        print("Error during file upload:", e)
        raise HTTPException(status_code=500, detail=f"File processing failed: {e}")
