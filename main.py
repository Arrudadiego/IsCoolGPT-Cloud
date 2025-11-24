import os
from fastapi import FastAPI
from pydantic import BaseModel
from groq import Groq

app = FastAPI(title="IsCoolGPT API", version="1.0.0")

# Pega a chave da AWS
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# Configura o cliente da Groq
if GROQ_API_KEY:
    client = Groq(api_key=GROQ_API_KEY)
else:
    client = None

class MessageInput(BaseModel):
    message: str

@app.get("/")
def read_root():
    return {"status": "online", "message": "IsCoolGPT rodando com Groq (Llama 3)!"}

@app.post("/chat")
def chat_endpoint(input_data: MessageInput):
    if not client:
        return {"error": "Chave da GROQ_API_KEY não configurada no servidor."}
    
    try:
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": input_data.message,
                }
            ],
            model="llama3-8b-8192", # Modelo muito rápido e free
        )
        
        return {
            "response": chat_completion.choices[0].message.content,
            "model_used": "llama3-8b-8192 (Groq)"
        }
    except Exception as e:
        return {"error": str(e)}

@app.get("/health")
def health_check():
    return {"status": "healthy"}