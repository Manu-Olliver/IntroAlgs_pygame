import os
from src.config import CAMINHO_CASOS, TOTAL_RODADAS, CASOS_POR_RODADA


def carregar_recorde(caminho_arquivo):
    """Lê a maior pontuação salva em arquivo; retorna 0 se ainda não existir."""
    if not os.path.exists(caminho_arquivo):
        return 0
    with open(caminho_arquivo, "r", encoding="utf-8") as arquivo:
        conteudo = arquivo.read().strip()
        if conteudo.isdigit():
            return int(conteudo)
    return 0


def salvar_recorde(caminho_arquivo, novo_recorde):
    """Salva a nova maior pontuação em arquivo de texto."""
    pasta = os.path.dirname(caminho_arquivo)
    if pasta and not os.path.exists(pasta):
        os.makedirs(pasta)
    with open(caminho_arquivo, "w", encoding="utf-8") as arquivo:
        arquivo.write(str(novo_recorde))


def obter_rodadas(caminho_arquivo=CAMINHO_CASOS):
    """Lê os casos do arquivo .txt e organiza em uma matriz de rodadas."""
    rodadas = []
    for _ in range(TOTAL_RODADAS):
        rodadas.append([])

    with open(caminho_arquivo, "r", encoding="utf-8") as arquivo:
        for linha in arquivo:
            linha_limpa = linha.strip()
            if not linha_limpa or linha_limpa.startswith("#"):
                continue

            partes = linha_limpa.split("|")
            numero_rodada = int(partes[0])
            caso = {
                "id": int(partes[1]),
                "categoria": partes[2],
                "texto": partes[3],
                "acao_correta": partes[4],
                "indicador_afetado": partes[5],
                "explicacao": partes[6],
            }

            indice_rodada = numero_rodada - 1
            if 0 <= indice_rodada < TOTAL_RODADAS and len(rodadas[indice_rodada]) < CASOS_POR_RODADA:
                rodadas[indice_rodada].append(caso)

    return rodadas