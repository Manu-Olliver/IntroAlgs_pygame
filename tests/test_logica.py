from src.config import (
    CREDIBILIDADE_MAX,
    MORAL_MAX,
    PRODUTIVIDADE_MAX,
    PENALIDADE_ERRO,
    PONTOS_ACERTO,
)
from src.funcoes import (
    iniciar_status,
    avaliar_decisao,
    aplicar_penalidade_tempo,
    verificar_derrota,
    quebrar_texto_em_linhas,
)
from src.dados import obter_rodadas


def test_iniciar_status():
    status = iniciar_status()
    assert status["credibilidade"] == CREDIBILIDADE_MAX
    assert status["moral"] == MORAL_MAX
    assert status["produtividade"] == PRODUTIVIDADE_MAX


def test_avaliar_decisao_acerto():
    status = iniciar_status()
    caso = {
        "acao_correta": "APROVAR",
        "indicador_afetado": "credibilidade",
        "explicacao": "Informação oficial.",
    }
    acertou, feedback, novo_status, novos_pontos = avaliar_decisao(caso, "APROVAR", status, 0)

    assert acertou is True
    assert novos_pontos == PONTOS_ACERTO
    assert novo_status["credibilidade"] == CREDIBILIDADE_MAX
    assert "CORRETO" in feedback


def test_avaliar_decisao_erro_desconta_indicador():
    status = iniciar_status()
    caso = {
        "acao_correta": "REJEITAR",
        "indicador_afetado": "moral",
        "explicacao": "Viola a privacidade.",
    }
    acertou, feedback, novo_status, novos_pontos = avaliar_decisao(caso, "APROVAR", status, 10)

    assert acertou is False
    assert novos_pontos == 10
    assert novo_status["moral"] == MORAL_MAX - PENALIDADE_ERRO
    assert "ERRO" in feedback


def test_aplicar_penalidade_tempo():
    status = iniciar_status()
    novo_status = aplicar_penalidade_tempo(status)
    assert novo_status["produtividade"] == PRODUTIVIDADE_MAX - PENALIDADE_ERRO


def test_verificar_derrota():
    status_ok = iniciar_status()
    assert verificar_derrota(status_ok) is False

    status_zerado = {"credibilidade": 0, "moral": 10, "produtividade": 10}
    assert verificar_derrota(status_zerado) is True


def test_obter_rodadas_do_arquivo():
    rodadas = obter_rodadas("data/casos.txt")
    assert len(rodadas) == 3
    assert len(rodadas[0]) == 3
    assert "texto" in rodadas[0][0]