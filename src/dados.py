def salvar_recorde(caminho_arquivo, pontuacao):
    """Salva a pontuação recorde em arquivo texto."""
    with open(caminho_arquivo, "w", encoding="utf-8") as arquivo:
        arquivo.write(str(pontuacao))


def carregar_recorde(caminho_arquivo):
    """Carrega o recorde salvo; retorna 0 se não existir valor válido."""
    try:
        with open(caminho_arquivo, "r", encoding="utf-8") as arquivo:
            conteudo = arquivo.read().strip()

            if conteudo == "":
                return 0

            return int(conteudo)

    except FileNotFoundError:
        return 0


def obter_rodadas():
    """
    Retorna uma lista de 3 rodadas, cada uma contendo 3 casos (dicionários)
    produzidos por IA para o editor aprovar ou rejeitar antes da publicação.
    """
    return [
        # --- RODADA 1 ---
        [
            {
                "id": 1,
                "categoria": "Privacidade",
                "texto": "Nota urgente: O novo portal da prefeitura publicou o CPF e o endereco residencial de todos os moradores cadastrados para agilizar consultas.",
                "acao_correta": "REJEITAR",
                "indicador_afetado": "credibilidade",
                "explicacao": "Exposicao de dados pessoais (CPF e endereco) viola a privacidade e a LGPD."
            },
            {
                "id": 2,
                "categoria": "Fato Verificado",
                "texto": "Boletim meteorologico: A previsao indica chuvas moderadas para o fim de semana na regiao metropolitana, segundo o instituto oficial.",
                "acao_correta": "APROVAR",
                "indicador_afetado": "credibilidade",
                "explicacao": "Conteudo seguro, baseado em fonte oficial e sem dados sensiveis."
            },
            {
                "id": 3,
                "categoria": "Informacao Falsa",
                "texto": "Descoberta cientifica: Beber tres litros de agua com limao em jejum substitui completamente qualquer vacina contra virus respiratorios.",
                "acao_correta": "REJEITAR",
                "indicador_afetado": "credibilidade",
                "explicacao": "Desinformacao na area da saude que coloca os leitores em risco."
            },
        ],
        # --- RODADA 2 ---
        [
            {
                "id": 4,
                "categoria": "Preconceito / Vies",
                "texto": "Analise de RH: O algoritmo recomenda descartar automaticamente curriculos de candidatos moradores de bairros perifericos por baixa produtividade.",
                "acao_correta": "REJEITAR",
                "indicador_afetado": "moral",
                "explicacao": "Conteudo preconceituoso e discriminatorio gerado por vies algoritmico."
            },
            {
                "id": 5,
                "categoria": "Seguranca Digital",
                "texto": "Dica de tecnologia: Ativar a autenticacao em dois fatores ajuda a proteger contas pessoais contra invasoes e acessos nao autorizados.",
                "acao_correta": "APROVAR",
                "indicador_afetado": "moral",
                "explicacao": "Orientacao verdadeira, responsavel e util ao leitor."
            },
            {
                "id": 6,
                "categoria": "Informacao Falsa",
                "texto": "Turismo historico: Ouro Preto inaugura neste verao sua nova orla maritima, atraindo surfistas de todo o pais para o litoral mineiro.",
                "acao_correta": "REJEITAR",
                "indicador_afetado": "credibilidade",
                "explicacao": "Alucinacao geografica falsa: Minas Gerais nao possui litoral."
            },
        ],
        # --- RODADA 3 ---
        [
            {
                "id": 7,
                "categoria": "Privacidade",
                "texto": "Lista escolar: Confira abaixo a relacao completa com nome, telefone pessoal e diagnostico medico dos alunos atendidos na enfermaria.",
                "acao_correta": "REJEITAR",
                "indicador_afetado": "moral",
                "explicacao": "Divulgacao indevida de dados sensiveis de saude e contato pessoal."
            },
            {
                "id": 8,
                "categoria": "Educacao e IA",
                "texto": "Guia de estudos: Ferramentas de IA podem auxiliar na organizacao de resumos, mas suas respostas devem sempre ser revisadas em fontes confiaveis.",
                "acao_correta": "APROVAR",
                "indicador_afetado": "credibilidade",
                "explicacao": "Conteudo equilibrado que incentiva o uso critico e responsavel da IA."
            },
            {
                "id": 9,
                "categoria": "Preconceito / Vies",
                "texto": "Editorial automatico: Profissionais acima de 50 anos nao devem ser contratados na area de tecnologia por serem incapazes de aprender novas linguagens.",
                "acao_correta": "REJEITAR",
                "indicador_afetado": "moral",
                "explicacao": "Conteudo etarista e discriminatorio que fere os principios eticos da redacao."
            },
        ],
    ]