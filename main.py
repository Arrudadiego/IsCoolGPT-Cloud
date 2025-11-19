import os
import google.generativeai as genai
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="IsCoolGPT API", version="1.0.0")

# Pega a chave da AWS
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Configura o Gemini
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)
    model = genai.GenerativeModel('gemini-pro')
else:
    model = None

class MessageInput(BaseModel):
    message: str

@app.get("/")
def read_root():
    return {"status": "online", "message": "IsCoolGPT com Gemini AI Ativado!"}

@app.post("/chat")
def chat_endpoint(input_data: MessageInput):
    if not model:
        return {"error": "Chave da API não configurada no servidor."}
    
    try:
        response = model.generate_content(input_data.message)
        return {
            "response": response.text,
            "model_used": "gemini-pro"
        }
    except Exception as e:
        return {"error": str(e)}

@app.get("/health")
def health_check():
    return {"status": "healthy"}