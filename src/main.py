from fastapi import FastAPI
from pydantic import BaseModel
import uuid
import httpx
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

class WebhookData(BaseModel):
    event: str
    instance: str
    data: dict
    sender: str


@app.post("/webhook")
async def webhook_endpoint(data: WebhookData):
    """
    Endpoint para receber mensagens do WhatsApp via Evolution API,
    processá-las com o agente e enviar a resposta de volta.
    """
    print("\n--- INÍCIO DO LOG DO WEBHOOK ---")
    print(f"Evento recebido: {data.event}")
    print(f"Instância do WhatsApp: {data.instance}")
    print("\nDados recebidos (data):")
    print(data.data)

    try:
        remote_jid = data.data['key']['remoteJid']
        message_text = data.data['message']['ephemeralMessage']['message']['extendedTextMessage']['text']

        print(f"\nNúmero do remetente (JID): {remote_jid}")
        print(f"Mensagem recebida: '{message_text}'")

        response = await agent_executor.ainvoke({
            "messages": [("human", message_text)],
            "conversation_id": remote_jid
        })

        agent_response = response['messages'][-1].content
        print(f"Resposta gerada pelo agente: '{agent_response}'")


        api_url = f"http://localhost:8080/message/sendText/{data.instance}"
        headers = {
            "apikey": "chave_secreta_teste",
            "Content-Type": "application/json"
        }

        payload = {
            "number": remote_jid.replace("@s.whatsapp.net", ""),
            "text": agent_response
        }

        async with httpx.AsyncClient() as client:
            send_response = await client.post(api_url, headers=headers, json=payload)
            send_response.raise_for_status()
            print(f"Mensagem enviada com sucesso! Status: {send_response.status_code}")

    except KeyError:
        print("\nErro: Mensagem não é do tipo 'extendedTextMessage'. Ignorando...")
        return {"status": "ok", "message": "Mensagem ignorada"}

    except httpx.HTTPStatusError as e:
        print(f"\nErro ao enviar a mensagem para a Evolution API: {e}")
        return {"status": "error", "message": "Falha ao enviar resposta"}

    except Exception as e:
        print(f"\nOcorreu um erro: {e}")
        return {"status": "error", "message": "Erro interno do servidor"}

    print("--- FIM DO LOG DO WEBHOOK ---\n")
    return {"status": "ok"}
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








