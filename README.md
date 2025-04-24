# 🤖 Chat-BotWhatsApp

Este projeto implementa um chatbot inteligente para WhatsApp, utilizando a API WAHA (WhatsApp HTTP API) para integração com o WhatsApp Web e a API da Groq para processamento de linguagem natural com o modelo DeepSeek.

## 🧩 Visão Geral

- **WAHA**: API HTTP auto-hospedada que permite interações com o WhatsApp Web.
    
- **Flask**: Framework web utilizado para criar a API que recebe e processa mensagens.
    
- **Groq + llama: Integração com a API da Groq para utilizar o modelo llama no processamento das mensagens.
    
- **RAG (Retrieval-Augmented Generation)**: Técnica utilizada para melhorar as respostas do chatbot, permitindo acesso a fontes de dados externas.
    

## 🐳 Docker

O projeto utiliza contêineres Docker para facilitar a implantação:

1. **WAHA**: Contêiner baseado na imagem oficial do WAHA.
    
2. **API Flask**: Contêiner personalizado para a API desenvolvida em Flask.
    

Ambos os contêineres são orquestrados utilizando o Docker Compose.

## ⚙️ Configuração do WAHA

- Acesse o Swagger UI disponível no contêiner do WAHA.
    
- Configure um webhook para encaminhar as mensagens recebidas para a rota `chatbot/webhook` da API Flask.
    
- O WAHA será responsável por receber as mensagens do WhatsApp e repassá-las para a API Flask.
    

## 🧠 Integração com a IA (Groq + llama)

A integração com a IA é realizada da seguinte forma:

1. **Recebimento de Mensagens**: O WAHA recebe as mensagens do WhatsApp e as encaminha para a API Flask.
    
2. **Processamento com IA**: A API Flask utiliza a API da Groq para processar as mensagens com o modelo llama.
    
3. **Resposta ao Usuário**: A resposta gerada pela IA é enviada de volta ao usuário no WhatsApp.
     

## 🧩 Implementação do RAG (Retrieval-Augmented Generation)

Para melhorar as respostas do chatbot, foi implementada a técnica RAG:

1. **Carregamento de Documentos**: Um script carrega arquivos `.pdf` contendo informações relevantes.
    
2. **Divisão em Chunks**: Os documentos são divididos em pedaços menores (chunks) com sobreposição (overlap) para preservar o contexto.
    
3. **Geração de Embeddings**: Utiliza-se um modelo de embeddings para transformar os chunks em vetores numéricos.
    
4. **Armazenamento em Vector Store**: Os vetores são armazenados em uma base de dados vetorial para permitir buscas semânticas eficientes.
    

## 🚀 Como Executar o Projeto

1. **Clone o Repositório**:
    
    ```bash
    git clone https://github.com/DomRyaan/Chat-BotWhatsApp.git
    cd Chat-BotWhatsApp
    ```
    
2. **Configure as Variáveis de Ambiente**:
    
    Crie um arquivo `.env` com as seguintes variáveis:
    
    ```env
    GROQ_API_KEY=your_groq_api_key
    HUGGINGFACE_API_KEY=your_huggingface_api_key
    ```
    
3. **Inicie os Contêineres com Docker Compose**:
    
    ```bash
    docker-compose up --build
    ```
    
4. **Configure o WAHA**:
    
    - Acesse o Swagger UI do WAHA.
        
    - Configure o webhook para apontar para `http://localhost:5000/chatbot/webhook`.
        
5. **Conecte o WhatsApp**:
    
    - Siga as instruções do WAHA para escanear o QR code e conectar o WhatsApp.
        
