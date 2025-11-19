# Etapa 1: Builder (instala dependências)
FROM python:3.10-slim as builder

WORKDIR /app

COPY requirements.txt .
RUN pip install --user --no-cache-dir -r requirements.txt

# Etapa 2: Runtime (imagem final leve)
FROM python:3.10-slim

WORKDIR /app

# Copia apenas as dependências instaladas da etapa anterior
COPY --from=builder /root/.local /root/.local
COPY . .

# Garante que os scripts instalados estão no PATH
ENV PATH=/root/.local/bin:$PATH

# Expõe a porta que o FastAPI usa
EXPOSE 8000

# Comando para rodar a aplicação
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]