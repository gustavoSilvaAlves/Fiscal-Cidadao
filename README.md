#Fiscal Cidadão

Este é um projeto de um agente de IA especializado em buscar informações sobre deputados e atividades parlamentares na Câmara dos Deputados do Brasil.

O agente utiliza a API de Dados Abertos da Câmara e é construído com a biblioteca [LangGraph](https://github.com/langchain-ai/langgraph). Ele foi projetado para responder a consultas sobre:

- Informações detalhadas de deputados (nome, partido, UF, contato).
- Gastos da cota parlamentar (CEAP) por ano e mês.
- E outras consultas que o agente pode acionar através de ferramentas.

## ⚙️ Tecnologias

- **Python**: Linguagem de programação principal.
- **LangGraph**: Framework para construir agentes robustos e com estado.
- **LangChain**: Integração com LLMs e ferramentas.
- **FastAPI**: Servidor web para expor o agente como uma API.
- **Dotenv**: Gerenciamento de variáveis de ambiente.
- **Pipenv**: Gerenciamento de dependências.

## 🚀 Como Executar

### Pré-requisitos
- Python 3.11+
- Uma chave de API da OpenAI (ou um provedor de LLM compatível).

### Configuração
1.  **Clone o repositório**
    ```bash
    git clone [https://www.youtube.com/shorts/apr341idq8U](https://www.youtube.com/shorts/apr341idq8U)
    cd FiscalCidadao
    ```
2.  **Crie e ative o ambiente virtual**
    ```bash
    python -m venv venv
    .\venv\Scripts\activate
    ```
3.  **Instale as dependências**
    ```bash
    pip install -r requirements.txt
    ```
4.  **Configure as variáveis de ambiente**
    Crie um arquivo `.env` na raiz do projeto com a sua chave de API.
    ```env
    OPENAI_API_KEY="sua-chave-aqui"
    ```
### Executando o Swagger do FastAPI
Para iniciar o Swagger use o comando:
```bash
uvicorn src.main:app --reload
````
### Executando o Servidor de Desenvolvimento
Para iniciar a API e a interface visual do LangGraph para testes, use o comando:
```bash
langgraph dev --config langgraph.json

