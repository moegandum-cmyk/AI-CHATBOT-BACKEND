from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import openai
import os

app = FastAPI()

openai.api_key = os.getenv("OPENAI_API_KEY")

# ✅ Allow all origins for now (quick test)
# Later, replace ["*"] with your Netlify URL for security
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Message(BaseModel):
    text: str

@app.get("/")
async def root():
    return {"message": "Server is running!"}

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
