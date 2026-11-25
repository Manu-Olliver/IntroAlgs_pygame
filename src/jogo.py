import pygame

from src.config import (
    LARGURA_TELA,
    ALTURA_TELA,
    FPS,
    TITULO_JOGO,
    BRANCO,
    PRETO,
    CINZA_FUNDO,
    CINZA_BORDA,
    AZUL_ESCURO,
    VERDE,
    VERMELHO,
    AMARELO,
    CREDIBILIDADE_MAX,
    MORAL_MAX,
    PRODUTIVIDADE_MAX,
    PENALIDADE_ERRO,
    TEMPO_LIMITE_CASO,
    CAMINHO_RECORDE,
)
from src.dados import (
    salvar_recorde,
    carregar_recorde,
    obter_rodadas,
)
from src.funcoes import (
    iniciar_status,
    avaliar_decisao,
    aplicar_penalidade_tempo,
    verificar_derrota,
    quebrar_texto_em_linhas,
)


def desenhar_barra_status(tela, fonte, nome, valor, maximo, x, y, largura=220, altura=22):
    """Desenha uma barra de status com rótulo e preenchimento proporcional."""
    rotulo = fonte.render(f"{nome}: {valor}/{maximo}", True, PRETO)
    tela.blit(rotulo, (x, y - 22))

    pygame.draw.rect(tela, CINZA_BORDA, (x, y, largura, altura), border_radius=4)

    proporcao = valor / maximo
    largura_preenchida = int(largura * proporcao)

    if proporcao > 0.5:
        cor = VERDE
    elif proporcao > 0.25:
        cor = AMARELO
    else:
        cor = VERMELHO

    if largura_preenchida > 0:
        pygame.draw.rect(tela, cor, (x, y, largura_preenchida, altura), border_radius=4)

    pygame.draw.rect(tela, PRETO, (x, y, largura, altura), 2, border_radius=4)


def desenhar_botao(tela, fonte, texto, retangulo, cor_normal, cor_hover, pos_mouse):
    """Desenha um botão retangular com mudança de cor ao passar o mouse."""
    if retangulo.collidepoint(pos_mouse):
        cor_atual = cor_hover
    else:
        cor_atual = cor_normal

    pygame.draw.rect(tela, cor_atual, retangulo, border_radius=8)
    pygame.draw.rect(tela, PRETO, retangulo, 2, border_radius=8)

    texto_surf = fonte.render(texto, True, BRANCO)
    texto_rect = texto_surf.get_rect(center=retangulo.center)
    tela.blit(texto_surf, texto_rect)


