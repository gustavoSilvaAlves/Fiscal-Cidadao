import httpx
from src.config import BASE_URL

async def listar_deputados(nome: str = None, siglaUf: str = None, siglaPartido: str = None, itens: int = 10) -> str:
    """
    Lista deputados em exercício, podendo filtrar por nome, estado (siglaUf), ou partido (siglaPartido).
    """
    params = {k: v for k, v in {
        "nome": nome, "siglaUf": siglaUf, "siglaPartido": siglaPartido, "itens": itens
    }.items() if v is not None}

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
