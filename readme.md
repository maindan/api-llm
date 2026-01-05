# API LLM - Processamento de Comprovantes via WhatsApp

API desenvolvida em **FastAPI** para receber mensagens do WhatsApp, processar arquivos PDF ou imagens de comprovantes de pagamento, extrair dados usando OCR e IA, e registrar pagamentos em um banco de dados PostgreSQL.
## Funcionalidades

- Receber mensagens do WhatsApp via webhook.
- Processar arquivos PDF e imagens (JPEG/PNG) enviados.
- Extrair texto de comprovantes utilizando OCR (`pytesseract` e `pdfplumber`).
- Analisar e validar informações de pagamento usando IA (`ai_service`).
- Registrar pagamentos em banco PostgreSQL.
- Retornar feedback automático no WhatsApp sobre o status do comprovante.

## ⚙️ Configuração do Painel WAHA (WhatsApp HTTP API)

Este guia orienta como configurar a sessão do WhatsApp e conectar o fluxo de dados ao seu serviço FastAPI através do Dashboard do WAHA.


## 1. Acessando o Dashboard
Após rodar o comando `docker-compose up -d`, o painel estará disponível em:
- **URL:** `http://localhost:3000`
- **Usuário:** (Conforme definido no seu `.env` - padrão: `admin`)
- **Senha:** (Conforme definido no seu `.env`)


## 2. Criando uma Sessão (Session)
Para o bot funcionar, ele precisa de uma instância ativa:

1. Vá na aba **"Sessions"**.
2. Clique em **"Add Session"** (ou "+" no canto superior).
3. No campo **Session Name**, dê um nome (ex: `bot_comprovantes`).
4. Clique em **Save**.
5. No card da sessão criada, clique no botão **"Screenshot"** ou **"QR Code"** para abrir o código e escaneie com seu WhatsApp (Aparelhos Conectados).


## 3. Configurando o Webhook (Conexão com a API)
O Webhook é o "telefone" que o WAHA usa para avisar o seu FastAPI que chegou uma mensagem.

1. No Dashboard, vá até a aba **"Webhooks"**.
2. Clique em **"Add Webhook"**.
3. Preencha os campos seguindo estas orientações:
   - **URL:** `http://api-llm:8000/webhook/waha` 
     *(Nota: Usamos `api-llm` porque dentro da rede Docker os containers se comunicam pelo nome do serviço).*
   - **Events:** Selecione `message` e `message.any`.
   - **Enabled:** Marque como `True`.
4. Clique em **Save**.## Tecnologias

- Python 3.11+
- FastAPI
- SQLAlchemy
- PostgreSQL
- OCR com pytesseract e pdfplumber
- Requests e httpx para comunicação HTTP
- Uvicorn como servidor ASGI
- Docker
- Docker compose
## 🤖 Serviço de Mensagens e Automação de Comprovantes

Este documento descreve como a funcionalidade de mensagens está configurada neste projeto e como você pode customizá-la para criar um bot que recebe e processa comprovantes.

### 🛠️ Arquitetura do Serviço

O projeto utiliza uma arquitetura baseada em eventos para lidar com o WhatsApp:

1.  **WAHA (WhatsApp HTTP API):** Funciona como um gateway. Ele mantém a sessão do WhatsApp conectada e transforma as mensagens recebidas em requisições `POST` (webhooks).
2.  **FastAPI (api-llm):** Recebe o webhook do WAHA no endpoint configurado, processa a lógica de negócio e decide o que fazer com a mensagem.
3.  **PostgreSQL:** Armazena o log das mensagens, o status dos processamentos e os metadados dos comprovantes.
4.  **Groq/LLM (Opcional):** Utilizado para analisar o texto das mensagens ou extrair dados de comprovantes via OCR/Visão.


## 📩 Fluxo de Recebimento de Mensagens

Atualmente, o fluxo está configurado da seguinte forma:
- O WAHA recebe uma mensagem no celular conectado.
- O WAHA envia um JSON para o container `api` (ex: `http://api:8000/webhook`).
- O arquivo `app/endpoints/message.py` processa esse JSON.
- O banco de dados registra a transação através do `app/db/deps.py`.



## Env

O arquivo `.env` gerencia as credenciais, portas e chaves de API necessárias para que o banco de dados, o serviço de WhatsApp (WAHA) e a API FastAPI se comuniquem.


## 📋 Modelo de Configuração

Copie o conteúdo abaixo e salve em um arquivo chamado `.env` na raiz do projeto:

```env
# --- WAHA (WhatsApp HTTP API) ---
# Chave de segurança para as requisições da API
WAHA_API_KEY=
# Credenciais de acesso ao Dashboard (http://localhost:3000)
WAHA_DASHBOARD_USERNAME=admin
WAHA_DASHBOARD_PASSWORD=sua_senha
# Credenciais para a documentação Swagger (http://localhost:3000/docs)
WHATSAPP_SWAGGER_USERNAME=admin
WHATSAPP_SWAGGER_PASSWORD=sua_senha
# Porta de execução do serviço WAHA
WAHA_PORT=3000

# --- BANCO DE DADOS (PostgreSQL) ---
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_DB=llm_db
# URL de conexão interna para o SQLAlchemy (usando o nome do serviço 'db')
DATABASE_URL=postgresql://postgres:postgres@db:5432/llm_db

# --- INTELIGÊNCIA ARTIFICIAL E BOT ---
# Chave da API do Groq (obtenha em console.groq.com)
GROQ_API_KEY=sua_chave
# Seu número de WhatsApp no formato internacional (ex: 5592999999991@c.us)
SELF_NUMBER=5592999999991@c.us
## Pré-requisitos

Antes de começar, certifique-se de ter instalado:

- Python 3.11
- Docker e Docker Compose
- Waha (contêiner) configurado
- Para Windows: **Tesseract OCR** e bibliotecas de leitura de PDFs/imagens  

## Instalação

### Instalação do Tesseract no Windows

1. Baixe o instalador do Tesseract: [https://github.com/tesseract-ocr/tesseract](https://github.com/tesseract-ocr/tesseract)
2. Instale e adicione o caminho do executável (`C:\Program Files\Tesseract-OCR`) ao PATH do Windows.
3. Teste no terminal:  
```powershell
tesseract --version
```

### Rodar projeto com docker
1. Clone o repositório
```
git clone <repo_url>
cd api-llm
```
2. Crie e ative o ambiente virtual:
```
python -m venv venv
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate
```
3. Faça o build da aplicação:
```
docker-compose build api
docker-compose up -d
```
