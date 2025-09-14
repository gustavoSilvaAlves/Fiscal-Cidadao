import redis.asyncio as redis
from typing import List, Optional
import os
from dotenv import load_dotenv

load_dotenv()

REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379")
redis_client = redis.from_url(REDIS_URL, decode_responses=True)


async def cadastrar_deputado_monitoramento(celular: str, deputado_id: int) -> str:
    """
    Cadastra um deputado para monitoramento vinculado a um número de celular.
    """

    deputados_existentes: Optional[List[str]] = await redis_client.lrange(celular, 0, -1)

    if str(deputado_id) in deputados_existentes:
        return f"Deputado ID {deputado_id} já está cadastrado para monitoramento deste número."

    # Adiciona o deputado à lista
    await redis_client.rpush(celular, deputado_id)
    return f"Deputado ID {deputado_id} cadastrado com sucesso para monitoramento do número {celular}."


async def listar_deputados_monitoramento(celular: str) -> List[str]:
    """
    Retorna todos os deputados que estão sendo monitorados por um determinado número de celular.
    """
    deputados: Optional[List[str]] = await redis_client.lrange(celular, 0, -1)
    return deputados if deputados else []
