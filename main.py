import os
from fastapi import FastAPI
from pydantic import BaseModel
from groq import Groq

app = FastAPI(title="IsCoolGPT API", version="1.0.0")

# Pega a chave da AWS
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

class MessageInput(BaseModel):
    message: str

@app.get("/")
def read_root():
    return {"status": "online", "message": "IsCoolGPT rodando com Groq (Llama 3.3)!"}

@app.post("/chat")
def chat_endpoint(input_data: MessageInput):
    if not GROQ_API_KEY:
        return {"error": "ERRO FATAL: A variavel GROQ_API_KEY nao foi encontrada na AWS."}
    
    try:
        # Inicializa o cliente
        client = Groq(api_key=GROQ_API_KEY)
        
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": input_data.message,
                }
            ],
            # MODELO ATUALIZADO AQUI 👇
            model="llama-3.3-70b-versatile",
        )
        
        return {
            "response": chat_completion.choices[0].message.content,
            "model_used": "llama-3.3-70b-versatile (Groq)"
        }
    except Exception as e:
        return {"error": f"Erro na IA: {str(e)}"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}