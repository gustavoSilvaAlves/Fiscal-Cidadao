import httpx
from typing import Optional

BASE_URL = "https://dadosabertos.camara.leg.br/api/v2"


async def listar_deputados(
        nome: str = None,
        siglaUf: str = None,
        siglaPartido: str = None,
        itens: int = 10
) -> str:
    """
    Lista deputados em exercício, podendo filtrar por nome, estado (siglaUf), ou partido (siglaPartido).
    """
    params = {
        "nome": nome,
        "siglaUf": siglaUf,
        "siglaPartido": siglaPartido,
        "itens": itens
    }
    params = {k: v for k, v in params.items() if v is not None}

    async with httpx.AsyncClient() as client:
        resp = await client.get(f"{BASE_URL}/deputados", params=params, headers={"Accept": "application/json"})

    if resp.status_code != 200:
        return f"Erro ao buscar deputados: {resp.status_code}"

    data = resp.json().get("dados", [])
    if not data:
        return "Nenhum deputado encontrado."

    if len(data) == 1:
        return await detalhar_deputado(data[0]['id'])

    resultado = ["Foram encontrados vários deputados. Escolha o ID para ver detalhes:"]
    for d in data:
        resultado.append(f"ID: {d['id']} - Nome: {d['nome']} ({d['siglaPartido']}-{d['siglaUf']})")

    return "\n".join(resultado)


async def detalhar_deputado(id: int) -> str:
    """
    Busca informações detalhadas de um deputado específico pelo ID.
    Retorna nome completo, CPF, data de nascimento, escolaridade e partido.
    """
    async with httpx.AsyncClient() as client:
        resp = await client.get(f"{BASE_URL}/deputados/{id}", headers={"Accept": "application/json"})

    if resp.status_code != 200:
        return f"Erro ao buscar detalhes do deputado: {resp.status_code}"

    dados = resp.json().get("dados", {})
    if not dados:
        return "Deputado não encontrado."

    gabinete_info = dados.get('ultimoStatus', {}).get('gabinete', {})
    redes_sociais = dados.get('redeSocial', [])
    redes_sociais_str = '\n'.join(redes_sociais) if redes_sociais else 'Não informado'

    detalhes = (
        f"Id Deputado: {dados.get('id')}\n"
        f"Nome: {dados.get('nomeCivil')}\n"
        f"CPF: {dados.get('cpf')}\n"
        f"Data de Nascimento: {dados.get('dataNascimento')}\n"
        f"Escolaridade: {dados.get('escolaridade')}\n"
        f"Partido: {dados.get('ultimoStatus', {}).get('siglaPartido')}\n"
        f"UF: {dados.get('ultimoStatus', {}).get('siglaUf')}\n"
        f"Telefone do Gabinete: {gabinete_info.get('telefone')}\n"
        f"E-mail do Gabinete: {gabinete_info.get('email')}\n"
        f"Prédio do Gabinete: {gabinete_info.get('predio')}\n"
        f"Andar do Gabinete: {gabinete_info.get('andar')}\n"
        f"Redes Sociais:\n{redes_sociais_str}"
    )

    return detalhes


async def buscar_gastos_parlamentares(
        id: int,
        ano: Optional[int] = None,
        mes: Optional[int] = None,
        itens: int = 100
) -> str:
    """
    Busca os gastos da cota parlamentar (CEAP) de um deputado.
    Pode ser filtrada por ano e mês.
    Retorna uma lista resumida das despesas mais recentes.
    """
    params = {
        "ano": ano,
        "mes": mes,
        "itens": itens,
        "ordenarPor": "dataDocumento",
        "ordem": "desc"
    }
    params = {k: v for k, v in params.items() if v is not None}

    async with httpx.AsyncClient() as client:
        resp = await client.get(
            f"{BASE_URL}/deputados/{id}/despesas",
            params=params,
            headers={"Accept": "application/json"}
        )

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