def executar_jogo():
    """Executa o loop principal do jogo IA Verifica - Nem tudo é verdade."""
    pygame.init()

    tela = pygame.display.set_mode((LARGURA_TELA, ALTURA_TELA))
    pygame.display.set_caption(TITULO_JOGO)

    fonte_banner = pygame.font.SysFont("arial", 34, bold=True)
    fonte_titulo = pygame.font.SysFont("arial", 24, bold=True)
    fonte_subtitulo = pygame.font.SysFont("arial", 18, bold=True)
    fonte_texto = pygame.font.SysFont("arial", 20)
    fonte_pequena = pygame.font.SysFont("arial", 16)

    relogio = pygame.time.Clock()
    rodando = True

    rodadas = obter_rodadas()
    indice_rodada = 0
    indice_caso = 0

    status = iniciar_status()
    pontos = 0
    recorde = carregar_recorde(CAMINHO_RECORDE)

    inicio_caso_ms = pygame.time.get_ticks()
    aguardando_proximo = False
    feedback_atual = ""
    acertou_ultimo = False
    estado_jogo = "MENU"  # "MENU", "INSTRUCOES", "JOGANDO", "VITORIA" ou "DERROTA"

    # Retângulos dos botões clicáveis com o mouse
    btn_jogar = pygame.Rect(275, 250, 250, 55)
    btn_instrucoes = pygame.Rect(275, 325, 250, 55)
    btn_sair = pygame.Rect(275, 400, 250, 55)
    btn_voltar = pygame.Rect(275, 495, 250, 50)

    while rodando:
        relogio.tick(FPS)
        agora_ms = pygame.time.get_ticks()
        pos_mouse = pygame.mouse.get_pos()

        # Cálculo do tempo restante apenas enquanto o jogador está na partida
        if estado_jogo == "JOGANDO":
            segundos_passados = (agora_ms - inicio_caso_ms) // 1000
            tempo_restante = max(0, TEMPO_LIMITE_CASO - segundos_passados)

            if not aguardando_proximo and tempo_restante == 0:
                status = aplicar_penalidade_tempo(status)
                acertou_ultimo = False
                feedback_atual = (
                    f"TEMPO ESGOTADO! (-{PENALIDADE_ERRO} Produtividade) "
                    "Voce demorou demais para revisar o conteudo."
                )
                aguardando_proximo = True
        else:
            tempo_restante = TEMPO_LIMITE_CASO

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                rodando = False

            # --- CONTROLES EXCLUSIVOS POR MOUSE (MENU E INSTRUÇÕES) ---
            if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
                if estado_jogo == "MENU":
                    if btn_jogar.collidepoint(evento.pos):
                        indice_rodada = 0
                        indice_caso = 0
                        status = iniciar_status()
                        pontos = 0
                        aguardando_proximo = False
                        feedback_atual = ""
                        inicio_caso_ms = pygame.time.get_ticks()
                        estado_jogo = "JOGANDO"

                    elif btn_instrucoes.collidepoint(evento.pos):
                        estado_jogo = "INSTRUCOES"

                    elif btn_sair.collidepoint(evento.pos):
                        rodando = False

                elif estado_jogo == "INSTRUCOES":
                    if btn_voltar.collidepoint(evento.pos):
                        estado_jogo = "MENU"

            # --- CONTROLES POR TECLADO (PARTIDA E TELAS FINAIS) ---
            if evento.type == pygame.KEYDOWN:
                if estado_jogo == "JOGANDO":
                    if not aguardando_proximo:
                        decisao = ""
                        if evento.key == pygame.K_a:
                            decisao = "APROVAR"
                        elif evento.key == pygame.K_r:
                            decisao = "REJEITAR"

                        if decisao != "":
                            caso_atual = rodadas[indice_rodada][indice_caso]
                            acertou_ultimo, feedback_atual, status, pontos = avaliar_decisao(
                                caso_atual, decisao, status, pontos
                            )
                            aguardando_proximo = True

                            if pontos > recorde:
                                recorde = pontos
                                salvar_recorde(CAMINHO_RECORDE, recorde)

                    elif evento.key == pygame.K_SPACE:
                        if verificar_derrota(status):
                            estado_jogo = "DERROTA"
                        else:
                            if indice_caso + 1 < len(rodadas[indice_rodada]):
                                indice_caso += 1
                                aguardando_proximo = False
                                feedback_atual = ""
                                inicio_caso_ms = pygame.time.get_ticks()
                            elif indice_rodada + 1 < len(rodadas):
                                indice_rodada += 1
                                indice_caso = 0
                                aguardando_proximo = False
                                feedback_atual = ""
                                inicio_caso_ms = pygame.time.get_ticks()
                            else:
                                estado_jogo = "VITORIA"

                elif estado_jogo in ("VITORIA", "DERROTA"):
                    if evento.key == pygame.K_r:
                        indice_rodada = 0
                        indice_caso = 0
                        status = iniciar_status()
                        pontos = 0
                        aguardando_proximo = False
                        feedback_atual = ""
                        inicio_caso_ms = pygame.time.get_ticks()
                        estado_jogo = "JOGANDO"
                    elif evento.key == pygame.K_m:
                        estado_jogo = "MENU"

        # --- RENDERIZAÇÃO ---
        tela.fill(CINZA_FUNDO)

        if estado_jogo == "MENU":
            pygame.draw.rect(tela, AZUL_ESCURO, (0, 0, LARGURA_TELA, 150))

            titulo_menu = fonte_banner.render("IA VERIFICA", True, BRANCO)
            subtitulo_menu = fonte_titulo.render("Nem tudo é verdade", True, BRANCO)
            tela.blit(titulo_menu, titulo_menu.get_rect(center=(LARGURA_TELA // 2, 55)))
            tela.blit(subtitulo_menu, subtitulo_menu.get_rect(center=(LARGURA_TELA // 2, 105)))

            rec_surf = fonte_subtitulo.render(f"Recorde Atual: {recorde} pontos", True, AZUL_ESCURO)
            tela.blit(rec_surf, rec_surf.get_rect(center=(LARGURA_TELA // 2, 195)))

            desenhar_botao(tela, fonte_titulo, "JOGAR", btn_jogar, VERDE, (24, 110, 24), pos_mouse)
            desenhar_botao(tela, fonte_titulo, "INSTRUÇÕES", btn_instrucoes, AZUL_ESCURO, (50, 90, 145), pos_mouse)
            desenhar_botao(tela, fonte_titulo, "SAIR", btn_sair, VERMELHO, (145, 20, 20), pos_mouse)

        elif estado_jogo == "INSTRUCOES":
            pygame.draw.rect(tela, AZUL_ESCURO, (0, 0, LARGURA_TELA, 70))
            titulo_inst = fonte_titulo.render("INSTRUÇÕES DO JOGO", True, BRANCO)
            tela.blit(titulo_inst, titulo_inst.get_rect(center=(LARGURA_TELA // 2, 35)))

            caixa_inst = pygame.Rect(40, 95, 720, 375)
            pygame.draw.rect(tela, BRANCO, caixa_inst, border_radius=8)
            pygame.draw.rect(tela, AZUL_ESCURO, caixa_inst, 2, border_radius=8)

            regras = [
                "• Objetivo: Você é editor de uma redação e precisa revisar 3 rodadas com 3 textos",
                "  gerados por Inteligência Artificial antes que sejam publicados.",
                "",
                "• O que observar: Identifique informações falsas, preconceitos/vieses ou exposição",
                "  indevida de dados pessoais (privacidade).",
                "",
                "• Controles na partida:",
                "    [ A ] APROVAR o texto seguro e verdadeiro.",
                "    [ R ] REJEITAR o texto com problemas éticos, falsos ou de privacidade.",
                "    [ ESPAÇO ] Avançar para o próximo caso após ver o resultado.",
                "",
                f"• Penalidades: Errar desconta {PENALIDADE_ERRO} pontos de Credibilidade ou Moral.",
                f"  Ultrapassar os {TEMPO_LIMITE_CASO}s do caso desconta {PENALIDADE_ERRO} pontos de Produtividade.",
                "• Derrota: Se qualquer uma das 3 barras chegar a zero, o jogo termina.",
            ]

            y_inst = 115
            for linha in regras:
                linha_surf = fonte_pequena.render(linha, True, PRETO)
                tela.blit(linha_surf, (60, y_inst))
                y_inst += 24

            desenhar_botao(tela, fonte_titulo, "VOLTAR", btn_voltar, AZUL_ESCURO, (50, 90, 145), pos_mouse)

        elif estado_jogo == "JOGANDO":
            # Cabeçalho
            pygame.draw.rect(tela, AZUL_ESCURO, (0, 0, LARGURA_TELA, 65))
            titulo_surf = fonte_titulo.render("IA VERIFICA - Nem tudo é verdade", True, BRANCO)
            placar_surf = fonte_subtitulo.render(
                f"Pontos: {pontos} | Recorde: {recorde}", True, BRANCO
            )
            tela.blit(titulo_surf, (25, 19))
            tela.blit(placar_surf, (560, 22))

            # Barras de status
            desenhar_barra_status(tela, fonte_pequena, "Credibilidade", status["credibilidade"], CREDIBILIDADE_MAX, 30, 105)
            desenhar_barra_status(tela, fonte_pequena, "Moral", status["moral"], MORAL_MAX, 290, 105)
            desenhar_barra_status(tela, fonte_pequena, "Produtividade", status["produtividade"], PRODUTIVIDADE_MAX, 550, 105)

            caso_atual = rodadas[indice_rodada][indice_caso]

            # Cartão do texto a ser revisado
            caixa_rect = pygame.Rect(30, 155, 740, 240)
            pygame.draw.rect(tela, BRANCO, caixa_rect, border_radius=8)
            pygame.draw.rect(tela, AZUL_ESCURO, caixa_rect, 2, border_radius=8)

            info_caso = fonte_subtitulo.render(
                f"Rodada {indice_rodada + 1}/{len(rodadas)} | "
                f"Caso {indice_caso + 1}/{len(rodadas[indice_rodada])} | "
                f"Tema: {caso_atual['categoria']}",
                True,
                AZUL_ESCURO,
            )
            tela.blit(info_caso, (50, 172))

            cor_tempo = VERMELHO if tempo_restante <= 5 else PRETO
            tempo_surf = fonte_subtitulo.render(f"Tempo: {tempo_restante}s", True, cor_tempo)
            tela.blit(tempo_surf, (655, 172))

            linhas_texto = quebrar_texto_em_linhas(caso_atual["texto"], fonte_texto, 690)
            y_texto = 215
            for linha in linhas_texto:
                linha_surf = fonte_texto.render(linha, True, PRETO)
                tela.blit(linha_surf, (50, y_texto))
                y_texto += 30

            # Painel inferior de comandos ou feedback
            if not aguardando_proximo:
                instrucao = fonte_subtitulo.render(
                    "Analise o conteúdo produzido pela IA antes da publicação:", True, PRETO
                )
                tela.blit(instrucao, (30, 425))

                btn_aprovar = fonte_titulo.render("[ A ] APROVAR", True, VERDE)
                btn_rejeitar = fonte_titulo.render("[ R ] REJEITAR", True, VERMELHO)
                tela.blit(btn_aprovar, (30, 468))
                tela.blit(btn_rejeitar, (360, 468))
            else:
                cor_fb = VERDE if acertou_ultimo else VERMELHO
                linhas_fb = quebrar_texto_em_linhas(feedback_atual, fonte_subtitulo, 730)
                y_fb = 415
                for linha in linhas_fb:
                    fb_surf = fonte_subtitulo.render(linha, True, cor_fb)
                    tela.blit(fb_surf, (30, y_fb))
                    y_fb += 26

                prox_surf = fonte_subtitulo.render(
                    "Pressione [ ESPAÇO ] para continuar...", True, AZUL_ESCURO
                )
                tela.blit(prox_surf, (30, 525))

        elif estado_jogo == "VITORIA":
            msg1 = fonte_titulo.render("VITÓRIA! TODAS AS RODADAS CONCLUÍDAS!", True, VERDE)
            msg2 = fonte_texto.render(
                f"Você manteve os indicadores da redação acima de zero. Pontuação: {pontos}",
                True,
                PRETO,
            )
            msg3 = fonte_subtitulo.render(
                "Pressione [ R ] para jogar novamente ou [ M ] para o Menu.", True, AZUL_ESCURO
            )
            tela.blit(msg1, (140, 230))
            tela.blit(msg2, (70, 285))
            tela.blit(msg3, (145, 345))

        elif estado_jogo == "DERROTA":
            msg1 = fonte_titulo.render("DERROTA! REDAÇÃO ENCERRADA!", True, VERMELHO)
            msg2 = fonte_texto.render(
                "Uma das barras (Credibilidade, Moral ou Produtividade) chegou a zero.",
                True,
                PRETO,
            )
            msg3 = fonte_subtitulo.render(
                "Pressione [ R ] para tentar novamente ou [ M ] para o Menu.", True, AZUL_ESCURO
            )
            tela.blit(msg1, (195, 230))
            tela.blit(msg2, (65, 285))
            tela.blit(msg3, (145, 345))

        pygame.display.flip()

    pygame.quit()