from langgraph.prebuilt import create_react_agent
from dotenv import load_dotenv


load_dotenv()


from .tools import listar_deputados, detalhar_deputado, buscar_gastos_parlamentares


tools = [
    listar_deputados,
    detalhar_deputado,
    buscar_gastos_parlamentares
]


agent_executor = create_react_agent(
    model="gpt-4o-mini",
    tools=tools,
    prompt="Você é um agente especializado em busca de informações da câmara dos deputados. "
           "Utilize as ferramentas que vc tem disponível para responder as perguntas dos usuários. "
           "Seja sempre formal e imparcial referente as informações que vc responde ao usuário."
)