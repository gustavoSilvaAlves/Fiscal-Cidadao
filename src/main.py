from fastapi import FastAPI
from pydantic import BaseModel
import uuid


from .agent.core import agent_executor


app = FastAPI(
    title="Fiscal Cidadão API",
    description="API para monitoramento de atividades parlamentares.",
    version="0.1.0"
)



class ChatRequest(BaseModel):
    query: str
    conversation_id: str



class ChatResponse(BaseModel):
    response: str
    conversation_id: str



class StartChatResponse(BaseModel):
    conversation_id: str


@app.get("/")
async def read_root():
    """Endpoint de teste para verificar se a API está online."""
    return {"status": "API online"}


@app.get("/start_chat", response_model=StartChatResponse)
async def start_chat():
    """
    Inicia uma nova conversa e retorna um ID único para o cliente.
    """
    new_uuid = str(uuid.uuid4())
    return StartChatResponse(conversation_id=new_uuid)


@app.post("/chat", response_model=ChatResponse)
async def chat_with_agent(request: ChatRequest):
    """
    Endpoint principal para interagir com o agente. Requer um conversation_id.
    """

    response = await agent_executor.ainvoke({"messages": [("human", request.query)]})

    last_message = response['messages'][-1].content

    return ChatResponse(response=last_message, conversation_id=request.conversation_id)








