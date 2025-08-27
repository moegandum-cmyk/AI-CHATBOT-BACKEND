from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import openai
import os

# Load API key
openai.api_key = os.getenv("OPENAI_API_KEY")

app = FastAPI()

# ✅ Allow frontend to connect (Netlify + local dev)
origins = [
    "http://localhost:5500",   # if testing locally
    "https://jade-selkie-2bfdf0.netlify.app",  # replace with your Netlify domain
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Message(BaseModel):
    text: str

@app.post("/chat")
async def chat(message: Message):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": message.text}]
        )
        reply = response["choices"][0]["message"]["content"]
        return {"reply": reply}
    except Exception as e:
        return {"error": str(e)}
