from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import os

app = FastAPI(title="IsCoolGPT API", version="1.0.0")

# Modelo de entrada de dados para garantir validação
class MessageInput(BaseModel):
    message: str
    model: str = "default-model"

@app.get("/")
def read_root():
    return {"status": "online", "message": "IsCoolGPT Backend is running!"}

@app.post("/chat")
def chat_endpoint(input_data: MessageInput):
    # AQUI entra a lógica do seu LLM depois (OpenAI, HuggingFace, etc)
    # Por enquanto, vamos retornar um eco para validar o deploy
    return {
        "response": f"Você disse: '{input_data.message}'. (LLM Placeholder)",
        "model_used": input_data.model
    }

@app.get("/health")
def health_check():
    # Importante para o Load Balancer da AWS saber se o container está vivo
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)