from src.config import (
    PENALIDADE_ERRO,
    CREDIBILIDADE_MAX,
    MORAL_MAX,
    PRODUTIVIDADE_MAX,
)


def limitar_valor(valor, minimo, maximo):
    """Mantém um valor dentro do intervalo [minimo, maximo]."""
    if valor < minimo:
        return minimo
    if valor > maximo:
        return maximo
    return valor


def iniciar_status():
    """Cria o dicionário inicial das três barras de status do editor."""
    return {
        "credibilidade": CREDIBILIDADE_MAX,
        "moral": MORAL_MAX,
        "produtividade": PRODUTIVIDADE_MAX,
    }


def avaliar_decisao(caso, decisao_jogador, status, pontos):
    """
    Avalia a decisão ('APROVAR' ou 'REJEITAR') do jogador para um caso.
    Retorna: (acertou, mensagem_feedback, novo_status, novos_pontos)
    """
    novo_status = {
        "credibilidade": status["credibilidade"],
        "moral": status["moral"],
        "produtividade": status["produtividade"],
    }

    if decisao_jogador == caso["acao_correta"]:
        novos_pontos = pontos + 10
        mensagem = f"CORRETO! {caso['explicacao']}"
        return True, mensagem, novo_status, novos_pontos

    tetos = {
        "credibilidade": CREDIBILIDADE_MAX,
        "moral": MORAL_MAX,
        "produtividade": PRODUTIVIDADE_MAX,
    }
    indicador = caso["indicador_afetado"]
    novo_status[indicador] = limitar_valor(
        novo_status[indicador] - PENALIDADE_ERRO, 0, tetos[indicador]
    )
    mensagem = f"ERROU! (-{PENALIDADE_ERRO} {indicador.capitalize()}) {caso['explicacao']}"
    return False, mensagem, novo_status, pontos


def aplicar_penalidade_tempo(status):
    """Reduz 5 pontos da barra Produtividade quando o tempo limite se esgota."""
    novo_status = {
        "credibilidade": status["credibilidade"],
        "moral": status["moral"],
        "produtividade": limitar_valor(
            status["produtividade"] - PENALIDADE_ERRO, 0, PRODUTIVIDADE_MAX
        ),
    }
    return novo_status


def verificar_derrota(status):
    """Retorna True se qualquer uma das três barras chegar a zero."""
    return (
        status["credibilidade"] <= 0
        or status["moral"] <= 0
        or status["produtividade"] <= 0
    )


def quebrar_texto_em_linhas(texto, fonte, largura_maxima):
    """Divide um texto longo em uma lista de linhas que cabem na largura da caixa."""
    palavras = texto.split(" ")
    linhas = []
    linha_atual = ""

    for palavra in palavras:
        teste = linha_atual + palavra + " "
        if fonte.size(teste)[0] <= largura_maxima:
            linha_atual = teste
        else:
            linhas.append(linha_atual.strip())
            linha_atual = palavra + " "

    if linha_atual.strip() != "":
        linhas.append(linha_atual.strip())

    return linhas