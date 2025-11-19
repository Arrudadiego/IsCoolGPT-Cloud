import os
import requests
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="IsCoolGPT API", version="1.0.0")

# Pega a chave da AWS
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

class MessageInput(BaseModel):
    message: str

@app.get("/")
def read_root():
    return {"status": "online", "message": "IsCoolGPT com Gemini (Modo REST) Ativado!"}

@app.post("/chat")
def chat_endpoint(input_data: MessageInput):
    if not GEMINI_API_KEY:
        return {"error": "Chave da API não configurada no servidor."}
    
    # URL direta da API do Google (Bypassing library errors)
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEMINI_API_KEY}"
    
    headers = {"Content-Type": "application/json"}
    data = {
        "contents": [{
            "parts": [{"text": input_data.message}]
        }]
    }
    
    try:
        # Faz a chamada direta
        response = requests.post(url, headers=headers, json=data)
        
        if response.status_code == 200:
            result = response.json()
            # Garimpa o texto da resposta do JSON do Google
            try:
                answer = result['candidates'][0]['content']['parts'][0]['text']
            except:
                answer = "O Google respondeu mas não entendi o formato. Resposta bruta: " + str(result)
                
            return {
                "response": answer,
                "model_used": "gemini-1.5-flash (Via REST)"
            }
        else:
            # Se der erro, mostra exatamente o que o Google reclamou
            return {
                "error": f"Erro do Google ({response.status_code}): {response.text}"
            }
            
    except Exception as e:
        return {"error": f"Erro interno: {str(e)}"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}