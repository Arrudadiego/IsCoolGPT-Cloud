import os
import requests
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="IsCoolGPT API", version="1.0.0")

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

class MessageInput(BaseModel):
    message: str

@app.get("/")
def read_root():
    return {"status": "online", "message": "IsCoolGPT com Gemini Pro (Stable) Ativado!"}

@app.post("/chat")
def chat_endpoint(input_data: MessageInput):
    if not GEMINI_API_KEY:
        return {"error": "Chave da API não configurada no servidor."}
    
    # MUDANÇA AQUI: Usando 'gemini-pro' que é o modelo mais estável
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key={GEMINI_API_KEY}"
    
    headers = {"Content-Type": "application/json"}
    data = {
        "contents": [{
            "parts": [{"text": input_data.message}]
        }]
    }
    
    try:
        response = requests.post(url, headers=headers, json=data)
        
        if response.status_code == 200:
            result = response.json()
            try:
                answer = result['candidates'][0]['content']['parts'][0]['text']
            except:
                answer = "Resposta recebida mas formato inesperado: " + str(result)
                
            return {
                "response": answer,
                "model_used": "gemini-pro (Stable)"
            }
        else:
            return {
                "error": f"Erro do Google ({response.status_code}): {response.text}"
            }
            
    except Exception as e:
        return {"error": f"Erro interno: {str(e)}"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}