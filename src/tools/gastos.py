import httpx
from typing import Optional

from src.config import BASE_URL

async def buscar_gastos_parlamentares(id: int, ano: Optional[int] = None, mes: Optional[int] = None, itens: int = 100) -> str:
    """
    Busca os gastos da cota parlamentar (CEAP) de um deputado.
    Pode ser filtrada por ano e mês.
    Retorna uma lista resumida das despesas mais recentes.
    """

    params = {k: v for k, v in {
        "ano": ano, "mes": mes, "itens": itens, "ordenarPor": "dataDocumento", "ordem": "desc"
    }.items() if v is not None}

    async with httpx.AsyncClient() as client:
        resp = await client.get(f"{BASE_URL}/deputados/{id}/despesas", params=params, headers={"Accept": "application/json"})

    if resp.status_code != 200:
        return f"Erro ao buscar cota parlamentar: {resp.status_code}"

    data = resp.json().get("dados", [])
    if not data:
        return "Nenhum gasto de cota parlamentar encontrado para o período."

    resultado = [f"Gastos de Cota Parlamentar para o Deputado (ID: {id}):"]
    for despesa in data:
        tipo_despesa = despesa.get('tipoDespesa', "Não encontrado o tipo da despesa")
        valor = despesa.get('valorLiquido', 0.0)
        documento = despesa.get('tipoDocumento', 'Não informado')
        fornecedor = despesa.get('nomeFornecedor', 'Não informado')
        data_doc = despesa.get('dataDocumento', 'Não informado')
        link_nota = despesa.get('urlDocumento', 'Não encontrei o link de download da Nota fiscal')

        resultado.append(
            f"| Tipo de despesa: {tipo_despesa} | Tipo de documento: {documento} | Fornecedor: {fornecedor} | Valor: R${valor:,.2f} | Data: {data_doc} | Link da nota fiscal: {link_nota}"
        )

    return "\n".join(resultado)
