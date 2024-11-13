from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from model_no_wrappers import chatbot_response_no_wrapper
from model_with_wrappers import chatbot_response_with_wrapper
import pandas as pd
import networkx as nx

app = FastAPI()

# CORS setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Or specify "http://localhost:3000" if that's where your frontend is
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Message(BaseModel):
    text: str
    use_wrapper: bool = False

@app.post("/chat/")
async def chat(message: Message):
    try:
        if message.use_wrapper:
            response = chatbot_response_with_wrapper(message.text)
        else:
            response = chatbot_response_no_wrapper(message.text)
        return {"response": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/upload/")
async def upload_file(file: UploadFile = File(...)):
    try:
        # Load the uploaded Excel file as a DataFrame
        df = pd.read_excel(file.file, engine='openpyxl')
        confirmation_message = "File received and loaded into the system as a DataFrame."

        # Generate class recommendations
        recommended_classes = recommend_classes(df)
        
        return {
            "confirmation": confirmation_message,
            "recommended_classes": recommended_classes
        }
    except Exception as e:
        print("Error during file upload:", e)  # Log the error for debugging
        raise HTTPException(status_code=500, detail=str(e))

def recommend_classes(df):
    # Example class recommendation logic
    # Assuming the DataFrame has 'Course' and 'Prerequisite' columns
    graph = nx.DiGraph()
    
    for _, row in df.iterrows():
        course = row.get('Course')
        prerequisite = row.get('Prerequisite')
        if pd.notna(prerequisite):  # Add edge only if there's a prerequisite
            graph.add_edge(prerequisite, course)
        else:
            graph.add_node(course)
    
    # Example completed courses (replace with actual logic)
    completed_courses = set(['Course1', 'Course2', 'Course3'])
    
    # Topological sort for recommendations
    topologically_sorted_courses = list(nx.topological_sort(graph))
    recommended_courses = [
        course for course in topologically_sorted_courses if course not in completed_courses
    ][:5]  # Limit recommendations to 5
    
    return recommended_courses