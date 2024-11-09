from fastapi import FastAPI, HTTPException
from model_no_wrapper import chatbot_response_no_wrapper
from model_with_wrapper import chatbot_response_with_wrapper
from pydantic import BaseModel

app = FastAPI()

class Message(BaseModel):
    text: str
    use_wrapper: bool = False  # Specify which model to use

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
