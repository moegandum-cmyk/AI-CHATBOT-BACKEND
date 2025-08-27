from fastapi import FastAPI
from pydantic import BaseModel
import openai
import os

# Initialize FastAPI
app = FastAPI()

# Load OpenAI API key from environment
openai.api_key = os.getenv("OPENAI_API_KEY")

# Request body model
class Message(BaseModel):
    text: str

# ✅ Root route (so Render URL shows something instead of "Not Found")
@app.get("/")
async def root():
    return {"message": "Server is running!"}

# ✅ Chatbot route
@app.post("/chat")
async def chat(message: Message):
    try:
        client = openai.OpenAI(api_key=openai.api_key)
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": message.text}]
        )
        reply = response.choices[0].message.content
        return {"reply": reply}

    except Exception as e:
        return {"error": str(e)}
