***

# IsCoolGPT: Assistente de Estudos em Cloud

**Autor:** Diego Arruda  
**Projeto:** Projeto Final Cloud 25.2

---

## 1. Visão Geral

O **IsCoolGPT** é um assistente educacional inteligente focado em Cloud Computing, DevOps e desenvolvimento de software.  
A solução foi implementada como uma API RESTful de alta performance, utilizando **Python com FastAPI** em uma arquitetura serverless moderna na AWS, com pipeline de CI/CD totalmente automatizado.

- A API se conecta à plataforma **Groq** (utilizando o modelo **Llama 3.3**) para gerar respostas em tempo real com baixíssima latência, garantindo uma experiência fluida para os estudantes.

---

## 2. Diagrama de Arquitetura do Sistema

### Fluxo do Usuário (Aplicação)

```mermaid
flowchart LR
    A[Estudante] -->|1. JSON POST /chat| B[API FastAPI - ECS Fargate]
    B -->|2. Prompt| C[Groq API - Llama 3_3]
    C -->|3. Resposta Gerada| B
    B -->|4. Resposta JSON| A

    subgraph Infraestrutura AWS
        B
        D[ECR - Registro de Imagens]
        E[CloudWatch Logs]
    end

    B --> E
```

## Fluxo de DevOps (CI/CD)

```mermaid
flowchart TD
    A[Desenvolvedor] -->|1. git push master| B[GitHub Repositorio]
    B -->|2. Aciona Pipeline| C[GitHub Actions CI/CD]
    C -->|3. Roda Testes Python| D[Testes Automatizados]
    C -->|4. Build e Push da Imagem| E[AWS ECR]
    C -->|5. Atualiza Servico ECS| F[AWS ECS Deploy]
    F -->|6. Puxa Imagem| E
    F -->|7. Roda Nova Task| G[AWS Fargate]
    G -->|8. Envia Logs| H[CloudWatch Logs]
```


## 3. Stack de Tecnologias e Decisões
| Componente         | Tecnologia Escolhida      | Justificativa                                                                                                       |
| ------------------ | ------------------------- | ------------------------------------------------------------------------------------------------------------------- |
| Backend (API)      | Python 3.10 + FastAPI          | Framework moderno, assíncrono e de alta performance, ideal para microsserviços de IA                                     |
| LLM (IA)           | Groq API – Llama 3.3      | Utilização de inferência ultra-rápida com modelos Open Source de ponta (Llama 3), sem custo de licença.                      |
| Containerização    | Docker                    | Portabilidade e consistência do ambiente da aplicação via Dockerfile otimizado (Multi-stage).                                                              |                                                                  |
| CI/CD              | GitHub Actions            | Pipeline automatizado que executa testes (Pytest) e deploy contínuo na AWS a cada push na main.                                   |
| Registro de Imagem | AWS ECR                   | Armazenamento seguro e privado das imagens Docker, integrado nativamente ao ECS.                                                                   |
| Orquestração       | AWS ECS + Fargate         | Gerenciamento de containers serverless, eliminando a necessidade de administrar instâncias EC2.                                                             |
| Segurança          | IAM & Security Groups    | Controle de acesso rigoroso (Least Privilege) e restrição de tráfego de rede (Apenas porta 8000). |                                       |
| Documentação       | Swagger UI (OpenAPI)    | Documentação automática e interativa disponível nativamente no FastAPI (`/docs`).                                                            |
| Testes       | Pytest | Suite de testes automatizados para garantir a integridade dos endpoints antes do deploy.                                                      |


## 4. Como Executar Localmente (Docker)

Pré-requisitos:

* Ter o Docker instalado.
* Possuir uma chave de API da Groq.

### 4.1 Construir a Imagem Docker
No diretório raiz do projeto:
```
docker build -t iscoolgpt:local .
```
### 4.2 Executar o Contêiner
``` docker run -p 8000:8000 \
    -e GROQ_API_KEY="SUA_CHAVE_AQUI" \
    iscoolgpt:local
```

## 5. Como Usar a API (Endpoints)
Endpoint principal

* POST /chat

Aceita um JSON com a pergunta do usuário e retorna a resposta gerada pela LLM Llama 3.3 via Groq.

Exemplo de chamada (cURL):

``` curl -X POST http://localhost:8000/chat \
     -H "Content-Type: application/json" \
     -d '{"message": "Explique o que é AWS Fargate"}'
```

**Endpoints Adicionais**

* **Health Check:** ``GET /health``

Verifica se a API está online (usado pelo Load Balancer/ECS).

* **Documentação Interativa (Swagger):** Acesse no navegador: ``http://localhost:8000/docs``

***